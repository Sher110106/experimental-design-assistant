"""Step 2: Search for relevant datasets."""
from state import PipelineState
from tools.firecrawl_client import search_datasets
from utils.fallback_data import get_fallback_datasets


def step2_search(state: PipelineState) -> PipelineState:
    """Search for datasets based on problem type and subcategory."""
    problem_type = state.step1.get("problem_type", "classification")
    subcategory = state.step1.get("subcategory", "")
    query = f"best public datasets for {subcategory} {problem_type} machine learning"

    datasets = search_datasets(query)
    if not datasets:
        # Retry with simpler query
        datasets = search_datasets(f"{problem_type} datasets kaggle")

    if not datasets:
        state.add_error("step2", "Firecrawl search failed, using fallback datasets")
        datasets = get_fallback_datasets(problem_type)

    state.step2 = {
        "datasets": datasets,
        "search_query": query,
    }
    return state
