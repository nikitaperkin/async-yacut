import aiohttp
import asyncio
import urllib

from . import app


AUTH_HEADERS = {
    'Authorization': f'OAuth {app.config["DISK_TOKEN"]}'
}
API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'

UPLOAD_LINK = f'{API_HOST}{API_VERSION}/disk/resources/upload'

DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'


async def async_upload_files_to_yadisk(files):
    if files is not None:
        tasks = []
        async with aiohttp.ClientSession() as session:
            for file in files:
                tasks.append(
                    asyncio.ensure_future(
                        upload_file_and_get_url(session, file)
                    )
                )
            urls = await asyncio.gather(*tasks)
        return urls


async def upload_file_and_get_url(session, file):
    async with session.get(
        url=UPLOAD_LINK,
        headers=AUTH_HEADERS,
        params={
            'path': f'app:/{file.filename}',
            'overwrite': 'True',
        }
    ) as response:
        data = await response.json()
        upload_url = data['href']

    async with session.put(
        upload_url,
        data=file.read()
    ) as response:
        location = response.headers.get('Location', '')
        location = urllib.parse.unquote(location)
        location = location.replace('/disk', '')

    async with session.get(
        url=DOWNLOAD_LINK_URL,
        headers=AUTH_HEADERS,
        params={'path': location}
    ) as response:
        data = await response.json()
        download_url = data['href']

    return download_url