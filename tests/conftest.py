from pathlib import Path

import pytest


@pytest.fixture
def project_root() -> Path:
    """Return the repository root for shared test setup."""
    return Path(__file__).resolve().parents[1]


@pytest.fixture
def artifacts_dir(project_root: Path) -> Path:
    """Ensure the artifacts directory exists for later phases."""
    path = project_root / "artifacts"
    path.mkdir(exist_ok=True)
    return path
