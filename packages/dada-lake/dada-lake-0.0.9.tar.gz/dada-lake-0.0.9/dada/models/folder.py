from sqlalchemy import func
import logging

import dada_settings

from dada.models.base import DBTable
from dada.models.core import db
from dada.models.mixin import GroupTableMixin, UserMixin
from dada.models.field import FieldCacheMixin
from dada.models.folder_desktop import FolderDesktop
from dada.models.tag_join_table import FolderTag
from dada.models.theme_table import FolderTheme


FOLDER_MODEL_LOGGER = logging.getLogger()


class Folder(DBTable, GroupTableMixin, UserMixin, FieldCacheMixin):

    __tablename__ = "folder"
    __module__ = "dada.models.folder"
    __defaults__ = dada_settings.FOLDER_DEFAULTS
    __id_fields__ = ["id", "name", "slug"]
    __tag_join_table__ = FolderTag
    __theme_table__ = FolderTheme

    # relationships
    files = db.relationship("FileFolder", lazy="joined")
    desktops = db.relationship("Desktop", secondary="folder_desktop", lazy="joined")
    tags = db.relationship("Tag", secondary="folder_tag", lazy="joined")
    theme = db.relationship("FolderTheme", lazy="joined")

    # relationships

    __table_args__ = (
        db.Index(f"folder_name_uniq_idx", "name", "user_id", unique=True),
        db.Index(f"folder_slug_uniq_idx", "slug", "user_id", unique=True),
        db.Index("folder_vector_idx", "vector", postgresql_using="gin"),
    )
