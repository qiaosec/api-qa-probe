import json
import tempfile
import unittest
from pathlib import Path

from src.api_qa_probe.cli import execute
from src.api_qa_probe.loader import load_cases
from src.api_qa_probe.runner import evaluate_case, run_cases, to_markdown_report


ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "sample_data" / "api_cases.json"


class ApiQaProbeTests(unittest.TestCase):
    def test_load_cases(self):
        cases = load_cases(SAMPLE)
        self.assertEqual(len(cases), 5)
        self.assertEqual(cases[0]["case_id"], "API-001")

    def test_evaluate_case_detects_failures(self):
        cases = load_cases(SAMPLE)
        failing = evaluate_case(cases[3])
        self.assertFalse(failing["passed"])
        self.assertTrue(any("expected status" in item for item in failing["failures"]))

    def test_run_cases_summary(self):
        report = run_cases(str(SAMPLE))
        self.assertEqual(report["summary"]["total_cases"], 5)
        self.assertEqual(report["summary"]["failed"], 2)

    def test_markdown_report_contains_sections(self):
        report = run_cases(str(SAMPLE))
        markdown = to_markdown_report(report)
        self.assertIn("## Summary", markdown)
        self.assertIn("## Failing Cases", markdown)

    def test_cli_json_output(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "report.json"
            rendered = execute(str(SAMPLE), "json", str(output_path))
            payload = json.loads(rendered)
            self.assertEqual(payload["summary"]["total_cases"], 5)
            self.assertTrue(output_path.exists())


if __name__ == "__main__":
    unittest.main()
