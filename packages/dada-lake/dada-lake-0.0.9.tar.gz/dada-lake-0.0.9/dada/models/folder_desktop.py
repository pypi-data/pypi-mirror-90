from sqlalchemy import ForeignKey, Index

from dada.models.core import db
from dada.models.base import DBTable
from dada.models.mixin import JoinFieldTableMixin, PositionalTableMixin
from dada.models.field import FieldCacheMixin


class FolderDesktop(
    DBTable, JoinFieldTableMixin, PositionalTableMixin, FieldCacheMixin
):

    __tablename__ = "folder_desktop"
    __module__ = "dada.models.folder_desktop"
    __from_id__ = "folder_id"
    __to_id__ = "desktop_id"

    folder_id = db.Column(db.Integer, ForeignKey("folder.id"), index=True)
    desktop_id = db.Column(db.Integer, ForeignKey("desktop.id"), index=True)

    # relationships

    folder = db.relationship("Folder", lazy=True)
    desktop = db.relationship("Desktop", lazy=True)

    __table_args__ = (
        Index(
            "folder_desktop_position_uniq_idx",
            "desktop_id",
            "folder_id",
            "position",
            unique=True,
        ),
    )

    # relationships
    desktop = db.relationship("Desktop", lazy=True)
    folder = db.relationship("Folder", lazy=True)
