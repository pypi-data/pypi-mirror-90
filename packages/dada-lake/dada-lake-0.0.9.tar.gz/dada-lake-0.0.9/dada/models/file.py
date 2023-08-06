import os
from io import BytesIO
from uuid import uuid4
import mimetypes
import base64
import hashlib
import logging
from typing import Optional

from flask import request
from marshmallow import fields
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy_utils.types import TSVectorType

import dada_settings
import dada_file
from dada_types import T, gen
import dada_archive
from dada_utils import path, dates

from dada import queue as Q
from dada_errors import RequestError
from dada.models.base import DBTable
from dada.models.core import db, s3conn
from dada.models.mixin import (
    SlugTableMixin,
    SearchTableMixin,
    PrivateTableMixin,
    FieldTableMixin,
    ParanoidTableMixin,
    UserMixin,
    GroupTableMixin,
)
from dada.models.field import FieldCacheMixin
from dada.models.file_folder import FileFolder
from dada.models.tag_join_table import FileTag
from dada.models.theme_table import FileTheme

FILE_LOGGER = logging.getLogger()

# kind of a hack to enforce fields reserved
# and also have request validators for
# these same names (they come from the File model)
# TODO: move this somewhere else or figure out
# how to validate based off model schema?


class File(
    DBTable, GroupTableMixin, ParanoidTableMixin, FieldCacheMixin, UserMixin,
):

    __tablename__ = "file"
    __module__ = "dada.models.file"
    __id_columns__ = ["id", "check_sum"]
    __file_store__ = True
    __audit_store__ = False
    __slug_format__ = "{entity_type}-{file_name}-{check_sum}"
    __slug_columns__ = [
        "file_name",
    ]
    __internal_columns__ = ["id"]
    __tag_join_table__ = FileTag
    __theme_table__ = FileTheme

    # bundle idq1w`
    bundle_id = db.Column(
        T.bundle_id.col, db.ForeignKey("file.id"), index=True, default=None
    )

    # audio / video / image / data , etc
    file_type = db.Column(
        T.file_type.col(
            *dada_settings.FILE_DEFAULTS_FILE_TYPES,
            name="file_file_type_enum",
            create_type=True,
        ),
        index=True,
        default=dada_settings.FILE_DEFAULTS_DEFAULT_TYPE,
    )

    # audio_loop / audio_hit / audio_clip / image_loop / ec
    file_subtype = db.Column(
        T.file_subtype.col(
            *dada_settings.FILE_DEFAULTS_FILE_SUBTYPES,
            name="file_file_subtype_enum",
            create_type=True,
        ),
        index=True,
        default=dada_settings.FILE_DEFAULTS_DEFAULT_FILE_SUBTYPE,
    )

    # core file metadata
    file_name = db.Column(T.file_name.col)
    check_sum = db.Column(T.check_sum.col, index=True)
    mimetype = db.Column(T.mimetype.col, index=True)
    byte_size = db.Column(T.byte_size.col, index=True, default=None)
    ext = db.Column(T.ext.col, index=True, default=0)
    file_modified_at = db.Column(T.date_tz.col, default=dates.now, index=True)

    __table_args__ = (db.Index(f"file_vector_idx", "vector", postgresql_using="gin"),)

    # one-> many relationships
    folders = db.relationship("Folder", secondary="file_folder", lazy=True)
    tags = db.relationship("Tag", secondary="file_tag", lazy="joined")

    # see: https://docs.sqlalchemy.org/en/13/orm/self_referential.html
    bundled_files = db.relationship("File", lazy=True)

    # one->one relationships
    theme = db.relationship("FileTheme", lazy="joined")

    def __repr__(self):
        """"""
        return f"<File:{self.file_type}:{self.file_subtype}:{self.s3_latest_file_url}>"

    # bundling
    @property
    def is_part_of_bundle(self) -> T.bool.py:
        """
        Return true/false if this file is part of a bundle
        :return bool
        """
        return self.bundle_id is not None

    # version based on checksum
    @property
    def global_backup_version(self) -> T.text.py:
        """
        Get a text representation of the entity's version.
        """
        if self.check_sum:
            return self.check_sum

        return (
            getattr(self, self.__version_update_column__ or "updated_at") or dates.now()
        ).strftime(self.__version_string_format__)

    @property
    def global_file_name(self) -> T.file_name.py:
        """
        An informative filepath
        """
        if self.file_name is None:
            return f"{self.file_type}__{self.file_subtype}__{self.check_sum[0:9]}"
        return self.file_name

    @property
    def global_file_path(self) -> T.path.py:
        """
        The full path to this file.
        """
        return f"{self.s3_file_name}.{self.ext}"

    @property
    def attachment_name(self) -> T.file_name.py:
        """
        A simple filepath
        """
        return f"{self.file_name}.{self.ext}"

    @property
    def attachment_path(self) -> T.path.py:
        """
        A simple filepath
        """
        return f"{self.file_name}.{self.ext}"

    @property
    def api_download_url(self) -> T.url.py:
        """
        Url for api download
        """
        return f"{dada_settings.BASE_URL}/files/{self.id}/download"

    @property
    def api_stream_url(self) -> T.url.py:
        """
        Url for api streaming
        """
        return f"{dada_settings.BASE_URL}/files/{self.id}/stream"

    # crud classmethods
    @classmethod
    def upsert(cls, **kwargs):
        # check for file contents
        fobj = kwargs.pop("file", None)
        if fobj is not None:
            if kwargs.get("file_name") is None:
                kwargs["file_name"] = path.get_name(fobj.filename)
            if kwargs.get("ext") is None:
                kwargs["ext"] = path.get_ext(fobj.filename)
            filepath = path.get_tempfile_from_fobj(fobj, ext=kwargs["ext"])
            return cls.upsert_from_local_filepath(filepath, **kwargs)

        # create/ update metadata
        instance = cls.exists(**kwargs)
        if not instance:
            raise RequestError(
                "You cannot create a new file without adding an actual file!"
            )

        # ensure presence of file type
        # for field determinations
        kwargs.update(
            dict(file_type=instance.file_type, file_subtype=instance.file_subtype)
        )
        return instance.update(**kwargs)

    @classmethod
    def upsert_from_local_archive(cls, filepath, user_id, **kwargs):
        """
        Add files from a local archive (zip/rar/etc)
        """
        if not path.exists(filepath):
            raise ValueError(f"filepath '{filepath}' does not exist")

        for fp in dada_archive.extract_all(filepath, **kwargs):
            cls.upsert_from_local_filepath(fp, user_id, **kwargs)

    @classmethod
    def upsert_from_local_directory(
        cls, directory, user_id, ignore_hidden=True, **kwargs
    ):
        """"""
        if not path.exists(directory):
            raise ValueError(f"directory '{directory}' does not exist")
        for fp in path.list_files(directory, ignore_hidden=ignore_hidden):
            cls.upsert_from_local_filepath(fp, user_id, **kwargs)

    @classmethod
    def upsert_from_local_filepath(
        cls, filepath, **kwargs,
    ):
        """
        Given a a filepath and optional defaults, instaniate a File instance.
        """
        if not path.exists(filepath):
            raise RequestError(
                f"Cannot create file from '{filepath}' as it does not exist"
            )

        # ensure core metadata
        gl = dada_file.load(filepath, **kwargs)
        gl.ensure_dada(filepath)

        # upsert
        instance = cls.exists(**gl.db)
        if not instance:
            instance = cls.add(**gl.db)
        else:
            instance.update(**gl.db)

        # queue the file save job
        Q.dada_file.save.delay(filepath, **instance.to_dict())

        # return
        return instance

    @classmethod
    def gen_random(cls):
        # TODO: make this a class method on the Base Model using schema inference.
        # pick a file
        p = gen.choose(dada_settings.FILE_DEFAULTS_FILE_FIXTURES)
        d = {
            "name": T.text.gen(max_len=52),
            "file_name": T.file_name.gen(),
            "info": T.text.gen(max_len=512),
            "file_type": T.file_type.gen(),
            "check_sum": T.check_sum.gen(),
            "file_subtype": T.file_subtype.gen(),
            "byte_size": int(T.byte_size.gen()),
            "ext": "mp3",
            "mimetype": "audio/mpeg",
            "fields": {},
        }

        # GENERATE RANDOM DATA FOR DEFAULT FIELDS per type
        fields = dada_settings.FIELD_TYPE_DEFAULTS.get(d["file_type"], [])
        for field in fields:
            typ = field.get("type")
            name = field["name"]
            value = gen.random_thing(typ, name, infer_type=True)
            d["fields"][name] = value

        # GENERATE A RANDOM FOLDER ASSIGNMENT
        d["folder_id"] = [
            gen.choose(
                range(1, dada_settings.FOLDER_DEFAULTS_NUMBER_DEFAULT_FOLDERS, 1)
            )
        ]
        return d

    @classmethod
    def create_defaults(
        cls,
        user_id: T.user_id.py,
        tag_id: T.tag_id_array.py = [],
        folder_id: T.folder_id_array.py = [],
    ) -> None:
        """
        Create Random Defaults
        TODO: refactor / deprecate this.
        """
        for i in range(dada_settings.FILE_DEFAULTS_NUMBER_DEFAULT_FILES):
            # CREATE A DATABASE RECORD
            instance = cls.add(user_id=user_id, tag_id=tag_id, **cls.gen_random())
            FILE_LOGGER.info(
                f"Created default file({instance.file_type}:{instance.file_subtype}): {instance.name}... "
            )

    # ///////////
    # Core metadata etraction / type inference
    # //////////
    @property
    def human_size(self):
        if self.byte_size is None:
            return "null"
        return T.byte_size.hum(int(self.byte_size))

    @property
    def local_urls(self):
        return dada_file.load(url=None, location="loc", **self.to_dict()).urls.loc

    @property
    def global_urls(self):
        return dada_file.load(url=None, location="s3_int", **self.to_dict()).urls.glob
