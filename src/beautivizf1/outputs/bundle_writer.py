from datetime import datetime, timezone
from pathlib import Path

from beautivizf1.domain.artifact_bundle import ArtifactBundle


def prepare_bundle_directory(output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def build_artifact_bundle(
    *,
    bundle_id: str,
    selection_id: str,
    output_dir: Path,
    core_schema_version: str,
    created_at: datetime | None = None,
) -> ArtifactBundle:
    bundle_dir = prepare_bundle_directory(output_dir)

    return ArtifactBundle(
        bundle_id=bundle_id,
        selection_id=selection_id,
        rendered_visualization=bundle_dir / "visualization.html",
        embed_export=bundle_dir / "embed.html",
        dataset_export=bundle_dir / "dataset.csv",
        manifest=bundle_dir / "manifest.json",
        verification_notes=bundle_dir / "notes.md",
        core_schema_version=core_schema_version,
        created_at=created_at or datetime.now(timezone.utc),
    )
