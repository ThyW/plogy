#!/usr/bin/env python3

import json
from flask import Flask, jsonify, request
from flask.wrappers import Response
from errors import *
from extern_api import authenticate_user

app = Flask(__name__)


@app.route("/add_post", methods=["POST"])
def add_post() -> Response:
    if body := json.loads(str(request.get_json())):
        if type(body) is dict:
            if authenticate_user(body["userId"]):
                # TODO:
                # save this to the db
                return jsonify(body)
            else:
                return make_error(app, Error.unauthorized)
        else:
            return make_error(app, Error.invalid_input)
    else:
        return make_error(app, Error.not_json)


@app.route("/posts", methods=["GET"])
def posts() -> Response | str:
    uid = request.args.get("userId")
    id = request.args.get("id")
    if uid and id:
        uid_int, id_int = -1, -1
        try:
            uid_int = int(uid)
            id_int = int(id)
        except ValueError:
            return make_error(app, Error.unsupported_query_parameter)
        if uid_int and id_int:
            # find the post specified by the parameters or return not found
            return ""
    elif uid and not id:
        uid_int = -1
        try:
            uid_int = int(uid)
        except ValueError:
            return make_error(app, Error.unsupported_query_parameter)
        if uid_int:
            # return post with the given user id
            return ""
    elif not uid and id:
        id_int = -1
        try:
            id_int = int(id)
        except ValueError:
            return make_error(app, Error.unsupported_query_parameter)
        if id_int:
            # return a post with that id
            return ""

    # return all posts
    return ""


@app.route("/remove/<int:id>", methods=["GET"])
def remove(id: int) -> str | Response:
    # find post by id and remove it if found
    return ""


@app.route("/edit/<int:id>")
def edit(id: int) -> str | Response:
    # find the post in the db first
    if body := json.loads(str(request.get_json())):
        if type(body) == dict:
            if title := body["title"]:
                # get post and set new title
                pass
            elif post_body := body["body"]:
                # get post and set new body
                pass
    else:
        return make_error(app, Error.not_json)

    return ""


app.run(debug=True)
