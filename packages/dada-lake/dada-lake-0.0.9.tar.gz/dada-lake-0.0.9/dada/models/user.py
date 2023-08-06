from uuid import uuid4
import logging

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import func

import dada_settings
from dada_types import T, gen
import dada_text

from dada_errors import AuthError, NotFoundError, ForbiddenError
from dada.models.base import DBTable
from dada.models.core import db
from dada.models.field import FieldCacheMixin
from dada.models.tag_join_table import UserTag
from dada.models.theme_table import UserTheme
from dada.models.mixin import (
    SlugTableMixin,
    SearchTableMixin,
    FieldTableMixin,
    ParanoidTableMixin,
)


USER_LOGGER = logging.getLogger()


class User(
    DBTable,
    ParanoidTableMixin,
    SlugTableMixin,
    SearchTableMixin,
    FieldTableMixin,
    FieldCacheMixin,
):
    __tablename__ = "user"
    __module__ = "dada.models.user"
    __id_fields__ = ["id", "name", "email"]
    __defaults__ = dada_settings.USER_DEFAULTS
    __tag_join_table__ = UserTag
    __theme_table__ = UserTheme
    __internal_columns__ = [
        "created_at",
        "updated_at",
        "deleted_at",
        "id",
        "slug",
        "password",
        "api_key",
        "admin",
    ]

    # authentication details
    email = db.Column(T.email.col, index=True, unique=True)
    password = db.Column(T.password.col)
    admin = db.Column(T.bool.col, default=False)
    api_key = db.Column(T.api_key.col, index=True, unique=True)

    # relationships
    desktops = db.relationship("Desktop", lazy="joined")
    folders = db.relationship("Folder", lazy="joined")
    files = db.relationship("File", lazy=True)

    tags = db.relationship("Tag", secondary="user_tag", lazy="joined")
    theme = db.relationship("UserTheme", lazy="joined")

    __table_args__ = (
        db.Index("user_name_uniq_idx", "name", unique=True),
        db.Index("user_slug_uniq_idx", "slug", unique=True),
        db.Index("user_email_uniq_idx", "email", unique=True),
        db.Index("user_vector_idx", "vector", postgresql_using="gin"),
    )

    @classmethod
    def gen_password(cls, password):
        return generate_password_hash(password)

    @classmethod
    def gen_api_key(cls):
        """"""
        return (
            f"{dada_text.get_slug(gen.random_artist_name())}-{gen.random_short_hash()}"
        )

    @classmethod
    def create(cls, *args, **kwargs):
        """
        Create a user
        """
        # instantiate user
        instance = cls()
        # set password hash
        instance.password = cls.gen_password(kwargs["password"])

        # set api key (internally we can pass in a non-random api key for testing/deving)
        instance.api_key = kwargs.get("api_key", cls.gen_api_key())

        # set core columns
        instance.set_cols(*args, **kwargs)

        # return created instance
        return instance

    @classmethod
    def login(cls, **kwargs):
        """
        Login a user.
        """
        instance = cls.get_by_email(email=kwargs.get("email"))

        if instance is None:
            raise AuthError(f'[login] A user with email "{email}" does not exist.')

        # check the supplied password if not the super user
        if not instance.check_password(kwargs.get("password")):
            raise ForbiddenError("[login] Invalid password.")

        return instance

    @classmethod
    def get_by_api_key(cls, api_key):
        """
        Fetch a user by their api key.
        """
        return db.session.query(cls).filter(cls.api_key == api_key).first()

    @classmethod
    def get_by_email(cls, email):
        """
        fetch a user by their api key.
        """
        return db.session.query(cls).filter(cls.email == email).first()

    def check_password(self, password):
        """
        Check password via hashing algo
        """
        return check_password_hash(self.password, password)
