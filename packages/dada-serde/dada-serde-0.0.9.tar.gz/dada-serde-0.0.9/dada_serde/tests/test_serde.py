import os
import logging
import unittest
from datetime import datetime


import dada_settings
from dada_test import BaseTest

import dada_serde


TEST_LOGGER = logging.getLogger()


class SerDeTests(BaseTest):

    # //////////////
    # serde
    # /////////////

    def test_serde_obj_from_json(self):
        """
        Since we use obj_from_json to also validate json objects
        it should accept dictionaries and lists as inputs and simple pass them through
        """
        o1 = dada_serde.json_to_obj(["foo", "bar"])
        o2 = dada_serde.json_to_obj('["foo","bar"]')
        assert o1 == o2

    def test_serde_obj_from_json_invalid_json(self):
        try:
            dada_serde.json_to_obj("['foo']")
        except:
            assert True
        else:
            assert False


if __name__ == "__main__":
    unittest.main()
