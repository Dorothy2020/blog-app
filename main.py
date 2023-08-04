from typing import List
from fastapi import FastAPI, Depends, status, Response,HTTPException
import schemas, models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from hashing import Hash

# helps in creating models into the database
models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()  # this from database
    try:
        yield db
    finally:
        db.close()  # everything is done close the db


app = FastAPI()  # An instance of FastApI


@app.post("/blog", status_code=status.HTTP_201_CREATED)  # this will help in create the forth item /item
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)  # we refresh to return the newly created blog
    return new_blog

# delete blog
@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id,db:Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False) # delete using sqlalchemy
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'

# update a blog
@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id,request:schemas.Blog,db:Session = Depends(get_db)):
    blog =db.query(models.Blog).filter(models.Blog.id  ==  id).update(request.dict())
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {id} is not found')

    blog.update(request.dict())

    db.commit()

    return 'updated'

# get all blogs from database

@app.get('/blog')
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


# get blogs with id, raising exceptions and getting http status code
@app.get('/blog/{id}', status_code=200, response_model=List[schemas.ShowBlog]) # I need to get a list of the schema
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f"Blog with the id {id} is not available"}
    return blog



@app.post('/user')
def create_user(request:schemas.User,db:Session = Depends(get_db)):
    new_user = models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
