from datetime import datetime

from dada_test import BaseTest

from dada_types import Parameters


class ParameterTests(BaseTest):
    def test_params(self):
        """
        Test int <-> text converstion / generation
        """
        p = Parameters({"path": {"type": "path", "info": "A filepath"}})
        kwargs = p.validate(path=self.get_fixture("space-time-motion.mp3"))
        assert kwargs["path"].endswith("space-time-motion.mp3")

    def test_date_param(s):
        """"""
        p = Parameters({"date": {"type": "date_tz", "info": "A Date"}})
        kwargs = p.validate(date="2015-06-07")
        assert isinstance(kwargs["date"], datetime)

    def test_int_param(s):
        """"""
        p = Parameters({"size": {"type": "int", "info": "An integer"}})
        kwargs = p.validate(size="1")
        assert isinstance(kwargs["size"], int)

    def test_num_param(s):
        """"""
        p = Parameters({"size": {"type": "num", "info": "An integer"}})
        kwargs = p.validate(size="1.01")
        assert isinstance(kwargs["size"], float)

    def test_bad_int_param(s):
        """"""
        p = Parameters({"size": {"type": "int", "info": "An integer"}})
        try:
            kwargs = p.validate(size="1a")
        except:
            assert True
        else:
            print(f"Shouldve failed to parse {kwargs}")
            assert False

    def test_fields_param(s):
        """"""
        p = Parameters({"fields": {"type": "fields", "info": "JSON fields"}})
        kwargs1 = p.validate(fields={"foo": "bar"})
        assert kwargs1["fields"]["foo"] == "bar"
        kwargs2 = p.validate(fields='{"foo": "bar"}')
        assert kwargs2["fields"]["foo"] == kwargs1["fields"]["foo"]

    def test_param_good_options(s):
        """"""
        p = Parameters(
            {
                "cat_type": {
                    "type": "text",
                    "info": "Cats",
                    "options": ["tuxedo", "tabby", "the cutest"],
                }
            }
        )
        p.validate(cat_type="tuxedo")
        assert "tuxedo" in p.params["cat_type"].options

    def test_param_bad_options(s):
        """"""
        p = Parameters(
            {
                "cat_type": {
                    "type": "text",
                    "info": "Cats",
                    "options": ["tuxedo", "tabby", "the cutest"],
                }
            }
        )
        try:
            p.validate(cat_type="the fluffiest")
        except:
            assert True
        else:
            print("Should've failed to validate an invalid option")
            assert False

    def test_param_list_good_options(s):
        """"""
        p = Parameters(
            {
                "cat_types": {
                    "type": "text_array",
                    "info": "Cats",
                    "options": ["tuxedo", "tabby", "the cutest"],
                }
            }
        )
        kwargs = p.validate(cat_types="tuxedo")  # should force list
        assert isinstance(kwargs["cat_types"], list)
        assert "tuxedo" in p.params["cat_types"].options

    def test_param_list_bad_options(s):
        """"""
        p = Parameters(
            {
                "cat_types": {
                    "type": "text_array",
                    "info": "Cats",
                    "options": ["tuxedo", "tabby", "the cutest"],
                }
            }
        )
        try:
            p.validate(cat_types="the fluffiest")
        except:
            assert True
        else:
            print("Should've failed to validate an invalid option")
            assert False

    def test_param_list_bad_options(s):
        """"""
        p = Parameters(
            {
                "cat_types": {
                    "type": "text_array",
                    "info": "Cats",
                    "options": ["tuxedo", "tabby", "the cutest"],
                }
            }
        )
        try:
            p.validate(cat_types="the fluffiest")
        except:
            assert True
        else:
            print("Should've failed to validate an invalid option")
            assert False


if __name__ == "__main__":
    unittest.main()
