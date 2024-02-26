from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
  title: str
  content: str
  published: bool = True

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

@app.get('/')
def root():
  return {"messege": "Hello world"}


@app.get('/posts')
def get_posts():
  cursor.execute("""SELECT * FROM posts""")
  posts = cursor.fetchall()
  # print(posts)
  return {"data": posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
  cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
  new_post = cursor.fetchone()
  # print(new_post)
  conn.commit()
  return {"data": new_post}

  # post_dict = post.model_dump()
  # post_dict['id'] = randrange(0, 100000)
  # my_posts.append(post_dict)
  # return {"data": "created post"}


@app.get('/posts/{id}')
def get_post(id: int): #response: Response need to be passed if if we use response
  cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
  post=cursor.fetchone()
  # print(test_post)
  # post = find_post(id)
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
  return {"post details": post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

  cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
  # index = find_index_post(id)
  deleted_post = cursor.fetchone()
  conn.commit()
  if deleted_post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exists')
  # my_posts.pop(inde)
  return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id: int, post: Post):

  cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
  # index = find_index_post(id)
  updated_post = cursor.fetchone()
  conn.commit()
  if updated_post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exists')
  
  # post_dict = post.model_dump()
  # post_dict['id'] = id
  # my_posts[index] = post_dict
  return {"data": updated_post}

