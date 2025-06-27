# sms/gateways.py

from typing import Final
from sms.interfaces import ISMSGateway


class SMSGateway(ISMSGateway):

    CARRIER_DOMAINS: Final[dict[str, str]] = {
        "verizon": "vtext.com",
        "att": "txt.att.net",
        "tmobile": "tmomail.net",
        "sprint": "messaging.sprintpcs.com",
        "boost": "sms.myboostmobile.com",
        "cricket": "sms.cricketwireless.net",
        "googlefi": "msg.fi.google.com",
        "uscelluar": "mms.uscc.net"
    }

    def format_number(self, phone_number: str, carrier: str) -> str:
        domain = self.CARRIER_DOMAINS.get(carrier.lower())
        if domain is None:
            raise ValueError(f"Unsupported carrier: {carrier}")
        return f"{phone_number}@{domain}"
