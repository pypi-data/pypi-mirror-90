import os
from datetime import timedelta, datetime

from fss_utils.jwt_validate import JWTValidator
from fss_utils.vouch_helper import VouchHelper

CILOGON_JWKS_URL = os.getenv('CILOGON_JWKS_URL')
CILOGON_KEY_REFRESH = os.getenv('CILOGON_KEY_REFRESH')
t = datetime.strptime(CILOGON_KEY_REFRESH, "%H:%M:%S")

jwt_validator = JWTValidator(CILOGON_JWKS_URL,
                             timedelta(hours=t.hour, minutes=t.minute, seconds=t.second))

vouch_cookie_name = os.getenv('VOUCH_COOKIE_NAME')
vouch_secret = os.getenv('VOUCH_COOKIE_SECRET')
vouch_compression = os.getenv('VOUCH_COOKIE_COMPRESSION')
vouch_compression_enable = False
if vouch_compression.lower() == 'true':
    vouch_compression_enable = True

vouch_helper = VouchHelper(secret=vouch_secret, compression=vouch_compression_enable,
                           cookie_name=vouch_cookie_name)
