
from dataclasses import dataclass


@dataclass(frozen=True)
class SMTPSettings:
    host: str
    port: int = 25
    use_tls: bool = False
    username: str | None = None
    password: str | None = None


@dataclass(frozen=True)
class SMSSettings:
    sender_email: str
