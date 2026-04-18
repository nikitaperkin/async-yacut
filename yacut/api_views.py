import re

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import OCCUPIED_ID, get_unique_short_id

CUSTOM_ID_PATTERN = re.compile(r'^[a-zA-Z0-9]{1,16}$')


@app.route('/api/id/', methods=['POST'])
def add_short_link():
    data = request.get_json(silent=True)

    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    custom_id = data.get('custom_id')

    if custom_id:
        if custom_id == OCCUPIED_ID or not CUSTOM_ID_PATTERN.match(custom_id):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
        if URLMap.query.filter_by(short=custom_id).first():
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.'
            )
    else:
        custom_id = get_unique_short_id()

    url_map = URLMap(original=data['url'], short=custom_id)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<string:short_id>/')
def get_short_link(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url_map.original}), 200
