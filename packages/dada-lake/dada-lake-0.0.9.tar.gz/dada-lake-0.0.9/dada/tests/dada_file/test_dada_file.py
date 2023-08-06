import time
from datetime import datetime

import dada_file
from dada_utils import path
from dada.tests.core import S3Test
from dada.models.core import s3conn

# TODO: copy these to dada-file


class DadaFileTests(S3Test):
    def test_load_local_external(self):

        url = self.get_fixture("Archive.zip")
        df = dada_file.load(url)
        # test file writing.
        df.save_locally()

        # test for metadata existence
        assert df.db.id is None
        assert df.db.check_sum == "1641279865bcaafea6c14604edb896e9"
        assert df.db.file_type == "bundle"
        assert df.db.file_subtype == "raw"
        assert df.db.ext == "zip"
        assert df.db.size == 926
        assert df.db.mimetype == "application/zip"
        assert isinstance(df.db.created_at, datetime)
        assert isinstance(df.db.updated_at, datetime)
        assert df.urls.input.file.latest == url

        # test for file existence
        assert path.exists(df.urls.loc.file.latest)
        assert path.exists(df.urls.loc.file.version)
        assert path.get_check_sum(df.urls.loc.file.latest) == path.get_check_sum(
            df.urls.input.file.latest
        )

    def test_partition_url(self):
        url = "s3://abelsonlive/dada/e=file/t=audio/s=track/x=mp3/y=20/m=5/d=22/h=10/i=1/v=dklfkasdflkdsajfalsdf-20052210/Screen Shot 2020-05-19 at 9.10.58 AM.png"
        df = dada_file.load(url)
        assert df.is_part_url
        assert df.db["entity_type"] == "file"
        assert df.db["file_type"] == "audio"
        assert df.db["file_subtype"] == "track"
        assert df.db["ext"] == "png"
        assert df.db["created_year2"] == 20
        assert df.db["check_sum"] == "dklfkasdflkdsajfalsdf"
        assert df.db["version"] == "dklfkasdflkdsajfalsdf-20052210"
        assert df.db["updated_at"] == datetime(2020, 5, 22, 10, 0)
        assert df.db["created_at"] == datetime(2020, 5, 22, 10, 0)
        assert df.db["id"] == 1

    def test_save_s3_ext_file_locally(self):
        url = "s3://abelsonlive/dada/e=file/t=audio/s=track/x=mp3/y=20/m=5/d=22/h=10/i=1/v=dklfkasdflkdsajfalsdf-20052210/Screen Shot 2020-05-19 at 9.10.58 AM.png"
        df = dada_file.load(url)
        df.save_locally()
        assert path.exists(df.urls.loc.file.latest)
        assert path.exists(df.urls.loc.file.version)
        assert path.exists(df.urls.loc.dada.latest)
        assert path.exists(df.urls.loc.dada.version)

    def test_save_s3_ext_file_globally(self):
        url = "s3://abelsonlive/dada/e=file/t=audio/s=track/x=mp3/y=20/m=5/d=22/h=10/i=1/v=dklfkasdflkdsajfalsdf-20052210/Screen Shot 2020-05-19 at 9.10.58 AM.png"
        df = dada_file.load(url)
        df.save_locally()
        df.serve_globally()
        assert s3conn.exists(df.urls.glob.file.latest)
        assert s3conn.exists(df.urls.glob.file.version)
        assert s3conn.exists(df.urls.glob.dada.latest)
        assert s3conn.exists(df.urls.glob.dada.version)

    def test_bundle_extraction(self):
        url = self.get_fixture("Archive.zip")
        df = dada_file.load(url)
        df.save_locally()
        assert len(df.local_bundle_urls) == 2
        assert path.exists(df.dirs.local_bundle.latest + "file1.txt")
        assert path.exists(df.dirs.local_bundle.latest + "file2.txt")
        df.serve_globally()
        assert len(df.s3_bundle_urls) == 2
        assert s3conn.exists(df.dirs.s3_bundle.latest + "file1.txt")
        assert s3conn.exists(df.dirs.s3_bundle.latest + "file2.txt")
        assert len(df.db.fields["bundle_contents"]) == 2
        assert set(df.db.fields["bundle_contents"]) == set(["file1.txt", "file2.txt"])

    def test_local_mp3_extraction(self):
        url = self.get_fixture("eril-brinh2.mp3")
        df = dada_file.load(url)
        df.ensure_dada(url)
        assert df.db.ext == "mp3"
        assert df.db.file_type == "audio"
        df.save_locally()
        assert df.db.ext == "mp3"
        assert df.db.file_type == "audio"
        df.serve_globally()
        assert df.db.ext == "mp3"
        assert df.db.file_type == "audio"
