import base64
import logging
from smtp.secure_connection import STARTTLSSMTPConnection
from sms.gateways import SMSGateway
from config.settings import SMTPSettings
from typing import NoReturn

logger = logging.getLogger("client")

class SMSMailer:
    def __init__(self, smtp_settings: SMTPSettings) -> None:
        self.smtp_settings = smtp_settings
        self.gateway = SMSGateway()

    def send_sms(
        self, 
        phone_number: str, 
        carrier: str, 
        message_body: str
        ) -> NoReturn:

        to_address = self.gateway.format_number(phone_number, carrier)
        logger.info(f"Preparing to send SMS to {to_address}")
        conn = STARTTLSSMTPConnection(self.smtp_settings.host, self.smtp_settings.port)
        try:
            conn.connect()
            for cmd in [
                    "AUTH LOGIN",
                    base64.b64encode(
                        self.smtp_settings.username.encode())
                        .decode(),
                    base64.b64encode(
                        self.smtp_settings.password.encode())
                        .decode()
                        ]:
                
                resp = conn.send_command(cmd)
                if not (resp.startswith("334") or resp.startswith("235")): 
                    raise RuntimeError(f"Auth failed: {resp}")
                
            for cmd, err in [(f"MAIL FROM:<{self.smtp_settings.username}>", 
                            "MAIL FROM rejected"),
                            (f"RCPT TO:<{to_address}>", "RCPT TO rejected")]:
                
                if not conn.send_command(cmd).startswith("250"): raise RuntimeError(f"{err}")

            if not conn.send_command("DATA").startswith("354"): raise RuntimeError("DATA not accepted")

            msg = (
                f"From: {self.smtp_settings.username}\r\nTo: {to_address}\r\nSubject: [ALERT]\r\n"
                "Content-Type: text/plain; charset=utf-8\r\n\r\n" 
                + message_body + 
                "\r\n.\r\n")
            
            conn.sock.sendall(msg.encode())
            if not conn._recv().startswith("250"): 
                raise RuntimeError("Message send failed")
            conn.send_command("QUIT")
            logger.info("SMS sent successfully")

        except Exception as e:
            logger.error(f"Failed to send SMS: {e}")
            raise
        finally:
            conn.close()
            logger.debug("Connection closed")


