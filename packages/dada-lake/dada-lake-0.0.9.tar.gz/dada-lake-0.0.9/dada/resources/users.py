from flask import g, Blueprint
from flask_apispec import use_kwargs, marshal_with, doc
from marshmallow import Schema, fields

from dada_types import T
from dada.models.user import User
from dada.models.tag_join_table import UserTag
from dada.models.api_response import UserResponse
from dada.resources.core import crud_blueprint_from_model


class UpsertUserRequest(Schema):
    """
    We use a custom request schema for user creation/ update
    """

    __name__ = "user_upsert_request"

    name = T.name.val
    email = T.email.val
    password = T.password.val
    admin = T.bool.val
    fields = T.fields.val
    theme = T.json.val
    tags = T.tag_id_slug_array.val

    class Meta:
        strict = True


# custom record response
class SecureUserReponse(UserResponse):
    class Meta:
        exclude = ["password", "api_key", "email", "vector"]


# ///////////////
# Base CRUD Folders API
# ///////////////
SEARCH_DOCS = """
"""
UPSERT_DOCS = """
"""
FETCH_DOCS = """
"""
DELETE_DOCS = """
"""

USERS_APP = crud_blueprint_from_model(
    blueprint=Blueprint("users", __name__),
    core_model=User,
    base_response_schema=SecureUserReponse,
    upsert_request_schema=UpsertUserRequest,
    upsert_requires_admin=True,
    delete_requires_admin=True,
    relationships=[UserTag],
    doc_tags=["users"],
    # search_docs=SEARCH_DOCS,
    # upsert_docs=UPSERT_DOCS,
    # fetch_docs=FETCH_DOCS,
    # delete_docs=DELETE_DOCS
)

# ///////////////////////
# POST /users/login
# ///////////////////////

USER_LOGIN_DOCS = (
    "Login using an ``email`` address and a ``password``, returns your ``api_key``"
)


class UserLoginRequest(Schema):
    """
    We use a custom request schema for user login
    """

    __name__ = "user_login_request"

    email = fields.Email(required=True)
    password = fields.String(required=True)

    class Meta:
        strict = True


class UserLoginResponse(UserResponse):
    __name__ = "user_login_response"

    class Meta:
        exclude = ["password"]


@USERS_APP.route("/login", methods=["POST"])
@use_kwargs(UserLoginRequest(), location="query_path_json_or_form")
@marshal_with(UserLoginResponse())
@doc(description=USER_LOGIN_DOCS, tags=["users"])
def login(**kwargs):
    # authenticate a user
    return User.login(**kwargs)
