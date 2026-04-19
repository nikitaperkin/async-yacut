from flask import jsonify, request, url_for
from http import HTTPStatus

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .constants import MSG_SHORT_ID_TAKEN, REDIRECT_VIEW

MSG_NO_REQUEST_BODY = 'Отсутствует тело запроса'
MSG_URL_REQUIRED = '"url" является обязательным полем!'
MSG_INVALID_SHORT_ID = 'Указано недопустимое имя для короткой ссылки'
MSG_NOT_FOUND = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def add_short_link():
    data = request.get_json(silent=True)

    if not data:
        raise InvalidAPIUsage(MSG_NO_REQUEST_BODY)
    if 'url' not in data:
        raise InvalidAPIUsage(MSG_URL_REQUIRED)

    custom_id = data.get('custom_id')

    if custom_id:
        if URLMap.is_invalid_custom_id(custom_id):
            raise InvalidAPIUsage(MSG_INVALID_SHORT_ID)
        if URLMap.is_duplicate_custom_id(custom_id):
            raise InvalidAPIUsage(MSG_SHORT_ID_TAKEN)
    else:
        custom_id = URLMap.get_unique_short_id()

    url_map = URLMap.create(original=data['url'], short=custom_id)
    return jsonify(
        {
            'url': url_map.original,
            'short_link': url_for(
                REDIRECT_VIEW,
                short_id=url_map.short,
                _external=True
            )
        }
    ), 201


@app.route('/api/id/<string:short_id>/')
def get_short_link(short_id):
    url_map = URLMap.get(short_id)
    if url_map is None:
        raise InvalidAPIUsage(MSG_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK
