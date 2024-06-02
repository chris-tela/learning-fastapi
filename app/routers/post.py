from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import  Optional, List
# gives us access to other sql functions like COUNT(*)
from sqlalchemy import func


router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)





# PATH operation
# decorator, references FastAPI() instance --> get method sends request to API --> "/" is the path after url, ex "/posts/vote" would be http://127.0.0.1:8000/posts/vote

# List[] is imported from typing, returns a list of dictionaries
@router.get("/" , response_model=List[schemas.PostOut])
# limit is default posts shown, ex 10 = 10 posts shown
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, offset: int = 0, search: Optional[str] = ""):
    #cursor.execute("""SELECT * FROM public.post""")
    #fetch all gets all from the db
    #posts = cursor.fetchall()
    # posts  = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(offset)
    # performing a left OUTER join
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    print(results)
    return results

# when creating a code, you should return status 201 
@router.post("/", status_code = status.HTTP_201_CREATED, response_model= schemas.Post)
# oauth2.get_current_user adds a dependency that expects a access token --> meaning a user should be logged in to create a post
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO public.post (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.priv))
    #new_post = cursor.fetchone()
    
    #commits to the postgres database
    #conn.commit()
    # ** unloads all of Post()'s properties into a python dictionary, where models.post() converts it into SQL to be added into the database
    new_post = models.Post(user_id = current_user.id, **post.__dict__)
    db.add(new_post)
    db.commit()
    #retrieve new post, store it back in variable new_post
    db.refresh(new_post)

    return new_post
# title (str), content (str)



#retrieving data of one post
# {id} is the specific id a user is interested in, called a PATH parameter
@router.get("/{id}", response_model=schemas.PostOut)
# :int automatically converts to integer
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Find first instance and return
    
    # return post features and number of votes
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()


    
 #   post = find_post(id)
    if not results:
        raise  HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"not found")


    
   # cursor.execute(f"""SELECT * FROM public.post WHERE ID = %s """, (str(id)))
   # post = cursor.fetchone()
    return results


@router.delete("/{id}")
def delete_post(id: int, status_code = status.HTTP_204_NO_CONTENT, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # delete post, find index in array that has the ID to be deleted
    #my_posts.pop(index)

    #cursor.execute("""DELETE FROM public.post WHERE ID = %s  RETURNING *""", (str(id)))
    #deleted = cursor.fetchone()
    #conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post wiht id: {id} does not exist")
    
    # check if post id is under current user --> you cannot delete another users post
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not your account!")

    post_query.delete(synchronize_session = False)
    db.commit()
    
    return Response(status_code = status.HTTP_204_NO_CONTENT)



# updating operation, id is post that needs to be updated
@router.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE public.post SET title = %s, content = %s, published = %s WHERE ID = %s RETURNING *""", (post.title, post.content, post.priv, str(id)))
    #updated = cursor.fetchone()
    #conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post wiht id: {id} does not exist")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not your account!")

    post_query.update(updated_post.__dict__, synchronize_session=False)

    db.commit()
    return post_query.first()
