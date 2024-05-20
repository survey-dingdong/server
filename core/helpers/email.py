from fastapi_mail import ConnectionConfig, FastMail

from core.config import config

conf = ConnectionConfig(
    MAIL_USERNAME=config.MAIL_USERNANE,
    MAIL_PASSWORD=config.MAIL_PASSWORD,
    MAIL_FROM=config.MAIL_USERNANE,
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

email_client = FastMail(conf)
