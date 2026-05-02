"""Mock tests for API clients."""
from unittest.mock import patch, MagicMock
from tools.grok_client import call_grok
from tools.firecrawl_client import search_datasets


def test_call_grok_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": '{"key": "value"}'}}]
    }
    mock_response.raise_for_status = MagicMock()

    with patch("tools.grok_client.requests.post", return_value=mock_response):
        result = call_grok("system", "user")
        assert result == '{"key": "value"}'


def test_search_datasets_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": [
            {"title": "IMDB", "description": "Sentiment", "url": "http://imdb.com", "metadata": {"source": "Kaggle"}}
        ]
    }
    mock_response.raise_for_status = MagicMock()

    with patch("tools.firecrawl_client.requests.post", return_value=mock_response):
        result = search_datasets("NLP datasets")
        assert len(result) == 1
        assert result[0]["name"] == "IMDB"
