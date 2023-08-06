"""
Model Mixin For Constructing Schema and Re-using Logic
"""
import logging

from sqlalchemy import func
from sqlalchemy.ext.declarative import as_declarative, declared_attr

import dada_settings
from dada_types import T
from dada_utils import dates
from dada_text import emoticon

from dada.models.core import db

# /////////
# Mixins for ease of Model creation
# ////////

MIXIN_LOGGER = logging.getLogger()


class ParanoidTableMixin:
    """
    Adding "paranoid" behavoir for deletion
    """

    deleted_at = db.Column(T.date_tz.col, default=None, index=True)

    @classmethod
    def is_paranoid(cls):
        return True


class PrivateTableMixin:
    """
    Adding public / private visibility to a table.
    """

    is_private = db.Column(T.is_private.col, default=False)


class SearchTableMixin:
    """
    Adding search functionality to an entity
    """

    __vector_column_name__ = "vector"
    __vector_columns__ = ["name", "info"]  # a list of columns to vectorize
    vector = db.Column(T.vector.col)
    info = db.Column(T.info.col, index=False)


class SlugTableMixin:

    name = db.Column(T.name.col, index=True)
    slug = db.Column(T.slug.col, index=True)

    @property
    def title(self):
        """"""
        return self.slug.replace("_", " ").title()

    @classmethod
    def exists(cls, **kwargs: dict):
        """"""
        q = db.session.query(cls)
        if "id" in kwargs:
            q = q.filter(cls.id == kwargs.get("id"))
        elif "slug" in kwargs:
            q = q.filter(cls.slug == kwargs.get("slug"))
        if not q.first():
            return False
        return True


class DadaTypeTableMixin:
    """
    Tables which have an associated dada type (eg Fields / Edges)
    """

    __type_column_name__ = "type"

    @property
    def dada_type_name(self):
        """
        interna
        """
        return self.dada_type.__dada_type__

    @property
    def dada_type(self):
        """
        interna
        """
        return T.get(self.__type_column_name__)


class EmojiTableMixin:
    """
    Tables which have Emoji
    TODO: just make this a theme table mixin
    """

    emoji = db.Column(T.emoji.col, default=T.emoji.gen)

    @property
    def emoji_char(self):
        return emoticon.emoji_from_string(self.emoji_slack_code)

    @property
    def emoji_slack_code(self):
        return f":{self.emoji}:"

    @property
    def emoji_obj(self):
        return EMOJI.get(self.emoji)


# ///
# Type Checking Mixin Tables
# ///


class FileTypeTableMixin:
    """
    Tables which regulate input based on file type (tags, fields, sources)
    """

    # what type(s) of files does this field apply to?
    accepts_file_types = db.Column(
        T.file_type_array.col(
            T.file_type.col(
                *(dada_settings.FILE_DEFAULTS_FILE_TYPES + ["all"]),
                name=f"accepts_file_types_enum",
                create_type=True,
            )
        ),
        index=True,
        default=["all"],
    )
    accepts_file_subtypes = db.Column(
        T.file_subtype_array.col(
            T.file_subtype.col(
                *(dada_settings.FILE_DEFAULTS_FILE_SUBTYPES + ["all"]),
                name=f"accepts_file_subtypes_enum",
                create_type=True,
            )
        ),
        index=True,
        default=["all"],
    )


class FieldTableMixin:
    """"""

    __fields_column_name__ = "fields"
    fields = db.Column(T.fields.col, default={})


# /////////
# Modular positional table (Folders and Desktops)
# /////////
class JoinTableMixin:

    # set this to determine id column names
    __from_id__ = "file_id"
    __to_id__ = "folder_id"

    @classmethod
    def get_from_id_foreign_key_column_name(cls):
        return cls.__from_id__

    @classmethod
    def get_to_id_foreign_key_column_name(cls):
        return cls.__to_id__

    @classmethod
    def get_from_entity_type(cls):
        return cls.get_from_id_foreign_key_column_name().replace("_id", "")

    @classmethod
    def get_to_entity_type(cls):
        return cls.get_to_id_foreign_key_column_name().replace("_id", "")

    @classmethod
    def api_get_from_endpoint(cls):
        return cls.get_from_entity_type() + "s"

    @classmethod
    def api_get_to_endpoint(cls):
        return cls.get_to_entity_type() + "s"

    @property
    def __id_columns__(self):
        return [self.__from_id__, self.__to_id__]

    @property
    def from_col(elf):
        return getattr(cls, cls.__from_id__)

    @property
    def to_col(self):
        return getattr(cls, cls.__to_id__)

    @classmethod
    def get(cls, **kwargs):
        return (
            db.session.query(cls)
            .filter(cls.from_col == kwargs.get(cls.__from_id__))
            .filter(cls.to_col == kwargs.get(cls.__to_id__))
            .first()
        )

    @classmethod
    def exists(cls, **kwargs):
        """"""
        return cls.get(**kwargs) is not None


