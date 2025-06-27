import logging
from socket import create_connection, socket as Socket
from typing import Optional
from smtp.interfaces import SMTPConnection

logger = logging.getLogger(__name__)

class PlainSMTPConnection(SMTPConnection):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sock: Optional[Socket] = None

    def connect(self) -> str:
        logger.info(f"Connecting to {self.host}:{self.port}")
        self.sock = create_connection((self.host, self.port), timeout=10)
        response = self._recv()
        logger.debug(f"Server greeting: {response.strip()}")
        return response

    def send_command(self, command: str) -> str:
        if self.sock is None:
            raise ConnectionError("No socket connection.")
        logger.debug(f"Sending command: {command.strip()}")
        self.sock.sendall(command.encode("utf-8") + b"\r\n")
        response = self._recv()
        logger.debug(f"Response: {response.strip()}")
        return response

    def send(self, message: str) -> str:
        if self.sock is None:
            raise ConnectionError("No socket connection.")
        logger.info("Sending message body")
        self.sock.sendall(message.encode("utf-8") + b"\r\n")
        response = self._recv()
        logger.debug(f"Send response: {response.strip()}")
        return response

    def close(self) -> None:
        if self.sock:
            logger.info("Closing socket")
            self.sock.close()
            self.sock = None

    def _recv(self) -> str:
        response = b""
        while True:
            chunk = self.sock.recv(1024)
            response += chunk
            if b"\r\n" in chunk or not chunk:
                break
        return response.decode("utf-8", errors="replace")
