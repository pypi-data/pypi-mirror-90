"""
Base Classes From Which All Other Models Inherit From
TODO: abstract out into `dada-api`
"""
import re
import logging
from typing import Dict, List, Optional, Any, Callable, Union

from flask import request, g
from marshmallow import fields, Schema
from sqlalchemy import TypeDecorator, cast, func, Table, or_, and_, asc, desc
from sqlalchemy.dialects.postgresql import ARRAY

import dada_settings
import dada_file
import dada_text
from dada_utils import path, dates
from dada_types import T, DadaType
from dada_types.base import SerializableObject
from dada_types.flt import FilterString
from dada_errors import NotFoundError

from dada.models.core import db, s3conn
from dada.models.api_mixin import *

# /////////
# Core Class For inheritance (almost everything important should be serializable to json!)
# /////////

BASE_LOGGER = logging.getLogger()
# TODO move these somewhere else.

SEARCH_BY_RELS = [
    "users",
    "tags",
    "files",
    "folders",
    "desktops",
]

UPSERT_RELS = [
    "tags",
    "folders",
    "desktops",
]

SEARCH_BY_REL = ["user", "file"]


class DBTable(db.Model, SerializableObject):
    """
    A highly-reusable DB Table for inheritance in our models

    # S3 FILE STORE
    Files and snapshots are stored as partitions
    ```
    a = app name
    c = collection name (files / data)
    e = entity_type
    y = 2-digit created year
    m = created month
    d = created day
    h = created hour
    i = id or some backup name
    ...
    contents/
    ... the contents of the file
    ```
    """

    __abstract__ = True

    #
    __api_endpoint__ = None
    __id_columns__ = ["id", "slug", "name"]  # fields to check existence by
    __internal_columns__ = [
        "created_at",
        "updated_at",
        "deleted_at",
        "file_modified_at",
        "id",
        "slug",
    ]  # fields that are only set internally
    __vector_columns__ = ["name", "info"]
    __vector_column_name__ = "vector"
    __vector_process_steps__ = [
        "rm_html",
        "rm_punct",
        "rm_whitespace",
        "decode",
        "lower",
    ]
    __slug_column_name__ = "slug"
    __slug_delim__ = "-"  # the slug separator
    __slug_columns__ = ["name"]  # columns to use for generating a unique entity slug
    __snake_columns__ = []  # columns to force snake case for
    __fields_column_name__ = "fields"  # the column name where fields objects are stored
    __fields_cache_expiration__ = (
        30  # The number of seconds after which to turn of fields caching
    )
    __file_store__ = False  # Does this table store files or just metadata?

    # join tables to set for auto-populaiton
    __tag_join_table__ = None
    __theme_table__ = None
    __theme_relationship_name__ = "theme"
    __to_dict_excludes__ = ["file"]

    __core_dada_schema__ = None
    __dada_schema__ = None  # The full list of columns in the table (not including relationships / fields)
    __column_names__ = (
        None  # The names of the above columns (should be the same a the keys of schame)
    )
    __column_set__ = None

    # api settings
    __api_paginate_search_results__ = True  # whether or not to paginate search results

    __defaults__ = []  # defaults to generate on API creation.

    # internals
    _meta_cache = (
        {}
    )  # a cache of table name to sql alchemy object for internal joins / lookups

    # the order of these columns determine their
    # render order. If none are present, no slug
    # will be set
    # every column has em

    # core columns
    id = db.Column(T.id.col, primary_key=True, index=True)
    created_at = db.Column(T.date_tz.col, default=T.date_tz.gen, index=True)
    updated_at = db.Column(
        T.date_tz.col, default=T.date_tz.gen, onupdate=T.date_tz.gen, index=True
    )

    # //////
    #  schema introspection / type mapping
    # //////
    @property
    def db_meta(self):
        return MetaData(bind=db.engine, reflect=True)

    @classmethod
    def get_entity_type(cls) -> T.entity_type.py:
        """
        Return a string that describes what type of resource this is.
        :return bool
        """
        table_name = cls.__tablename__
        if table_name.endswith("s"):
            return table_name[:-1]
        return table_name.lower()

    @property
    def entity_type(self):
        """
        The name of this entity (eg `file_folder`)
        """
        return self.get_entity_type()

    # //////
    #  schema introspection / type mapping
    # //////

    @classmethod
    def get_core_columns(cls) -> Dict[str, db.Column]:
        """
        Fetch a mapping of this entity's core column names to sqlalchemy column types
        :return dict
        """
        schema = {}
        for col_name in dir(cls.__table__._columns):
            if not col_name.startswith("_"):
                col_obj = getattr(cls.__table__._columns, col_name)
                schema[col_name] = col_obj.type
        return schema

    @classmethod
    def get_core_dada_types(cls) -> Dict[str, DadaType]:
        """
        Fetch a mapping of this entity's core column names to dada type objecs
        :return dict
        """
        schema = {}
        for name, col in cls.get_core_columns().items():

            # attempt to fetch a core type name
            dada_type = T.get(name, partial=True, partial_guess_arrays=True)

            # if the type is not supported,
            # try to get the mapping back to the core type
            # fall back on text
            if not dada_type:
                dada_type = T.get(getattr(col, "__dada_type__", "text"), default="text")

            # set the type for this column name
            schema[name] = dada_type
        return schema

    @classmethod
    def get_core_dada_schema_def(cls) -> Dict[str, Dict[str, Any]]:
        """
        Fetch a mapping of column names to dada type names
        :return dict
        """
        schema = {}
        for name, type in cls.get_core_dada_types().items():
            # attempt to fetch a core type name
            schema[name] = type.to_dict()
        return schema

    @classmethod
    def get_core_dada_schema(cls) -> Dict[str, T.dada_type.py]:
        """
        Fetch a mapping of column names to dada type names
        :return dict
        """
        if not cls.__core_dada_schema__:
            cls.__core_dada_schema__ = {}
            for name, type in cls.get_core_dada_types().items():
                cls.__core_dada_schema__[name] = type.__dada_type__
        return cls.__core_dada_schema__

    @classmethod
    def get_core_sql_schema(cls) -> Dict[str, T.text.py]:
        """
        Fetch a mapping of column names to sql column type names
        :return dict
        """
        schema = {}
        for name, type in cls.get_core_dada_types().items():
            # attempt to fetch a core type name
            schema[name] = type.sql
        return schema

    @classmethod
    def get_fields(cls) -> Dict[str, Any]:
        """
        Fetch a mapping of column names to dada type names
        :return dict
        """
        if cls.has_fields():
            cache_response = cls.__field_cache__.get(entity_type=cls.get_entity_type())
            return cache_response.value
        return {}

    @classmethod
    def get_field_dada_types(cls) -> Dict[str, DadaType]:
        """
        Fetch a mapping of column names to dada type names
        :return dict
        """
        schema = {}
        if cls.has_fields():
            for field_name, field_schema in cls.get_fields().items():
                schema[field_name] = T.get(field_schema["type"])
        return schema

    @classmethod
    def get_field_schema(cls) -> Dict[str, Dict[str, Any]]:
        """
        Fetch a mapping of field names to dictionary representations
        :return dict
        """
        schema = {}
        for name, type in cls.get_field_dada_types().items():
            # attempt to fetch a core type name
            schema[name] = type.to_dict()
        return schema

    @classmethod
    def get_field_dada_schema(cls) -> Dict[str, T.dada_type.py]:
        """
        Fetch a mapping of column names to dada type names
        :return dict
        """
        schema = {}
        for name, type in cls.get_field_dada_types().items():
            # attempt to fetch a core type name
            schema[name] = type.__dada_type__
        return schema

    @classmethod
    def get_field_sql_schema(cls) -> Dict[str, T.text.py]:
        """
        Fetch a mapping of column names to dada type names
        :return dict
        """
        schema = {}
        for name, type in cls.get_field_dada_types().items():
            # attempt to fetch a core type name
            schema[name] = type.sql
        return schema

    @classmethod
    def get_dada_types(cls) -> Dict[str, Union[DadaType, Dict[str, DadaType]]]:
        """
        Fetch a mapping of column + field names to dada type object
        :return dict
        """
        schema = cls.get_core_dada_types()
        schema[cls.get_fields_column_name()] = cls.get_field_dada_types()
        return schema

    @classmethod
    def get_dada_schema(
        cls,
    ) -> Dict[str, Union[T.dada_type.py, Dict[str, T.dada_type.py]]]:
        """
        Fetch a mapping of column + field names to dada type object
        :return dict
        """
        schema = cls.get_core_dada_schema()
        schema[cls.get_fields_column_name()] = cls.get_field_dada_schema()
        return schema

    @classmethod
    def get_sql_schema(cls) -> Dict[str, Union[T.text.py, Dict[str, T.text.py]]]:
        """
        Fetch a mapping of column + field names to sql schema names
        :return dict
        """
        schema = cls.get_core_sql_schema()
        schema[cls.get_fields_column_name()] = cls.get_field_sql_schema()
        return schema

    # ///////////////////////
    #  Generative Marshmallow Api Request Schema
    # /////////////////////

    @classmethod
    def api_get_endpoint(cls):
        """
        The api endpoint for an entity (eg `File` -> `files`)
        """
        if not cls.__api_endpoint__:
            cls.__api_endpoint__ = cls.get_entity_type() + "s"
        return cls.__api_endpoint__

    @classmethod
    def get_api_search_dict(cls) -> dict:
        """
        generate a dictionary of input parameters for the search endpoint  and
        their corresponding marshmallow.Field schema
        """
        schema_dict = {
            ID_FIELD_PARAM: IdListField,
            FILTER_FIELD_PARAM: FilterField,
            FILTER_COMBINE_FIELD_PARAM: FilterCombineField,
            ORDER_FIELD_PARAM: OrderField,
        }
        if cls.has_slug():
            schema_dict[SLUG_FIELD_PARAM] = SlugListField

        if cls.has_name():
            schema_dict[NAME_FIELD_PARAM] = NameListField

        if cls.has_vector():
            schema_dict.update(
                {
                    SEARCH_FIELD_PARAM: SearchField,
                    SEARCH_COMBINE_FIELD_PARAM: SearchCombineField,
                }
            )

        if cls.has_pagination():
            schema_dict.update(
                {PAGE_FIELD_PARAM: PageField, PER_PAGE_FIELD_PARAM: PerPageField}
            )

        # special handling for files
        if cls.get_entity_type() == "file":
            schema_dict.update({BUNDLE_ID_FIELD_PARAM: T.file_id_array.val})

        # auto populate relation-based filter options
        for rel in SEARCH_BY_RELS:
            if rel.endswith("s"):
                entity_name = rel[:-1]
            if cls.has_entities(rel) or cls.has_entity(entity_name):
                schema_dict[entity_name] = T.get(f"{entity_name}_id_slug_array").val
                schema_dict[f"{entity_name}x"] = RelCombineField
        return schema_dict

    @classmethod
    def api_get_search_schema(cls) -> Schema:
        """
        Fetch a marshmallow schema representing paramaters to pass
        to the api
        :return Marshmallow Schema
        """
        return Schema.from_dict(cls.get_api_search_dict())

    @classmethod
    def api_get_upsert_dict(cls) -> dict:
        """
        Fetch a marshmallow schema representing paramaters to pass
        to the api for the POST /entity/ method
        :return Marshmallow Schema
        """
        schema_dict = {}
        for field_name, dada_type in cls.get_core_dada_types().items():

            # allow id columns in upserts for checking existence
            if field_name in cls.__id_columns__:
                schema_dict[field_name] = dada_type.val

            # ignore internal columns (eg: dates)
            if field_name in cls.__internal_columns__:
                continue

            # vectors are always auto-set
            if field_name == cls.__vector_column_name__:
                continue

            # everything else should be upsert-able
            schema_dict[field_name] = dada_type.val

        # allow for setting of select entites on upsert. all other relationships
        # should be set via their associated api methods
        if cls.has_theme():
            if not cls.get_entity_type().endswith("_theme"):
                # i am a sick developer
                req_schema = cls.__theme_table__.api_get_upsert_schema()
                rel_class_name = f"{cls.api_get_endpoint().title()}Theme"
                schema_dict["theme"] = fields.Nested(
                    type(f"{rel_class_name}UpsertRequest", (req_schema,), {})(),
                    missing={},
                )

        if cls.has_tags():
            schema_dict["tags"] = T.tag_id_slug_array.val

        if cls.has_fields():
            schema_dict["fields"] = T.fields.val

        # special handling for files / folders / desktops
        if cls.get_entity_type() == "file":
            schema_dict["folders"] = T.folder_id_slug_array.val

        if cls.get_entity_type() == "folder":
            schema_dict[
                "files"
            ] = T.file_id_slug_array.val  # create a folder from a list of files
            schema_dict[
                "desktops"
            ] = T.desktop_id_slug_array.val  # create a folder and add it to a desktop

        if cls.get_entity_type() == "desktop":
            schema_dict[
                "folders"
            ] = T.folder_id_slug_array.val  # create a desktop from a list of folders
            schema_dict["desktops"] = T.desktop_id_slug_array.val

        if cls.__file_store__ == True:
            schema_dict[FILE_CONTENTS_PARAM] = FileContentsField

        return schema_dict

    @classmethod
    def api_get_upsert_schema(cls) -> Schema:
        """
        Fetch a marshmallow schema representing paramaters to pass
        to the api for the POST /entity/ method
        :return Marshmallow Schema
        """
        return Schema.from_dict(cls.api_get_upsert_dict())

    @classmethod
    def api_get_fetch_dict(cls) -> dict:
        # attempt to get infer the dada type name
        type_name = cls.get_foreign_key_column_name()
        if cls.has_slug():
            type_name += "_slug"
        return {"id": T.get(type_name, "id").val}  # accept either an Id or a slug.

    @classmethod
    def api_get_fetch_schema(cls) -> Schema:
        """
        Fetch a marshmallow schema for this entity representing paramaters to pass
        to the api for the get /entity/id method
        :return Marshmallow Schema
        """
        return Schema.from_dict(cls.api_get_fetch_dict())

    @classmethod
    def api_get_delete_dict(cls) -> dict:
        return cls.api_get_fetch_dict()

    @classmethod
    def api_get_delete_schema(cls) -> Schema:
        """
        Fetch a marshmallow schema for this entity representing paramaters to pass
        to the api for the DELETE /entity/id method
        :return Marshmallow Schema
        """
        # same as fetch schema
        return Schema.from_dict(cls.api_get_delete_dict())

    # ///////////////////////
    #  Schema properties
    # /////////////////////

    @classmethod
    def get_column_names(cls):
        if not cls.__column_names__:
            cls.__column_names__ = list(cls.get_core_dada_schema().keys())
        return cls.__column_names__

    @classmethod
    def get_column_set(cls) -> frozenset:
        if not cls.__column_set__:
            cls.__column_set__ = frozenset(cls.get_column_names())
        return cls.__column_set__

    @classmethod
    def is_core_field(cls, name):
        """
        Check if a field should be stored in the core entity table
        """
        return name in cls.get_column_set()

    @classmethod
    def is_ext_field(cls, name):
        """
        Check if a field should be stored in 'fields' json
        """
        return name not in cls.get_column_set()

    @classmethod
    def is_internal_field(cls, name):
        """
        Check if a field should be stored in 'fields' json
        """
        return name in cls.__internal_columns__

    @classmethod
    def get_foreign_key_column_name(cls) -> T.fk.py:
        """
        The foreign key column name this resource will have in other tables
        :return bool
        """
        return f"{cls.get_entity_type()}_id"

    @property
    def foreign_key_column_name(self) -> str:
        """
        The name of this entity in other tables
        """
        return self.get_foreign_key_column_name()

    @classmethod
    def get_to_dict_keys(cls):
        return [
            key
            for key in list(
                set(
                    list(cls.api_get_upsert_dict().keys())
                    + cls.__internal_columns__
                    + cls.__id_columns__
                )
            )
            if key not in cls.__to_dict_excludes__
        ]

    # /////////////////////////////////////////
    # Check for presence of attributes
    # //////////////////////////////////////////

    @classmethod
    def has_pagination(cls) -> bool:
        """
        True/false whether this object has slug
        :return bool
        """
        return getattr(cls, "__api_paginate_search_results__", True)

    @classmethod
    def has_id(cls) -> bool:
        """
        True/false whether this object has an ID
        :return bool
        """
        return hasattr(cls, "id")

    @classmethod
    def has_user(cls) -> bool:
        """
        True/false whether this object has an ID
        :return bool
        """
        return hasattr(cls, "user_id")

    @classmethod
    def has_name(cls) -> bool:
        """
        True/false whether this object has a name
        :return bool
        """
        return hasattr(cls, "name")

    @classmethod
    def has_slug(cls) -> bool:
        """
        True/false whether this object has slug
        :return bool
        """
        return hasattr(cls, cls.get_slug_column_name())

    @classmethod
    def has_info(cls) -> bool:
        """
        True/false whether this object has info
        :return bool
        """
        return hasattr(cls, "info")

    @classmethod
    def get_slug_column_name(cls) -> Optional[str]:
        """
        Get this entity's vector column name (default: slug)
        """
        return getattr(cls, "__slug_column_name__", "slug")

    @property
    def is_slug_snakified(self) -> bool:
        """
        Check if any of the values that make up the slug field are tagged for snake casing.
        """
        for col in self.__snake_columns__:
            if col in self.__slug_columns__:
                return True
        return False

    @classmethod
    def prepare_slug(cls, slug: str):
        """
        Make a slug absolute based on its entity name
        """
        prefix = cls.get_entity_type() + "-"
        if not slug.startswith(prefix):
            slug = prefix + slug
        return slug

    @classmethod
    def get_vector_column_name(cls) -> Optional[str]:
        """
        Get this entity's vector column name (defaul: vector)
        """
        return getattr(cls, "__vector_column_name__", "vector")

    @classmethod
    def has_vector(cls) -> bool:
        """
        True/false whether this object has a search vector
        :return bool
        """
        return hasattr(cls, cls.get_vector_column_name())

    @classmethod
    def get_fields_column_name(cls) -> str:
        """
        Get this entity's fields column name
        """
        return getattr(cls, "__fields_column_name__", "fields")

    @classmethod
    def has_fields(cls) -> bool:
        """
        True/false whether this object has fields
        :return bool
        """
        return hasattr(cls, cls.get_fields_column_name())

    @classmethod
    def has_theme(cls) -> bool:
        """
        True/false whether this object has fields
        :return bool
        """
        return hasattr(cls, getattr(cls, "__theme_relationship_name__", "theme"))

    # /////////////////////
    #  entity relationships
    # /////////////////////

    @classmethod
    def has_entity(cls, entity: str) -> bool:
        """
        Given an entity name, return true if the current entity has a direct relationship to the given entity
        :return bool
        """
        if hasattr(cls, entity):
            return True
        return False

    @classmethod
    def has_entities(cls, entity: str) -> bool:
        """
        Given an entity name, return true if the current entity has a direct relationship to the given entity
        :return bool
        """
        if hasattr(cls, f"{entity}s"):
            return True
        return False

    @classmethod
    def has_tags(cls) -> bool:
        """
        Given an entity name, return true if the current entity can be tagged
        :return bool
        """
        return cls.has_entities("tag")

    @classmethod
    def has_rel(cls, entity: str) -> bool:
        """
        Given an entity name, return true if the current entity has any relationship to the given entity
        :return bool
        """
        if entity.endswith("s"):
            entity = entity[:-1]
        return cls.has_entity(entity) or cls.has_entities(entity)

    # /////////////////////
    #  date booleans
    # /////////////////////

    @property
    def has_been_updated(self) -> bool:
        """
        True/false whether this object has tags
        :return bool
        """
        return self.updated_at > self.created_at

    @property
    def has_been_deleted(self) -> T.bool.py_optional:
        """
        True/false whether this object has tags
        :return bool
        """
        if hasattr(self, "deleted_at"):
            return self.deleted_at is not None
        return None

    @property
    def file_has_been_modified(self) -> T.bool.py_optional:
        """
        True/false whether a file's contents have benen modified has been s
        :return bool
        """
        if not self.__file_store__:
            raise NotImplementedError(
                "Last modifed at logic only applies to file store entities"
            )
        if not hasattr(self, "file_modified_at"):
            return None
        return (
            (self.file_modified_at is not None)
            and (self.file_modified_at > self.created_at)
            and (self.file_modified_at >= self.updated_at)
        )

    @classmethod
    def is_paranoid(cls) -> bool:
        """
        Whether or not deleted records are retained
        """
        return False

    @classmethod
    def is_positional(cls):
        """
        Whether or not records have a configurable position / order
        """
        return True

    # /////////////////////
    #  table / relationship introspection
    # /////////////////////

    # query helpers
    @classmethod
    def get_table(cls, rel_name: str) -> Optional[Table]:
        """
        Get a sqlalchemy table object from the app engine metadata.
        We use this internally to generate associations between tables eg `{entity}_tag`  or `{entity}_field`
        :param rel_name: The table name to get
        """
        if not rel_name in cls._meta_cache:
            tbl = self.db_meta.tables.get(rel_name, None)
            if not tbl:
                raise ValueError(f"[get_table] No Table with name {rel_name} exists!")
            cls._meta_cache[rel_name] = tbl
        return cls._meta_cacha.get(rel_name, None)

    @classmethod
    def get_tag_join_table(cls) -> Optional[Table]:
        """
        Get this entity's tag join table eg `{entity}_tag`
        :param rel_name: The table name to get
        """
        if not cls.has_tags():
            return None
        return cls.get_table(f"{cls.get_entity_type()}_tag")

    @classmethod
    def get_theme_table(cls) -> Optional[Table]:
        """
        Get this entity's theme table eg `{entity}_theme`
        :param rel_name: The table name to get
        """
        if not cls.has_theme():
            return None
        return cls.get_table(f"{cls.get_entity_type()}_theme")

    @classmethod
    def get_user_table(cls) -> Optional[Table]:
        """
        Get the user table. WE use this for api authentication
        :param rel_name: The table name to get
        """
        return cls.get_table("user")

    @classmethod
    def get_file_table(cls) -> Optional[Table]:
        """
        Get the user table. WE use this for api authentication
        :param rel_name: The table name to get
        """
        return cls.get_table("file")

    # /////////////////////
    #  Get by id/slug/name
    # /////////////////////

    @classmethod
    def get_by_id(cls, id, **kwargs):
        """
        Fetch an entity by its ID
        """
        return db.session.query(cls).filter(cls.id == id).first()

    @classmethod
    def get_by_id_or_404(cls, *args, **kwargs):
        """
        Fetch an entity by its ID or raise a 404
        """
        obj = cls.get(*args, **kwargs)
        if not obj:
            raise NotFoundError(f"No {cls.get_entity_type()} with id {args[0]} exists")
        return obj

    @classmethod
    def get_by_slug(cls, slug, **kwargs):
        """
        A slug is a unique entity identifier eg:
        """
        if not cls.has_slug():
            raise NotImplementedError(
                f"{cls.get_entity_type()} does not have a slug attribute!"
            )

        return db.session.query(cls).filter(cls.slug == cls.prepare_slug(slug)).first()

    @classmethod
    def get_by_slug_or_404(cls, *args, **kwargs):
        """"""
        obj = cls.get_by_slug(*args, **kwargs)
        if not obj:
            raise NotFoundError(
                f"No {cls.get_entity_type()} with slug {args[0]} exists"
            )
        return obj

    @classmethod
    def get_by_name(cls, name, **kwargs):
        """
        A name
        """
        if "name" in cls.__snake_columns__:
            name = dada_text.get_snake(name)
        return db.session.query(cls).filter(cls.name == name).first()

    @classmethod
    def get_by_name_or_404(cls, *args, **kwargs):
        """"""
        obj = cls.get_by_name(*args, **kwargs)
        if not obj:
            raise NotFoundError(
                f"No {self.cls.get_entity_type()} with name {args[0]} exists"
            )
        return obj

    @classmethod
    def get(cls, *args, **kwargs):
        """
        Overide this for custom id/slug handling
        """
        obj = None
        if isinstance(args[0], int) or not dada_text.is_not_int(args[0]):
            obj = cls.get_by_id(*args, **kwargs)
        elif cls.has_slug():
            obj = cls.get_by_slug(*args, **kwargs)
        return obj

    @classmethod
    def get_or_404(cls, *args, **kwargs):
        """
        Fetch this entity by slug/id or return a 404
        """
        obj = cls.get(*args, **kwargs)
        if not obj:
            prop = "id"
            if cls.has_slug():
                prop += "/slug"
            raise NotFoundError(
                f"No {cls.get_entity_type()} with {prop} {args[0]} exists"
            )
        return obj

    @classmethod
    def exists(cls, *args, **kwargs):
        """
        Check if this model exists based on user / __id_fields__
        """
        qry = db.session.query(cls)

        # check for user-based models
        if cls.has_user():
            uid = kwargs.get("user_id", None)
            if uid:
                qry = qry.filter(cls.user_id == kwargs.get("user_id"))

        # check for id columns

        # breakout for present of id column
        id_val = kwargs.get("id", None)
        if id_val:
            return qry.filter(cls.id == id_val).first()

        # breakout for presence of slug column
        if cls.has_slug() and "slug" in cls.__id_columns__:
            slug_val = kwargs.get(cls.get_slug_column_name(), None)
            if slug_val:
                return qry.filter(cls.slug == cls.prepare_slug(slug_val)).first()

        # search by other id columns
        for id_col in cls.__id_columns__:
            if id_col in ["id", "slug"]:
                continue

            id_val = kwargs.get(id_col, None)
            if not id_val:
                continue

            id_attr = getattr(cls, id_col, None)
            if not id_attr:
                BASE_LOGGER.warning(
                    f"{cls.get_entity_type()} does not have id column {id_col}. Try seting ``__id_columns__`` for this model."
                )
                continue
            return qry.filter(id_attr == id_val).first()

    # //////////////////////////////////
    # search / filter
    # /////////////////////////////////

    # TODO: dry these up or just only use filter strings?
    @classmethod
    def filter_by_id(cls, qry=None, **kwargs):
        """"""
        if not qry:
            qry = db.session.query(cls)

        ids = kwargs.pop(ID_FIELD_PARAM, [])
        if len(ids):
            qry = qry.filter(cls.id.in_(ids))
        return qry

    @classmethod
    def filter_by_user_id(cls, query_strings=None, **kwargs):
        """"""
        if not qry:
            qry = db.session.query(cls)

        ids = kwargs.pop(USER_ID_FIELD_PARAM, [])
        if ids is not None and len(ids):
            qry = qry.filter(cls.user_id.in_(ids))
        return qry

    # query helpers
    @classmethod
    def filter_by_slug(cls, qry=None, **kwargs):
        """"""
        if not qry:
            qry = db.session.query(cls)
        slugs = kwargs.pop(SLUG_FIELD_PARAM, [])
        if slugs is not None and len(slugs):
            qry = qry.filter(cls.slug.in_(slugs))
        return qry

    # query helpers
    @classmethod
    def filter_by_name(cls, qry=None, **kwargs):
        """"""
        if not qry:
            qry = db.session.query(cls)
        names = kwargs.pop(NAME_FIELD_PARAM, [])
        if names is not None and len(names):
            qry = qry.filter(cls.name.in_(names))
        return qry

    @classmethod
    def filter_by_websearch(cls, qry=None, **kwargs):
        """"""
        if not qry:
            qry = db.session.query(cls)

        query_strings = kwargs.pop(SEARCH_FIELD_PARAM, [])
        if query_strings is None or not len(query_strings) or not cls.has_vector():
            return qry

        # get the search vector column
        vector = getattr(cls, cls.get_vector_column_name())

        # build up search filters
        search_filters = []
        for query_string in query_strings:
            # add a query
            search_filters.append(
                vector.op("@@")(func.websearch_to_tsquery(query_string))
            )

        # simple single search
        if len(search_filters) == 1:
            qry = qry.filter(search_filters[0])

        # multi-search
        elif len(search_filters) > 1:
            combine_func = (
                or_ if kwargs.pop(SEARCH_COMBINE_FIELD_PARAM, "or") == "or" else and_
            )
            qry = qry.filter(combine_func(*search_filters))

        # return updated query
        return qry

    @classmethod
    def filter_by_filter_string(cls, qry=None, **kwargs):
        """
        multi-filter via filter-strings
        :param filter: A list of filter strings to apply, eg `created_at:>=:2015`
        """
        if not qry:
            qry = db.session.query(cls)

        # get kwargs / passthrough
        raw_filter_strings = kwargs.get(FILTER_FIELD_PARAM, [])

        BASE_LOGGER.debug(f"got filter strings {raw_filter_strings}")
        if not len(raw_filter_strings):
            return qry

        # get entity + field schema
        core_dada_schema = cls.get_core_dada_types()
        field_dada_schema = cls.get_field_dada_types()

        # build up filter operations
        filter_operations = []
        for raw_string in raw_filter_strings:
            BASE_LOGGER.debug(
                f"[filter-by-filter-string] parsing filter strings {raw_string}"
            )
            ####################
            # filter string parsing
            # ###################
            fs = FilterString(raw_string, context="sql")

            # lookup schema / column
            if cls.is_core_field(fs.field_name):
                BASE_LOGGER.debug(
                    f"[filter-by-filter-string] {fs.field_name} is core field"
                )
                dada_type = core_dada_schema.get(fs.field_name)
                column = getattr(cls, fs.field_name)

            elif fs.field_name in field_dada_schema:
                BASE_LOGGER.debug(f"[filter-by-filter-string] {fs.field_name} is json")
                dada_type = field_dada_schema.get(fs.field_name)
                column = cls.fields[fs.field_name].astext.cast(dada_type.col)

            else:
                BASE_LOGGER.debug(
                    f"[filter-by-filter-string] Cannot filter `{cls.get_entity_type()}` with `{raw_string}` because it does not have field `{fs.field_name}`"
                )
                continue

            # register the filter string's type
            fs.set_type(dada_type.__dada_type__)

            BASE_LOGGER.debug(f"[filter-by-filter-string] using filter {fs.to_dict()}")
            # add the filter operation
            filter_operations.append(
                fs.match_sql(column, value_is_array=dada_type.is_array)
            )

        # combine filters
        if kwargs.get(FILTER_COMBINE_FIELD_PARAM, "and").lower() == "or":

            # or
            return qry.filter(or_(*filter_operations))

        # and
        return qry.filter(and_(*filter_operations))

    @classmethod
    def filter_by_rel(cls, qry=None, rel="tag", **kwargs):
        """
        TODO: make this part of filter strings, eg: tags:in:foo,bar
        Apply a filter by testing for a relationship which another entity
        (This is kind of a hack but it reduces a lot of unnecessary boiler plate code in each api method)
        :param qry: A sqlalchemy query, if not provided one will be created
        :param rel: The name of the relationship (eg 'tag')
        """
        rel_plural = rel + "s"
        rel_op = rel + "x"

        if not qry:
            qry = db.session.query(cls)

        rel_vals = kwargs.pop(rel_plural, [])

        # pass through query object
        # before table introspection
        if rel_vals is None or not len(rel_vals):
            return qry

        # determine relationship
        if cls.has_entity(rel):
            rel_col = getattr(cls, rel)

        elif cls.has_entities(rel):
            rel_col = getattr(cls, rel_plural)

        else:
            raise NotImplementedError(
                f"{cls.get_entity_type()} does not have a relationship to {rel}"
            )

        # introsepct table object
        table = cls.get_table(rel)
        if not table:
            raise NotImplementedError(f"Not relation {rel} exists!")

        # prepare filter values
        filter_col = table.c.id
        if cls.has_slug() and dada_text.is_not_int(rel_vals[0]):
            is_rel_slug = True
            filter_col = table.c.slug
            rel_vals = [cls.prepare_slug(r, entity=rel) for r in rel_vals]

        if kwargs.get(rel_op, "any") == "any":
            return qry.filter(rel_col.any(filter_column.in_(rel_vals)))
        return qry.filter(rel_col.all(filter_column.in_(rel_vals)))

    @classmethod
    def sort_by_order_string(cls, qry=None, **kwargs):
        """
        Multi-sort via order-strings
        :param o: A list of order strings to apply, eg `-created_at`
        """
        if not qry:
            qry = db.session.query(cls)

        o_strings = kwargs.get(ORDER_FIELD_PARAM, [])

        if not len(o_strings):
            return qry

        # get entity + field schema
        core_dada_schema = cls.get_core_dada_types()
        field_dada_schema = cls.get_field_dada_types()

        sort_operations = []
        for o_string in o_strings:
            field_name = o_string
            order_fx = asc
            if o_string.startswith("-"):
                order_fx = desc
                field_name = o_string[1:]
            if cls.is_core_field(field_name):
                sort_col = getattr(cls, field_name)
            else:
                sort_col = cls.fields[field_name].astext.cast(dada_type.col)
            sort_operations.append(order_fx(sort_col))
        return qry.order_by(*sort_operations)

    @classmethod
    def paginate(cls, qry=None, **kwargs):
        """
        Paginate a query
        """
        if not qry:
            qry = db.session.query(cls)
        return qry.paginate(
            page=int(kwargs.get(PAGE_FIELD_PARAM, 1)),
            per_page=int(
                kwargs.get(
                    PER_PAGE_FIELD_PARAM,
                    dada_settings.FILE_DEFAULTS_NUMBER_DEFAULT_FIELDS_PER_FILE,
                )
            ),
            error_out=False,
        ).items

    @classmethod
    def search(cls, *args, **kwargs):
        """
        General purpose model / relationship search
        """

        # base query
        qry = db.session.query(cls)

        # search by core id/slug
        qry = cls.filter_by_id(qry, **kwargs)

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # TODO: ADD user-based restrictions / is_private filters
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        if cls.has_slug():
            qry = cls.filter_by_slug(qry, **kwargs)

        if cls.has_name():
            qry = cls.filter_by_name(qry, **kwargs)

        # (file) search by bundle id
        if cls.get_entity_type() == "file":
            b = kwargs.get(BUNDLE_ID_FIELD_PARAM, [])
            if len(b):
                qry = qry.filter(cls.bundle_id.in_(b))

        # (optional) search vectors
        if cls.has_vector():
            qry = cls.filter_by_websearch(qry, **kwargs)

        # filter strings
        qry = cls.filter_by_filter_string(qry, **kwargs)

        # relationships
        for rel in SEARCH_BY_RELS:
            if cls.has_rel(rel):
                qry = cls.filter_by_rel(qry, rel)

        # sort strings
        qry = cls.sort_by_order_string(qry, **kwargs)

        # pagination
        if cls.has_pagination():
            return cls.paginate(qry, **kwargs)

        # return all results
        return qry.all()

    @classmethod
    def add(cls, *args, **kwargs):
        """"""
        kwargs.setdefault("__add__", True)
        kwargs.setdefault("__commit__", True)
        kwargs.setdefault("__add_core_first__", True)
        instance = cls.create(*args, **kwargs)
        return instance

    @classmethod
    def create(cls, *args, **kwargs):
        """
        instantiate  an object but dont add or commit it
        """
        instance = cls()
        instance.set_cols(**kwargs)
        return instance

    def update(self, **kwargs):
        """
        update
        """
        kwargs.setdefault("__add__", True)
        kwargs.setdefault("__commit__", True)
        self.set_cols(**kwargs)
        if kwargs.get("__add__"):
            db.session.add(self)
        if kwargs.get("__commit__"):
            db.session.commit()

    @classmethod
    def upsert(cls, *args, **kwargs):
        """"""
        instance = cls.exists(*args, **kwargs)
        if not instance:
            return cls.add(*args, **kwargs)
        instance.update(**kwargs)
        return instance

    # ////////////////
    # Search
    # /////////////////
    @classmethod
    def all(cls):
        """
        Fetch all of this entity's records
        """
        return [r for r in db.session.query(cls).all()]

    # //////////
    # Setters
    # /////////

    def set_tags(self, tag_id: List[int] = [], **kwargs) -> None:
        """
        Tag this resource
        """
        if not isinstance(tag_id, list):
            tag_id = [tag_id]

        # create tag association
        for tid in tag_id:
            join_table_kwargs = {
                f"{self.foreign_key_column_name}": self.id,
                "tag_id": tid,
                "__commit__": False,
            }
            self.__tag_join_table__.upsert(**join_table_kwargs)

    def set_theme(self, **kwargs) -> None:
        """
        Set a theme for an entity
        """
        self.__theme_table__.upsert(**kwargs)

    # ######################
    # Search vector creation
    # ######################

    def prepare_vector(self, raw_text: str) -> str:
        """
        Prepare text to be added to a search vector
        """
        val = dada_text.process(raw_text, steps=self.__vector_process_steps__)
        if isinstance(val, list):
            val = " ".join([v.strip() for v in val])
        return val

    def get_core_vector_text(self, **kwargs):
        """
        Get the vector text from the input columns
        """
        vector_text = ""
        # get core vector columns
        for col in self.__vector_columns__:
            # get the column value / self
            col_value = kwargs.get(col, getattr(self, col, ""))

            # handle lists
            if isinstance(col_value, list):
                for col_el in col_value:
                    if isinstance(el, str):
                        vector_text += " " + self.prepare_vector(col_el)

            # handle dictionaries
            elif isinstance(col_value, dict):
                for col_val_key, col_val_val in col_value.items():
                    if instance(col_val_val, str):
                        vector_text += " " + self.prepare_vector(col_val_val)

            elif isinstance(col_value, str):
                vector_text += " " + self.prepare_vector(col_value)
        return vector_text

    def get_field_vector_text(self, **field_values):
        """
        Get the vector text from the input fields
        """
        vector_text = ""
        field_obj = self.get_fields()
        for field_name, field_value in field_values.items():
            field_rec = field_obj.get(field_name)
            if field_rec is None:
                continue
            if field_rec.get("is_searchable", False):
                vector_text += " " + self.prepare_vector(field_value)
        return vector_text.strip()

    def set_slug(self, *args, **kwargs):
        """
        Set the slug from input kwargs / current attributes
        """
        slug_elements = [self.get_entity_type()]
        for col in self.__slug_columns__:
            if col not in kwargs:
                slug_elements.append(dada_text.get_snake(str(getattr(self, col))))
            else:
                slug_elements.append(dada_text.get_snake(str(kwargs.get(col))))
        slug_value = self.__slug_delim__.join(slug_elements)
        setattr(self, self.get_slug_column_name(), slug_value)

    def set_vector(self, *args, **kwargs) -> None:
        """
        Set the search vectors for a an entity
        :param kwargs: input kwargs
        :return None
        """
        field_values = kwargs.pop(self.get_fields_column_name(), {})
        core_vector_text = self.get_core_vector_text(**kwargs)
        field_vector_text = self.get_field_vector_text(**field_values)
        vector_text = (core_vector_text + " " + field_vector_text).strip().lower()
        setattr(self, self.get_vector_column_name(), func.to_tsvector(vector_text))

    def set_core_attributes(self, *args, **kwargs) -> None:
        """
        Set special fields depending ont the resource
        """

        # cache parsed fields here
        # to pass to search vector
        prepared_fields = {}

        # add fields
        if self.has_slug():
            self.set_slug(*args, **kwargs)

        # add fields
        if self.has_fields():
            raw_fields = kwargs.pop(self.get_fields_column_name(), {})
            prepared_fields.update(self.update_fields(raw_fields, **kwargs))
            self.set_fields(prepared_fields)

            # pass through parsed fields to other functions
            kwargs[self.get_fields_column_name()] = prepared_fields

        if self.has_vector():
            self.set_vector(*args, **kwargs)

        # add theme
        if self.has_theme():
            raw_theme = kwargs.pop(self.__theme_relationship_name__, {})
            raw_theme[self.get_foreign_key_column_name()] = self.id
            self.set_theme(**raw_theme)

        # add tags
        if self.has_tags():
            tag_id = kwargs.pop("tags_id", [])
            self.set_tags(tag_id)

    def set_relationships(self, *args, **kwargs) -> None:
        """
        Override this method to set custom relationships for an Entity
        """
        return None

    def set_core_cols(self, *args, **kwargs) -> None:
        """
        update an instance, ensuring we can set this column
        """
        # update simple types
        for key, value in kwargs.items():
            if value is None:
                continue
            # filter out created at / updated  at  / id etc
            if self.is_internal_field(key):
                continue
            if not self.is_core_field(key):
                continue
            if key in self.__snake_columns__:
                value = dada_text.get_snake(value)
            setattr(self, key, value)

    def set_cols(self, *args, **kwargs) -> None:
        """
        Set an entity's attributes
        """
        self.set_core_cols(**kwargs)
        db.session.add(self)
        db.session.commit()
        self.set_core_attributes(**kwargs)
        self.set_relationships(**kwargs)
        db.session.add(self)
        db.session.commit()

    # ///////////////////////////
    # field validation
    # ///////////////////////////

    def is_field_acceptable(
        self,
        entity_type=T.entity_type.py,
        file_type: T.file_type.py_optional = None,
        file_subtype: T.file_subtype.py_optional = None,
        accepts_entity_types: T.entity_type_array = [],
        accepts_file_types: T.file_type_array = [],
        accepts_file_subtypes: T.file_subtype_array = [],
    ) -> bool:
        """
        Check whether a given type/subtype is acceptable for this field
        :param entity_type: A dada Entity Type
        :param file_type: A dada File Type
        :param file_subtype: A dada File Subtype
        :param accepts_entity_types: T.entity_type_array = [],
        :param accepts_file_types: T.file_type_array = [],
        :param accepts_file_subtypes: T.file_subtype_array = []
        :return bool
        """

        # filter by entitty
        if entity_type in accepts_entity_types:

            # special handling for files
            if entity_type == "file":

                # test for odd case when a field accepts all file types but only a subtype
                if "all" in accepts_file_types:
                    if file_subtype in accepts_file_subtypes:
                        return True

                # test for permissive subtype but restrictive file type
                if "all" in accepts_file_subtypes:
                    if file_type in accepts_file_types:
                        return True

                # now just test for inclusion
                if (
                    file_type in accepts_file_types
                    and file_subtype in accepts_file_subtypes
                ):
                    return True
            else:
                return True

        # otherwise reject
        return False

    def validate_field(
        self, field_rec: Dict[str, Any], field_name: str, field_value: Any, **kwargs
    ) -> Any:
        """
        Validate a file field before insertion
        """

        # get the field record
        # if the field is not supported, ignore it
        if not field_rec:
            FILE_MODEL_LOGGER.debug(
                f"[validate_field] Ignoring unsupported field: {field_name}"
            )
            return

        # check if the field applies to this file
        if not self.is_field_acceptable(
            entity_type=self.entity_type,
            file_type=kwargs.get("file_type"),
            file_subtype=kwargs.get("file_subtype"),
            accepts_entity_types=field_rec.get("accepts_entity_types", []),
            accepts_file_types=field_rec.get("accepts_file_types", []),
            accepts_file_subtypes=field_rec.get("accepts_file_subtypes", []),
        ):

            MIXIN_LOGGER.debug(
                f"""
                Ignoring unsupported field: {field_rec['name']}:{field_rec['type']} for file type with kwargs: {kwargs}
                This field accepts entity_types: {field_rec['accepts_file_types']},
                file_types: {field_rec['accepts_file_types']},
                and file_subtypes: {field_rec['accepts_file_subtypes']}
                """
            )
            return

        # deserialize this value
        dada_type = T.get(field_rec["type"])
        try:
            value = dada_type.validate(field_value)
        except Exception as e:
            raise ValueError(
                f"Could not add `{field_rec.name}` to entity `{self.entity_type}` because `{field_value}` was invalid:\nERROR {e}"
            )

        # filter out nulls
        if not value and field_rec.get("is_required", False):
            raise ValueError(
                f"Could not create {self.entity_type} because it was missing required field: {field_name}"
            )

        # filter out nulls
        if (
            field_rec.get("is_text", False)
            and not field_rec.get("is_array", False)
            and text.is_null(value)
        ):
            return None

        # null/empty -> empty list for array
        if field_rec.dada_type.is_array and text.is_null(value):
            return []

        # if not value
        return value

    def prepare_fields(self, fields: dict, **kwargs) -> dict:
        # meta fields
        # loop through fields and apply corresponding validations
        field_data = {}

        # todo: add this to cache?
        field_obj_dict = self.get_fields()

        #
        for field_name, field_value in fields.items():

            # get the field record
            field_rec = field_obj_dict.get(field_name, None)

            # perform validations
            value = self.validate_field(field_rec, field_name, field_value, **kwargs)

            # ignore nulls
            if value:

                # create dictionary of deserialized values
                field_data[field_rec.name] = value

        return field_data

    def update_fields(self, fields: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        Set the fields for a an entity
        :param fileds: the raw fields to set for this entity
        :return None
        """
        fields_column_name = self.get_fields_column_name()
        raw_fields = kwargs.pop(fields_column_name, {})

        # prepare new fields
        new_fields = self.prepare_fields(raw_fields, **kwargs)

        # preserve old fields
        old_fields = getattr(self, fields_column_name, {})
        if old_fields is None:
            old_fields = {}

        # update old fields with new fields
        old_fields.update(new_fields)
        return fields

    def set_fields(self, fields: Dict[str, Any], **kwargs) -> None:
        """
        set the fields
        """
        setattr(self, self.get_fields_column_name(), fields)

    # ///
    # Default generation.
    # ///

    @classmethod
    def has_defaults(cls):
        """"""
        return len(cls.__defaults__) > 0

    @classmethod
    def create_defaults(
        cls, user_id: T.user_id.py = None, tag_id: T.tag_id_array.py = []
    ):
        """"""
        if cls.has_defaults():
            for record in cls.__defaults__:
                if user_id:
                    record["user_id"] = user_id
                if tag_id:
                    record["tags"] = [tag_id]
                instance = cls.upsert(**record)
                BASE_LOGGER.info(
                    f"created default {cls.get_entity_type()}:{instance.name}"
                )

    def to_dict(self):
        """
        Serialize a model as  python dictionary.
        """
        d = {}
        for attr in self.get_to_dict_keys():
            val = getattr(self, attr)
            if hasattr(val, "to_dict"):
                val = val.to_dict()
            elif attr in ["theme", "source"]:  # TODO improve this?
                if len(val):
                    val = val[0].to_dict()
            d[attr] = val
        return d
