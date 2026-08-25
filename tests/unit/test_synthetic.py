import csv
import unittest

from workorder_ai.synthetic import WORK_CODES, generate_workorders, write_workorders_csv


class SyntheticGeneratorTests(unittest.TestCase):
    def test_generator_is_deterministic(self) -> None:
        self.assertEqual(generate_workorders(10, seed=7), generate_workorders(10, seed=7))

    def test_generated_records_follow_contract(self) -> None:
        records = generate_workorders(250, seed=42)

        self.assertEqual(len(records), 250)
        self.assertEqual(len({record.phase_id for record in records}), 250)
        self.assertTrue(all(record.workorder_id.startswith("WO-") for record in records))
        self.assertTrue(all(record.historical_work_code in WORK_CODES for record in records))
        self.assertTrue(all(record.description.strip() for record in records))

    def test_generator_includes_quality_challenges(self) -> None:
        records = generate_workorders(2_000, seed=42)

        self.assertTrue(any(record.asset_id is None for record in records))
        self.assertEqual(len({record.historical_work_code for record in records}), len(WORK_CODES))

    def test_generator_rejects_invalid_row_count(self) -> None:
        with self.assertRaisesRegex(ValueError, "rows must be at least 1"):
            generate_workorders(0)

    def test_csv_writer_preserves_row_count(self) -> None:
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as directory:
            records = generate_workorders(25)
            output = write_workorders_csv(records, f"{directory}/workorders.csv")

            with output.open(encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))

        self.assertEqual(len(rows), 25)
        self.assertTrue(rows[0]["phase_id"].startswith("PH-"))


if __name__ == "__main__":
    unittest.main()
