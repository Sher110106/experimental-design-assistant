"""Step 4: Design evaluation strategy."""
from state import PipelineState
from tools.grok_client import call_grok
from utils.prompts import STEP4_SYSTEM, STEP4_USER
from utils.parsers import extract_json, validate_step4


def step4_eval(state: PipelineState) -> PipelineState:
    """Design evaluation metrics and validation strategy."""
    user_prompt = STEP4_USER.format(
        problem_type=state.step1.get("problem_type", "unknown"),
        subcategory=state.step1.get("subcategory", ""),
        models=state.step3.get("models", []),
    )
    try:
        response = call_grok(STEP4_SYSTEM, user_prompt)
        data = extract_json(response)
        if data is None:
            raise ValueError("Failed to parse JSON from Grok response")
        state.step4 = validate_step4(data)
    except Exception as e:
        state.add_error("step4", str(e))
        state.step4 = validate_step4({})
    return state
