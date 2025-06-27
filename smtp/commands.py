from typing import Final

class SMTPCommands:
    CRLF: Final[str] = "\r\n"

    @staticmethod
    def ehlo(domain: str = "localhost") -> str:
        return f"EHLO {domain}{SMTPCommands.CRLF}"

    @staticmethod
    def mail_from(address: str) -> str:
        return f"MAIL FROM:<{address}>{SMTPCommands.CRLF}"

    @staticmethod
    def rcpt_to(address: str) -> str:
        return f"RCPT TO:<{address}>{SMTPCommands.CRLF}"

    @staticmethod
    def data() -> str:
        return f"DATA{SMTPCommands.CRLF}"

    @staticmethod
    def quit() -> str:
        return f"QUIT{SMTPCommands.CRLF}"
