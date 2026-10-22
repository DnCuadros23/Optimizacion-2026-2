"""Fixtures compartidas entre tests: ubicación de los datos crudos (data/raw)."""
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def data_dir() -> Path:
    """Carpeta donde están los .tsp originales (berlin52, eil51, etc.)."""
    return ROOT / "data" / "raw"
