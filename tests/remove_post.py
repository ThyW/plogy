#!/usr/bin/env python3

import requests

URL = "http://localhost:5000/posts/remove/128"


def test(_: bool = False) -> None:
    r = requests.get(URL)
    assert r != 200
