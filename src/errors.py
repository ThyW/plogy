from flask import Flask
from flask.wrappers import Response
import json


class Error:
    not_json = 1
    unauthorized = 2
    invalid_input = 3
    unsupported_query_parameter = 4


def make_error(app: Flask, type: int) -> Response:
    ret = None
    match type:
        case Error.not_json:
            ret = app.response_class(
                response=json.dumps(
                    {
                        "error": f"NotJson-{type}",
                        "message": "POST request did not contain a JSON message.",
                        "detail": "Please make sure you are sending the correct request with JSON.",
                    }
                ),
                status=400,
                mimetype="application/json",
            )
        case Error.unauthorized:
            ret = app.response_class(
                response=json.dumps(
                    {
                        "error": f"AuthentificationFailed",
                        "message": "This action was not authenticated using the propper userId",
                        "detail": "Check that you are sending the correct userId in your request.",
                    }
                ),
                status=403,
                mimetype="application/json",
            )
        case Error.invalid_input:
            ret = app.response_class(
                response=json.dumps(
                    {
                        "error": f"InvalidInput",
                        "message": "The JSON provied in this request was invalid.",
                        "detail": "Please make sure that you are sending the correct JSON.",
                    }
                ),
                status=400,
                mimetype="application/json",
            )
        case Error.unsupported_query_parameter:
            ret = app.response_class(
                response=json.dumps(
                    {
                        "error": f"UnsupportedQueryParameter",
                        "message": "One or more of the provided query parameters are wrong.",
                        "detail": "Please make sure that all query parameters are supported and have to correct values.",
                    }
                ),
                status=400,
                mimetype="application/json",
            )
        case _:
            ret = app.response_class(
                response=json.dumps(
                    {
                        "error": "Unknown",
                        "message": "Server ran into an unknown error.",
                        "detail": "Make sure you sent the correct request",
                    }
                ),
                status=500,
                mimetype="application/json",
            )
    return ret
