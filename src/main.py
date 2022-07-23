#!/usr/bin/env python3

from flask import jsonify, request
from flask.wrappers import Response
from flask_swagger import swagger
import requests
from errors import *
from extern_api import authenticate_user, find_post
from db import Addresses, Coordinates, Posts, Users, Companies, app, db


@app.route("/v1/api/posts/add", methods=["POST"])
def add_post() -> Response:
    """
    Add a new post.
    This checks the userId of the user creating the post and rejects it, if that user is not present in the database of users.
    ---
    definitions:
        - schema:
            id: Post
            properties:
                userId:
                    type: integer
                    description: Post creator's userId.
                title:
                    type: integer
                    description: Title of the post.
                body:
                    type: integer
                    description: Body of the post.
    parameters:
        - in: body
          name: body
          schema:
              type: object
              required:
                  - userId
                  - title
                  - body
              properties:
                  userId:
                      type: int
                      description: UserId of the user adding the post.
                  title:
                      type: string
                      description: Title of the added post.
                  body:
                      type: string
                      description: Body or content of the added post.
    produces:
        - application/json
    responses:
        200:
            description: The new post was added.
        400:
            description: Request did not contain valid JSON, JSON did not contain correct values
        403:
            description: The userId was wrong; there are no such users with this userId
    """
    if request.json:
        body = None
        try:
            body = json.loads(str(request.get_json()))
        except:
            return make_error(app, Error.invalid_input)
        if body:
            if type(body) is dict:
                if (
                    (user_id := body["userId"])
                    and (body["title"])
                    and (body["body"])
                ):
                    if Users.query.filter_by(id=user_id).first():
                        # add new post
                        db.session.add(Posts.from_json(body))
                        db.session.commit()

                        return Response(status=200)
                    elif user_json := authenticate_user(user_id):
                        geo = Coordinates.from_json(user_json["address"]["geo"])
                        db.session.add(geo)
                        db.session.commit()

                        address = Addresses.from_json(
                            user_json["address"], geo.id
                        )
                        db.session.add(address)
                        db.session.commit()

                        company = Companies.from_json(user_json["company"])
                        db.session.add(company)
                        db.session.commit()

                        user = Users.from_json(
                            user_json, address.id, company.id
                        )
                        db.session.add(user)
                        db.session.commit()

                        db.session.add(Posts.from_json(body))

                        return Response(status=200)
                    else:
                        return make_error(app, Error.unauthorized)
            else:
                return make_error(app, Error.unauthorized)
        else:
            return make_error(app, Error.invalid_input)
    else:
        return make_error(app, Error.not_json)


@app.route("/v1/api/posts/", methods=["GET"])
def posts() -> Response | str:
    """
    List all available posts
    ---
    responses:
        200:
            description: Return a list of all posts.
            content: application/json
            schema:
                type: object
                properties:
                    list:
                        type: array
                        items:
                            $ref: "#/definitions/Post"
    """
    ret = dict()
    ret["list"] = list()
    posts = Posts.query.all()
    for post in posts:
        ret["list"].append(post.to_json())
    return jsonify(ret)


@app.route("/v1/api/posts/id/<int:id>", methods=["GET"])
def post_by_id(id: int) -> Response | str:
    """
    Attempt to find and return a post with the given ID.
    ---
    parameters:
        - in: path
          name: id
          type: integer
          required: true
          description: Post ID of the post we want to get.
    responses:
        200:
            description: Return the post.
            schema:
                $ref: '#/definitions/Post'
        404:
            description: Post was not found.
    """
    # find the post by id and return in json
    if post_query := Posts.query.filter_by(id=id).first():
        return jsonify(post_query.to_json())
    elif post := find_post(id):
        requests.post("http://localhost:5000/posts/add", json=json.dumps(post))
        return jsonify(post)
    return make_error(app, Error.not_found)


@app.route("/v1/api/posts/userId/<int:user_id>")
def post_by_uid(user_id: int) -> Response | str:
    """
    Attempt to find and return a list of posts made by the same user.
    ---
    parameters:
        - in: path
          name: user_id
          type: integer
          required: true
          description: UserId of the user who's posts we wish to list.
    responses:
        200:
            description: Return a list of posts.
            schema:
                type: object
                properties:
                    list:
                        type: array
                        items:
                            schema:
                                $ref: '#/definitions/Post'
    """
    ret = {"list": list()}
    posts = Posts.query.filter_by(user_id=user_id).all()
    for post in posts:
        ret["list"].append(post.to_json())
    else:
        return jsonify(ret)


@app.route("/v1/api/posts/remove/<int:id>", methods=["GET"])
def remove(id: int) -> Response:
    """
    Remove a post, given its ID.
    ---
    parameters:
        - in: path
          name: id
          type: integer
          required: true
          description: ID of the post we wish to remove.
    responses:
        200:
            description: Post has been successfully removed.
        404:
            description: Post was not found, therefore not removed.
    """
    # find post by id and remove it if found
    post = Posts.query.filter_by(id=id).first()
    if post:
        post.delete()
        db.session.commit()
        return Response(status=200)
    else:
        return make_error(app, Error.not_found)


@app.route("/v1/api/posts/edit/<int:id>", methods=["POST"])
def edit(id: int) -> str | Response:
    """
    Attempt to modify a post, given it's ID.
    ---
    parameters:
        - in: path
          name: id
          type: integer
          required: true
          description: Id of the post we wish to modify.
        - in: body
          schema:
              type: object
              properties:
                  userId:
                      type: int
                      description: Only the author of the post can change it.
                  title:
                      type: string
                      description: New title want to set for the post, if empty, the existing field is not modified.
                  body:
                      type: string
                      description: New body of the post, if empty, the existing field is not modified.
    responses:
        200:
            description: Post has been successfully edited.
        400:
            description: Request JSON data was invalid or not present.
        404:
            description: Post not found.
    """
    # find the post in the db first
    if request.json:
        body = None
        try:
            body = json.loads(str(request.get_json()))
        except:
            return make_error(app, Error.invalid_input)
        if body:
            if user_id := body["userId"]:
                if query := Posts.query.filter_by(id=id).first():
                    if not query.user_id == user_id:
                        return make_error(app, Error.unauthorized)
                    if title := body["title"]:
                        query.title = title
                    if body_content := body["body"]:
                        query.body = body_content
                    db.session.commit()
                    return Response(status=200)
                else:
                    return make_error(app, Error.not_found)
            else:
                return make_error(app, Error.invalid_input)
        else:
            return make_error(app, Error.invalid_input)
    return make_error(app, Error.not_json)


@app.route("/v1/api/swagger.json")
def spec() -> Response:
    """
    Return the API description.
    ---
    responses:
        200:
            description: API JSON returned
    """
    spec = swagger(app)
    spec["info"]["title"] = "Post API"
    spec["info"]["version"] = "0.1.0"
    return jsonify(swagger(app))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, host="0.0.0.0")
    print("created all")
