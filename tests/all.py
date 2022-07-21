#!/usr/bin/env python3
from add_post import test as add_post
from extern_api_test import test as extern_api
from posts import test as posts
from edit_post import test as edit_post
from remove_post import test as remove_post

import requests
import sys


def test():
    if "-s" or "--silent" in sys.argv:
        add_post(True)
        extern_api(True)
        posts(True)
        edit_post(True)
        remove_post(True)

    else:
        add_post()
        extern_api()
        posts()
        edit_post()
        remove_post()

        print(requests.get("http://localhost:5000/api/swagger.json").json())


test()
