from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 256)]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Optional(), Length(1, 16)]
    )
    submit = SubmitField('Создать')


class UploadFileForm(FlaskForm):
    files = MultipleFileField(
        'Выберите файлы',
        validators=[
            DataRequired(message='Выберите хотя бы один файл')
        ]
    )
    submit = SubmitField('Загрузить')