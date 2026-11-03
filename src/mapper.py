#!/usr/bin/env python3
"""
Agent Accountability Mapper - minimal prototype

Takes a plain-language description of an AI agent system and produces
a first-draft accountability package:
- RACI matrix
- Residual risk statements
- Decision gates
- Human oversight points

This is a rule-based mock for demonstration. In a real version the core
generation would use an LLM with structured output + RAG over governance
patterns.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class Agent:
    name: str
    role_hint: str = ""


@dataclass
class AccountabilityPackage:
    agents: List[Agent] = field(default_factory=list)
    system_owner: str = "System Owner"
    human_agents: str = "Human Agents"
    residual_risks: List[str] = field(default_factory=list)
    decision_gates: List[str] = field(default_factory=list)
    oversight_points: List[str] = field(default_factory=list)


def extract_agents(text: str) -> List[Agent]:
    """Very simple heuristic: look for lines that look like agent names."""
    agents = []
    # Match patterns like "- Intake Agent receives..." or "Intake Agent:"
    patterns = [
        r"[-*]\s*([A-Z][a-zA-Z\s]+?Agent)\b",
        r"\b([A-Z][a-zA-Z\s]+?Agent)\b",
    ]
    seen = set()
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            name = match.group(1).strip()
            if name not in seen and len(name) < 40:
                seen.add(name)
                agents.append(Agent(name=name))
    return agents


def build_package(description: str) -> AccountabilityPackage:
    agents = extract_agents(description)
    if not agents:
        agents = [Agent(name="Primary Agent")]

    pkg = AccountabilityPackage(agents=agents)

    # Residual risks – simple template based on presence of keywords
    if any("intake" in a.name.lower() or "classif" in description.lower() for a in agents):
        pkg.residual_risks.append(
            "Incorrect classification or routing by an upstream agent may delay or mis-prioritise cases. "
            "Mitigation: human review of high-severity items + daily sample checks."
        )
    if any("research" in a.name.lower() or "knowledge" in description.lower() for a in agents):
        pkg.residual_risks.append(
            "Research or knowledge-retrieval agent may surface outdated or incorrect content. "
            "Mitigation: version-controlled knowledge base + policy check by a review agent + human override."
        )
    if any("draft" in a.name.lower() or "reply" in description.lower() or "generat" in description.lower() for a in agents):
        pkg.residual_risks.append(
            "Generated content may contain tone, factual or policy violations. "
            "Mitigation: dedicated review step before release + mandatory human approval on high-risk items."
        )
    if not pkg.residual_risks:
        pkg.residual_risks.append(
            "General residual risk: agent behaviour may drift after updates. "
            "Mitigation: versioned prompts, change logs, and scheduled human review of residual-risk register."
        )

    # Decision gates (always present)
    pkg.decision_gates = [
        "System Owner must sign the full accountability package before first production deployment.",
        "Any material change to agent prompts, tools, or knowledge sources that affects high-risk routing requires re-sign-off by System Owner and the relevant Review / Oversight owner.",
        "Go-live is blocked until residual-risk statements have named owners and review frequencies.",
    ]

    # Oversight points
    pkg.oversight_points = [
        "High-severity or high-urgency items require mandatory human approval before action is taken.",
        "Weekly sample review of completed cases by a senior human reviewer.",
        "Monthly review of the residual-risk register by the System Owner.",
        "Prompt and knowledge-base changes are logged and reviewed within 5 business days.",
    ]

    return pkg


def render_raci(pkg: AccountabilityPackage) -> str:
    headers = ["Activity"] + [a.name + " Owner" for a in pkg.agents] + [pkg.system_owner, pkg.human_agents]
    rows = [
        ["Design & prompt configuration"] + ["C"] * len(pkg.agents) + ["A", "I"],
        ["Deployment to production"] + ["I"] * len(pkg.agents) + ["A", "C"],
        ["Daily / continuous monitoring"] + ["R"] * len(pkg.agents) + ["A", "C"],
        ["Incident response"] + ["C"] * len(pkg.agents) + ["A", "R"],
        ["Model / knowledge / prompt updates"] + ["C"] * len(pkg.agents) + ["A", "I"],
    ]

    # Simple markdown table
    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "|".join(["---"] * len(headers)) + "|")
    for row in rows:
        # Pad or trim to match header length
        while len(row) < len(headers):
            row.append("I")
        lines.append("| " + " | ".join(row[: len(headers)]) + " |")

    lines.append("")
    lines.append("R = Responsible · A = Accountable · C = Consulted · I = Informed")
    return "\n".join(lines)


def render_package(pkg: AccountabilityPackage) -> str:
    out = []
    out.append("# Accountability Package (Draft)\n")
    out.append("## Detected Agents\n")
    for a in pkg.agents:
        out.append(f"- {a.name}")
    out.append("")

    out.append("## RACI Matrix\n")
    out.append(render_raci(pkg))
    out.append("")

    out.append("## Residual Risk Statements\n")
    for i, risk in enumerate(pkg.residual_risks, 1):
        out.append(f"{i}. {risk}")
    out.append("")

    out.append("## Decision Gates\n")
    for i, gate in enumerate(pkg.decision_gates, 1):
        out.append(f"{i}. {gate}")
    out.append("")

    out.append("## Human Oversight Points\n")
    for point in pkg.oversight_points:
        out.append(f"- {point}")
    out.append("")

    out.append("---\n")
    out.append("*This is a first-draft generated by Agent Accountability Mapper. All statements must be reviewed, edited and owned by the real system owner and role holders before use.*")
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description="Agent Accountability Mapper – draft generator")
    parser.add_argument(
        "input_file",
        nargs="?",
        default=None,
        help="Path to a text file containing the system description",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Optional path to write the markdown output",
    )
    args = parser.parse_args()

    if args.input_file:
        description = Path(args.input_file).read_text(encoding="utf-8")
    else:
        # Fallback demo description
        description = """
We run a customer-support multi-agent setup.
- Intake Agent receives tickets and classifies urgency.
- Research Agent pulls relevant knowledge-base articles and past tickets.
- Draft Agent writes the reply.
- Review Agent checks tone and policy compliance before the reply is sent.
- Escalation Agent routes high-risk or complex tickets to human agents.
The system uses an external LLM API and a private knowledge base.
Human agents handle final approval on all high-urgency tickets.
"""

    pkg = build_package(description)
    result = render_package(pkg)

    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
        print(f"Wrote draft to {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
