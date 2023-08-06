from flask import Blueprint

from dada.models.tag import Tag
from dada.models.tag_join_table import TagTag
from dada.models.api_response import TagResponse
from dada.resources.core import crud_blueprint_from_model

# ///////////////
# Sites API
# ///////////////
SEARCH_DOCS = """
"""
UPSERT_DOCS = """
"""
FETCH_DOCS = """
"""
DELETE_DOCS = """
"""

TAGS_APP = crud_blueprint_from_model(
    blueprint=Blueprint("tags", __name__),
    core_model=Tag,
    base_response_schema=TagResponse,
    doc_tags=["tags"],
    relationships=[TagTag],
    # search_docs=SEARCH_DOCS,
    # upsert_docs=UPSERT_DOCS,
    # fetch_docs=FETCH_DOCS,
    # delete_docs=DELETE_DOCS
)
