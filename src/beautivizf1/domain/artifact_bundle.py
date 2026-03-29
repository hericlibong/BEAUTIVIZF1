from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(slots=True)
class ArtifactBundle:
    bundle_id: str
    selection_id: str
    rendered_visualization: Path
    embed_export: Path
    dataset_export: Path
    manifest: Path
    verification_notes: Path
    core_schema_version: str
    created_at: datetime


VisualizationBundle = ArtifactBundle
