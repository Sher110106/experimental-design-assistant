"""Integration tests for the pipeline."""
import requests
from unittest.mock import patch, MagicMock
from pipeline import run_pipeline


def test_run_pipeline_success():
    """Test full pipeline with mocked API calls."""
    grok_responses = [
        # Step 1
        {"choices": [{"message": {"content": '{"problem_type": "NLP", "subcategory": "sentiment", "constraints": ["cpu"]}'}}]},
        # Step 3
        {"choices": [{"message": {"content": '{"models": [{"name": "BERT"}], "baselines": ["NB"]}'}}]},
        # Step 4
        {"choices": [{"message": {"content": '{"metrics": [{"name": "F1", "justification": "imbalanced", "priority": "primary"}], "validation_strategy": "5-fold CV", "statistical_tests": ["t-test"]}'}}]},
        # Step 5
        {"choices": [{"message": {"content": "# Experiment Plan\n\n## Setup\nUse IMDB."}}]},
    ]
    grok_iter = iter(grok_responses)

    def make_request_mock(*args, **kwargs):
        url = args[0] if args else kwargs.get("url", "")
        if "firecrawl" in url:
            mock = MagicMock()
            mock.status_code = 200
            mock.json.return_value = {
                "data": [{"title": "IMDB", "description": "Sentiment", "url": "http://imdb.com", "metadata": {"source": "Kaggle"}}]
            }
            mock.raise_for_status = MagicMock()
            return mock
        else:
            mock = MagicMock()
            mock.status_code = 200
            mock.json.return_value = next(grok_iter)
            mock.raise_for_status = MagicMock()
            return mock

    with patch.object(requests, "post", side_effect=make_request_mock):
        state = run_pipeline("I want to do sentiment analysis")

    assert state.step1["problem_type"] == "NLP"
    assert len(state.step2["datasets"]) == 1
    assert len(state.step3["models"]) == 1
    assert len(state.step4["metrics"]) == 1
    assert "Experiment Plan" in state.step5["experiment_plan"]
