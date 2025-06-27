from dataclasses import dataclass
from sms.interfaces import ISMSMessage


@dataclass
class SMSMessage(ISMSMessage):
    sender: str
    recipient: str
    body: str

    def format(self) -> str:
        return (
            f"From: {self.sender}\r\n"
            f"To: {self.recipient}\r\n"
            f"Subject: SMS\r\n"
            f"Content-Type: text/plain; charset=utf-8\r\n"
            f"\r\n"
            f"{self.body}\r\n.\r\n"
        )
