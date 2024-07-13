import pytest
from faker import Faker
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from httpx import Response


@pytest.mark.asyncio
async def test_create_chat_success(
        app: FastAPI,
        client: TestClient,
        faker: Faker
):
    url = app.url_path_for('create_chat_handler')
    title_text = faker.text(max_nb_chars=30)
    response: Response = client.post(url=url, json={'title': title_text})
    assert response.is_success
    json_data = response.json()
    assert json_data['title'] == title_text


@pytest.mark.asyncio
async def test_create_chat_title_too_long(
        app: FastAPI,
        client: TestClient,
        faker: Faker
):
    url = app.url_path_for('create_chat_handler')
    title_text = faker.text(max_nb_chars=340)
    response: Response = client.post(url=url, json={'title': title_text})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    json_data = response.json()

    assert json_data['detail']['error']


@pytest.mark.asyncio
async def test_create_chat_title_empty(
        app: FastAPI,
        client: TestClient,
        faker: Faker
):
    url = app.url_path_for('create_chat_handler')
    response: Response = client.post(url=url, json={'title': ''})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    json_data = response.json()

    assert json_data['detail']['error']
