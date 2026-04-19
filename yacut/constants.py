from string import ascii_letters, digits
import re


MAX_LEN_ORIGINAL = 2048
MAX_LEN_SHORT = 16
MAX_LEN_AUTO = 6
MAX_GENERATE_ATTEMPTS = 10
OCCUPIED_SHORT = 'files'

SHORT_ALLOWED_CHARS = f'{ascii_letters}{digits}'

SHORT_PATTERN = re.compile(rf'^[{SHORT_ALLOWED_CHARS}]+$')

REDIRECT_VIEW = 'redirect_view'
