from fastapi import FastAPI, status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import  List, Optional
from .. import schemas, models, oauth
from ..database import get_db


router = APIRouter(
    prefix="/posts",
    tags=['posts']
)

@router.get("/")
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth.get_creat_user),
                     limit : int = 10, skip : int = 0, search: Optional[str] = ""):

    

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")
                       ).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True
                              ).filter(models.Post.owner_id == current_user.id, models.Post.title.contains(search)
                                       ).group_by(models.Post.id).limit(limit).offset(skip)
    
    
    

    posts_out = [schemas.PostOut(**{**one_post[0].__dict__, "owner": one_post[0].owner.__dict__,  "votes": one_post[1]}) for one_post in results]

    return {"data": posts_out}




@router.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth.get_creat_user)):




    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return {"data": posts}





@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(post: schemas.PostCreat, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_creat_user)):

    

    

    new_post= models.Post(owner_id=current_user.id ,**post.dict())
    
    


    db.add(new_post)
    db.commit()
    db.refresh(new_post)


    
    new_post_out=schemas.Post(**new_post.__dict__)

    return {"data": new_post_out}




@router.get("/{id}")
def get_posts(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_creat_user)):


    post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")
                       ).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True
                              ).filter(models.Post.id == id).group_by(models.Post.id).first()
    


    

    if not post[0]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} was not founds")
    
    if post[0].owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"This post cant be accessed once it is not your post")
    

    post_out = schemas.PostOut(**{**post[0].__dict__, "owner": post[0].owner.__dict__, "votes": post[1]})

    return {"post_detail": post_out}





@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_creat_user)):

    


    post = db.query(models.Post).filter(models.Post.id == id)
    post_query = post.first()

    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found")
    
    if post_query.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"This post cant be deleted once it is not your post")


    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)




@router.put("/{id}")
def update_post(id: int, updated_post: schemas.PostBase, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_creat_user)):
    
    
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()


    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"This post cant be updated once it is not your post")



    post_query.update(updated_post.dict(), synchronize_session=False)
    
    db.commit()

    
    post_out = schemas.Post(**post_query.first().__dict__)

    return {'data': post_out}