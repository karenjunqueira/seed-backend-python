from pwdlib import PasswordHash

PWD_CONTEXT = PasswordHash.recommended()

class PasswordUtil:
 
    @staticmethod
    def get_password_hash(password: str):
        return PWD_CONTEXT.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str):
        return PWD_CONTEXT.verify(plain_password, hashed_password)
