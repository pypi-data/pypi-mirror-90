from flask import Blueprint

from dada.models.desktop import Desktop
from dada.models.tag_join_table import DesktopTag
from dada.models.api_response import DesktopResponse
from dada.resources.core import crud_blueprint_from_model

# ///////////////
# Desktops API
# ///////////////
SEARCH_DOCS = """
"""
UPSERT_DOCS = """
"""
FETCH_DOCS = """
"""
DELETE_DOCS = """
"""

DESKTOPS_APP = crud_blueprint_from_model(
    blueprint=Blueprint("desktops", __name__),
    core_model=Desktop,
    base_response_schema=DesktopResponse,
    doc_tags=["desktops"],
    relationships=[DesktopTag],
    # search_docs=SEARCH_DOCS,
    # upsert_docs=UPSERT_DOCS,
    # fetch_docs=FETCH_DOCS,
    # delete_docs=DELETE_DOCS
)
