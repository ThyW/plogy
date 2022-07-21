import requests

API_URL_USERS = "https://jsonplaceholder.typicode.com/users/"
API_URL_POST = "https://jsonplaceholder.typicode.com/posts/"


def authenticate_user(uid: int) -> dict | None:
    response = requests.get(f"{API_URL_USERS}{uid}")
    if response.ok:
        if ret := response.json():
            return ret
    return None


def find_post(id: int) -> dict | None:
    response = requests.get(f"{API_URL_POST}{id}")
    if response.ok:
        if ret := response.json():
            return ret
    return None
