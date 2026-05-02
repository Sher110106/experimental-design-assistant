"""Tests for JSON parsers."""
import pytest
from utils.parsers import extract_json, validate_step1, validate_step3, validate_step4


def test_extract_json_direct():
    assert extract_json('{"key": "value"}') == {"key": "value"}


def test_extract_json_markdown():
    text = '```json\n{"key": "value"}\n```'
    assert extract_json(text) == {"key": "value"}


def test_extract_json_invalid():
    assert extract_json("not json") is None


def test_validate_step1():
    data = {"problem_type": "NLP", "subcategory": "sentiment", "constraints": ["cpu"]}
    result = validate_step1(data)
    assert result["problem_type"] == "NLP"
    assert result["constraints"] == ["cpu"]


def test_validate_step1_missing_keys():
    data = {}
    result = validate_step1(data)
    assert result["problem_type"] == "unknown"
    assert result["constraints"] == []


def test_validate_step3():
    data = {"models": [{"name": "BERT"}], "baselines": ["NB"]}
    result = validate_step3(data)
    assert len(result["models"]) == 1


def test_validate_step4():
    data = {}
    result = validate_step4(data)
    assert result["validation_strategy"] == "5-fold cross-validation"
    assert result["metrics"] == []
