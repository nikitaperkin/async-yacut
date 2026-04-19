from http import HTTPStatus

from flask import jsonify, redirect, request, url_for

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from yacut import db

NO_REQUEST_BODY = 'Отсутствует тело запроса'
URL_REQUIRED = '"url" является обязательным полем!'
NOT_FOUND = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def add_short_link():
    data = request.get_json(silent=True)

    if not data:
        raise InvalidAPIUsage(NO_REQUEST_BODY)
    if 'url' not in data:
        raise InvalidAPIUsage(URL_REQUIRED)

    try:
        url_map = URLMap.create(
            original=data['url'],
            short=data.get('custom_id'),
        )
        db.session.commit()
    except ValueError as e:
        raise InvalidAPIUsage(str(e))

    return jsonify(
        {
            'url': url_map.original,
            'short_link': url_map.get_short_link()
        }
    ), HTTPStatus.CREATED


@app.route('/api/id/<string:short>/')
def get_short_link(short):
    if (url_map := URLMap.get(short)) is None:
        raise InvalidAPIUsage(NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK


@app.route('/api/docs/')
def swagger_ui():
    return redirect('https://editor.swagger.io/?url={}'.format(
        url_for('openapi_spec', _external=True)
    ))


@app.route('/api/docs/openapi.yml')
def openapi_spec():
    return app.send_static_file('openapi.yml')