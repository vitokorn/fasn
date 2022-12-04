import datetime
import re
import traceback

from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm

from db import get_user, cur, con
from models import TokenSchema, Refresh, UserAuth, UserOut, UserLogin
from utils import create_access_token, create_refresh_token, decode_token, get_hashed_password, verify_password

router = APIRouter()


@router.post('/auth/login_form', summary="Create access and refresh tokens for user", response_model=TokenSchema,tags=['auth'])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username,None)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user[1]
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    dt = datetime.datetime.now()
    cur.execute(f"UPDATE users_snuser SET last_activity = '{dt}',last_login = '{dt}' WHERE email = '{user[2]}'")
    con.commit()

    return {
        "access_token": create_access_token(user[2]),
        "refresh_token": create_refresh_token(user[2]),
    }


@router.post('/auth/login', summary="Create access and refresh tokens for user", response_model=TokenSchema,tags=['auth'])
async def login(data: UserLogin):
    user = get_user(data.username,None)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user[1]
    if not verify_password(data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    dt = datetime.datetime.now()
    cur.execute(f"UPDATE users_snuser SET last_activity = '{dt}',last_login = '{dt}' WHERE email = '{user[2]}'")
    con.commit()

    return {
        "access_token": create_access_token(user[2]),
        "refresh_token": create_refresh_token(user[2]),
    }

@router.post('/auth/refresh', summary="Refresh access token for user", response_model=TokenSchema,tags=['auth'])
async def refresh(refresh:Refresh):
    expired,email = decode_token(refresh.refresh_token)
    if expired:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired"
        )
    user = get_user(None,email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    return {
        "access_token": create_access_token(user[2]),
        "refresh_token": create_refresh_token(user[2]),
    }


@router.post('/auth/signup', summary="Create new user", response_model=UserOut,tags=['auth'])
async def reg(data: UserAuth):
    # querying database to check if user already exist
    user = get_user(data.username,None)
    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
    )
    try:
        print(data.email)
    except:
        print(traceback.format_exc())
    regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    if regex.search(data.email):
        user = {
            'email': data.email,
            'password': get_hashed_password(data.password),
            'first_name': data.first_name,
            'username': data.username
        }
        date_joined = datetime.datetime.now()
        params = (data.username,data.email,user['password'],date_joined,0,data.first_name,"",0,1,date_joined)
        insert = cur.execute(f"INSERT INTO users_snuser (username,email,password,date_joined,is_superuser,first_name,last_name,is_staff,is_active,last_activity) values (?,?,?,?,?,?,?,?,?,?)",params)
        con.commit()
        var = insert.lastrowid
        user['id'] = var
        print(user)
        return user
    else:
        raise HTTPException(detail="email is not valid", status_code=status.HTTP_400_BAD_REQUEST)
