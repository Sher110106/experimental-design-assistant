"""Main pipeline runner for the Experimental Design Assistant."""
import json
import sys
from state import PipelineState
from steps.step1_extract import step1_extract
from steps.step2_search import step2_search
from steps.step3_models import step3_models
from steps.step4_eval import step4_eval
from steps.step5_plan import step5_plan


def run_pipeline(user_input: str) -> PipelineState:
    """Run the full 5-step pipeline."""
    state = PipelineState(input=user_input)

    print("[Step 1/5] Extracting problem type...")
    state = step1_extract(state)
    print(f"  -> Problem: {state.step1.get('problem_type', 'unknown')} | {state.step1.get('subcategory', '')}")

    print("[Step 2/5] Searching datasets...")
    state = step2_search(state)
    print(f"  -> Found {len(state.step2.get('datasets', []))} datasets")

    print("[Step 3/5] Suggesting models...")
    state = step3_models(state)
    print(f"  -> Suggested {len(state.step3.get('models', []))} models")

    print("[Step 4/5] Designing evaluation...")
    state = step4_eval(state)
    print(f"  -> Metrics: {[m['name'] for m in state.step4.get('metrics', [])]}")

    print("[Step 5/5] Generating experiment plan...")
    state = step5_plan(state)
    print("  -> Done!")

    if state.errors:
        print(f"\n⚠️  {len(state.errors)} error(s) occurred:")
        for err in state.errors:
            print(f"   [{err['step']}] {err['message']}")

    return state


def save_output(state: PipelineState, filepath: str = "output/result.json"):
    """Save the final state to a JSON file."""
    import os
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(state.to_dict(), f, indent=2)
    print(f"\nOutput saved to {filepath}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = input("Enter your research idea: ")

    state = run_pipeline(user_input)
    save_output(state)

    # Also print the final plan
    print("\n" + "=" * 60)
    print("FINAL EXPERIMENT PLAN")
    print("=" * 60)
    print(state.step5.get("experiment_plan", "No plan generated."))
