import os
from dada_test import BaseTest

import dada_settings
from dada_utils import path

import dada_http


class UtilTests(BaseTest):
    def test_http_download_file(self):
        local_path = dada_http.download_file("http://example.com/")
        self.assertTrue(path.exists(local_path))
        path.remove(local_path)

    def test_http_download_file(self):
        self.assertTrue(dada_http.exists("http://example.com/"))


if __name__ == "__main__":
    unittest.main()
