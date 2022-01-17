from fastapi import FastAPI, Body, Depends
from models import PostSchema, UserSchema, UserLoginSchema
from auth.jwt_handler import sign_jwt
from auth.jwtbearer import JWTBEARER

# create list of posts with id, title, content
posts = [
    {
        'id': 1,
        'title': 'First post',
        'content': 'This is the first post'

    },
    {
        'id': 2,
        'title': 'Tigers',
        'content': 'Tigers are cool'
    },
    {
        'id': 3,
        'title': 'Tortoises',
        'content': 'Tortoises are cool'
    }
]

users = []

app = FastAPI()


@app.get("/", tags=['test'])
def greet():
    return {"message": "Hello World"}


@app.get('/posts', tags=['posts'])
def get_all_posts():
    return {'data': posts}


@app.get('/posts/{post_id}', tags=['posts'])
def get_post_by_id(post_id: int):
    if post_id > len(posts) or post_id < 0:
        return {
            'error': 'This post does not exist'
        }
    for post in posts:
        if post['id'] == post_id:
            return {
                'data': post
            }


@app.post('/posts', tags=['posts'], dependencies=[Depends(JWTBEARER)])
def add_post(post: PostSchema):
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        'message': 'Post added successfully'
    }


@app.post('/user/signup', tags=['users'])
def signup_user(user: UserSchema = Body(default=None)):
    users.append(user)
    return sign_jwt(user.email)


def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        return False


@app.post('/user/login', tags=['users'])
def user_login(user: UserLoginSchema = Body(default=None)):
    if check_user(user):
        return sign_jwt(user.email)
    return {
        'message': 'Invalid credentials'
    }
