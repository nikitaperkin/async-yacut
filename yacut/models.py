from datetime import datetime
import random
from string import ascii_letters, digits

from flask import url_for

from .constants import (
    MAX_LEN_ORIGINAL, MAX_LEN_SHORT, CUSTOM_ID_PATTERN,
    MAX_GENERATE_ATTEMPTS, OCCUPIED_ID, REDIRECT_VIEW
)
from yacut import app, db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LEN_ORIGINAL), nullable=False)
    short = db.Column(db.String(MAX_LEN_SHORT), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get(short_id):
        return URLMap.query.filter_by(short=short_id).first()

    @staticmethod
    def is_invalid_custom_id(custom_id):
        return (custom_id == OCCUPIED_ID
                or not CUSTOM_ID_PATTERN.match(custom_id))

    @staticmethod
    def is_duplicate_custom_id(custom_id):
        return URLMap.get(custom_id) is not None

    @staticmethod
    def get_unique_short_id():
        for _ in range(MAX_GENERATE_ATTEMPTS):
            short_id = ''.join(
                random.choice(ascii_letters + digits)
                for _ in range(app.config['MAX_LEN_AUTO'])
            )
            if not URLMap.get(short_id) and short_id != OCCUPIED_ID:
                return short_id

    @staticmethod
    def create(original, short):
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    def get_short_link(self):
        return url_for(
            REDIRECT_VIEW,
            short_id=self.short,
            _external=True
        )