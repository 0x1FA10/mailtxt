from base64 import b64encode
from typing import List


class SMTPAuth:

    @staticmethod
    def auth_login_sequence(username: str, password: str) -> List[str]:

        encoded_user = b64encode(username.encode()).decode()
        encoded_pass = b64encode(password.encode()).decode()

        return [
            "AUTH LOGIN\r\n",
            f"{encoded_user}\r\n",
            f"{encoded_pass}\r\n"
        ]
