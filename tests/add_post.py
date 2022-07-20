#!/usr/bin/env python3

import requests
import json

URL = "http://localhost:5000/add_post"


def test() -> None:
    data = {"hello": "world"}
    bad_data = "wrong"
    good_response = requests.post(URL, json=json.dumps(data))
    bad_response = requests.post(URL, data=bad_data)

    assert good_response.status_code == 200
    assert bad_response.status_code == 400

    print(f"{good_response.json()}\n{bad_response.json()}")


test()
