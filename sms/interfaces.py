from abc import ABC, abstractmethod

class ISMSMessage(ABC):
    @abstractmethod
    def format(self) -> str:
        """Format the SMS message as a string ready for SMTP."""
        pass


class ISMSGateway(ABC):
    @abstractmethod
    def format_number(self, phone_number: str, carrier: str) -> str:
        """Format the phone number and carrier into an email address."""
        pass
