"""Prompt templates for each pipeline step."""

STEP1_SYSTEM = """You are an ML research assistant. Your job is to classify a user's research idea into a structured taxonomy."""

STEP1_USER = """Given the following research idea, classify it and return ONLY a JSON object with these exact keys:
- "problem_type": one of [classification, regression, NLP, CV, time_series, reinforcement_learning, generative]
- "subcategory": specific sub-task (e.g., "sentiment analysis", "image segmentation")
- "constraints": list of practical constraints (compute, data size, latency, etc.)

Research idea: {input}

Return valid JSON only. No markdown, no explanation."""

STEP3_SYSTEM = """You are an ML engineer selecting models for a specific problem. Choose 3-5 models ranging from simple to state-of-the-art."""

STEP3_USER = """Given the following problem and available datasets, suggest appropriate models and baselines.

Problem type: {problem_type}
Subcategory: {subcategory}
Constraints: {constraints}
Datasets: {datasets}

Return ONLY a JSON object with:
- "models": list of objects with keys "name", "type" (baseline or advanced), "reason", "library"
- "baselines": list of baseline model names

Return valid JSON only."""

STEP4_SYSTEM = """You are an ML research methodologist. Design a rigorous evaluation strategy."""

STEP4_USER = """Given the following problem and models, design an evaluation strategy.

Problem type: {problem_type}
Subcategory: {subcategory}
Models: {models}

Return ONLY a JSON object with:
- "metrics": list of objects with keys "name", "justification", "priority" (primary or secondary)
- "validation_strategy": string describing validation approach
- "statistical_tests": list of statistical test names

Return valid JSON only."""

STEP5_SYSTEM = """You are a research project manager. Generate a detailed, reproducible experiment plan in Markdown."""

STEP5_USER = """Generate a comprehensive experiment plan based on all the information gathered so far.

Research Idea: {input}
Problem Type: {problem_type}
Subcategory: {subcategory}
Constraints: {constraints}
Datasets: {datasets}
Models: {models}
Baselines: {baselines}
Metrics: {metrics}
Validation Strategy: {validation_strategy}
Statistical Tests: {statistical_tests}

Write a structured Markdown document with these sections:
1. Overview
2. Setup (datasets, libraries)
3. Baselines
4. Main Experiments
5. Evaluation
6. Ablation Plan
7. Timeline

Be specific and actionable."""
