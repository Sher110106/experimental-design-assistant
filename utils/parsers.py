"""JSON extraction and validation utilities."""
import json
import re
from typing import Any


def extract_json(text: str) -> dict | None:
    """Extract JSON from text, handling markdown fences."""
    # Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try extracting from markdown code block
    pattern = r"```(?:json)?\s*(.*?)\s*```"
    matches = re.findall(pattern, text, re.DOTALL)
    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue

    # Try extracting raw JSON object
    pattern = r"(\{.*\})"
    matches = re.findall(pattern, text, re.DOTALL)
    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue

    return None


def validate_step1(data: dict) -> dict:
    """Validate and normalize Step 1 output."""
    required = ["problem_type", "subcategory", "constraints"]
    for key in required:
        if key not in data:
            data[key] = "unknown" if key != "constraints" else []
    if not isinstance(data["constraints"], list):
        data["constraints"] = [str(data["constraints"])]
    return data


def validate_step3(data: dict) -> dict:
    """Validate and normalize Step 3 output."""
    if "models" not in data or not isinstance(data["models"], list):
        data["models"] = []
    if "baselines" not in data or not isinstance(data["baselines"], list):
        data["baselines"] = []
    return data


def validate_step4(data: dict) -> dict:
    """Validate and normalize Step 4 output."""
    if "metrics" not in data or not isinstance(data["metrics"], list):
        data["metrics"] = []
    if "validation_strategy" not in data:
        data["validation_strategy"] = "5-fold cross-validation"
    if "statistical_tests" not in data or not isinstance(data["statistical_tests"], list):
        data["statistical_tests"] = []
    return data
