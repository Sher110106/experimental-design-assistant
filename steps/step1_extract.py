"""Step 1: Extract problem type from user input."""
from state import PipelineState
from tools.grok_client import call_grok
from utils.prompts import STEP1_SYSTEM, STEP1_USER
from utils.parsers import extract_json, validate_step1


def step1_extract(state: PipelineState) -> PipelineState:
    """Extract problem type, subcategory, and constraints."""
    user_prompt = STEP1_USER.format(input=state.input)
    try:
        response = call_grok(STEP1_SYSTEM, user_prompt)
        data = extract_json(response)
        if data is None:
            raise ValueError("Failed to parse JSON from Grok response")
        state.step1 = validate_step1(data)
    except Exception as e:
        state.add_error("step1", str(e))
        state.step1 = validate_step1({})
    return state
