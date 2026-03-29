from pathlib import Path

from beautivizf1.chat import handle_chat_message, handle_format_choice, propose_formats
from beautivizf1.data_sources.f1_provider import F1Provider
from beautivizf1.domain.format_selection import VisualizationFormat
from beautivizf1.domain.source_dataset import SourceDataset
from beautivizf1.interpretation.intent_parser import InterpretationOutcome
from beautivizf1.services.visualization_service import VisualizationService


class ExplodingProvider(F1Provider):
    source_name = "test-provider"

    def fetch_dataset(self, **kwargs: object) -> SourceDataset:
        raise AssertionError("The provider must not be called during format selection.")


def test_format_selection_flow_stops_after_a_valid_explicit_choice(tmp_path: Path) -> None:
    service = VisualizationService(provider=ExplodingProvider(), output_dir=tmp_path)

    interpretation = handle_chat_message(
        "Je veux comparer les écarts des pilotes en qualifications 2025.",
        request_id="req-format-flow",
        service=service,
    )

    assert interpretation.outcome is InterpretationOutcome.INTERPRETED
    assert interpretation.intent is not None

    proposal = propose_formats(interpretation)

    assert proposal.request_id == "req-format-flow"
    assert proposal.available_formats == (
        VisualizationFormat.HEATMAP,
        VisualizationFormat.LINE_CHART_RACE,
    )
    assert proposal.generation_allowed is False
    assert proposal.next_step == "explicit_format_choice_required"
    assert "écarts" in proposal.need_summary

    choice_result = handle_format_choice(proposal, "heatmap", selection_id="sel-format-flow")

    assert choice_result.status == "selected"
    assert choice_result.selection is not None
    assert choice_result.selection.selection_id == "sel-format-flow"
    assert choice_result.selection.intent_id == proposal.intent_id
    assert choice_result.selection.chosen_format is VisualizationFormat.HEATMAP
    assert choice_result.generation_allowed is True
    assert choice_result.next_step == "generation_can_be_prepared"
