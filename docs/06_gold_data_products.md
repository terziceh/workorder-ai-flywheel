# 06 — Gold Data Products

## Objective

Create consumer-specific datasets for training, inference, feedback, evaluation, and monitoring.

## Planned tables and grains

| Table | Grain |
|---|---|
| `gold_training_dataset` | One approved labeled phase |
| `gold_inference_dataset` | One phase eligible for recommendation |
| `gold_model_inference` | One candidate rank per phase and model version |
| `gold_human_feedback` | One reviewer action per inference case |
| `gold_model_evaluation` | One evaluated case per model version |
| `gold_retraining_dataset` | One governed training example per approved review |
| `gold_monitoring_metrics` | One metric per model/time window/segment |

## Status

Planned for milestone v0.3. Each implementation will include keys, refresh logic, quality rules, and consumer documentation.
