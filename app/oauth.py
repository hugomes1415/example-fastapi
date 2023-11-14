from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models, config
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

ouath2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = config.settings.secret_key
ALGORITHM = config.settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.access_token_expire_time

def creat_access_token(data: dict):
    to_encode = data.copy()

    expire =  datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verif_access_token(token: str, credencials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])



        id = str(payload.get("user_id"))

        if id is None:
            raise credencials_exception
        


        token_data = schemas.TokenData(id=id) 

    except JWTError:
        raise credencials_exception
    
    return token_data

def get_creat_user(token: str = Depends(ouath2_scheme), db: Session = Depends(database.get_db)):
    crededentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                            detail = f"could not validate credencials", headers={"WWW-Authenticate": "Bearer"})
    
    token = verif_access_token(token, crededentials_exception)

    

    user = db.query(models.User).filter(models.User.id == token.id).first()



    return user