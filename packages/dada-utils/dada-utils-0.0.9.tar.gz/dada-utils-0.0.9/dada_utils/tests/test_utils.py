import os
import unittest
from datetime import datetime

from dada_test import BaseTest

from dada_utils import dates, path
import dada_settings


class UtilTests(BaseTest):

    # //////////////
    # dates
    # /////////////

    def test_dates_is_field_date(self):
        assert dates.is_field_date("created_at")
        assert dates.is_field_date("release_date")
        assert dates.is_field_date("created_datetime")
        assert dates.is_field_date("created")
        files = archive.extract_all(self.get_fixture("Archive.zip"))
        assert set([f.split("/")[-1] for f in files]) == set(["file1.txt", "file2.txt"])

    # //////////////
    # path
    # /////////////

    def test_path_check_sum(self):
        FP = self.get_fixture("eril-brinh2.mp3")
        assert path.get_check_sum(FP) == path.exec(f"md5 -q {FP}").stdout.strip()

    def test_path_get_location(self):
        assert path.get_location("s3://foo/bar") == "s3_ext"
        assert path.get_location(f"s3://{settings.S3_BUCKET}/bar") == "s3_int"
        assert path.get_location(f"/Users/folders") == "loc_ext"
        assert path.get_location(f"{settings.LOCAL_DIR}/foo/bar") == "loc_int"
        assert path.get_location(f"foo/bar") == "loc_rel"
        assert path.get_location(f"https://web.com") == "web"
        assert path.get_location(f"web.com/file.txt") == "web"

    def test_path_get_created_at(self):
        assert isinstance(
            path.get_updated_at(self.get_fixture("Archive.zip")), datetime
        )

    def test_path_get_updated_at(self):
        assert isinstance(
            path.get_updated_at(self.get_fixture("Archive.zip")), datetime
        )

    def test_get_ext_and_mimetype(self):
        assert path.get_ext_and_mimetype(self.get_fixture("space-time-motion.mp3")) == (
            "mp3",
            "audio/mpeg",
        )
        assert path.get_ext_and_mimetype(self.get_fixture("Archive.zip")) == (
            "zip",
            "application/zip",
        )

    def test_get_ext_with_gz(self):
        assert path.get_ext("file.json.gz") == "json.gz"
        assert path.get_ext("file.mp3.gz") == "mp3.gz"
        assert path.get_ext("file.gz") == "gz"

    def test_get_gzipped_ungzipped_names(self):
        assert path.get_gzipped_name("file.mp3") == "file.mp3.gz"
        assert path.get_gzipped_name("file.mp3.gz") == "file.mp3.gz"
        assert path.get_ungzipped_name("FilE.mp3.GZ") == "FilE.mp3"
        assert path.get_ungzipped_name("the.gzip.file.mp3.gz") == "the.gzip.file.mp3"

    def test_path_get_name_removes_gz(self):
        assert path.get_name("file.json.gz") == "file"
        assert path.get_name("file.json") == "file"
        assert path.get_name("json.file.json.gz") == "json.file"


if __name__ == "__main__":
    unittest.main()
