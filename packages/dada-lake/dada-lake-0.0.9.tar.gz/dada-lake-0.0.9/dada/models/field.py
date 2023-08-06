import json
import logging

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import ARRAY, ENUM
from sqlalchemy_utils.types import TSVectorType

import dada_settings
from dada_utils import dates
from dada_types import T
from dada_cache import RedisCache

from dada_errors import RequestError, NotFoundError
from dada.models.base import DBTable
from dada.models.core import db, rdsconn
from dada.models.mixin import (
    SlugTableMixin,
    SearchTableMixin,
    FileTypeTableMixin,
    DadaTypeTableMixin,
    ThemeTableMixin,
)
from dada.models.tag_join_table import FieldTag

FIELD_MODEL_LOGGER = logging.getLogger()


class FieldTheme(DBTable, ThemeTableMixin):
    """
    This exists here to avoid cross-import of Field table
    """

    __tablename__ = "field_theme"
    __module__ = "dada.models.theme_table"
    __id_columns__ = ["field_id"]

    field_id = db.Column(T.field_id.col, db.ForeignKey("field.id"), index=True)

    # relationships
    field = db.relationship("Field", lazy=True)
    __table_args__ = (db.Index(f"field_theme_uniq_field_idx", "field_id", unique=True),)


class Field(
    DBTable, SlugTableMixin, SearchTableMixin, FileTypeTableMixin, DadaTypeTableMixin,
):

    __tablename__ = "field"
    __module__ = "dada.models.field"
    __id_columns__ = ["id", "slug", "name"]
    __snake_columns__ = ["name"]
    __type_column_name__ = "type"
    __defaults__ = dada_settings.FIELD_DEFAULTS
    __tag_join_table__ = FieldTag
    __theme_table__ = FieldTheme

    type = db.Column(
        T.dada_type.col(*T.__dada_types__, name=f"field_type_enum"), index=True,
    )
    is_searchable = db.Column(T.bool.col, index=False, default=False)
    is_required = db.Column(T.bool.col, index=False, default=False)
    default = db.Column(T.text.col, index=False, default=None)
    options = db.Column(T.text_array.col, index=False, default=[])

    # fields limited by entity types
    accepts_entity_types = db.Column(
        T.entity_type_array.col(
            T.entity_type.col(
                *dada_settings.FIELD_DEFAULTS_ENTITY_TYPES,
                name="field_accepts_entity_types_enum",
                create_type=True,
            )
        ),
        index=True,
        default=[],
    )

    # relationships

    tags = db.relationship("Tag", secondary="field_tag", lazy="joined")
    theme = db.relationship("FieldTheme", lazy="joined",)

    __table_args__ = (
        db.Index(
            "field_name_entity_types_uniq_idx",
            "name",
            "accepts_entity_types",
            unique=True,
        ),
        db.Index("field_vector_idx", "vector", postgresql_using="gin"),
    )

    def __repr__(self):
        """"""
        return f'<Field:{self.name}/{"|".join(self.accepts_entity_types)}/{"|".join(self.accepts_file_subtypes)}/{self.type}>'

    @classmethod
    def get_fields(cls) -> dict:
        """
        Get all field objects as a dictionary
        """
        return {f.name: f for f in cls.all()}

    @classmethod
    def get_fields_for_entity(cls, entity_type: T.entity_type.py) -> dict:
        """
        Get all field objects as a dictionary
        """
        q = db.session.query(cls).filter(
            cls.accepts_entity_types.contains([entity_type])
        )
        return {field.name: field.to_dict() for field in q.all()}

    @property
    def has_options(self):
        """
        "core" file fields are not stored in the database,
        so we use these property as a symbolic differentiator when they are
        presented together in a list
        """
        return len(self.options) > 0

    @property
    def core(self):
        """
        "core" fields are not stored in the database,
        so we use these property as a symbolic differentiator when they are
        presented together in a list
        """
        return False

    @property
    def dada_type(self):
        return T.get(self.type)

    @property
    def is_fk(self) -> bool:
        """"""
        return self.dada_type.is_fk

    @property
    def is_pk(self) -> bool:
        """"""
        return self.dada_type.is_pk

    @property
    def is_num(self) -> bool:
        """"""
        return self.dada_type.is_num

    @property
    def is_int(self) -> bool:
        """"""
        return self.dada_type.is_int

    @property
    def is_json(self) -> bool:
        """"""
        return self.dada_type.is_json

    @property
    def is_date(self) -> bool:
        """"""
        return self.dada_type.is_date

    @property
    def is_text(self) -> bool:
        """"""
        return self.dada_type.is_text

    @property
    def sql(self) -> bool:
        """"""
        return self.dada_type.sql

    @property
    def is_enum(self) -> bool:
        """"""
        return self.dada_type.is_enum

    @property
    def is_array(self) -> bool:
        """"""
        return self.dada_type.is_array

    # ///

    def to_dict(self) -> dict:
        """
        Serializable object
        """
        return {
            "id": self.id,
            "name": self.name,
            "cat": self.dada_type.cat,
            "title": self.title,
            "slug": self.slug,
            "core": self.core,
            "sql": self.sql,
            "info": self.info,
            "type": self.type,
            "options": self.options,
            "default": self.default,
            "is_required": self.is_required,
            "is_searchable": self.is_searchable,
            "accepts_entity_types": self.accepts_file_types,
            "accepts_file_types": self.accepts_file_types,
            "accepts_file_subtypes": self.accepts_file_subtypes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_num": self.is_num,
            "is_text": self.is_text,
            "is_array": self.is_array,
            "is_json": self.is_json,
            "is_enum": self.is_enum,
            "is_int": self.is_int,
            "is_fk": self.is_fk,
            "is_pk": self.is_pk,
            "has_options": self.has_options,
        }


class __FieldCache__(RedisCache):
    """
    A class for caching entity-specific results from the fields
    database.
    """

    __module__ = "dada.models.field"
    __name__ = "field_cache"
    __dada_type__ = "field_cache"
    rdsconn = rdsconn

    def do(self, entity_type: T.entity_type.py) -> dict:
        """"""
        return Field.get_fields_for_entity(entity_type)


# import this and us it like so: FieldCache.get('file')
FieldCache = __FieldCache__(key_prefix="field_cache", expiration=120)


class FieldCacheMixin:
    """
    A mixin for providing access to fields in a model
    """

    __module__ = "dada.models.field"
    __field_table__ = Field
    __field_cache__ = FieldCache


FieldTheme.__field_table__ = Field
FieldTheme.__field_cache__ = FieldCache
