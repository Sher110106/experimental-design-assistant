"""Shared state management for the pipeline."""
from dataclasses import dataclass, field
from typing import Any


@dataclass
class PipelineState:
    input: str = ""
    step1: dict = field(default_factory=dict)
    step2: dict = field(default_factory=dict)
    step3: dict = field(default_factory=dict)
    step4: dict = field(default_factory=dict)
    step5: dict = field(default_factory=dict)
    errors: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "input": self.input,
            "step1": self.step1,
            "step2": self.step2,
            "step3": self.step3,
            "step4": self.step4,
            "step5": self.step5,
            "errors": self.errors,
        }

    def add_error(self, step: str, message: str):
        self.errors.append({"step": step, "message": message})
