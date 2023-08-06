"""
Base Classes From Which All Other Models Inherit From
"""

from marshmallow import fields, Schema

import dada_settings
from dada_types import T


# ///////////
# Api Request Schema Generation / Docs
# TODO: Should this be in typeS?
# /////////////

# Comon Search Fields
ID_FIELD_PARAM = "i"
IdListField = fields.List(
    T.id.val,
    missing=[],
    description="""A list of entitiy identifiers to filter for. Eg: i=1&i=2""",
)

USER_ID_FIELD_PARAM = "u"

BUNDLE_ID_FIELD_PARAM = "b"
BundleIdListField = fields.List(
    T.bundle_id.val,
    missing=[],
    description="""A list of file id's representing bundles, the contents of which to return. to filter for. Eg: b=1&b=2""",
)


# filter on list of file ids
SLUG_FIELD_PARAM = "s"
SlugListField = fields.List(
    T.slug.val,
    missing=[],
    description="""A list of slug (`s`) identifiers to inclusively filter for. Eg: s=foo&s=bar""",
)


# filter on list of file ids
NAME_FIELD_PARAM = "n"
NameListField = fields.List(
    T.name.val,
    missing=[],
    description="""A list of name identifiers to inclusively filter for. Eg: n=foo&n=bar""",
)

FILTER_FIELD_PARAM = "f"
FilterField = fields.List(
    T.filter.val,
    missing=[],
    error_messages={"type": " filter ('f') must be a string."},
    description="""A dada-lake-specific syntax for filtering by file and field values.
    Each `filter` string consists of three elements, the `field_name`, the `operator`, and the `value.
    These three elements are seprated by the `:` character. 
    For instance, to find all Artists whose name is _exactly_ "Brian", pass in:
        f=artist:eq:Brian
    To apply a regular expression to the artist field pass in:
        f=artist:re:^Brian.*
    You can combine filters together, as well
        f=artist:eq:Brian&f=bpm:gte:120&f=bpm:lte:130
    To control the behavior of multiple filters, use the `fx` parameter:
        f=artist:eq:Brian&f=bpm:gte:120&f=bpm:lte:130&fx=and
    By default, the value of `fx` is `and`.
    You can access a list of fields by making the following request:
        GET /fields/
    """,
)

FILTER_COMBINE_FIELD_PARAM = "fx"
FilterCombineField = fields.Str(
    missing="and",
    error_messages={"type": "Filter string combine function ('fx') must be a string."},
    description="""The logic for combining `filter` parameters, either **`or`** or **`and`**""",
)

# full text search
SEARCH_FIELD_PARAM = "q"
SearchField = fields.List(
    fields.Str,
    missing=[],
    error_messages={"type": " search query ('q') must be a string."},
    description="""A list of postgresql _websearch_ syntax queries to search for. Eg: q=brian AND karen
    See the [Postgresql docs](https://www.postgresql.org/docs/11/textsearch-controls.html) for more details.
    **NOTE**: By default, this will search against all `searchable` **Fields**.
    You can also search against individual Fields using the `filter` parameter and the `lk` operator, Eg:
    f=artist:lk:brian%
    """,
)

SEARCH_COMBINE_FIELD_PARAM = "qx"
SearchCombineField = fields.Str(
    missing="and",
    error_messages={"type": "Search query combine function ('qx') must be a string."},
    description="""The logic for combining `q` parameters, either **`or`** or **`and`**""",
)

# minus prefix to define asc or desc, can accept multiple args
ORDER_FIELD_PARAM = "o"
OrderField = fields.List(
    T.sort.val,
    missing=[],
    error_messages={"type": "The order ('o') must be a string"},
    description="""A list of Core Entity properties or **Fields** to _order_ by. Eg:
    o=bpm                        # bpm ascending
    o=-artist                    # Artist name descending
    o=-artist&o=-bpm&o=id  # Artist name descending + Bpm descending + id asc
    """,
)

# pagination
PAGE_FIELD_PARAM = "p"
PageField = fields.Int(
    missing=1,
    description="""`p`: The page number of the of entity result set to iterate through""",
)
PER_PAGE_FIELD_PARAM = "pp"
PerPageField = fields.Int(
    missing=dada_settings.FILE_SEARCH_RESULTS_PER_PAGE,
    description="""(`pp`: The number of entities to include in each reseponse.""",
)

FILE_CONTENTS_PARAM = "file"
FileContentsField = fields.Field(
    missing=None, location="files", description=f"""The **File**'s contents.,"""
)

RelCombineField = fields.Str(
    description="""The logic for filtering based on relationships. ``any`` will return entities that have relations to any of the included id/slugs. ``all`` will return entities that have relations to all of the included id/slugs""",
    missing="any",
    error_messages={
        "type": "Relationship combine function ('{entity}x') must be a string."
    },
)
