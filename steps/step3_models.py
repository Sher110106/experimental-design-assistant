"""Step 3: Suggest models and baselines."""
from state import PipelineState
from tools.grok_client import call_grok
from utils.prompts import STEP3_SYSTEM, STEP3_USER
from utils.parsers import extract_json, validate_step3


def step3_models(state: PipelineState) -> PipelineState:
    """Suggest models and baselines."""
    user_prompt = STEP3_USER.format(
        problem_type=state.step1.get("problem_type", "unknown"),
        subcategory=state.step1.get("subcategory", ""),
        constraints=state.step1.get("constraints", []),
        datasets=state.step2.get("datasets", []),
    )
    try:
        response = call_grok(STEP3_SYSTEM, user_prompt)
        data = extract_json(response)
        if data is None:
            raise ValueError("Failed to parse JSON from Grok response")
        state.step3 = validate_step3(data)
    except Exception as e:
        state.add_error("step3", str(e))
        state.step3 = validate_step3({})
    return state
