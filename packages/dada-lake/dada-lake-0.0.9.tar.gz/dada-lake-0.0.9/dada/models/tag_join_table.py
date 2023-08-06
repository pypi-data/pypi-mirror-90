"""
Tag Join Tables
TODO: figure out how to dry this up?
"""
import logging

from dada_types import T

from dada.models.base import DBTable
from dada.models.core import db
from dada.models.mixin import (
    TagTableMixin,
    JoinTableMixin,
    JoinTableMixin,
)


TAG_JOIN_MODEL_LOGGER = logging.getLogger()


class FileTag(DBTable, TagTableMixin, JoinTableMixin):

    __tablename__ = "file_tag"
    __module__ = "dada.models.tag_join_table"
    __from_id__ = "file_id"

    file_id = db.Column(T.file_id.col, db.ForeignKey("file.id"), index=True)

    # relationships
    file = db.relationship("File", lazy=True)


class FieldTag(DBTable, TagTableMixin, JoinTableMixin):

    __tablename__ = "field_tag"
    __module__ = "dada.models.tag_join_table"
    __from_id__ = "field_id"

    field_id = db.Column(T.field_id.col, db.ForeignKey("field.id"), index=True)
    # relationships
    field = db.relationship("Field", lazy=True)


class FolderTag(DBTable, TagTableMixin, JoinTableMixin):

    __tablename__ = "folder_tag"
    __module__ = "dada.models.tag_join_table"
    __from_id__ = "folder_id"

    folder_id = db.Column(T.folder_id.col, db.ForeignKey("folder.id"), index=True)

    # relationships
    folder = db.relationship("Folder", lazy=True)


class DesktopTag(DBTable, TagTableMixin, JoinTableMixin):

    __tablename__ = "desktop_tag"
    __module__ = "dada.models.tag_join_table"
    __from_id__ = "desktop_id"

    desktop_id = db.Column(T.desktop_id.col, db.ForeignKey("desktop.id"), index=True)

    # relationships
    desktop = db.relationship("Desktop", lazy=True)


class UserTag(DBTable, TagTableMixin, JoinTableMixin):

    __tablename__ = "user_tag"
    __module__ = "dada.models.tag_join_table"
    __from_id__ = "user_id"

    user_id = db.Column(T.user_id.col, db.ForeignKey("user.id"), index=True)

    # relationships
    user = db.relationship("User", lazy=True)


# //////////////////////////////////////////////////////////////////
# Etc.
# //////////////////////////////////////////////////////////////////


class TagTag(DBTable, JoinTableMixin):
    """
    A mapping of tagged tags?
    """

    __tablename__ = "tag_tag"
    __module__ = "dada.models.tag_join_table"
    __from_id__ = "from_tag_id"
    __to_id__ = "to_tag_id"

    from_tag_id = db.Column(T.tag_id.col, db.ForeignKey("tag.id"), index=True)
    to_tag_id = db.Column(T.tag_id.col, db.ForeignKey("tag.id"), index=True)

    # relationships
    from_tag = db.relationship("Tag", foreign_keys=[from_tag_id], lazy=True)
    to_tag = db.relationship("Tag", foreign_keys=[to_tag_id], lazy=True)
