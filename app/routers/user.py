from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, utils, models
from ..database import get_db



router = APIRouter(
    prefix="/user",
    tags=['users']
)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def creat_user(user: schemas.UserCreat, db: Session = Depends(get_db)):


    
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())

    if db.query(models.User).filter(models.User.email == new_user.email).first() != None:
        raise HTTPException(status_code=status.HTTP_306_RESERVED, 
                            detail=f"{new_user.email} is already been used")

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    
    
    return new_user.__dict__

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id : int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()


    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user with {id} was not found")
    
    return user.__dict__