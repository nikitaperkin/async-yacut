from string import ascii_letters, digits
import re


MAX_LEN_ORIGINAL = 256
MAX_LEN_SHORT = 16
MAX_GENERATE_ATTEMPTS = 10
OCCUPIED_ID = 'files'

SHORT_ALLOWED_CHARS = f'{ascii_letters}{digits}'

CUSTOM_ID_PATTERN = re.compile(
    r'^[{chars}]{{1,{max_len}}}$'.format(
        chars=SHORT_ALLOWED_CHARS,
        max_len=MAX_LEN_SHORT,
    )
)

REDIRECT_VIEW = 'redirect_view'
MSG_SHORT_ID_TAKEN = 'Предложенный вариант короткой ссылки уже существует.'