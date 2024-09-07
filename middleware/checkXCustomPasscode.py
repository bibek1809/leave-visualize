from flask import request
from utils import Configuration
from utils.token_encryption import TokenEncryptor


class PasscodeValidator:

    @staticmethod
    def validate(passcode):
        decrypted_passcode = TokenEncryptor.decrypt_token(passcode)
        if decrypted_passcode != Configuration.X_CUSTOM_PASSCODE:
            return False
        return True

