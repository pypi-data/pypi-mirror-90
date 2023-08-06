from flask import Blueprint, Response, send_file
from flask_apispec import use_kwargs, marshal_with, doc
from marshmallow import fields

import dada_serde
from dada_utils import path
from dada.models.file import File
from dada.models.file_folder import FileFolder
from dada.models.tag_join_table import FileTag
from dada.models.api_response import FileResponse
from dada.models.api_request import APIRequest
from dada.resources.core import crud_blueprint_from_model
import dada_settings

# ///////////////
# Base CRUD Files API
# ///////////////
SEARCH_DOCS = """
"""
UPSERT_DOCS = """
"""
FETCH_DOCS = """
"""
DELETE_DOCS = """
"""

FILES_APP = crud_blueprint_from_model(
    blueprint=Blueprint("files", __name__),
    core_model=File,
    base_response_schema=FileResponse,
    relationships=[FileFolder, FileTag],
    doc_tags=["files"],
    # search_docs=SEARCH_DOCS,
    # upsert_docs=UPSERT_DOCS,
    # fetch_docs=FETCH_DOCS,
    # delete_docs=DELETE_DOCS
)

# /////////////////////////
# GET /files/{id}/stream
# /////////////////////////


BaseFetchRequest = File.api_get_fetch_schema()


class StreamFileRequest(APIRequest, BaseFetchRequest):
    __name__ = "file_stream_request"

    # chunk_size = fields.Integer(default=1024)


@FILES_APP.route("/<id>/stream")
@use_kwargs(StreamFileRequest(), location="query_path")
@doc(description="Stream a file's contents", tags=["files"])
def stream_file(**kwargs):
    file = File.get_or_404(kwargs.get("id"))
    tmp_fp = path.get_tempfile(name=file.file_name, ext=file.ext)
    file.s3_download_file(tmp_fp)
    return send_file(
        tmp_fp,
        as_attachment=False,
        attachment_filename=file.attachment_path,
        mimetype=file.mimetype,
    )


# /////////////////////////
# GET /files/{id}/download
# /////////////////////////


class DownloadFileRequest(APIRequest, BaseFetchRequest):
    __name__ = "file_download_request"
    pass


# TODO: fix this to work with dada-file
@FILES_APP.route("/<id>/download")
@use_kwargs(DownloadFileRequest(), location="query_path")
@doc(description="Download a file", tags=["files"])
def download_file(**kwargs):
    file = File.get_or_404(kwargs.get("id"))
    tmp_fp = path.get_tempfile(name=file.file_name, ext=file.ext)
    file.s3_download_file(tmp_fp)
    return send_file(
        tmp_fp,
        as_attachment=True,
        attachment_filename=file.attachment_path,
        mimetype=file.mimetype,
    )


# /////////////////////////
# GET /files/{id}/versisons/
# /////////////////////////


class ListFileVersionsRequest(APIRequest, BaseFetchRequest):
    __name__ = "file_version_list_request"
    pass


# TODO: fix this to work with dada-file
@FILES_APP.route("/<id>/versions")
@use_kwargs(ListFileVersionsRequest(), location="query_path")
@doc(
    description="List previous versions of this file on S3. TODO: add filering / restoration to this.",
    tags=["files"],
)
def list_file_versions(**kwargs):
    file = File.get_or_404(kwargs.get("id"))
    return dada_serde.jsonify(
        {"id": file.id, "is_private": file.is_private, "s3_urls": file.s3_urls}
    )
