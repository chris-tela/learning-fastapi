from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session

# creating a 
router = APIRouter(
    prefix= "/users",
    tags = ['Users']
)

#PATH OPERATIONS with User
# response_model is the way the data is sent back to user. in this case we do not want to send back their password
@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.UserOut)
# we're going to be using our database to create a new user, so db: session is needed
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #create hash of user first - user.password, referencing utils file       
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.__dict__)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model= schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"user with id: {id} does not exist")
    return user