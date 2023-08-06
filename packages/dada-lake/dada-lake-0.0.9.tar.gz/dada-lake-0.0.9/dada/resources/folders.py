from flask import Blueprint

from dada.models.folder import Folder
from dada.models.folder_desktop import FolderDesktop
from dada.models.tag_join_table import FolderTag
from dada.models.api_response import FolderResponse
from dada.resources.core import crud_blueprint_from_model

# ///////////////
# Base CRUD Folders API
# ///////////////
SEARCH_DOCS = """
"""
UPSERT_DOCS = """
"""
FETCH_DOCS = """
"""
DELETE_DOCS = """
"""

FOLDERS_APP = crud_blueprint_from_model(
    blueprint=Blueprint("folders", __name__),
    core_model=Folder,
    base_response_schema=FolderResponse,
    relationships=[FolderDesktop, FolderTag],
    # search_docs=SEARCH_FOLDER_DOCS,
    # upsert_docs=UPSERT_FOLDER_DOCS,
    # fetch_docs=FETCH_FOLDER_DOCS,
    # delete_docs=DELETE_FOLDER_DOCS
)
