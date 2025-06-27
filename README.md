# 📬 Email-to-SMS Gateway via SMTP

This project provides a simple Python interface for sending SMS messages using email-to-SMS gateways via a configurable SMTP client. It’s useful for sending alerts, notifications, or messages to mobile phones from internal applications.

---

## 🧰 Features

- Send SMS messages via email using carrier gateways
- Configurable SMTP and SMS settings
- Secure authentication using environment variables or config classes
- Simple API with `SMSMailer.send_sms()`

---

## 📦 Requirements

- Python 3.7+
- A valid SMTP account (e.g., Gmail)
- Carrier that supports email-to-SMS (e.g., `number@vtext.com` for Verizon)

# 📬 Email-to-SMS Gateway via SMTP

This project provides a simple Python interface for sending SMS messages using email-to-SMS gateways via a configurable SMTP client. It’s useful for sending alerts, notifications, or messages to mobile phones from internal applications.

---

## 🧰 Features

- Send SMS messages via email using carrier gateways  
- Configurable SMTP and SMS settings  
- Secure authentication using environment variables or config classes  
- Simple API with `SMSMailer.send_sms()`

---

## 📦 Requirements

- Python 3.7+
- A valid SMTP account (e.g., Gmail)
- Carrier that supports email-to-SMS (e.g., `number@vtext.com` for Verizon)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Here's how to use the library with your own configuration.

### 1. Set Up Your Python Script

Import the necessary classes and initialize logging:

```python
from config.settings import SMTPSettings, SMSSettings
from client import SMSMailer
from config.logging_config import setup_logging

setup_logging()
```

### 2. Define Your SMTP Settings

Create an instance of `SMTPSettings` with your SMTP provider's credentials.

> ⚠️ Warning: Do not hard-code credentials in production. Use environment variables or a secrets manager.

```python
smtp_settings = SMTPSettings(
    host="smtp.gmail.com",
    port=587,
    use_tls=True,
    username="your-email@gmail.com",
    password="your-app-password"
)
```

### 3. Define Your SMS Settings

Specify the email address used to send SMS messages:

```python
sms_settings = SMSSettings(
    sender_email="your-email@gmail.com"
)
```

### 4. Create the Mailer and Send an SMS

Instantiate the mailer and send a message to a phone number using the carrier’s email-to-SMS gateway:

```python
mailer = SMSMailer(smtp_settings)

mailer.send_sms(
    phone_number="15551234567",
    carrier="uscelluar",
    message_body="Hello"
)
```

This sends an email to `15551234567@email.uscc.net`, which will arrive as an SMS on the recipient’s phone.

---

## 🛠️ Supported Carriers

The `carrier` argument should be one of the supported carriers defined in your application. Example mappings:

| Carrier    | Gateway Domain     |
|------------|--------------------|
| att        | txt.att.net        |
| verizon    | vtext.com          |
| tmobile    | tmomail.net        |
| uscelluar  | email.uscc.net     |

You can extend the list in your configuration or mapping logic.

---

## 🔒 Security Best Practices

- Use [App Passwords](https://support.google.com/accounts/answer/185833?hl=en) for Gmail accounts instead of your main password.  
- Never hard-code secrets in source code — use environment variables or a `.env` file.  
- Restrict access to the SMTP service to internal apps only.  
- Validate phone numbers and messages to prevent abuse or spam.

---

## 🧪 Example Project Structure

```
email-to-sms/
├── client.py              # SMSMailer implementation
├── config/
│   ├── settings.py        # SMTP and SMS settings classes
│   ├── logging_config.py  # Logging setup
├── main.py                # Example usage script
├── README.md
└── requirements.txt
```

---

## ❓ FAQ

**Q: Why isn't the message sending?**  
A: Check the following:

- SMTP credentials are correct  
- App password is enabled (if using Gmail)  
- Port and TLS settings match your SMTP provider  
- Phone number format is correct (no spaces or dashes)  
- Carrier supports email-to-SMS  

**Q: Can I use this with Outlook, Yahoo, etc.?**  
A: Yes, just update the `host`, `port`, and credentials in the `SMTPSettings`.

---

# NOTE:
This project is a WIP and will recieve updates due time
