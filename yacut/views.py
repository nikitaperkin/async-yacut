from http import HTTPStatus

from flask import flash, redirect, render_template

from . import app
from .constants import REDIRECT_VIEW
from .forms import URLMapForm, UploadFileForm
from .models import URLMap
from yacut import db
from .yadisk import async_upload_files_to_yadisk

SHORT_TAKEN = 'Предложенный вариант короткой ссылки уже существует.'
UPLOAD_ERROR = 'Не удалось загрузить файлы. Попробуйте ещё раз.'


@app.route('/<string:short>', endpoint=REDIRECT_VIEW)
def redirect_view(short):
    if (url_map := URLMap.get(short)) is None:
        return render_template('404.html'), HTTPStatus.NOT_FOUND
    return redirect(url_map.original)


@app.route('/', methods=['GET', 'POST'])
def add_short_link_view():
    form = URLMapForm()

    if not form.validate_on_submit():
        return render_template('short_link.html', form=form)

    try:
        url_map = URLMap.create(
            original=form.original_link.data,
            short=form.custom_id.data,
        )
        db.session.commit()
    except ValueError:
        flash(SHORT_TAKEN)
        return render_template('short_link.html', form=form)

    return render_template(
        'short_link.html',
        form=form,
        short_link=url_map.get_short_link()
    )


@app.route('/files', methods=['GET', 'POST'])
async def add_files_link_view():
    form = UploadFileForm()

    if not form.validate_on_submit():
        return render_template('file_short_link.html', form=form)

    files = form.files.data

    try:
        file_urls = await async_upload_files_to_yadisk(files)
    except Exception:
        flash(UPLOAD_ERROR)
        return render_template('file_short_link.html', form=form)

    try:
        url_maps = [
            URLMap.create(original=file_url) for file_url in file_urls
        ]
        db.session.commit()
    except ValueError as e:
        flash(f'{UPLOAD_ERROR} {e}')
        return render_template('file_short_link.html', form=form)

    return render_template(
        'file_short_link.html',
        form=form,
        file_links=[
            {
                'name': uploaded_file.filename,
                'link': url_map.get_short_link()
            }
            for uploaded_file, url_map in zip(files, url_maps)
        ]
    )
