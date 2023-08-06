import logging


from sqlalchemy import func
from sqlalchemy.dialects.postgresql import ENUM

import dada_settings
from dada_types import T
from dada_types.col import EnumArrayCol

from dada.models.core import db
from dada.models.base import DBTable
from dada.models.mixin import (
    SlugTableMixin,
    SearchTableMixin,
    FileTypeTableMixin,
    UserMixin,
)
from dada.models.theme_table import TagTheme
from dada.models.field import FieldCacheMixin


TAG_MODEL_LOGGER = logging.getLogger()


class Tag(
    DBTable,
    SlugTableMixin,
    SearchTableMixin,
    FileTypeTableMixin,
    UserMixin,
    FieldCacheMixin,
):

    __tablename__ = "tag"
    __module__ = "dada.models.tag"
    __id_fields__ = ["id", "name", "slug"]
    __defaults__ = dada_settings.TAG_DEFAULTS
    __theme_table__ = TagTheme

    # tags limited by entity types
    accepts_entity_types = db.Column(
        T.entity_type_array.col(
            T.entity_type.col(
                *(dada_settings.TAG_DEFAULTS_ACCEPTS_ENTITY_TYPES_ALL),
                name="tag_accepts_entity_types_enum",
                create_type=True,
            )
        ),
        index=True,
        default=dada_settings.TAG_DEFAULTS_ACCEPTS_ENTITY_TYPES_DEFAULT,
    )

    # tag theme
    theme = db.relationship("TagTheme", lazy="joined")

    # tagged entities
    tagged_fields = db.relationship("FieldTag", lazy="joined")
    tagged_files = db.relationship("FileTag", lazy="joined")
    tagged_folders = db.relationship("FolderTag", lazy="joined")
    tagged_desktops = db.relationship("DesktopTag", lazy="joined")
    tagged_users = db.relationship("UserTag", lazy="joined")

    __table_args__ = (
        db.Index(f"tag_name_user_id_uniq_idx", "name", "user_id", unique=True),
        db.Index("tag_vector_idx", "vector", postgresql_using="gin"),
    )

    def to_dict(self):
        """
        Serializable object
        """
        d = {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "slug": self.slug,
            "emoji": self.emoji_char,
            "info": self.info,
            "accepts_entity_types": self.accepts_entity_types,
            "accepts_file_types": self.accepts_file_types,
            "accepts_file_subtypes": self.accepts_file_subtypes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "fields": self.fields,
        }
        # population relationships
        for entity in dada_settings.TAG_DEFAULTS_ACCENTS_ENTITY_TYPES:
            d[f"{entity}_id"] = [
                instance.id for instance in getattr(self, entity + "s", [])
            ]
        return d
