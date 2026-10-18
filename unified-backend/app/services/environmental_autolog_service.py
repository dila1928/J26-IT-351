"""
Environmental auto-log: replays `sensor_replay_master.csv` one row at a
time (standing in for a live sensor feed, same convention as
replay_lookup.py's history lookup) and writes just the raw reading -
timestamp, growth_stage, and the 4 sensor values - to a global Firestore
collection (`environmental_auto_readings`) so any signed-in mobile user
can pull it into "Auto" mode regardless of who is logged in. No
prediction here - the mobile app runs /environmental/predict itself once
the user confirms/edits the auto-filled values.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from app.services import firebase_client

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
REPLAY_PATH = DATA_DIR / "virtual_sensor_replay" / "sensor_replay_master.csv"

AUTO_READINGS_COLLECTION = "environmental_auto_readings"

TIMESTAMP_COL = "timestamp"
GROWTH_STAGE_COL = "growth_stage"
SENSOR_COLUMNS = ["air_temperature_c", "relative_humidity_pct", "light_intensity_lux", "soil_temperature_c"]

_replay_df: pd.DataFrame | None = None
_cursor = 0


def _load_replay() -> pd.DataFrame:
    global _replay_df
    if _replay_df is None:
        df = pd.read_csv(REPLAY_PATH)
        df[TIMESTAMP_COL] = pd.to_datetime(df[TIMESTAMP_COL])
        df = df.sort_values(TIMESTAMP_COL).reset_index(drop=True)
        _replay_df = df
    return _replay_df


def _next_row() -> pd.Series:
    """Advances a module-level cursor through the replay file, wrapping
    around at the end, so each call returns the next simulated reading."""
    global _cursor
    df = _load_replay()
    row = df.iloc[_cursor % len(df)]
    _cursor += 1
    return row


def auto_log() -> dict:
    row = _next_row()

    # Stamp with the current wall-clock time (not the replay file's own
    # 2025 timestamp) so the reading looks like a fresh live sample, and so
    # the environmental model's day/night + feature logic uses "now".
    now = pd.Timestamp.utcnow().tz_localize(None)
    reading_timestamp = now.isoformat()
    growth_stage = str(row[GROWTH_STAGE_COL])
    sensor_values = {col: float(row[col]) for col in SENSOR_COLUMNS}

    record = {
        "timestamp": reading_timestamp,
        "growth_stage": growth_stage,
        **sensor_values,
    }

    saved = firebase_client.add_document(AUTO_READINGS_COLLECTION, record)
    return saved
