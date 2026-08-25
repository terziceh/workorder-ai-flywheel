# 00 — Business Problem

## Objective

Define a general facilities-maintenance problem that can be solved publicly without exposing any organization-specific information.

## Users

- Work-control reviewer validating maintenance classifications
- Data analyst auditing historical code quality
- Data engineer maintaining the lakehouse pipeline
- Data scientist evaluating recommendation models

## Problem statement

Text-heavy work orders may contain incomplete context, overlapping categories, inconsistent historical labels, and repeated template language. These issues reduce reporting quality and make supervised model evaluation unreliable.

## Proposed solution

Build a Databricks lakehouse that prepares synthetic work orders for ranked recommendation, preserves model-version evidence, captures reviewer decisions, and generates governed retraining-ready data.

## MVP success criteria

- Synthetic source batches flow reproducibly through Bronze, Silver, and Gold.
- Data-quality failures are observable instead of silently deleted.
- A documented baseline produces Top-3 work-code recommendations.
- The SLM is evaluated against the baseline before adoption.
- A reviewer can accept, correct, or flag a recommendation.
- Every review action retains the model and input context needed for evaluation.

## Out of scope for the first release

- Direct integration with an employer system
- Fully automated work-code assignment
- Real-time streaming
- Automatic production retraining
- Employer authentication or authorization
- Claims of enterprise production readiness
