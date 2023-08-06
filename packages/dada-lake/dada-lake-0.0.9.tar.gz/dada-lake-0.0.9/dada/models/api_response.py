"""
Marshmallow Response Objects Via Flask-Marshmallow 

Seet: https://marshmallow.readthedocs.io/en/stable/api_reference.html

TOOD: Can we just do this inside of resources.core now?

"""
from typing import List

from flask import Response
from marshmallow import fields

from dada_types import T, NewVal
from dada_serde import jsonify

from dada.models.core import db, ma
from dada.models.user import User
from dada.models.tag import Tag
from dada.models.file import File
from dada.models.field import Field, FieldTheme
from dada.models.folder import Folder
from dada.models.desktop import Desktop
from dada.models.file_folder import FileFolder
from dada.models.folder_desktop import FolderDesktop
from dada.models.tag_join_table import *
from dada.models.theme_table import *

# ///////////////////
# Base Response
# ///////////////////
class BaseResponse(ma.SQLAlchemyAutoSchema):
    class Meta:
        sqla_session = db.session
        strict = True


## /////////////////////////////////
### File
## /////////////////////////////////


class FileFolderResponse(BaseResponse):
    __dada_type__ = "file_folder"

    class Meta:
        model = FileFolder


class FolderDesktopResponse(BaseResponse):
    __dada_type__ = "folder_desktop"

    class Meta:
        model = FolderDesktop


# ///////////////////////
# Theme Table Responses
# //////////////////////


class FileThemeResponse(BaseResponse):
    __dada_type__ = "file_theme"

    class Meta:
        model = FileTheme


class FolderThemeResponse(BaseResponse):
    __dada_type__ = "folder_theme"

    class Meta:
        model = FolderTheme


class DesktopThemeResponse(BaseResponse):
    __dada_type__ = "desktop_theme"

    class Meta:
        model = DesktopTheme


class TagThemeResponse(BaseResponse):
    __dada_type__ = "tag_theme"

    class Meta:
        model = TagTheme


class FieldThemeResponse(BaseResponse):
    __dada_type__ = "field_theme"

    class Meta:
        model = TagTheme


class UserThemeResponse(BaseResponse):
    __dada_type__ = "user_theme"

    class Meta:
        model = TagTheme


# ////////////////////////
# Tag Join Table Responses
# ///////////////////////


class FileTagResponse(BaseResponse):
    __dada_type__ = "file_tag"

    class Meta:
        model = FileTag


class FolderTagResponse(BaseResponse):
    __dada_type__ = "folder_tag"

    class Meta:
        model = FolderTag


class DesktopTagResponse(BaseResponse):
    __dada_type__ = "desktop_tag"

    class Meta:
        model = DesktopTag


class TagTagResponse(BaseResponse):
    __dada_type__ = "tag_tag"

    class Meta:
        model = TagTag


class FieldTagResponse(BaseResponse):
    __dada_type__ = "field_tag"

    class Meta:
        model = FieldTag


class UserTagResponse(BaseResponse):
    __dada_type__ = "user_tag"

    class Meta:
        model = UserTag


# ///////////////////
# low-level models
# ////////////////////


class TagResponse(BaseResponse):
    __dada_type__ = "tag"

    theme = NewVal("tag_theme", fields.Nested(TagThemeResponse))

    class Meta:
        model = Tag
        exclude = ["vector"]


class FieldResponse(BaseResponse):
    __dada_type__ = "field"

    core = T.bool.val

    tags = NewVal("field_tag_array", fields.List(fields.Nested(TagResponse)))
    theme = NewVal("field_theme", fields.Nested(FieldThemeResponse))

    class Meta:
        model = Field
        exclude = ["vector"]


# ////////////////////////////
# Core Models
# ////////////////////////////


class DesktopResponse(BaseResponse):
    __dada_type__ = "desktop"

    # relationships
    folders = NewVal(
        "desktop_folder_array", fields.List(fields.Nested(FolderDesktopResponse))
    )
    tags = NewVal("desktop_tag_array", fields.List(fields.Nested(TagResponse)))
    theme = NewVal("desktop_theme", fields.Nested(DesktopThemeResponse))

    class Meta(BaseResponse.Meta):
        model = Desktop
        exclude = ["vector"]


class DesktopsForFolderResponse(DesktopResponse):
    pass


class FolderResponse(BaseResponse):
    __dada_type__ = "folder"

    # relationships
    files = NewVal("folder_file_array", fields.List(fields.Nested(FileFolderResponse)))
    desktops = NewVal(
        "folder_desktop_array", fields.List(fields.Nested(DesktopsForFolderResponse))
    )
    tags = NewVal("folder_tag_array", fields.List(fields.Nested(TagResponse)))
    theme = NewVal("folder_theme", fields.Nested(FolderThemeResponse))

    class Meta(BaseResponse.Meta):
        exclude = ["vector"]
        model = Folder


class FoldersForFileResponse(FolderResponse):
    pass


class FileResponse(BaseResponse):
    __dada_type__ = "file"
    theme = NewVal("file_theme", fields.Nested(FileThemeResponse))

    # urls
    s3_urls = fields.Dict()

    human_size = T.text.val

    folders = NewVal("folder_array", fields.List(fields.Nested(FoldersForFileResponse)))
    tags = NewVal("folder_tag_array", fields.List(fields.Nested(TagResponse)))

    class Meta(BaseResponse.Meta):
        model = File
        exclude = ["vector"]


class UserResponse(BaseResponse):

    __dada_type__ = "user"

    tags = NewVal("user_tag_array", fields.List(fields.Nested(TagResponse)))
    files = NewVal(
        "user_file_array",
        fields.List(fields.Nested(FileResponse, only=("id", "slug"),)),
    )
    folders = NewVal(
        "user_folder_array",
        fields.List(fields.Nested(FolderResponse, only=("id", "slug"))),
    )
    desktops = NewVal(
        "user_desktop_array",
        fields.List(fields.Nested(DesktopResponse, only=("id", "slug"))),
    )
    theme = NewVal("user_theme", fields.Nested(UserThemeResponse))

    class Meta(BaseResponse.Meta):
        model = User
        exclude = ["vector"]
