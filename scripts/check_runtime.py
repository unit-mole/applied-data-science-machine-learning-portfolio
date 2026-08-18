"""Verify the supported Python runtime and import the required scientific stack."""

from __future__ import annotations

import importlib
import importlib.metadata
import os
import sys
import tempfile

os.environ.setdefault(
    "MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "portfolio-matplotlib")
)

SUPPORTED_MIN = (3, 12)
SUPPORTED_MAX_EXCLUSIVE = (3, 14)
PACKAGES = {
    "numpy": "numpy",
    "pandas": "pandas",
    "scipy": "scipy",
    "scikit-learn": "sklearn",
    "matplotlib": "matplotlib",
    "openpyxl": "openpyxl",
}


def main() -> int:
    current = sys.version_info[:2]
    if not (SUPPORTED_MIN <= current < SUPPORTED_MAX_EXCLUSIVE):
        print(
            "Unsupported Python runtime: "
            f"{sys.version.split()[0]}. Use Python 3.12 or Python 3.13."
        )
        return 1

    print(f"Python {sys.version.split()[0]}: supported")
    for distribution, module in PACKAGES.items():
        importlib.import_module(module)
        print(f"{distribution} {importlib.metadata.version(distribution)}: import passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
