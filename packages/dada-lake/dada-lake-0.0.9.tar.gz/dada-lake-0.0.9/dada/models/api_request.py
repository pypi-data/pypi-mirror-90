from marshmallow import Schema, fields, pre_load
from flask import g, current_app, request

import dada_settings
from dada_errors import AuthError, ForbiddenError

from dada.models.user import User


# DOC STRINGS #

API_KEY_QUERY_DOC = """Your API Key.

You can pass this in as a query parameter, Eg:

    /?api_key=dev

This value can be retrieved by logging in with your `username` and `password` via:

    POST /users/login
"""

API_KEY_HEADER_DOC = f"""Your API Key.

You can pass this in as a request header, Eg:

   {dada_settings.API_KEY_HEADER}: dev

This value can be retrieved by logging in with your `username` and `password` via:

    POST /users/login
"""

# REQUEST MIXINS


class APIRequest(Schema):

    api_key = fields.Str(required=True, description=API_KEY_QUERY_DOC)

    api_header = fields.Str(
        load_from=dada_settings.API_KEY_HEADER,
        missing=None,
        description=API_KEY_HEADER_DOC,
    )

    @pre_load
    def authenticate(self, incoming, **kwargs):
        api_key = incoming.get("api_key")
        if not api_key:
            api_key = incoming.get("api_header")
            if not api_key:
                raise AuthError("An api_key is required for this request.")

        g.user = User.get_by_api_key(api_key)
        # if it doesn't exist, throw an error
        if not g.user:
            raise ForbiddenError("Invalid api_key")
        return incoming

    class Meta:

        strict = True
