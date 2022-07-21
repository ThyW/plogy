#!/usr/bin/env python3

import json
import requests

URL = "http://localhost:5000/posts/edit/1"


def test(_: bool = False) -> None:
    data = {"userId": 1, "title": "New title", "body": "world"}
    response = requests.post(URL, json=json.dumps(data))

    assert response.status_code == 200
