import datetime

from sqlalchemy import ForeignKey, func, Index

from dada.models.base import DBTable
from dada.models.core import db
from dada.models.field import FieldCacheMixin
from dada.models.mixin import JoinFieldTableMixin, PositionalTableMixin


class FileFolder(DBTable, JoinFieldTableMixin, PositionalTableMixin, FieldCacheMixin):

    __tablename__ = "file_folder"
    __module__ = "dada.models.file_folder"
    __from_id__ = "file_id"
    __to_id__ = "folder_id"

    file_id = db.Column(db.Integer, ForeignKey("file.id"), index=True)
    folder_id = db.Column(db.Integer, ForeignKey("folder.id"), index=True)

    __table_args__ = (
        Index("file_folder_uniq_idx", "file_id", "folder_id", "position", unique=True),
    )

    # relationships

    file = db.relationship("File", lazy=True)
    folder = db.relationship("Folder", lazy=True)
