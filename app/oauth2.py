from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#SECRET_KEY
#Algorithm for encryption
#Expiration time --> how long the user can stay logged in after performing a login 

#any long text
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):

    #make a copy of data: dict to manipulate a few things without changing the original
    to_encode = data.copy()
    # expiry is the current time + expire_minutes time which is 30
    # ex. u login at 15:00 --> 30 minutes = relogin at 15:30
    current_time = datetime.now(timezone.utc)
    # fixing timezones
    expire = current_time + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES) 
    print(expire)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
    return encoded_jwt
def verify_access_token(token: str, credentials_exception):
    try:
        # decode token to verify it
        print(0)
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        print(1)
        # get users id from the decoded string --> we pass the token in as user_id
        id: str = payload.get("user_id")
        print(2)
        if id is None:
            raise credentials_exception
        #validate token schema
        token_data = schemas.TokenData(id = str(id))
    except JWTError as e:
        print(f"JWTError: {e}")

        raise credentials_exception
    
    return token_data
    
# pass this as a dependency, will verify and extract id for us
# once access token returns token data, get_current_user fetches the user_id from the db
def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    # provides logic for verifying token that access is working

    token = verify_access_token(token, credentials_exception)
    # find first ID given
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user