
from abc import ABC, abstractmethod

class SMTPConnection(ABC):
    @abstractmethod
    def connect(self) -> str: pass

    @abstractmethod
    def send_command(self, command: str) -> str: pass

    @abstractmethod
    def send(self, message: str) -> str: pass

    @abstractmethod
    def close(self) -> None: pass
