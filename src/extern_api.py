import requests

API_URL = "https://jsonplaceholder.typicode.com/users/"


def authenticate_user(uid: int) -> bool:
    return requests.get(f"{API_URL}{uid}") == 200
