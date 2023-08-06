import os
import unittest
import json
import logging
from contextlib import contextmanager

from flask import g
from sqlalchemy import inspect

from dada_test import BaseTest
from dada.factory import create_app
from dada.models.core import db, s3conn
from dada.models.user import User
from dada.models.field import Field

TEST_LOGGER = logging.getLogger()


class S3Test(BaseTest):
    def setUp(self):
        for key in s3conn.list_keys(""):
            s3conn.delete(key)

    def tearDown(self):
        for key in s3conn.list_keys(""):
            s3conn.delete(key)


class APITest(BaseTest):
    def setUp(self):
        """
        Build the database
        """
        os.environ["SICKDB_ENV"] = "test"
        self.app = create_app()
        self.user = None
        self.fields_created = False
        with self.app.app_context():
            db.create_all()
            self.user = User.get_by_email("test-email")
            if not self.user:
                self.user = User.create(
                    name="test-user",
                    password="test-password",
                    email="test-email",
                    admin=True,
                )
                self.user.admin = True
                db.session.add(self.user)
                db.session.commit()
                if not self.fields_created:
                    Field.create_defaults()
                    self.fields_created = True
            self.api_key = self.user.api_key

    def tearDown(self):
        """
        Build the database
        """
        with self.app.app_context():
            db.session.remove()
            inspector = inspect(db.engine)
            for table in inspector.get_table_names():
                db.session.execute(f'DROP TABLE "{table}" CASCADE;')

    @contextmanager
    def api(self):
        with self.app.app_context():
            with self.app.test_client() as api:
                g.user = self.user
                yield api

    def post(
        self,
        path,
        data,
        serialize=True,
        content_type="application/json",
        parse_response=True,
    ):
        if serialize:
            data = json.dumps(data)
        with self.api() as api:

            response = api.post(
                path,
                data=data,
                query_string={"api_key": self.api_key},
                content_type=content_type,
            )
            data = None
            if parse_response:
                data = json.loads(response.data)
            return data, response

    def get(self, path, parse_response=True, query_string={}):
        """issue a get request in the test context"""
        query_string["api_key"] = self.api_key
        with self.api() as api:
            response = api.get(
                path, query_string=query_string, content_type="application/json"
            )
            data = None
            if parse_response:
                data = json.loads(response.data)
            return data, response

    def put(
        self,
        path,
        data,
        serialize=True,
        content_type="application/json",
        parse_response=True,
    ):
        """issue a put request in the test context"""
        if serialize:
            data = json.dumps(data)
        with self.api() as api:
            response = api.put(
                path,
                data=data,
                query_string={"api_key": self.api_key},
                content_type=content_type,
            )
            data = None
            if parse_response:
                data = json.loads(response.data)
            return data, response

    def delete(self, path):
        """issue a delete request in the test context"""
        with self.api() as api:
            response = api.delete(
                path, query_string={"api_key": self.api_key}, data=data
            )
            data = None
            if response.data:
                data = json.loads(response.data)
            return data, response

    def upsert_fixture_file(self, fp, **kwargs):
        """upsert a fixture file"""
        with open(self.get_fixture(fp), "rb") as f:
            kwargs.update({"file": f})
            data, response = self.post(
                f"/files/",
                data=kwargs,
                content_type="multipart/form-data",
                serialize=False,
            )
        return data, response
