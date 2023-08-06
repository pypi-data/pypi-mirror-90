"""
Custom Methods for accessing metdata about yourself / changing password + api key
"""
from flask import g, Blueprint
from flask_apispec import use_kwargs, marshal_with, doc
from marshmallow import fields

from dada_types import T
from dada.models.api_request import APIRequest
from dada.models.api_response import UserResponse

ME_APP = Blueprint("me", __name__)


# ///////////////////////
# GET /me #
# ///////////////////////


class FetchMeRequest(APIRequest):
    __name__ = "me_fetch_request"


BaseMeResponse = UserResponse(exclude=["password"])


class GetMeResponse:
    __name__ = "me_fetch_response"


@ME_APP.route("/", methods=["GET"])
@use_kwargs(FetchMeRequest(), location="query_path")
@marshal_with(BaseMeResponse)
@doc(description="Get metadata about yourself", tags=["users", "me"])
def get_me(**kwargs):
    """"""
    return g.user


# ///////////////////////////
# PUT/PATCH/UPDATE /me #
# //////////////////////////


class UpdateMeRequest(APIRequest):
    """
    We use a custom schema for password change / api key refresh
    # TODO: maybe separate out these things into different api methods?
            eg: /me/refresh-apikey or /me/change-password
    """

    name = T.name.val
    email = T.email.val
    old_password = T.password.val
    new_password = T.password.val
    refresh_api_key = fields.Bool(missing=False)
    fields = T.fields.val
    theme = T.json.val
    tags = T.tag_id_slug_array.val


class UpdateMeResponse(UserResponse):
    __name__ = "me_update_response"

    class Meta:
        exclude = ["password"]


@ME_APP.route("/", methods=["PUT"])
@use_kwargs(UpdateMeRequest(), location="query_path_json_or_form")
@marshal_with(UpdateMeResponse())
@doc(description="Update your own metadata", tags=["users", "me"])
def update_me(**kwargs):

    # pop out special kwargs
    old_password = kwargs.pop("old_password", None)
    new_password = kwargs.pop("new_password", None)
    refresh_api_key = kwargs.pop("refresh_api_key", None)

    if old_password and new_password:
        if not g.user.check_password(old_password):
            raise ForbiddenError("Invalid password.")
        g.user.password = g.user.gen_password(new_password)

    # check if we should refresh the apikey
    if refresh_api_key:
        g.user.api_key = g.user.gen_api_key()

    # update user
    g.user.update(**kwargs)
    return g.user
