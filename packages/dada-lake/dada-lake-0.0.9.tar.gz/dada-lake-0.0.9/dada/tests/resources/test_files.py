import unittest

from dada.tests.core import APITest
from dada.models.core import s3conn
from dada.models.field import Field
from dada_types import gen
from dada_utils import path


class FilesResourceTest(APITest):

    # ///////////////////////////
    # Upsert
    # //////////////////////////

    def test_file_upsert(self):
        """
        Test file upsert by id / checksum
        """

        # create a field
        data, response = self.upsert_fixture_file("eril-brinh2.mp3")
        assert (data["file_name"]) == "eril-brinh2"

        # pass in the the check sum to link to previous version
        nu_data, response = self.upsert_fixture_file(
            "eril-brinh2.mp3", check_sum=data["check_sum"]
        )

        # everything should be the same
        assert data["check_sum"] == nu_data["check_sum"]
        assert data["id"] == nu_data["id"]

        newer_data, response = self.upsert_fixture_file(
            "eril-brinh2.mp3", id=data["id"]
        )

        # now pass in the id
        assert nu_data["check_sum"] == newer_data["check_sum"]
        assert nu_data["id"] == newer_data["id"]

        # TODO: redo this
        # we should have only created 1 version on s3:
        # ver_data, response = self.get("/files/{id}/versions".format(**newer_data))
        # cur_version = ver_data.get("s3_urls", {}).get("file", {}).get('version')
        # assert cur_version is not None

        # # but we should have also created a "backup" version
        # prev_versions = ver_data.get("s3_previous_file_versions", [])
        # assert len(prev_versions) == 1
        # prev_version = prev_versions[0]
        # assert cur_version != prev_versions

        # # and these vesions should have the same check sum
        # prev_tmp_fp = s3conn.download(prev_version)
        # cur_tmp_fp = s3conn.download(cur_version)

        # prev_check_sum = path.get_check_sum(prev_tmp_fp)
        # cur_check_sum = path.get_check_sum(cur_tmp_fp)

        # assert prev_check_sum == cur_check_sum

        # # and it should be the same as the original check sum
        # assert cur_check_sum == data["check_sum"]

    def test_file_bundle(self):
        #  create a "bundle" file
        data, response = self.upsert_fixture_file("Archive.zip")
        assert data["file_type"] == "bundle"


if __name__ == "__main__":
    unittest.main()
