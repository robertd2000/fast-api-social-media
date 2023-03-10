import pytest
from httpx import AsyncClient

from conf_test_db import client
from auth.token import create_access_token
from main import app
from test.users.test_users import test_create_user


@pytest.mark.asyncio
async def test_create_post():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        user_access_token = create_access_token({"sub": "user@gmail.com"})
        create_response = await ac.post(
            '/posts/', headers={'Authorization': f'Bearer {user_access_token}'},
            json={"title": "First post!!!", "body": "My first post!!!"})
        get_response = await ac.get(f'/posts/{1}')
    assert create_response.status_code == 201, create_response.text
    assert get_response.status_code == 200, get_response.text


@pytest.mark.asyncio
async def test_like_post():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await test_create_post()
        test_create_user()
        user_access_token_1 = create_access_token({"sub": "user@gmail.com"})
        rejected_response = await ac.post(f'/posts/{1}/like', json={"post_id": 1},
                                          headers={'Authorization': f'Bearer {user_access_token_1}'})

        user_access_token_2 = create_access_token({"sub": "admin@email.com"})
        resolved_like_response_v1 = await ac.post(f'/posts/{1}/like', json={"post_id": 1},
                                                  headers={'Authorization': f'Bearer {user_access_token_2}'})
        resolved_unlike_response = await ac.post(f'/posts/{1}/like', json={"post_id": 1},
                                                 headers={'Authorization': f'Bearer {user_access_token_2}'})
        resolved_like_response_v2 = await ac.post(f'/posts/{1}/like', json={"post_id": 1},
                                                  headers={'Authorization': f'Bearer {user_access_token_2}'})
    assert rejected_response.status_code == 403, rejected_response.text
    assert resolved_like_response_v1.status_code == 200, resolved_like_response_v1.text
    assert resolved_unlike_response.status_code == 200, resolved_unlike_response.text
    assert resolved_like_response_v2.status_code == 200, resolved_like_response_v2.text

    assert rejected_response.json()['detail'] == '???? ???? ???????????? ?????????????? ?????????????????????? ????????!'
    assert resolved_like_response_v1.json()['message'] == '???????? ?????????????? ??????????????????!'
    assert resolved_unlike_response.json()['message'] == '???????? ?????????????? ??????????!'
    assert resolved_like_response_v2.json()['message'] == '???????? ?????????????? ??????????????????!'


@pytest.mark.asyncio
async def test_dislike_post():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await test_create_post()
        test_create_user()
        user_access_token_1 = create_access_token({"sub": "user@gmail.com"})
        rejected_response = await ac.post(f'/posts/{1}/dislike', json={"post_id": 1},
                                          headers={'Authorization': f'Bearer {user_access_token_1}'})

        user_access_token_2 = create_access_token({"sub": "admin@email.com"})
        resolved_dislike_response_v1 = await ac.post(f'/posts/{1}/dislike', json={"post_id": 1},
                                                     headers={'Authorization': f'Bearer {user_access_token_2}'})
        resolved_un_dislike_response = await ac.post(f'/posts/{1}/dislike', json={"post_id": 1},
                                                     headers={'Authorization': f'Bearer {user_access_token_2}'})
        resolved_dislike_response_v2 = await ac.post(f'/posts/{1}/dislike', json={"post_id": 1},
                                                     headers={'Authorization': f'Bearer {user_access_token_2}'})
    assert rejected_response.status_code == 403, rejected_response.text
    assert resolved_dislike_response_v1.status_code == 200, resolved_dislike_response_v1.text
    assert resolved_un_dislike_response.status_code == 200, resolved_un_dislike_response.text
    assert resolved_dislike_response_v2.status_code == 200, resolved_dislike_response_v1.text

    assert rejected_response.json()['detail'] == '???? ???? ???????????? ???????????????????? ?????????????????????? ????????!'
    assert resolved_dislike_response_v1.json()['message'] == '?????????????? ?????????????? ??????????????????!'
    assert resolved_un_dislike_response.json()['message'] == '?????????????? ?????????????? ??????????!'
    assert resolved_dislike_response_v2.json()['message'] == '?????????????? ?????????????? ??????????????????!'


def test_get_posts():
    response = client.get('/posts')
    assert response.status_code == 200, response.text


@pytest.mark.asyncio
async def test_get_post():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await test_create_post()
        rejected_response = await ac.get(f'/posts/{10}')
        response_v1 = await ac.get(f'/posts/{1}')
        await test_like_post()
        response_v2 = await ac.get(f'/posts/{1}')

    assert rejected_response.status_code == 404, rejected_response.text
    assert rejected_response.json()['detail'] == '???????? ?? id 10 ???? ????????????!'

    assert response_v1.status_code == 200, response_v1.text
    assert response_v1.json()['Post']['title'] == 'First post!!!'
    assert response_v1.json()['likes'] == 0
    assert response_v1.json()['dislikes'] == 0

    assert response_v2.status_code == 200, response_v2.text
    assert response_v2.json()['Post']['title'] == 'First post!!!'
    assert response_v2.json()['likes'] == 1
    assert response_v2.json()['dislikes'] == 0


@pytest.mark.asyncio
async def test_delete_post():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        rejected_unauthenticated_response = await ac.delete(f'/posts/{1}')
        user_access_token = create_access_token({"sub": "user@gmail.com"})
        rejected_response = await ac.delete(f'/posts/{1}', headers={'Authorization': f'Bearer {user_access_token}'})
        await test_create_post()
        response = await ac.delete(f'/posts/{1}', headers={'Authorization': f'Bearer {user_access_token}'})

    assert rejected_unauthenticated_response.status_code == 401, rejected_unauthenticated_response.text
    assert rejected_unauthenticated_response.json()['detail'] == 'Not authenticated'

    assert rejected_response.status_code == 404, rejected_response.text
    assert rejected_response.json()['detail'] == '???????? ?? id 1 ???? ????????????!'

    assert response.status_code == 200, response.text
    assert response.json()['message'] == '???????? ?? id 1 ?????????????? ????????????!'


@pytest.mark.asyncio
async def test_update_post():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        rejected_unauthenticated_response = await ac.put(f'/posts/{1}/update',
                                                         json={'title': 'New title!!!', 'body': 'Updated'})
        user_access_token = create_access_token({"sub": "user@gmail.com"})
        rejected_response = await ac.put(f'/posts/{1}/update', headers={'Authorization': f'Bearer {user_access_token}'},
                                         json={'title': 'New title!!!', 'body': 'Updated'})
        await test_create_post()
        response = await ac.put(f'/posts/{1}/update', headers={'Authorization': f'Bearer {user_access_token}'},
                                json={'title': 'New title!!!', 'body': 'Updated'})

    assert rejected_unauthenticated_response.status_code == 401, rejected_unauthenticated_response.text
    assert rejected_unauthenticated_response.json()['detail'] == 'Not authenticated'

    assert rejected_response.status_code == 404, rejected_response.text
    assert rejected_response.json()['detail'] == '???????? ?? id 1 ???? ????????????!'

    assert response.status_code == 200, response.text
    assert response.json()['title'] == 'New title!!!'
