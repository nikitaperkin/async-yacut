from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import MAX_LEN_ORIGINAL, MAX_LEN_SHORT, SHORT_PATTERN

ORIGINAL_LINK_LABEL = 'Длинная ссылка'
CUSTOM_SHORT_LABEL = 'Ваш вариант короткой ссылки'
FILES_LABEL = 'Выберите файлы'

REQUIRED_FIELD = 'Обязательное поле'
UPLOAD_FILE_REQUIRED = 'Выберите хотя бы один файл'
SHORT_INVALID = 'Допустимы только латинские буквы и цифры'

CREATE_SUBMIT_TEXT = 'Создать'
UPLOAD_SUBMIT_TEXT = 'Загрузить'


class URLMapForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK_LABEL,
        validators=[
            DataRequired(message=REQUIRED_FIELD),
            Length(max=MAX_LEN_ORIGINAL)
        ]
    )
    custom_id = StringField(
        CUSTOM_SHORT_LABEL,
        validators=[
            Optional(),
            Length(max=MAX_LEN_SHORT),
            Regexp(SHORT_PATTERN, message=SHORT_INVALID)
        ]
    )
    submit = SubmitField(CREATE_SUBMIT_TEXT)


class UploadFileForm(FlaskForm):
    files = MultipleFileField(
        FILES_LABEL,
        validators=[
            DataRequired(message=UPLOAD_FILE_REQUIRED)
        ]
    )
    submit = SubmitField(UPLOAD_SUBMIT_TEXT)
