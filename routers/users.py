from fastapi import APIRouter, Depends

from db import cur
from deps import get_current_user
from models import User

router = APIRouter()


@router.get("/users/:id",dependencies=[Depends(get_current_user)],tags=['users'])
def user_data(id):
    query = f'SELECT id,last_login,username,first_name,email,last_activity FROM users_snuser WHERE id = {id}'
    res = cur.execute(f"{query}")
    print(query)
    result = res.fetchone()
    user = User(id=result[0],last_login=result[1],username=result[2],first_name=result[3],email=result[4],last_activity=result[5])
    return user


@router.get("/users/activity",dependencies=[Depends(get_current_user)],tags=['users'])
def activity():
    query = f'SELECT id,last_login,username,first_name,email,last_activity FROM users_snuser'
    res = cur.execute(f"{query}")
    print(query)
    result = res.fetchall()
    act = []
    for r in result:
        act.append(User(id=r[0],last_login=r[1],username=r[2],first_name=r[3],email=r[4],last_activity=r[5]))
    return act
