"""
CRUD Generatation:
 Given a blueprint and a model, introspect the schema and generate a search / crud api,
 optionally adding relationship endpoints.

 This is an ugly hack for now but it works fine and reduces so much
 unnecessary code. this is due to our models all deriving from a single, fully-featured class
 Eventually, we'd like for the API to be automatically generated from the schema, and grow as the
 schema develops, rather than having definititions for each endpoint, but we still have 
 enough edge cases to justify declaring each resource as its own file.
 
 For now this will get us 75 % of the way there.
TODO: abstract out into `dada-api`
"""
import logging
from typing import List, Optional, Any
from marshmallow import Schema
from flask import Blueprint, g, make_response
from flask_apispec import use_kwargs, marshal_with, doc
from webargs.multidictproxy import MultiDictProxy
from webargs.flaskparser import parser

import dada_settings
from dada_utils import etc

from dada_errors import AuthError
from dada.models.base import DBTable
from dada.models.api_request import APIRequest

CORE_LOGGER = logging.getLogger()


@parser.location_loader("query_path")
def load_headers_query(request, schema):
    newdata = request.args.copy()
    newdata.update(request.view_args)
    newdata["api_header"] = request.headers.get(dada_settings.API_KEY_HEADER)
    return MultiDictProxy(newdata, schema)


@parser.location_loader("query_path_json_or_form")
def load_headers_query(request, schema):
    newdata = request.args.copy()
    newdata.update(request.view_args)
    newdata["api_header"] = request.headers.get(dada_settings.API_KEY_HEADER)
    newdata.update(request.form)
    newdata.update(request.json)
    return MultiDictProxy(newdata, schema)


