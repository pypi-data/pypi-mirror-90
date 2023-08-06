from sqlalchemy import func
import logging

import dada_settings
from dada_types import T

from dada.models.core import db
from dada.models.base import DBTable
from dada.models.field import FieldCacheMixin
from dada.models.tag_join_table import DesktopTag
from dada.models.theme_table import DesktopTheme
from dada.models.mixin import GroupTableMixin, UserMixin


DESKTOP_MODEL_LOGGER = logging.getLogger()


class Desktop(DBTable, GroupTableMixin, UserMixin, FieldCacheMixin):

    __tablename__ = "desktop"
    __module__ = "dada.models.desktop"
    __id_fields__ = ["id", "name", "slug"]
    __defaults__ = dada_settings.DESKTOP_DEFAULTS
    __tag_join_table__ = DesktopTag
    __theme_table__ = DesktopTheme

    tags = db.relationship("Tag", secondary="desktop_tag", lazy=True)
    folders = db.relationship("Folder", secondary="folder_desktop", lazy=True)
    theme = db.relationship("DesktopTheme", lazy=True)

    __table_args__ = (
        db.Index(f"desktop_slug_user_id_uniq_idx", "slug", "user_id", unique=True),
        db.Index(f"desktop_vector_idx", "vector", postgresql_using="gin"),
    )
