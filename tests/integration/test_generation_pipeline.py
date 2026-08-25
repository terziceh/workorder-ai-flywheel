import csv
import unittest
from tempfile import TemporaryDirectory

from workorder_ai.synthetic import generate_workorders, write_workorders_csv


class GenerationPipelineTests(unittest.TestCase):
    def test_generation_pipeline_creates_contract_columns(self) -> None:
        with TemporaryDirectory() as directory:
            output = write_workorders_csv(generate_workorders(100), f"{directory}/batch.csv")

            with output.open(encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                rows = list(reader)

        self.assertEqual(
            reader.fieldnames,
            [
                "workorder_id",
                "phase_id",
                "created_at",
                "facility_name",
                "location_code",
                "asset_id",
                "asset_type",
                "craft",
                "priority",
                "description",
                "historical_work_code",
                "source_batch",
            ],
        )
        self.assertEqual(len(rows), 100)


if __name__ == "__main__":
    unittest.main()
