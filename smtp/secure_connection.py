# smtp/secure_connection.py

import socket
import ssl
import logging
from smtp.interfaces import SMTPConnection

logger = logging.getLogger(__name__)

class STARTTLSSMTPConnection(SMTPConnection):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self) -> str:
        logger.info(f"Connecting to {self.host}:{self.port} (plain socket)")
        raw_sock = socket.create_connection((self.host, self.port), timeout=10)
        self.sock = raw_sock
        greeting = self._recv()

        
        self.send_command("EHLO localhost")

        
        self.send_command("STARTTLS")
        logger.info("Upgrading connection to TLS")
        context = ssl.create_default_context()
        self.sock = context.wrap_socket(raw_sock, server_hostname=self.host)

       
        return self.send_command("EHLO localhost")

    def send_command(self, command: str) -> str:
        logger.debug(f"Sending command: {command.strip()}")
        self.sock.sendall(command.encode("utf-8") + b"\r\n")
        return self._recv()

    def send(self, message: str) -> str:
        logger.info("Sending message")
        self.sock.sendall(message.encode("utf-8") + b"\r\n")
        return self._recv()

    def close(self) -> None:
        if self.sock:
            logger.info("Closing TLS socket")
            self.sock.close()
            self.sock = None

    def _recv(self) -> str:
        response = b""
        while True:
            chunk = self.sock.recv(1024)
            response += chunk
            if b"\r\n" in chunk or not chunk:
                break
        decoded = response.decode("utf-8", errors="replace")
        logger.debug(f"Response: {decoded.strip()}")
        return decoded
