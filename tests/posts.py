#!/usr/bin/env python3

import requests

URL = "http://localhost:5000/posts/"


def test(silent: bool = False) -> None:
    response = requests.get(URL)
    assert response.status_code == 200
    if not silent:
        print(response.json())

    response = requests.get(f"{URL}id/1")
    assert response.status_code == 200

    response = requests.get(f"{URL}userId/3")
    assert response.status_code == 200
