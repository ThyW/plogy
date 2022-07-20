#!/usr/bin/env python3
import requests

API_URL = "https://jsonplaceholder.typicode.com/users/"


def test() -> None:
    good_response = requests.get(f"{API_URL}1")
    bad_response = requests.get(f"{API_URL}25025")
    print(good_response.json())
    print(bad_response.json())

    assert good_response.status_code == 200
    assert bad_response.status_code != 200


test()
