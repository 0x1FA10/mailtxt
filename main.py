from config.settings import SMTPSettings, SMSSettings
from client import SMSMailer
from config.logging_config import setup_logging

setup_logging()

smtp_settings = SMTPSettings(
    host="smtp_server",
    port=587,
    use_tls=True,
    username="smtpuser",
    password="smptpassword"
)

sms_settings = SMSSettings(
    sender_email="youremail"
)

mailer = SMSMailer(smtp_settings)


mailer.send_sms(
    phone_number="123456729298",
    carrier="uscelluar",
    message_body="Hello"
)
