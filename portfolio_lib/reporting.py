"""Shared output and data-quality helpers."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


def ensure_output_dirs(project_root: Path) -> dict[str, Path]:
    """Create and return standard output directories."""
    paths = {
        "reports": project_root / "reports",
        "figures": project_root / "reports" / "figures",
        "tables": project_root / "reports" / "tables",
        "models": project_root / "models",
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths


def data_quality_table(frame: pd.DataFrame) -> pd.DataFrame:
    """Create a compact per-column data-quality inventory."""
    return pd.DataFrame({
        "column": frame.columns,
        "dtype": frame.dtypes.astype(str).values,
        "missing_count": frame.isna().sum().values,
        "missing_percent": (frame.isna().mean() * 100).round(3).values,
        "unique_values": frame.nunique(dropna=False).values,
        "constant": [frame[column].nunique(dropna=False) <= 1 for column in frame.columns],
    })


def _json_default(value: object) -> object:
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return None if not np.isfinite(value) else float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if isinstance(value, Path):
        return str(value)
    raise TypeError(f"Cannot serialize {type(value).__name__}")


def write_json(path: Path, payload: dict[str, object]) -> None:
    """Write deterministic, human-readable JSON."""
    path.write_text(json.dumps(payload, indent=2, default=_json_default), encoding="utf-8")

