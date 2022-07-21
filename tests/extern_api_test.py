#!/usr/bin/env python3
import requests

API_URL_POSTS = "https://jsonplaceholder.typicode.com/users/"
API_URL_USERS = "https://jsonplaceholder.typicode.com/users/"


def test(_: bool = False) -> None:
    good_response = requests.get(f"{API_URL_USERS}1")
    bad_response = requests.get(f"{API_URL_USERS}25025")

    assert good_response.status_code == 200
    assert bad_response.status_code != 200

    good_response = requests.get(f"{API_URL_POSTS}1")
    bad_response = requests.get(f"{API_URL_POSTS}25025")

    assert good_response.status_code == 200
    assert bad_response.status_code != 200
