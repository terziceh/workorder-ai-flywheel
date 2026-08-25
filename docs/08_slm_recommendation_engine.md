# 08 — SLM Recommendation Engine

## Objective

Determine whether an SLM adds useful context-aware ranking beyond the baseline.

## Required design documentation

- Input fields and why each is available at inference time
- Candidate-generation strategy
- Fictional work-code knowledge base
- Prompt/instruction version
- Structured-output contract
- Invalid-output and timeout handling
- Latency and compute requirements
- Evaluation against the baseline

## Decision rule

The SLM is retained only if it provides measurable workflow value relative to its complexity, latency, and operational requirements.

## Status

Planned for milestone v0.5.
