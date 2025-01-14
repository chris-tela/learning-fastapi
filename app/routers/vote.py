from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2

router = APIRouter(
    prefix = "/vote",
    tags = ["VOTE"]
)

@router.post("/", status_code = status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {vote.post_id} does not exist :(")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if(vote.dir == 1):
        #check if there is already a vote for post_id
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = f"user {current_user.id} has already voted on post {vote.post_id}!")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"msg": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail ="vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"msg": "successfully deleted vote"}




        
