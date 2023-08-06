import logging

from dada_test import BaseTest
import dada_settings

import dada_text

TEST_LOGGER = logging.getLogger()


class TextTests(BaseTest):
    def test_text_to_list(self):
        assert dada_text.to_list("1,2") == ["1", "2"]
        assert dada_text.to_list("1+2") == ["1", "2"]
        assert dada_text.to_list("[1,2]") == [1, 2]  # json
        assert dada_text.to_list("(1,2)") == ["1", "2"]

    def test_text_to_bool(self):
        assert dada_text.to_bool("y")
        assert dada_text.to_bool("yes")
        assert dada_text.to_bool("TRUE")
        assert dada_text.to_bool("1")
        assert dada_text.to_bool("t")
        assert not dada_text.to_bool("n")
        assert not dada_text.to_bool("f")
        assert not dada_text.to_bool("0")
        assert not dada_text.to_bool("FALSE")
        assert dada_text.to_bool("none") is None

    def test_text_is_null(self):
        assert dada_text.is_null("na")
        assert dada_text.is_null("NA")
        assert dada_text.is_null("<na>")
        assert dada_text.is_null("NaN")
        assert dada_text.is_null("null")
        assert dada_text.is_null("NONE")
        assert dada_text.is_null("-")
        assert not dada_text.is_null("okay")
        assert dada_text.is_null(None)

    def test_text_is_int(self):
        assert dada_text.is_int("1")
        assert dada_text.is_int("12345")
        assert not dada_text.is_int("1234.56")
        assert not dada_text.is_int("NaN")

    def test_text_is_not_int(self):
        assert dada_text.is_not_int("absdfa")
        assert dada_text.is_not_int("1dasf45")
        assert not dada_text.is_not_int("1234")
        assert not dada_text.is_not_int("1")


if __name__ == "__main__":
    unittest.main()
