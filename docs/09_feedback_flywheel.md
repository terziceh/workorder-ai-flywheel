# 09 — Human Feedback Flywheel

## Objective

Preserve reviewer decisions as governed evaluation evidence and potential retraining data.

## Review actions

- Accept a recommendation
- Correct the recommendation
- Flag an ambiguous case

## Required inference context

```text
inference_id
phase_id
model_version
prompt_version
predicted_code
prediction_rank
confidence
review_action
accepted_code
reviewed_at
inference_latency_ms
```

## Governance principle

Original predictions are immutable. Reviewer actions create new feedback records rather than overwriting inference history.

## Status

Planned for milestone v0.6.
