"""Run with:  python -m unittest discover tests"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import Thresholds
from src.pipeline import run_pipeline
from src.alerts import check_current


def base_current(**kw):
    cur = {"temp_c": 25, "humidity_pct": 50, "wind_ms": 3, "condition": "Clear",
           "description": "clear sky"}
    cur.update(kw)
    return cur


class TestAlerts(unittest.TestCase):
    def test_no_alerts_in_normal_weather(self):
        self.assertEqual(check_current(base_current(), None, Thresholds()), [])

    def test_heat_alert(self):
        kinds = [a.kind for a in check_current(base_current(temp_c=41), None, Thresholds())]
        self.assertIn("HEAT", kinds)

    def test_humidity_and_wind(self):
        kinds = [a.kind for a in check_current(base_current(humidity_pct=92, wind_ms=14), None, Thresholds())]
        self.assertIn("HUMIDITY", kinds)
        self.assertIn("WIND", kinds)

    def test_storm_is_critical(self):
        alerts = check_current(base_current(condition="Thunderstorm"), None, Thresholds())
        self.assertEqual(alerts[0].severity, "CRITICAL")

    def test_aqi_alert(self):
        alerts = check_current(base_current(), {"aqi": 5, "label": "Very Poor"}, Thresholds())
        self.assertEqual(alerts[0].kind, "AQI")


class TestPipeline(unittest.TestCase):
    def test_simulation_runs(self):
        r = run_pipeline("Varanasi", "simulation")
        self.assertEqual(len(r["forecast_df"]), 40)

    def test_heatwave_triggers_heat(self):
        r = run_pipeline("Delhi", "simulation", scenario="heatwave")
        self.assertIn("HEAT", [a.kind for a in r["alerts"]])

    def test_storm_triggers_storm_and_wind(self):
        kinds = [a.kind for a in run_pipeline("Mumbai", "simulation", scenario="storm")["alerts"]]
        self.assertIn("STORM", kinds)
        self.assertIn("WIND", kinds)


if __name__ == "__main__":
    unittest.main()
