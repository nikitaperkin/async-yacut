import random
import string

from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import URLMapForm, UploadFileForm
from .models import URLMap
from .yadisk import async_upload_files_to_yadisk


OCCUPIED_ID = 'files'
SHORT_ID_LENGTH = 6


def get_unique_short_id():
    while True:
        short_id = ''.join(
            random.choice(
                string.ascii_letters + string.digits
            ) for _ in range(SHORT_ID_LENGTH)
        )
        if short_id != OCCUPIED_ID and not URLMap.query.filter_by(
            short=short_id
        ).first():
            return short_id


@app.route('/<string:short_id>')
def redirect_view(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)


@app.route('/', methods=['GET', 'POST'])
def add_short_link_view():
    form = URLMapForm()

    if not form.validate_on_submit():
        return render_template('short_link.html', form=form)

    custom_id = form.custom_id.data

    if custom_id:
        if custom_id == OCCUPIED_ID or URLMap.query.filter_by(
            short=custom_id
        ).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('short_link.html', form=form)
    else:
        custom_id = get_unique_short_id()

    url_map = URLMap(original=form.original_link.data, short=custom_id)
    db.session.add(url_map)
    db.session.commit()

    short_link = url_for('redirect_view', short_id=custom_id, _external=True)
    return render_template('short_link.html', form=form, short_link=short_link)


@app.route('/files', methods=['GET', 'POST'])
async def add_files_link_view():
    form = UploadFileForm()

    if not form.validate_on_submit():
        return render_template('file_short_link.html', form=form)

    files = form.files.data
    file_urls = await async_upload_files_to_yadisk(files)
    short_links = []

    for file_url in file_urls:
        custom_id = get_unique_short_id()
        url_map = URLMap(original=file_url, short=custom_id)
        db.session.add(url_map)
        short_links.append(
            url_for('redirect_view', short_id=custom_id, _external=True)
        )

    db.session.commit()
    file_links = [
        {'name': f.filename, 'link': link}
        for f, link in zip(files, short_links)
    ]
    return render_template(
        'file_short_link.html',
        form=form,
        file_links=file_links,
    )