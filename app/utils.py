from passlib.context import CryptContext
# telling passlib what the default hashing algorithm is to hide passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated ='auto')


def hash(password: str):
    return pwd_context.hash(password)


def verify(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)