# Agent Accountability Mapper

Building AI course project

## Summary

Agent Accountability Mapper turns a short description of an AI agent system into a RACI matrix, residual-risk register, decision gates and human oversight points. It helps governance teams draft these documents in minutes instead of days.

## Background

Multi-agent systems are showing up in production faster than organisations can assign clear ownership. When one agent calls another, or when a tool fails and another agent steps in, the question “who is responsible?” becomes hard to answer. Manual frameworks take days to write and are often out of date within weeks.

This problem is common in any company running more than a handful of agents. It is especially acute in regulated sectors and in teams that must demonstrate compliance with the EU AI Act high-risk requirements or equivalent internal standards.

I have spent the last few years helping clients build these accountability structures by hand. The work is necessary but repetitive. A tool that can draft the first version accurately, then let humans refine it, would free governance leads to focus on the hard judgement calls instead of the formatting.

## How is it used?

A governance lead or system owner pastes a plain-language description of the agent system (or uploads a short architecture note). The tool returns four artefacts:

- RACI matrix with named roles for design, deployment, monitoring, and incident response
- Residual risk statements linked to specific agents or failure modes
- Decision gates that must be signed before go-live or major change
- Human oversight points with suggested review frequency

These documents are reviewed, edited, and signed by the real owners. The tool does not replace human accountability; it accelerates the first draft and keeps the language consistent across systems.

Typical use happens during design reviews, pre-deployment checklists, and periodic re-assessments when agents are updated or new agents are added.

## Data sources and AI methods

Primary sources:

- Public regulatory text (EU AI Act, NIST AI RMF, ISO 42001 excerpts)
- Curated examples of existing accountability frameworks (anonymised)
- Internal style guides for residual-risk language and RACI conventions

The full vision uses retrieval-augmented generation over a small, version-controlled knowledge base of governance patterns. Structured output constraints force the model to return tables and lists in fixed formats so the result can be pasted straight into existing documentation templates. Risk classification is handled by a lightweight classifier trained on labelled examples of high, medium, and low residual risk.

No real client system descriptions are stored. Users can run the tool locally or in a private instance.

### Current prototype

A working rule-based prototype is included in `src/mapper.py`. It:

- Extracts agent names from a plain-text system description
- Builds a first-draft RACI matrix
- Generates residual-risk statements from simple keyword patterns
- Adds standard decision gates and human oversight points

Run it like this:

```bash
python src/mapper.py example_input.md -o docs/my_draft.md
```

Or without arguments to use the built-in demo description. The output is markdown ready to review and edit. This is intentionally a mock; the production version would replace the rule engine with an LLM + RAG pipeline.

## Challenges

The tool does not decide who is accountable. It only drafts language that humans must still review and own. Hallucinated legal requirements remain a risk; every regulatory claim must be checked against the original text. Over-reliance is possible if teams treat the output as final instead of as a starting point. The quality of the input description still matters: vague system notes produce vague accountability maps.

Ethical considerations include the danger of creating a false sense of completeness and the need to keep the knowledge base up to date when regulations change.

## What next?

Short term: add support for importing existing architecture diagrams and exporting directly into Confluence or SharePoint templates. Medium term: connect the residual-risk register to live monitoring so that changes in agent behaviour trigger a review of the corresponding accountability entries. Longer term: open-source the core mapping logic and knowledge base so other governance teams can adapt it to their own regulatory environments.

Skills needed next: stronger structured-output tooling, a small evaluation set of real (anonymised) agent systems, and collaboration with people who run multi-agent platforms at scale.

## Acknowledgments

- Building AI course materials from Reaktor Innovations and the University of Helsinki
- Public texts of the EU AI Act and NIST AI Risk Management Framework
- Patterns drawn from practical work on AI agent accountability frameworks and the Article9.ai materials