def crud_blueprint_from_model(
    blueprint: Blueprint,
    core_model: DBTable,
    # search req/response
    base_response_schema: Schema,
    # individual method overrides
    search_request_locations: Optional[tuple] = "query_path",
    search_request_schema: Optional[Schema] = None,
    search_response_schema: Optional[Schema] = None,
    search_requires_admin: Optional[bool] = False,
    search_docs: Optional[str] = None,
    # upsert req/response
    upsert_request_locations: Optional[tuple] = "query_path_json_or_form",
    upsert_request_schema: Optional[Schema] = None,
    upsert_response_schema: Optional[Schema] = None,
    upsert_docs: Optional[str] = None,
    upsert_requires_admin: Optional[bool] = False,
    # fetch req/response
    fetch_request_locations: Optional[tuple] = "query_path",
    fetch_request_schema: Optional[Schema] = None,
    fetch_response_schema: Optional[Schema] = None,
    fetch_docs: Optional[str] = None,
    fetch_requires_admin: Optional[bool] = False,
    # delete req/response
    delete_request_locations: Optional[tuple] = "query_path",
    delete_request_schema: Optional[Schema] = None,
    delete_docs: Optional[str] = None,
    delete_requires_admin: Optional[bool] = False,
    # a list of tags to add to the api docs
    doc_tags: List[str] = [],
    # a list of database models to "nest" under the `core_model`
    relationships: List[DBTable] = [],
) -> Blueprint:
    """
    Construct a CRUD blueprint from a model, optionally adding relationship endpoints, documentation, and overrides
    """

    # //////////////////////////
    # Entity Metadata
    # //////////////////////////

    ENTITY_TYPE = core_model.get_entity_type()
    API_ENDPOINT = core_model.api_get_endpoint()
    RESPONSE_EXCLUDES = ["vector"] if core_model.has_vector() else []

    # //////////////////////////
    # GET /{entity}/
    # //////////////////////////

    if not search_request_schema:
        search_request_schema = core_model.api_get_search_schema()

    if not search_response_schema:
        search_response_schema = base_response_schema

    class Meta:
        excludes = RESPONSE_EXCLUDES

    SEARCH_DOCS = (
        search_docs
        or f"Search for ``{API_ENDPOINT}``, filtering by core attributes, fields, tags, and/or relationships"
    )
    SEARCH_TAGS = etc.uniq(doc_tags + ["admin"] if search_requires_admin else [])

    @use_kwargs(
        type(
            f"Search{API_ENDPOINT.title()}Request",
            (APIRequest, search_request_schema),
            {},
        )(),
        location=search_request_locations,
    )
    @marshal_with(
        type(
            f"Search{API_ENDPOINT.title()}Response",
            (search_response_schema,),
            {"Meta": Meta},
        )(many=True)
    )
    @doc(description=SEARCH_DOCS, tags=SEARCH_TAGS)
    def search_entity(**kwargs):
        """"""
        if search_requires_admin:
            if not g.user.admin:
                raise AuthError(f"You must be an admin to search for {API_ENDPOINT}.")
        return core_model.search(**kwargs)

    # add url rule

    blueprint.add_url_rule(
        "/", f"search_{API_ENDPOINT}", search_entity, methods=["GET"]
    )

    # //////////////////////////
    # POST|PUT|PATCH /{entity}/
    # /////////////////////////

    if not upsert_request_schema:
        upsert_request_schema = core_model.api_get_upsert_schema()

    if not upsert_response_schema:
        upsert_response_schema = base_response_schema

    UPSERT_DOCS = upsert_docs or f"Create or update ``{API_ENDPOINT}``."
    UPSERT_TAGS = etc.uniq(doc_tags + ["admin"] if upsert_requires_admin else [])

    @use_kwargs(
        type(
            f"{API_ENDPOINT.title()}UpsertRequest",
            (APIRequest, upsert_request_schema),
            {},
        )(),
        location=upsert_request_locations,
    )
    @marshal_with(
        type(
            f"{API_ENDPOINT.title()}UpsertResponse",
            (upsert_response_schema,),
            {"Meta": Meta},
        )()
    )
    @doc(description=UPSERT_DOCS, tags=UPSERT_TAGS)
    def upsert_entity(**kwargs):
        """"""
        if upsert_requires_admin:
            if not g.user.admin:
                raise AuthError(f"You must be an admin to create {API_ENDPOINT}.")
        if core_model.has_user():
            kwargs["user_id"] = g.user.id
        return core_model.upsert(**kwargs)

    # add url rule

    blueprint.add_url_rule(
        "/", f"upsert_one_{ENTITY_TYPE}", upsert_entity, methods=["POST"],
    )

    # /////////////////////////
    # GET /{entity}/{id}
    # /////////////////////////

    if not fetch_request_schema:
        fetch_request_schema = core_model.api_get_fetch_schema()

    if not fetch_response_schema:
        fetch_response_schema = base_response_schema

    FETCH_DOCS = fetch_docs or f"Fetch metdata about an individual ``{ENTITY_TYPE}``."
    FETCH_TAGS = etc.uniq(doc_tags + ["admin"] if fetch_requires_admin else [])

    @use_kwargs(
        type(
            f"{API_ENDPOINT.title()}FetchRequest",
            (APIRequest, fetch_request_schema),
            {},
        )(),
        location=fetch_request_locations,
    )
    @marshal_with(
        type(
            f"{API_ENDPOINT.title()}FetchResponse",
            (fetch_response_schema,),
            {"Meta": Meta},
        )()
    )
    @doc(description=FETCH_DOCS, tags=FETCH_TAGS)
    def fetch_entity(**kwargs):
        """"""
        if fetch_requires_admin:
            if not g.user.admin:
                raise AuthError(f"You must be an admin to fetch {API_ENDPOINT}.")
        return core_model.get_or_404(kwargs.get("id", None))

    # add url rule

    blueprint.add_url_rule(
        "/<id>", f"fetch_one_{ENTITY_TYPE}", fetch_entity, methods=["GET"]
    )

    # /////////////////////////
    # DELETE /{entity}/{id}
    # /////////////////////////

    if not delete_request_schema:
        delete_request_schema = core_model.api_get_delete_schema()

    DELETE_DOCS = delete_docs or f"Delete an individual ``{ENTITY_TYPE}``."
    DELETE_TAGS = etc.uniq(doc_tags + ["admin"] if delete_requires_admin else [])

    @use_kwargs(
        type(
            f"{API_ENDPOINT.title()}DeleteRequest",
            (APIRequest, delete_request_schema),
            {},
        )(),
        location=delete_request_locations,
    )
    @marshal_with(None, code=204)
    @doc(description=DELETE_DOCS, tags=DELETE_TAGS)
    def delete_entity(**kwargs):
        if delete_requires_admin:
            if not g.user.admin:
                raise AuthError(f"You must be an admin to delete {API_ENDPOINT}.")
        core_model.delete(kwargs.get("id", None))
        return make_response("", 204)

    # add url rule

    blueprint.add_url_rule(
        "/<id>", f"delete_one_{ENTITY_TYPE}", delete_entity, methods=["DELETE"]
    )

    # ////////////////////////////
    # END OF CRUD METHODS
    # ////////////////////////////

    if not len(relationships):
        # return the generated blueprint
        return blueprint

    # /////////////////////////////////
    # --------------------------------/
    # RELATIONSHIP ENDPOINT GENERATION
    # --------------------------------
    # /////////////////////////////////

    for rel_model in relationships:

        # get relationship metadata
        rel_entity_type = rel_model.get_entity_type()
        rel_from_fk = rel_model.get_from_id_foreign_key_column_name()
        rel_to_fk = rel_model.get_to_id_foreign_key_column_name()
        rel_to_entity_type = rel_model.get_to_entity_type()
        rel_to_api_endpoint = rel_model.api_get_to_endpoint()
        rel_is_positional = rel_model.is_positional()
        rel_has_fields = rel_model.has_fields()

        # construct the api endpoint
        rel_api_endpoint = f"/<{rel_from_fk}>/{rel_to_api_endpoint}/<{rel_to_fk}>"

        # append the endpoint to the list of tags
        rel_doc_tags = etc.uniq(doc_tags + [rel_to_entity_type])

        # ///////////////////////////
        # POST/PATCH/PUT /{from_entity}/{from_id}/{to_entity}/{to_id}
        # ///////////////////////////

        UPSERT_REL_DOCS = f"Add a {ENTITY_TYPE} to a {rel_to_entity_type}"

        if rel_is_positional:
            UPSERT_REL_DOCS += ", optionally updating its position"

        if rel_has_fields:
            UPSERT_REL_DOCS += ", and adding relation-specific ``fields``."

        rel_upsert_schema = rel_model.api_get_upsert_schema()
        rel_class_name = f"{API_ENDPOINT.title()}{rel_to_api_endpoint.title()}"

        @use_kwargs(
            type(
                f"{rel_class_name}UpsertRequest", (APIRequest, rel_upsert_schema), {}
            )(),
            location="query_path_json_or_form",
        )
        @marshal_with(
            type(
                f"{rel_class_name}UpsertResponse",
                (fetch_response_schema,),
                {"Meta": Meta},
            )()
        )
        @doc(description=UPSERT_REL_DOCS, tags=rel_doc_tags)
        def upsert_entity_to_rel(**kwargs):
            rel_model_instance = rel_model.upsert(**kwargs)
            core_model_instance = getattr(rel_model_instance, ENTITY_TYPE)
            return core_model_instance

        # add url rule

        blueprint.add_url_rule(
            rel_api_endpoint,
            f"upsert_to_{rel_to_entity_type}",
            upsert_entity_to_rel,
            methods=["POST"],
        )

        # ///////////////////////////
        # DELETE /{from_entity}/{from_id}/{to_entity}/{to_id}
        # ///////////////////////////

        DELETE_REL_DOCS = (
            f"Remove ``{API_ENDPOINT}`` from associated ``{rel_to_api_endpoint}``"
        )
        if rel_is_positional:
            DELETE_REL_DOCS += f", thereby re-setting the position of other ``{API_ENDPOINT}`` in the same ``{rel_to_entity_type}``"
        if rel_has_fields:
            DELETE_REL_DOCS += ", and removing any relation-specific fields."

        rel_delete_request = rel_model.api_get_delete_schema()

        @use_kwargs(
            type(
                f"{rel_class_name}DeleteRequest", (APIRequest, rel_delete_request), {}
            )(),
            location="query_path",
        )
        @marshal_with(
            type(
                f"{rel_class_name}DeleteResponse",
                (fetch_response_schema,),
                {"Meta": Meta},
            )()
        )
        @doc(description=DELETE_REL_DOCS, tags=rel_doc_tags)
        def remove_entity_from_rel(**kwargs):
            rel_model_instance = rel_model.get_or_404(**kwargs)
            rel_model_instance.delete()
            core_model_instance = getattr(rel_model_instance, ENTITY_TYPE)
            return core_model_instance

        # add url rule

        blueprint.add_url_rule(
            rel_api_endpoint,
            f"remove_from_{rel_to_entity_type}",
            remove_entity_from_rel,
            methods=["DELETE"],
        )

    # //////////////////////////////
    # End of Relationship Generation
    # //////////////////////////////
    return blueprint
