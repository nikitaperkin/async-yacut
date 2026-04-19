from datetime import datetime
from random import choices

from flask import url_for

from .constants import (
    MAX_GENERATE_ATTEMPTS, MAX_LEN_AUTO, MAX_LEN_ORIGINAL,
    MAX_LEN_SHORT, OCCUPIED_SHORT, REDIRECT_VIEW,
    SHORT_ALLOWED_CHARS, SHORT_PATTERN,
)
from yacut import db

INVALID_SHORT = 'Указано недопустимое имя для короткой ссылки'
INVALID_URL = (
    'Длина URL превышает допустимое значение ({}).'
).format(MAX_LEN_ORIGINAL)
SHORT_TAKEN = 'Предложенный вариант короткой ссылки уже существует.'
SHORT_GENERATION_ERROR = (
    'Не удалось сгенерировать уникальную короткую ссылку '
    '(лимит попыток: {}).'
).format(MAX_GENERATE_ATTEMPTS)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LEN_ORIGINAL), nullable=False)
    short = db.Column(db.String(MAX_LEN_SHORT), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_unique_short():
        for _ in range(MAX_GENERATE_ATTEMPTS):
            short = ''.join(choices(SHORT_ALLOWED_CHARS, k=MAX_LEN_AUTO))
            if short != OCCUPIED_SHORT and not URLMap.get(short):
                return short
        raise RuntimeError(SHORT_GENERATION_ERROR)

    @staticmethod
    def create(
        original, short=None, commit=True,
        validate_url=True, validate_short=True
    ):
        if validate_url and len(original) > MAX_LEN_ORIGINAL:
            raise ValueError(INVALID_URL)
        if short:
            if validate_short and (
                len(short) > MAX_LEN_SHORT or not SHORT_PATTERN.match(short)
            ):
                raise ValueError(INVALID_SHORT)
            if short == OCCUPIED_SHORT or URLMap.get(short) is not None:
                raise ValueError(SHORT_TAKEN)
        else:
            short = URLMap.get_unique_short()

        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        if commit:
            db.session.commit()
        return url_map

    def get_short_link(self):
        return url_for(
            REDIRECT_VIEW,
            short=self.short,
            _external=True
        )
