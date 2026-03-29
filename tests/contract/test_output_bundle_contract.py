from datetime import datetime
from pathlib import Path

from beautivizf1.domain.artifact_bundle import ArtifactBundle


def test_output_bundle_requires_the_expected_artifacts() -> None:
    bundle = ArtifactBundle(
        bundle_id="bundle-2026-heatmap-gap",
        selection_id="sel-2026-heatmap-gap",
        rendered_visualization=Path("artifacts/visualization.html"),
        embed_export=Path("artifacts/embed.html"),
        dataset_export=Path("artifacts/dataset.csv"),
        manifest=Path("artifacts/manifest.json"),
        verification_notes=Path("artifacts/notes.md"),
        core_schema_version="1.0",
        created_at=datetime.fromisoformat("2026-03-29T10:20:00+00:00"),
    )

    assert bundle.rendered_visualization.name == "visualization.html"
    assert bundle.embed_export.name == "embed.html"
    assert bundle.dataset_export.name == "dataset.csv"
    assert bundle.manifest.name == "manifest.json"
    assert bundle.verification_notes.name == "notes.md"
    assert bundle.core_schema_version == "1.0"


def test_output_bundle_uses_artifact_bundle_as_canonical_model() -> None:
    bundle = ArtifactBundle(
        bundle_id="bundle-2026-line-chart-race",
        selection_id="sel-2026-line-chart-race",
        rendered_visualization=Path("artifacts/visualization.html"),
        embed_export=Path("artifacts/embed.html"),
        dataset_export=Path("artifacts/dataset.csv"),
        manifest=Path("artifacts/manifest.json"),
        verification_notes=Path("artifacts/notes.md"),
        core_schema_version="1.0",
        created_at=datetime.fromisoformat("2026-03-29T10:21:00+00:00"),
    )

    assert bundle.__class__ is ArtifactBundle
