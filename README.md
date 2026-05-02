# Experimental Design Assistant

> A goal-driven multi-step LLM agent for ML research planning

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## What It Does

The **Experimental Design Assistant** takes a raw research idea (e.g. *"I want to build a sentiment classifier that runs on a CPU-only laptop"*) and outputs a complete, actionable experiment plan. The pipeline chains **5 sequential steps** — each one reads structured output from the previous step and produces structured input for the next — resulting in a coherent research roadmap with dataset suggestions, model choices, evaluation metrics, and a week-by-week timeline.

This is not a single prompt. It is a **reasoning pipeline** where every step depends on the previous one.

## Quick Start

```bash
# 1. Clone & enter the repo
git clone <repo-url>
cd experimental-design-assistant

# 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set API keys (or use the defaults already in config.py)
export GROQ_API_KEY="gsk_..."
export FIRECRAWL_API_KEY="fc-..."

# 5. Run the pipeline
python pipeline.py "I want to build a sentiment classifier for tweets that runs on mobile"
```

Results are saved to `output/result.json` and printed to stdout.

## Pipeline Architecture

```
User Input
    │
    ▼
┌─────────────────────────────────────────┐
│ Step 1: Problem Type Extraction  (LLM)  │
│   Input: raw research idea               │
│   Output: {problem_type, subcategory,    │
│            constraints}                  │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ Step 2: Dataset Search           (Tool) │
│   Input: problem_type, subcategory       │
│   Output: [{name, source, size, url}]   │
│   Tool: Firecrawl web search             │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ Step 3: Model Suggestions        (LLM)  │
│   Input: problem_type + datasets         │
│   Output: [{name, type, reason,         │
│            library}] + baselines         │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ Step 4: Evaluation Strategy      (LLM)  │
│   Input: problem_type + models           │
│   Output: {metrics, validation_strategy,│
│            statistical_tests}            │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ Step 5: Experiment Plan          (LLM)  │
│   Input: ALL previous state              │
│   Output: Markdown experiment plan       │
└─────────────────────────────────────────┘
```

## Why Multi-Step?

A single prompt cannot reliably:
- **Search live datasets** on the web
- **Tailor model suggestions** to the specific datasets found
- **Design evaluation metrics** that match the models chosen
- **Generate a coherent plan** that references all previous decisions

By breaking the task into 5 steps, each step has a single responsibility, intermediate outputs are inspectable, and failure is isolated to one step rather than the entire system.

## Shared State

All steps communicate through a shared `PipelineState` object:

```python
state = {
    "input": "raw user idea",
    "step1": {"problem_type": "NLP", "subcategory": "sentiment", "constraints": [...]},
    "step2": {"datasets": [...], "search_query": "..."},
    "step3": {"models": [...], "baselines": [...]},
    "step4": {"metrics": [...], "validation_strategy": "...", "statistical_tests": [...]},
    "step5": {"experiment_plan": "# Markdown plan..."},
    "errors": []
}
```

## Error Handling

| Failure Case | Handling |
|-------------|----------|
| Firecrawl API down / returns empty | Retry with simplified query → fallback to curated dataset lists |
| LLM API rate limited | Exponential backoff retry |
| LLM returns invalid JSON | Regex-based markdown fence extraction → retry with stricter prompt |
| No datasets found | Use fallback datasets matched to problem type |

## Tech Stack

- **Language:** Python 3.10+
- **LLM:** Groq (`openai/gpt-oss-120b`)
- **Web Search:** Firecrawl API
- **State:** Python `dataclass`
- **Testing:** `pytest` (10 tests, all passing)
- **No frameworks:** No LangChain, no LlamaIndex — pure Python

## Project Structure

```
.
├── pipeline.py              # Main runner
├── state.py                 # Shared state dataclass
├── config.py                # API keys & settings
├── requirements.txt         # Dependencies
├── README.md                # This file
├── tools/
│   ├── grok_client.py       # LLM API wrapper (Groq-compatible)
│   └── firecrawl_client.py  # Web search wrapper
├── steps/
│   ├── step1_extract.py     # Problem classification
│   ├── step2_search.py      # Dataset search
│   ├── step3_models.py      # Model suggestions
│   ├── step4_eval.py        # Evaluation design
│   └── step5_plan.py        # Plan generation
├── utils/
│   ├── prompts.py           # All prompt templates
│   ├── parsers.py           # JSON extraction & validation
│   └── fallback_data.py     # Curated fallback datasets
└── tests/
    ├── test_parsers.py      # Parser unit tests
    ├── test_steps.py        # API client mock tests
    └── test_pipeline.py     # Full integration test
```

## Testing

```bash
pytest tests/ -v
```

All 10 tests pass:
- 7 parser tests (JSON extraction, validation)
- 2 API client mock tests (Grok, Firecrawl)
- 1 full pipeline integration test

## Example Output

**Input:** *"I want to build a sentiment classifier for movie reviews that runs on a CPU-only laptop"*

**Step 1** extracts `classification / sentiment analysis` with constraints `[CPU-only, laptop hardware, low latency]`.

**Step 2** finds 5 real datasets via Firecrawl (Kaggle IMDB, UCI, Reddit discussions, etc.).

**Step 3** suggests 5 models: Logistic Regression + TF-IDF, Naive Bayes, LinearSVC, fastText, and DistilBERT — each with justification and recommended library.

**Step 4** designs 6 metrics (Accuracy, Macro-F1, Weighted-F1, Precision, Recall, AUROC), stratified 5-fold cross-validation, and 4 statistical tests.

**Step 5** generates a full Markdown experiment plan with hardware specs, software stack, preprocessing pipeline, baselines, experiment matrix, training details, ONNX optimization, evaluation protocol, ablation plan, and a 4-week timeline.

The complete structured output is saved to `output/result.json`.

## License

MIT
