from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import MAX_LEN_ORIGINAL, MAX_LEN_SHORT, CUSTOM_ID_PATTERN

ORIGINAL_LINK_LABEL = 'Длинная ссылка'
CUSTOM_ID_LABEL = 'Ваш вариант короткой ссылки'
FILES_LABEL = 'Выберите файлы'

MSG_REQUIRED_FIELD = 'Обязательное поле'
MSG_UPLOAD_FILE_REQUIRED = 'Выберите хотя бы один файл'
MSG_CUSTOM_ID_INVALID = 'Допустимы только латинские буквы и цифры'

CREATE_SUBMIT_TEXT = 'Создать'
UPLOAD_SUBMIT_TEXT = 'Загрузить'


class URLMapForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK_LABEL,
        validators=[
            DataRequired(message=MSG_REQUIRED_FIELD),
            Length(max=MAX_LEN_ORIGINAL)
        ]
    )
    custom_id = StringField(
        CUSTOM_ID_LABEL,
        validators=[
            Optional(),
            Length(max=MAX_LEN_SHORT),
            Regexp(CUSTOM_ID_PATTERN, message=MSG_CUSTOM_ID_INVALID)
        ]
    )
    submit = SubmitField(CREATE_SUBMIT_TEXT)


class UploadFileForm(FlaskForm):
    files = MultipleFileField(
        FILES_LABEL,
        validators=[
            DataRequired(message=MSG_UPLOAD_FILE_REQUIRED)
        ]
    )
    submit = SubmitField(UPLOAD_SUBMIT_TEXT)