from passlib.context import CryptContext
from passlib.exc import UnknownHashError
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
def hash(password: str) -> str:
    return pwd_context.hash(password)
def verify(provided_password: str, stored_hash: str) -> bool:
    try:
        validation_result = pwd_context.verify(provided_password, stored_hash)
    except UnknownHashError:
        return False
    except Exception:
        return False
    else:
        return validation_result
    
