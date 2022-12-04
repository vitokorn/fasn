import datetime

from fastapi import APIRouter, Depends

from db import cur,con
from deps import get_current_user,reuseable_oauth
from models import Post, PostAnalytics, PostDB, PostLike, PostDislike

router = APIRouter()


@router.get("/posts",dependencies=[Depends(get_current_user)],tags=['posts'])
def posts():
    query = f'SELECT id,title,description,author_id FROM posts_post'
    res = cur.execute(f"{query}")
    print(query)
    result = res.fetchall()
    act = []
    for r in result:
        act.append(PostDB(id=r[0],title=r[1],description=r[2],author_id=r[3]))
    return act


@router.get("/posts/analytics/", dependencies=[Depends(get_current_user)],tags=['posts'])
def analytics(date_from:str = '2022-11-25',date_to:str ='2022-12-01'):
    query = f'SELECT created_at_date as date,COUNT(case when like then 1 end) as likes,COUNT(case when dislike then 1 end) as dislikes FROM posts_poststatistic WHERE created_at_date >= "{date_from}" AND created_at_date <= "{date_to}" GROUP BY created_at_date ORDER BY created_at_date;'
    res = cur.execute(query)
    print(query)
    result = res.fetchall()
    stat = []
    for res in result:
        print(res[0])
        stat.append(PostAnalytics(date=res[0], likes=res[1], dislikes=res[2]))
    return stat


@router.post("/posts/create",dependencies=[Depends(reuseable_oauth)],tags=['posts'])
def create_post(post: Post):
    post_item = post.dict()
    title = post_item['title']
    description = post_item['description']
    author_id = post_item['author_id']
    created_at = datetime.date.today()
    updated_at = datetime.datetime.now()
    params = (title,description,author_id,created_at,updated_at)
    insert = cur.execute(f"INSERT INTO posts_post (title,description,author_id,created_at,updated_at) values (?,?,?,?,?)",params)
    con.commit()
    var = insert.lastrowid
    post_item['id'] = var
    return post_item


@router.post("/posts/like",dependencies=[Depends(get_current_user)],tags=['posts'])
def like_post(like:PostLike):
    like_item = like.dict()
    post = like_item['post_id']
    likeb = like_item['like']
    dislike = False
    user = like_item['user_id']
    created_at = datetime.datetime.now()
    created_at_date = datetime.date.today()
    params = (post,likeb,dislike,user,created_at,created_at_date)
    insert = cur.execute(f"INSERT INTO posts_poststatistic (post_id,like,dislike,user_id,created_at,created_at_date) values (?,?,?,?,?,?)",params)
    con.commit()
    var = insert.lastrowid
    like_item['id'] = var
    return {'message':f'Post {post} successfully liked'}


@router.post("/posts/dislike",dependencies=[Depends(get_current_user)],tags=['posts'])
def dislike_post(dislike:PostDislike):
    dislike_item = dislike.dict()
    post = dislike_item['post_id']
    like = False
    dislikeb = dislike_item['dislike']
    user = dislike_item['user_id']
    created_at = datetime.datetime.now()
    created_at_date = datetime.date.today()
    params = (post,like,dislikeb,user,created_at,created_at_date)
    insert = cur.execute(f"INSERT INTO posts_poststatistic (post,like,dislike,user,created_at,created_at_date) values (?,?,?,?,?,?)",params)
    con.commit()
    var = insert.lastrowid
    dislike_item['id'] = var
    return {'message':f'Post {post} successfully disliked'}
