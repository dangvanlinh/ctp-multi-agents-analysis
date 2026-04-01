"""Token usage tracker — track API costs across agents and phases."""

from dataclasses import dataclass, field
from datetime import datetime


# Pricing per 1M tokens (USD) — updated 2025-05
PRICING = {
    "claude-sonnet-4-20250514": {"input": 3.0, "output": 15.0},
    "gpt-4o": {"input": 2.5, "output": 10.0},
    "gemini-2.0-flash": {"input": 0.10, "output": 0.40},
}

# Fallback pricing
DEFAULT_PRICING = {"input": 3.0, "output": 15.0}


@dataclass
class UsageEntry:
    agent: str          # e.g. "Phase 0 - Data Request", "Round 1 - Analyst"
    model: str          # e.g. "claude-sonnet-4-20250514"
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    timestamp: str = ""


@dataclass
class TokenTracker:
    entries: list = field(default_factory=list)

    def log(self, agent: str, model: str, input_tokens: int, output_tokens: int):
        """Log a single API call's usage."""
        pricing = PRICING.get(model, DEFAULT_PRICING)
        cost = (
            input_tokens * pricing["input"] / 1_000_000
            + output_tokens * pricing["output"] / 1_000_000
        )
        entry = UsageEntry(
            agent=agent,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost,
            timestamp=datetime.now().strftime("%H:%M:%S"),
        )
        self.entries.append(entry)
        return entry

    @property
    def total_input(self) -> int:
        return sum(e.input_tokens for e in self.entries)

    @property
    def total_output(self) -> int:
        return sum(e.output_tokens for e in self.entries)

    @property
    def total_cost(self) -> float:
        return sum(e.cost_usd for e in self.entries)

    def summary_by_agent(self) -> list[dict]:
        """Group usage by agent name."""
        groups = {}
        for e in self.entries:
            if e.agent not in groups:
                groups[e.agent] = {"agent": e.agent, "model": e.model, "input": 0, "output": 0, "cost": 0.0}
            groups[e.agent]["input"] += e.input_tokens
            groups[e.agent]["output"] += e.output_tokens
            groups[e.agent]["cost"] += e.cost_usd
        return list(groups.values())

    def summary_by_model(self) -> list[dict]:
        """Group usage by model."""
        groups = {}
        for e in self.entries:
            if e.model not in groups:
                groups[e.model] = {"model": e.model, "input": 0, "output": 0, "cost": 0.0}
            groups[e.model]["input"] += e.input_tokens
            groups[e.model]["output"] += e.output_tokens
            groups[e.model]["cost"] += e.cost_usd
        return list(groups.values())
