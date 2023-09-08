from fastapi import APIRouter,Depends,status,HTTPException

from typing import List
from sqlalchemy.orm import Session
import schemas,database,models
from hashing import Hash
from repository import blog



router = APIRouter(
    prefix='/blog',
    tags=['Blogs']

)
get_db = database.get_db()


@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(database.get_db)):
    return blog.get_all(db)

@router.post('/', status_code=status.HTTP_201_CREATED)  # this will help in create the forth item /item
def create_blog(request: schemas.Blog, db: Session = Depends(database.get_db)):
    return blog.create(request,db)



@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(database.get_db)):
    return blog.destroy(id,db)

# update a blog
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)  # using docs tags
def update(id, request: schemas.Blog, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).update(request.dict())
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {id} is not found')

    blog.update(request.dict())

    db.commit()

    return 'updated'




@router.get('/{id}', status_code=200, response_model=List[schemas.ShowBlog])  # I need to get a list of the schema
def show(id, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")

    return blog



