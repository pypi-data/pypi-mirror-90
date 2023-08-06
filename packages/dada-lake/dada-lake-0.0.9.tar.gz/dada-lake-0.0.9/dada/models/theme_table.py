import logging

from dada_types import T

from dada.models.base import DBTable
from dada.models.core import db
from dada.models.mixin import ThemeTableMixin


TAG_JOIN_MODEL_LOGGER = logging.getLogger()


class FileTheme(DBTable, ThemeTableMixin):

    __tablename__ = "file_theme"
    __module__ = "dada.models.theme_table"
    __id_columns__ = ["file_id"]
    __internal_columns__ = [
        "created_at",
        "updated_at",
        "id",
    ]
    file_id = db.Column(T.file_id.col, db.ForeignKey("file.id"), index=True)

    # relationships
    file = db.relationship("File", lazy=True)

    __table_args__ = (db.Index(f"file_theme_uniq_file_idx", "file_id", unique=True),)


class FolderTheme(DBTable, ThemeTableMixin):

    __tablename__ = "folder_theme"
    __module__ = "dada.models.theme_table"
    __id_columns__ = ["folder_id"]
    __internal_columns__ = [
        "created_at",
        "updated_at",
        "id",
    ]
    folder_id = db.Column(T.folder_id.col, db.ForeignKey("folder.id"), index=True)

    # relationships
    folder = db.relationship("Folder", lazy=True)

    __table_args__ = (
        db.Index(f"folder_theme_uniq_folder_idx", "folder_id", unique=True),
    )


class DesktopTheme(DBTable, ThemeTableMixin):

    __tablename__ = "desktop_theme"
    __module__ = "dada.models.theme_table"
    __id_columns__ = ["desktop_id"]
    __internal_columns__ = [
        "created_at",
        "updated_at",
        "id",
    ]
    desktop_id = db.Column(T.desktop_id.col, db.ForeignKey("desktop.id"), index=True)

    # relationships
    desktop = db.relationship("Desktop", lazy=True)

    __table_args__ = (
        db.Index(f"desktop_theme_uniq_desktop_idx", "desktop_id", unique=True),
    )


class UserTheme(DBTable, ThemeTableMixin):

    __tablename__ = "user_theme"
    __module__ = "dada.models.theme_table"
    __id_columns__ = ["user_id"]
    __internal_columns__ = [
        "created_at",
        "updated_at",
        "id",
    ]
    user_id = db.Column(T.user_id.col, db.ForeignKey("user.id"), index=True)

    # relationships
    user = db.relationship("User", lazy=True)

    __table_args__ = (db.Index(f"user_theme_uniq_user_idx", "user_id", unique=True),)


class TagTheme(DBTable, ThemeTableMixin):

    __tablename__ = "tag_theme"
    __module__ = "dada.models.theme_table"
    __id_columns__ = ["tag_id"]
    __internal_columns__ = [
        "created_at",
        "updated_at",
        "id",
    ]
    tag_id = db.Column(T.tag_id.col, db.ForeignKey("tag.id"), index=True)

    # relationships
    tag = db.relationship("Tag", lazy=True)

    __table_args__ = (db.Index(f"tag_theme_uniq_tag_idx", "tag_id", unique=True),)
