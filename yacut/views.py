from flask import flash, redirect, render_template, url_for

from . import app
from .constants import MSG_SHORT_ID_TAKEN, REDIRECT_VIEW
from .forms import URLMapForm, UploadFileForm
from .models import URLMap
from .yadisk import async_upload_files_to_yadisk


@app.route('/<string:short_id>', endpoint=REDIRECT_VIEW)
def redirect_view(short_id):
    url_map = URLMap.get(short_id)
    if url_map is None:
        return render_template('404.html'), 404
    return redirect(url_map.original)


@app.route('/', methods=['GET', 'POST'])
def add_short_link_view():
    form = URLMapForm()

    if not form.validate_on_submit():
        return render_template('short_link.html', form=form)

    custom_id = form.custom_id.data

    if custom_id:
        if URLMap.is_invalid_custom_id(custom_id):
            flash(MSG_SHORT_ID_TAKEN)
            return render_template('short_link.html', form=form)
        if URLMap.is_duplicate_custom_id(custom_id):
            flash(MSG_SHORT_ID_TAKEN)
            return render_template('short_link.html', form=form)
    else:
        custom_id = URLMap.get_unique_short_id()

    url_map = URLMap.create(
        original=form.original_link.data,
        short=custom_id
    )

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
        flash('Не удалось загрузить файлы. Попробуйте ещё раз.')
        return render_template('file_short_link.html', form=form)

    short_ids = []

    for file_url in file_urls:
        short_id = URLMap.get_unique_short_id()
        URLMap.create(original=file_url, short=short_id)
        short_ids.append(short_id)

    return render_template(
        'file_short_link.html',
        form=form,
        file_links=[
            {
                'name': uploaded_file.filename,
                'link': url_for(
                    REDIRECT_VIEW,
                    short_id=short_id,
                    _external=True
                )
            }
            for uploaded_file, short_id in zip(files, short_ids)
        ]
    )
