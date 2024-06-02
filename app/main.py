
from fastapi import FastAPI
#extract fields from body, and convert to a python dictionary

from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from pydantic_settings import BaseSettings


# command that tells sql alchemy to create all the tables, not needed now
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# allowing origins to talk/send requests, in this example it allows google to send requests
# * lets anyone access the API, however not best for security purposes
origins = ["*"]
app.add_middleware(
    # pass in middleware
    # middleware is a function that runs before any request
    CORSMiddleware,
    # specify origin/domains allowed to talk/send requests to API
    allow_origins = origins,
    allow_credentials=True,
    # allowing specific http methods
    allow_methods=["*"],
    # allowing speicifc headers
    allow_headers=["*"],
)

# include post.router --> goes into post.py and looks for a match
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "hello"}

