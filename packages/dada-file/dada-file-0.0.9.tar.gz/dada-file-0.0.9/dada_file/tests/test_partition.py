import logging
import unittest

from dada_test import BaseTest
from dada_utils import dates
import dada_settings

from dada_file.partition import *


TEST_LOGGER = logging.getLogger()


class PartitionTests(BaseTest):
    def test_to_glob(self):
        url = to_glob(created_year2="20", ext="md")
        self.assertTrue(is_partition_url("/" + url))
        self.assertTrue("y=20" in url)
        self.assertTrue("x=md" in url)
        self.assertTrue(url.endswith("md"))

    def test_to_glob_date(self):
        now = dates.now()
        url = to_glob(created_at=now, updated_at=now)
        self.assertTrue(f"y={str(now.year)[2:]}" in url)
        self.assertTrue(now.strftime(VERSION_DATE_FORMAT) in url)

    def test_to_glob_latest(self):
        now = dates.now()
        url = to_glob(latest=True)
        self.assertTrue(f"/v=latest/" in url)


if __name__ == "__main__":
    unittest.main()
