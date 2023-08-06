import unittest

from dada.tests.core import APITest

from dada.models.field import Field
from dada_types import gen


class FieldsResourceTest(APITest):

    # ///////////////////////////
    # Search
    # //////////////////////////

    def test_api_search_by_websearch(self):
        """
        Test search by websearch query.
        """
        # create a field
        data, response = self.post(
            f"/fields/",
            data={
                "name": "searchable",
                "type": "text",
                "default": "baz",
                "is_required": False,
                "accepts_entity_types": ["file"],
                "accepts_file_types": ["image"],
                "accepts_file_subtypes": ["loop"],
            },
        )

        query_string = {"q": "searchable"}
        new_data, response = self.get("/fields/", query_string=query_string)
        assert data["id"] in [r["id"] for r in new_data]

    def test_api_search_by_one_id(self):
        """
        Test searching fields by a single Id
        """
        query_string = {"i": 1}
        data, response = self.get("/fields/", query_string=query_string)
        if not len(data) == 1:
            print(f"ERROR: got {len(data)} fields. Should have gotten 1")
            assert len(data[0]) > 1
        assert data[0]["id"] == 1

    def test_api_search_by_two_id(self):
        """
        Test searching fields by a list of ID
        """
        query_string = {"i": [1, 2]}
        data, response = self.get("/fields/", query_string=query_string)
        if not len(data) == 2:
            print(f"ERROR: got {len(data)} fields. Should have gotten 2")
            assert len(data[0]) > 2
        assert set([r["id"] for r in data]) == set([1, 2])

    def test_api_search_by_two_id_multiple_params(self):
        """
        Test searching fields by a multiple id params (should not work)
        """
        query_string = {"i": 1, "i": 2}
        data, response = self.get("/fields/", query_string=query_string)
        if not len(data) == 1:
            print(f"ERROR: got {len(data)} fields. Should have gotten 1")
            assert len(data[0]) != 2
        assert data[0]["id"] in [1, 2]

    def test_api_search_by_one_slug(self):
        """
        Test searching fields by a single slug
        """
        og_qs = {"i": 1}
        og_data, response = self.get("/fields/", query_string=og_qs)
        slug_qs = {"s": og_data[0]["slug"]}
        nu_data, response = self.get("/fields/", query_string=slug_qs)
        if not len(nu_data) == 1:
            print(f"ERROR: got {len(data)} fields. Should have gotten 1")
            assert len(data[0]) != 1
        assert nu_data[0]["id"] == 1

    def test_api_search_by_two_slugs(self):
        """
        Test searching fields by a list of slugs
        """
        og_qs = {"i": [1, 2]}
        og_data, response = self.get("/fields/", query_string=og_qs)
        slug_qs = {"s": [r["slug"] for r in og_data]}
        nu_data, response = self.get("/fields/", query_string=slug_qs)
        if not len(nu_data) == 2:
            print(f"ERROR: got {len(data)} fields. Should have gotten 2")
            assert len(data[0]) != 2
        assert set([r["id"] for r in nu_data]) == set([1, 2])

    def test_api_search_by_two_names(self):
        """
        Test searching fields by a list of slugs
        """
        og_qs = {"i": [3, 4]}
        og_data, response = self.get("/fields/", query_string=og_qs)
        slug_qs = {"n": [r["name"] for r in og_data]}
        nu_data, response = self.get("/fields/", query_string=slug_qs)
        if not len(nu_data) == 2:
            print(f"ERROR: got {len(nu_data)} fields. Should have gotten 2")
            assert len(og_data[0]) != 2
        assert set([r["id"] for r in nu_data]) == set([3, 4])

    def test_api_search_by_sw_filter_string(self):
        """
        Test searching fields by a list of slugs
        """
        og_qs = {"f": "name:->:id3_"}
        og_data, response = self.get("/fields/", query_string=og_qs)
        for record in og_data:
            assert record["name"].startswith("id3_")

    def test_api_search_by_ew_filter_string(self):
        """
        Test searching fields by a list of slugs
        """
        og_qs = {"f": "name:<-:bpm"}
        og_data, response = self.get("/fields/", query_string=og_qs)
        for record in og_data:
            assert record["name"].endswith("bpm")

    def test_api_search_by_gt_filter_string(self):
        """
        Test searching fields by a list of slugs
        """
        og_qs = {"f": "name:gt:id3_track_title"}
        og_data, response = self.get("/fields/", query_string=og_qs)
        for record in og_data:
            print(record["name"])
            assert "id3_track_title" not in record["name"]

    def test_api_get_field(self):
        """
        Test fetching a single field
        """
        data, response = self.get("/fields/1")
        assert data["id"] == 1
        slug = data.get("slug")
        data, response = self.get(f"/fields/{slug}")
        assert data["id"] == 1

    # ///////////////////////////
    #  Search Boolean Fields
    # //////////////////////////

    def test_api_search_by_eq_filter_string(self):
        """
        Test searching fields by a list of slugs
        """
        og_qs = {"f": "is_searchable:eq:true"}
        og_data, response = self.get("/fields/", query_string=og_qs)
        for record in og_data:
            assert record["is_searchable"]

    def test_api_search_by_neq_filter_string(self):
        """
        Test searching fields by a list of slugs
        """
        og_qs = {"f": "is_searchable:neq:true"}
        og_data, response = self.get("/fields/", query_string=og_qs)
        for record in og_data:
            assert not record["is_searchable"]

    def test_api_search_by_neq_filter_yes(self):
        """
        Test searching fields by a list of slugs
        """
        og_qs = {"f": "is_searchable:neq:yes"}
        og_data, response = self.get("/fields/", query_string=og_qs)
        for record in og_data:
            assert not record["is_searchable"]

    def test_api_search_by_neq_filter_no(self):
        """
        Test searching fields by a list of slugs
        """
        og_qs = {"f": "is_searchable:neq:no"}
        og_data, response = self.get("/fields/", query_string=og_qs)
        for record in og_data:
            assert record["is_searchable"]

    # ///////////////////////////
    #  Test Date Filtering
    # //////////////////////////

    def test_api_search_by_date_filter_year(self):
        """
        Test searching fields by a list of slugs
        """
        og_qs = {"f": "created_at:gt:2020"}
        og_data, response = self.get("/fields/", query_string=og_qs)
        for record in og_data:
            assert record["created_at"] >= "2020"

    def test_api_search_by_date_filter_mdy(self):
        """
        Test searching fields by a list of slugs
        """
        og_qs = {"f": "created_at:gt:Jan 1, 2020"}
        og_data, response = self.get("/fields/", query_string=og_qs)
        for record in og_data:
            assert record["created_at"] >= "2020"

    def test_api_search_by_date_filter_ymd(self):
        """
        Test searching fields by a list of slugs
        """
        og_qs = {"f": "created_at:gt:2020-01-01"}
        og_data, response = self.get("/fields/", query_string=og_qs)
        for record in og_data:
            assert record["created_at"] >= "2020"

    def test_api_search_by_date_filter_no_results(self):
        """
        Test searching fields by a list of slugs
        """
        og_qs = {"f": "created_at:lt:2020-01-01"}
        og_data, response = self.get("/fields/", query_string=og_qs)
        assert (len(og_data)) == 0

    def test_api_search_by_date_filter_bt(self):
        """
        Test searching fields by a list of slugs
        """
        og_qs = {"f": "created_at:bt:2020-05-01,2021-01-01"}
        og_data, response = self.get("/fields/", query_string=og_qs)
        for record in og_data:
            assert record["created_at"] >= "2020-05-01"
            assert record["created_at"] <= "2021-01-01"

    # ///////////////////////////
    #  Test ARRAY Filtering
    # //////////////////////////

    def test_api_search_by_array_eq_filter(self):
        """
        Test searching fields by a list of slugs
        """
        og_qs = {"f": "accepts_entity_types:==:file"}
        og_data, response = self.get("/fields/", query_string=og_qs)
        for record in og_data:
            assert record["accepts_entity_types"] == ["file"]

    def test_api_search_by_array_neq_filter(self):
        """
        Test searching fields by a list of slugs
        """
        og_qs = {"f": "accepts_entity_types:!=:file"}
        og_data, response = self.get("/fields/", query_string=og_qs)
        for record in og_data:
            assert record["accepts_entity_types"] != ["file"]

    def test_api_search_by_array_gt_filter(self):
        """
        Test searching fields by a list of slugs
        """
        og_qs = {"f": "accepts_entity_types:gt:file"}
        og_data, response = self.get("/fields/", query_string=og_qs)
        for record in og_data:
            assert record["accepts_entity_types"] != ["file"]

    def test_api_search_by_array_gte_filter(self):
        """
        Test searching fields by a list of slugs
        """
        og_qs = {"f": "accepts_entity_types:gte:file"}
        og_data, response = self.get("/fields/", query_string=og_qs)
        assert any(r["accepts_entity_types"] == ["file"] for r in og_data)

    def test_api_search_by_array_in_filter(self):
        """
        Test searching fields by a list of slugs
        """
        og_qs = {"f": "accepts_entity_types:in:file,folder"}
        og_data, response = self.get("/fields/", query_string=og_qs)
        for record in og_data:
            assert (
                "folder" in record["accepts_entity_types"]
                or "file" in record["accepts_entity_types"]
            )

    def test_api_search_by_array_lk_filter(self):
        """
        Test searching fields by a list of slugs
        """
        og_qs = {"f": r"accepts_entity_types:lk:%fi%"}
        og_data, response = self.get("/fields/", query_string=og_qs)
        for record in og_data:
            assert "file" in record["accepts_entity_types"]

    # ///////////////////////////
    #  Test ordering
    # //////////////////////////

    def test_api_search_order_by_id_desc(self):
        """
        Test ordering by id / filtering per page
        """
        og_qs = {"o": "-id", "pp": 2}
        og_data, response = self.get("/fields/", query_string=og_qs)
        assert len(og_data) == 2
        assert og_data[0]["id"] > og_data[1]["id"]

    def test_api_search_order_by_id_asc(self):
        """
        Test ordering by id / filtering per page
        """
        og_qs = {"o": "id", "pp": 2}
        og_data, response = self.get("/fields/", query_string=og_qs)
        assert len(og_data) == 2
        assert og_data[0]["id"] < og_data[1]["id"]

    # ///////////////////////////
    # Upsert
    # //////////////////////////

    def test_api_upsert_field(self):
        """
        Test upserting a field
        """
        data, response = self.post(
            f"/fields/",
            data={
                "name": "foo_bar",
                "type": "text",
                "default": "baz",
                "is_required": False,
                "accepts_entity_types": ["file"],
                "accepts_file_types": ["image"],
                "accepts_file_subtypes": ["loop"],
            },
        )

        assert data.get("name") == "foo_bar"
        new_data, response = self.get(f"/fields/{data['slug']}")
        assert new_data["id"] == data["id"]

        # test updating field via partial attributes
        new_data, response = self.post(
            "/fields/",
            data={
                "id": data["id"],
                "is_required": True,
                "accepts_entity_types": ["file", "folder"],
            },
        )

        assert new_data["is_required"]
        assert "folder" in new_data["accepts_entity_types"]
        assert data["id"] == new_data["id"]
        assert data["updated_at"] < new_data["updated_at"]


if __name__ == "__main__":
    unittest.main()
