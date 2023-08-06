from flask import Blueprint

from dada.models.field import Field
from dada.models.tag_join_table import FieldTag
from dada.models.api_response import FieldResponse
from dada.resources.core import crud_blueprint_from_model

# ///////////////
# Fields API
# TODO: set docs dynamically from __doc__ attribute of each ednpoint's assoicated method or some other custom attribute?
# ///////////////
SEARCH_DOCS = """
"""
UPSERT_DOCS = """
"""
FETCH_DOCS = """
"""
DELETE_DOCS = """
"""

FIELDS_APP = crud_blueprint_from_model(
    blueprint=Blueprint("fields", __name__),
    core_model=Field,
    base_response_schema=FieldResponse,
    doc_tags=["fields"],
    relationships=[FieldTag],
    upsert_requires_admin=True,
    delete_requires_admin=True,
    # search_docs=SEARCH_DOCS,
    # upsert_docs=UPSERT_DOCS,
    # fetch_docs=FETCH_DOCS,
    # delete_docs=DELETE_DOCS
)
