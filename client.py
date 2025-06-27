import base64
import logging
from smtp.secure_connection import STARTTLSSMTPConnection
from sms.gateways import SMSGateway
from config.settings import SMTPSettings

logger = logging.getLogger("client")

class SMSMailer:
    def __init__(self, smtp_settings: SMTPSettings) -> None:
        self.smtp_settings = smtp_settings
        self.gateway = SMSGateway()

    def send_sms(
        self,
        phone_number: str,
        carrier: str,
        message_body:
    str) -> None:
        to_address = self.gateway.format_number(phone_number, carrier)
        logger.info(f"Preparing to send SMS to {to_address}")


        if not all([
            self.smtp_settings.username,
            self.smtp_settings.password,
            message_body,
        ]) or None in (self.smtp_settings.username, self.smtp_settings.password, message_body):
            raise ValueError("SMTP credentials or message body cannot be None or empty")

        conn = STARTTLSSMTPConnection(self.smtp_settings.host, self.smtp_settings.port)
        try:
            conn.connect()


            encoded_username = base64.b64encode(
                self.smtp_settings.username.encode('utf-8')).decode('utf-8')
            encoded_password = base64.b64encode(
                self.smtp_settings.password.encode('utf-8')).decode('utf-8')

            for cmd in [
                "AUTH LOGIN",
                encoded_username,
                encoded_password
            ]:
                resp = conn.send_command(cmd)
                if not (resp.startswith("334") or resp.startswith("235")):
                    raise RuntimeError(f"Auth failed: {resp}")

            for cmd, err in [
                (f"MAIL FROM:<{self.smtp_settings.username}>", "MAIL FROM rejected"),
                (f"RCPT TO:<{to_address}>", "RCPT TO rejected")
            ]:
                if not conn.send_command(cmd).startswith("250"):
                    raise RuntimeError(f"{err}")

            if not conn.send_command("DATA").startswith("354"):
                raise RuntimeError("DATA not accepted")

            msg = (
                f"From: {self.smtp_settings.username}\r\n"
                f"To: {to_address}\r\n"
                f"Subject: [ALERT]\r\n"
                "Content-Type: text/plain; charset=utf-8\r\n\r\n"
                f"{message_body}\r\n.\r\n"
            )

            logger.debug(f"Constructed message:\n{msg}")

            if conn.sock is None:
                raise RuntimeError("Socket not connected")

            conn.sock.sendall(msg.encode('utf-8'))
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
