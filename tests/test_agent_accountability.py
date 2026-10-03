import json
import unittest
from pathlib import Path

from tools.agent_accountability import (
    AIU_PER_NANO,
    aggregate,
    cache_reuse_ratio,
    find_anomalies,
    load_events,
    main,
    render_html,
    render_markdown,
)

FIXTURE = Path(__file__).parents[1] / "fixtures" / "accountability-events.synthetic.json"


class LoadEventsTests(unittest.TestCase):
    def test_loads_synthetic_fixture(self):
        events = load_events(FIXTURE)
        self.assertEqual(len(events), 6)
        self.assertEqual(events[0]["phase"], "phase-1-foundation")

    def test_rejects_event_without_model(self):
        path = Path(self._tmpdir.name) / "bad.json"
        path.write_text(json.dumps([{"timestamp": "2026-01-15T00:00:00Z"}]), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "timestamp and model"):
            load_events(path)

    def setUp(self):
        import tempfile

        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)


class AggregationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.events = load_events(FIXTURE)

    def test_aggregate_by_model(self):
        by_model = aggregate(self.events, "model")
        self.assertEqual(by_model["synthetic-model-a"]["requests"], 3)
        self.assertEqual(by_model["synthetic-model-a"]["output_tokens"], 6700)
        self.assertEqual(by_model["synthetic-model-b"]["requests"], 3)

    def test_aggregate_by_phase(self):
        by_phase = aggregate(self.events, "phase")
        self.assertEqual(set(by_phase), {
            "phase-1-foundation",
            "phase-2-assessment-design",
            "phase-3-stabilization-planning",
        })

    def test_cache_reuse_ratio(self):
        totals = {"input_tokens": 100, "cache_read_tokens": 300}
        self.assertAlmostEqual(cache_reuse_ratio(totals), 0.75)

    def test_anomaly_detection_flags_large_and_slow_request(self):
        findings = find_anomalies(self.events, max_request_aiu=15.0, max_duration_ms=120_000)
        self.assertEqual(len(findings), 2)
        self.assertTrue(any("68.00 AIU" in f for f in findings))
        self.assertTrue(any("150.0s" in f for f in findings))

    def test_no_anomalies_under_generous_thresholds(self):
        findings = find_anomalies(self.events, max_request_aiu=1000.0, max_duration_ms=10**9)
        self.assertEqual(findings, [])


class RenderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.events = load_events(FIXTURE)

    def test_markdown_report_has_chart_and_honesty_note(self):
        report = render_markdown(self.events, "Test Report", 15.0, 120_000)
        self.assertIn("# Test Report", report)
        self.assertIn("synthetic-model-a", report)
        self.assertIn("not currency", report)
        self.assertIn("###", report) or self.assertIn("##", report)
        self.assertIn("#", report.split("## Usage by model")[1])  # ASCII bars present

    def test_html_report_is_self_contained_and_escaped(self):
        report = render_html(self.events, "Test <Report>", 15.0, 120_000)
        self.assertIn("Test &lt;Report&gt;", report)
        self.assertIn("<style>", report)
        self.assertNotIn("http://", report)
        self.assertNotIn("https://", report)


class CliTests(unittest.TestCase):
    def test_budget_exceeded_returns_1(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "report.md"
            code = main([str(FIXTURE), "--output", str(out), "--budget-aiu", "1.0"])
            self.assertEqual(code, 1)
            self.assertTrue(out.is_file())

    def test_normal_run_returns_0(self):
        code = main([str(FIXTURE), "--budget-aiu", "10000.0", "--format", "markdown"])
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
