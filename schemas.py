from pydantic import BaseModel


class Blog(BaseModel):
    title:str
    body: str
#we call pydantic models schema

#will create another schema to show blog
class ShowBlog(BaseModel):
    title:str
    body:str

    class Config:
        orm_mode =True

# create a User

class User(BaseModel):
    name:str
    email:str
    password:str