# /////////
# Combinations of Mixins for ease of Model creation
# /////////


# a useful grouping from Folders and Desktops


class GroupTableMixin(
    SlugTableMixin, SearchTableMixin, PrivateTableMixin, FieldTableMixin
):
    pass


class ThemeTableMixin(EmojiTableMixin, SlugTableMixin):
    """
    Base Mixin class for a theme table.
    """

    __id_columns__ = ["id", "slug"]
    __internal_columns__ = [
        "created_at",
        "updated_at",
        "id",
    ]
    pass


class JoinFieldTableMixin(JoinTableMixin, FieldTableMixin):
    pass


# /////////
# Declarative Mixins.
# These set columns / relationships and connot be naively
# combiled with other mixin without also inheriting from DBTable
# /////////


@as_declarative()
class PositionalTableMixin(object):
    """
    A mixin for file/folder folder/desktop macro/task relationships where ordering of the relationships matter.
    """

    @classmethod
    def is_positional(cls):
        return True

    @declared_attr
    def position(self):
        """
        The position of the from element inside the to element
        """
        return db.Column(T.position.col, default=1, index=True)

    @classmethod
    def get_max_position(cls, **kwargs):
        """"""
        max_position = (
            db.session.query(func.max(cls.position))
            .filter(cls.to_col == kwargs.get(cls.__to_id__))
            .first()
        )[0]
        return max_position or 0

    @classmethod
    def get_next_position(cls, **kwargs):
        """"""
        return cls.get_max_position(**kwargs) + 1

    @classmethod
    def create(cls, **kwargs):
        """
        Set the ids first before setting the position
        """
        instance = cls()

        # don't let the position get set normally
        position = kwargs.pop("position", None)

        # set the core columns
        instance.set_cols(**kwargs)

        # now set the position (TODO: figure out how to create a positional element and re-order other poitional elements to suit)
        # instance.position = position or cls.get_next_position(**kwargs)
        instance.position = cls.get_next_position(**kwargs)
        return instance

    def update(self, **kwargs):
        """
        Update the position of a positional table.
        """
        new_pos = kwargs.get("position")

        # if positions are the same, do nothing:
        if new_pos == self.position:
            return self

        # increment all greater or equal to new index
        db.session.query(self).filter(self.to_col == kwargs.get(self.__to_id__)).filter(
            self.position >= new_pos
        ).update({"position": (cls.position + 1)})
        db.session.commit()

        # set new position
        self.position = new_pos
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self, **kwargs):
        """
        Remove an element from a positional table and update
        the position of all other elements
        """

        cur_pos = self.position

        # decrement all indicies greater than the current index
        db.session.query(self).filter(self.to_col == kwargs.get(self.__to_id__)).filter(
            self.position > cur_pos
        ).update({"position": (self.position - 1)})

        # delete the record
        db.session.delete(self)
        db.session.commit()
        return self


@as_declarative()
class UserMixin(object):
    """
    Tables which are linked to users
    """

    @declared_attr
    def user_id(self):
        return db.Column(T.user_id.col, db.ForeignKey("user.id"), index=True)

    @declared_attr
    def user(cls):
        return db.relationship("User", lazy=True)


@as_declarative()
class TagTableMixin(object):
    """
    Base mixin class for a Tag Join Table
    """

    __to_id__ = "tag_id"

    @declared_attr
    def tag_id(cls):
        return db.Column(T.tag_id.col, db.ForeignKey("tag.id"), index=True)

    @declared_attr
    def tag(cls):
        return db.relationship("Tag", lazy=True)
