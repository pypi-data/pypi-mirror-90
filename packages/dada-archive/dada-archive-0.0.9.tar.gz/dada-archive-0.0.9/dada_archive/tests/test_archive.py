import os
import logging
import unittest
from datetime import datetime

from dada_test import BaseTest
import dada_settings
import dada_archive

TEST_LOGGER = logging.getLogger()


class ArchiveTests(BaseTest):
    def test_archive_extraction(self):
        files = dada_archive.extract_all(self.get_fixture("Archive.zip"))
        assert set([f.split("/")[-1] for f in files]) == set(["file1.txt", "file2.txt"])


if __name__ == "__main__":
    unittest.main()
