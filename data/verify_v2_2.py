"""Validate the ENEC 2026 Nuclear Enterprise 360 V2.2 clean database.

Usage:
    python verify_v2_2.py /path/to/nuclear_enterprise_360_v2_2_clean.db
"""

from pathlib import Path
import sqlite3
import sys

EXPECTED_COUNTS = {
    "assets": 128,
    "sensor_readings_a001_1min": 525600,
    "a001_sensor_hourly": 8760,
    "a001_source_documents": 9,
    "a001_source_document_links": 18,
    "a001_document_evidence": 18,
    "project_assets": 30,
    "asset_project_map": 30,
}

REQUIRED_OBJECTS = {
    "asset_360",
    "a001_sensor_hourly",
    "a001_event_timeline",
    "a001_project_risk_360",
    "a001_document_evidence",
    "asset_project_map",
    "asset_project_risk_map",
}

db_path = Path(sys.argv[1] if len(sys.argv) > 1 else "nuclear_enterprise_360_v2_2_clean.db")
if not db_path.exists():
    raise SystemExit(f"Database not found: {db_path}")

with sqlite3.connect(db_path) as con:
    objects = {
        row[0]
        for row in con.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%'"
        )
    }

    missing = sorted(REQUIRED_OBJECTS - objects)
    if missing:
        raise SystemExit(f"Missing required objects: {missing}")

    failures = []
    for name, expected in EXPECTED_COUNTS.items():
        actual = con.execute(f'SELECT COUNT(*) FROM "{name}"').fetchone()[0]
        status = "OK" if actual == expected else "FAIL"
        print(f"{status:4} {name:32} actual={actual:,} expected={expected:,}")
        if actual != expected:
            failures.append((name, actual, expected))

    views = {
        row[0]
        for row in con.execute("SELECT name FROM sqlite_master WHERE type='view'")
    }

    removed_beginner_views = {
        "a001_forecasting_1min",
        "a001_forecasting_series",
        "a001_sensor_daily",
    }
    unexpected = sorted(removed_beginner_views & views)
    if unexpected:
        failures.append(("removed_beginner_views", unexpected, "absent"))
        print("FAIL confusing legacy beginner views still present:", unexpected)
    else:
        print("OK   confusing legacy beginner forecasting views are absent")

if failures:
    raise SystemExit(f"Validation failed: {failures}")

print("\nV2.2 validation passed.")
