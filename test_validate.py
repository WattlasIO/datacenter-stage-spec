import json
import unittest
from pathlib import Path

import validate


class TestStageSpecValidator(unittest.TestCase):
    def test_example_record_passes(self) -> None:
        sample = Path(__file__).with_name("examples") / "valid-permitted-campus.json"
        rec = json.loads(sample.read_text(encoding="utf-8"))
        self.assertEqual(validate.validate_record(rec), [])

    def test_press_release_cannot_prove_construction(self) -> None:
        bad = {
            "project_name": "Press Release Only Campus",
            "state": "VA",
            "stage": "under_construction",
            "observed_date": "2026-11-24",
            "evidence": [
                {
                    "record_type": "press_release",
                    "url": "https://example.com/news/campus",
                    "filed_date": "2026-11-01",
                    "summary": "Company announced a planned campus in a press release.",
                }
            ],
        }
        errs = validate.validate_record(bad)
        self.assertTrue(any("not supported by evidence" in e for e in errs))

    def test_capacity_basis_enforced(self) -> None:
        bad = {
            "project_name": "Undisclosed MW Conflict",
            "state": "OH",
            "stage": "announced",
            "capacity": {"mw": 250, "basis": "undisclosed"},
            "observed_date": "2026-11-24",
            "evidence": [
                {
                    "record_type": "press_release",
                    "url": "https://example.com/ohio-campus",
                    "filed_date": "2026-10-01",
                    "summary": "Initial public announcement.",
                }
            ],
        }
        errs = validate.validate_record(bad)
        self.assertTrue(any("must be null" in e for e in errs))


if __name__ == "__main__":
    unittest.main()
