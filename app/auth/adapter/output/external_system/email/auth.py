from pathlib import Path

from fastapi_mail import MessageSchema, MessageType
from jinja2 import Environment, FileSystemLoader, Template

from app.auth.domain.port.output.auth import ExternalSystemPort
from app.auth.domain.vo import EmailVerificationType
from core.helpers.email import email_client

file_loader = FileSystemLoader(Path(__file__).parent / "templates")
env = Environment(loader=file_loader)


class EmailSender(ExternalSystemPort):
    def signup(self) -> tuple[str, Template]:
        title = "[dingdong-survey] 회원가입 인증 메일"
        template = env.get_template("signup.html")
        return title, template

    def reset_password(self) -> tuple[str, Template]:
        title = "[dingdong-survey] 비밀번호 재설정 메일"
        template = env.get_template("reset_password.html")
        return title, template

    async def send_email(
        self, email: str, code: str, verification_type: EmailVerificationType
    ) -> None:
        subject, template = getattr(self, verification_type)()
        html = template.render(code=code)
        message = MessageSchema(
            subject=subject,
            recipients=[email],
            body=html,
            subtype=MessageType.html,
        )

        await email_client.send_message(message)
