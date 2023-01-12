from passlib.context import CryptContext


pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:

    def bcrypt(password: str):
        hashed_pasword = pwd_ctx.hash(password)
        return hashed_pasword

    def verify(hashed_pasword, plain_password):
        return pwd_ctx.verify(plain_password, hashed_pasword)