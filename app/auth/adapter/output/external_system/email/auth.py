from pathlib import Path

from fastapi_mail import MessageSchema, MessageType
from jinja2 import Environment, FileSystemLoader

from app.auth.domain.port.output.auth import ExternalSystemPort
from core.helpers.email import email_client

file_loader = FileSystemLoader(Path(__file__).parent / "templates")
env = Environment(loader=file_loader)


class EmailSender(ExternalSystemPort):
    async def send_email(self, email: str, url: str) -> None:
        template = env.get_template("authentication.html")
        html = template.render(url=url)
        message = MessageSchema(
            subject="[survey-dingdong] 이메일 인증",
            recipients=[email],
            body=html,
            subtype=MessageType.html,
        )

        await email_client.send_message(message)
