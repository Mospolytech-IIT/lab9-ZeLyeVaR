from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, init_db
from . import crud, schemas

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, username=user.username, email=user.email, password=user.password)

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.post("/posts/", response_model=schemas.PostCreate)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db=db, title=post.title, content=post.content, user_id=post.user_id)

@app.get("/posts/")
def read_posts(db: Session = Depends(get_db)):
    return crud.get_posts(db)
