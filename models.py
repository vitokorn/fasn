from pydantic import BaseModel


class PostAnalytics():
    def __init__(self, date, likes, dislikes):
        self.date = date
        self.likes = likes
        self.dislikes = dislikes


class User():
    def __init__(self, id, last_login,username,first_name,email,last_activity):
        self.id = id
        self.last_login = last_login
        self.username = username
        self.first_name = first_name
        self.email = email
        self.last_activity = last_activity


class PostDB():
    def __init__(self,id,title,description,author_id):
        self.id = id
        self.title = title
        self.description = description
        self.author_id = author_id


class PostStatistic():
    def __init__(self, like, dislike, user_id):
        self.like = like
        self.dislike = dislike
        self.user_id = user_id


class Post(BaseModel):
    title:str
    description:str
    author_id: int


class PostLike(BaseModel):
    post_id: int
    like:bool
    user_id:int


class PostDislike(BaseModel):
    post_id: int
    dislike:bool
    user_id:int


class UserLogin(BaseModel):
    username:str
    password:str


class UserAuth(UserLogin):
    first_name:str
    email:str


class UserOut(BaseModel):
    id: int
    email: str
    username:str


class Tokens(BaseModel):
    access_token:str
    refresh_token:str


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class Refresh(BaseModel):
    refresh_token: str
