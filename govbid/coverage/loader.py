"""Loader for coverage bundles."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from govbid.util.files import require_file


def load_coverage_bundle(path: Path) -> Dict[str, Any]:
    """Load a coverage bundle from disk.

    Ensures the file exists and returns the parsed JSON. The authoritative
    coverage bundle should be placed in ``govbid/schemas/``.
    """
    require_file(path, hint="Place GovBid_Coverage_Bundle_v2.0.0.json in govbid/schemas/")
    return json.loads(path.read_text(encoding="utf-8"))
