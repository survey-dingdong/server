from app.auth.domain.port.output.auth import ExternalSystemPort


class ExternalSystemAdapter:
    def __init__(self, port: ExternalSystemPort):
        self.port = port

    async def send_email(self, email: str, code: str) -> None:
        await self.port.send_email(email=email, code=code)
