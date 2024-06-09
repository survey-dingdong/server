from app.auth.domain.port.output.auth import ExternalSystemPort
from app.auth.domain.vo import EmailVerificationType


class ExternalSystemAdapter:
    def __init__(self, port: ExternalSystemPort):
        self.port = port

    async def send_email(
        self, email: str, code: str, verification_type: EmailVerificationType
    ) -> None:
        await self.port.send_email(
            email=email, code=code, verification_type=verification_type
        )
