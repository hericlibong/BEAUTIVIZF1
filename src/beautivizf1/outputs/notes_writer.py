from pathlib import Path

from beautivizf1.domain.validated_visualization_dataset import ValidatedVisualizationDataset


def build_verification_notes(
    dataset: ValidatedVisualizationDataset,
) -> str:
    lines = [
        "# Verification notes",
        "",
        f"- Validation status: {dataset.validation_status.value}",
        f"- Source dataset: {dataset.source_dataset_id}",
        f"- Format: {dataset.chosen_format.value}",
        "",
        "## Validation notes",
    ]

    if dataset.validation_notes:
        lines.extend(f"- {note}" for note in dataset.validation_notes)
    else:
        lines.append("- No validation notes were provided.")

    return "\n".join(lines) + "\n"


def write_verification_notes(
    notes_path: Path,
    dataset: ValidatedVisualizationDataset,
) -> Path:
    notes_path.parent.mkdir(parents=True, exist_ok=True)
    notes_path.write_text(build_verification_notes(dataset), encoding="utf-8")
    return notes_path
