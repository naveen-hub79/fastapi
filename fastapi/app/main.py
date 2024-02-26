from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2

from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
import time
from . import models
from .routers import post, user
from .database import engine, SessionLocal, get_db



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
  try:
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='P@ssw0rd', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was successful !!!")
    break
  except Exception as error:
    print("Database connection failed")
    print("Error:",error)
    time.sleep(3)


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "title of post 2", "content": "content of post 2", "id": 2}]

def find_post(id):
  for p in my_posts:
    if p["id"] == id:
      return p

def find_index_post(id):
  for i,p in enumerate(my_posts):
    if p['id'] == id:
      return i
    

app.include_router(post.router)
app.include_router(user.router)


@app.get('/')
def root():
  return {"messege": "Hello world"}






