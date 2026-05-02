"""Step 5: Generate final experiment plan."""
from state import PipelineState
from tools.grok_client import call_grok
from utils.prompts import STEP5_SYSTEM, STEP5_USER


def step5_plan(state: PipelineState) -> PipelineState:
    """Generate the final experiment plan in Markdown."""
    user_prompt = STEP5_USER.format(
        input=state.input,
        problem_type=state.step1.get("problem_type", ""),
        subcategory=state.step1.get("subcategory", ""),
        constraints=state.step1.get("constraints", []),
        datasets=state.step2.get("datasets", []),
        models=state.step3.get("models", []),
        baselines=state.step3.get("baselines", []),
        metrics=state.step4.get("metrics", []),
        validation_strategy=state.step4.get("validation_strategy", ""),
        statistical_tests=state.step4.get("statistical_tests", []),
    )
    try:
        response = call_grok(STEP5_SYSTEM, user_prompt, temperature=0.4)
        state.step5 = {"experiment_plan": response}
    except Exception as e:
        state.add_error("step5", str(e))
        state.step5 = {"experiment_plan": f"# Error\nFailed to generate plan: {e}"}
    return state
