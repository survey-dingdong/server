from core.config import config

LOGIN_SESSION_PREFIX = f"{config.REDIS_KEY_PREFIX}::session"

REFRESH_TOKEN_PREFIX = f"{config.REDIS_KEY_PREFIX}::refresh_token"

EMAIL_VERIFICATION_PREFIX = f"{config.REDIS_KEY_PREFIX}::email_verificaiton"
