import asyncio
import urllib.parse

import aiohttp

from . import app


AUTH_HEADERS = {
    'Authorization': f'OAuth {app.config["DISK_TOKEN"]}'
}

UPLOAD_LINK = (
    f'{app.config["YADISK_API_HOST"]}'
    f'{app.config["YADISK_API_VERSION"]}/disk/resources/upload'
)

DOWNLOAD_LINK_URL = (
    f'{app.config["YADISK_API_HOST"]}'
    f'{app.config["YADISK_API_VERSION"]}/disk/resources/download'
)


async def async_upload_files_to_yadisk(files):
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(
            *(upload_file_and_get_url(session, file) for file in files)
        )


async def upload_file_and_get_url(session, file):
    async with session.get(
        url=UPLOAD_LINK,
        headers=AUTH_HEADERS,
        params={
            'path': f'app:/{file.filename}',
            'overwrite': 'True',
        }
    ) as response:
        upload_url = (await response.json())['href']

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
        return (await response.json())['href']
