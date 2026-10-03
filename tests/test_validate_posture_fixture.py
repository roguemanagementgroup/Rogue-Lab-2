import copy
import json
import unittest
from pathlib import Path

from scripts.validate_posture_fixture import validate_fixture


class ValidatePostureFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture_path = Path(__file__).parents[1] / "fixtures" / "windows-posture.synthetic.json"
        cls.fixture = json.loads(fixture_path.read_text(encoding="utf-8"))

    def test_synthetic_fixture_is_valid(self):
        validate_fixture(self.fixture)

    def test_rejects_non_synthetic_asset_reference(self):
        invalid_fixture = copy.deepcopy(self.fixture)
        invalid_fixture["asset_reference"] = "unapproved-endpoint"

        with self.assertRaisesRegex(ValueError, "synthetic opaque reference"):
            validate_fixture(invalid_fixture)

    def test_rejects_unapproved_field(self):
        invalid_fixture = copy.deepcopy(self.fixture)
        invalid_fixture["device_name"] = "not-permitted"

        with self.assertRaisesRegex(ValueError, "root keys"):
            validate_fixture(invalid_fixture)


if __name__ == "__main__":
    unittest.main()
