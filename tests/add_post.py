#!/usr/bin/env python3

import requests
import json

URL = "http://localhost:5000/posts/add"


def test(_: bool = False) -> None:
    data = {
        "userId": 3,
        "title": "3rd post this month!",
        "body": "Lorem ipsum dolor sit amet, qui minim labore adipisicing minim sint cillum sint consectetur cupidatat.",
    }
    r = requests.post(URL, json=json.dumps(data))

    assert r.status_code == 200
