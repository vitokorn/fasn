import string

import requests
import random
import json


def main():
    register_url = 'http://127.0.0.1:8000/auth/signup'
    auth_url = 'http://127.0.0.1:8000/auth/login'
    create_post_url = 'http://127.0.0.1:8000/posts/create'
    get_posts = 'http://127.0.0.1:8000/posts'
    like_post_url = 'http://127.0.0.1:8000/posts/like'
    dislike_post_url = 'http://127.0.0.1:8000/posts/dislike'

    with open('./config.json', 'r') as file:
        bot = json.load(file)

    number_of_users = bot['number_of_users']
    max_posts_per_user = bot['max_posts_per_user']
    max_likes_per_user = bot['max_likes_per_user']

    def create_user_bot():
        username = ''.join(random.choice(string.ascii_letters) for _ in range(7))
        password = ''.join(str(random.randrange(0, 101, 1)) for i in range(8))
        email = f'{username}@example.com'
        user_data = {
            "username": username,
            "password": password,
            "email": email,
            "first_name": username
        }
        print(user_data)
        req = requests.post(register_url, data=json.dumps(user_data))
        print(req.status_code)
        response = req.json()
        response['password'] = password
        return response

    def auth_bot(user):
        print(user)
        params = {
            "username": f"{user['username']}",
            "password": f"{user['password']}"
        }
        req = requests.post(auth_url, data=json.dumps(params))
        print(req.status_code)
        print(req.json())
        access_token = req.json()['access_token']
        return access_token

    def create_post_bot(user,headers):
        url = f"https://jsonplaceholder.typicode.com/posts?id={random.randrange(1, 100, 1)}"
        get_post = requests.get(url=url)
        response = get_post.json()
        print(response)
        data = {
            "title": f"{response[0]['title']}",
            "description": f"{response[0]['body']}",
            "author_id": user['id']
        }
        print(data)
        r = requests.post(create_post_url, headers=headers, data=json.dumps(data))
        print(r.status_code)

    def add_bot_like(user,headers):
        req = requests.get(url=get_posts,headers=headers)
        response = req.json()
        print(response)
        rndm_post_id = random.choice([i['id'] for i in response])
        data = {
            "post_id": rndm_post_id,
            "like": 1,
            "user_id": user['id']
        }
        reqlike = requests.post(like_post_url, headers=headers, data=json.dumps(data))
        print(reqlike.status_code)

    for _ in range(number_of_users):
        user = create_user_bot()
        authorization = auth_bot(user)
        headers = {'Authorization': f'Bearer {authorization}'}
        for _ in range(max_posts_per_user):
            create_post_bot(user,headers)
        for _ in range(max_likes_per_user):
            add_bot_like(user,headers)
    response_data = {'result': 'success'}
    return response_data


if __name__ == "__main__":
    main()
