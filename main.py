import time
import sqlite3

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi import status

from db import last_activity
from routers import auth,posts,users
from utils import decode_token

con = sqlite3.connect("db.sqlite3",check_same_thread=False)
cur = con.cursor()
app = FastAPI()
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(users.router)


@app.middleware("http")
async def add_activity_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Last-Activity"] = f'{time.time().__trunc__()}'
    if 'Authorization' in request.headers and request.headers['Authorization'] and 'Bearer' in request.headers['Authorization']:
        print('79')
        print(request.headers['Authorization'])
        token = request.headers['Authorization'].replace('Bearer ',"")
        expired,email = decode_token(token)
        if expired:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired"
            )
        last_activity(email)
    return response


@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')
