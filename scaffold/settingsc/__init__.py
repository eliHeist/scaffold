from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Import modular settings
from .apps import *
from .storage import *
from .security import *
from .templates import *

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Kampala'
USE_I18N = True
USE_TZ = True


