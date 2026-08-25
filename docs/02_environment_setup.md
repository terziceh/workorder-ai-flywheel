# 02 — Environment Setup

## Objective

Provide reproducible setup instructions for local development, GitHub collaboration, and the public Databricks implementation.

## Local environment

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
make check
```

## Databricks setup checklist

- Create a dedicated public-project catalog/schema or equivalent isolated namespace.
- Use only generated synthetic files.
- Store secrets outside code and notebooks.
- Document runtime and package assumptions.
- Export source-controlled notebook/code versions without cell outputs containing sensitive information.

## GitHub setup checklist

- Protect `main` after the first successful CI run.
- Require the CI check before merging.
- Use issues and pull requests even as a solo developer.
- Never store Databricks tokens, workspace URLs, or credentials in the repository.

## Status

Local packaging and CI configuration exist. Databricks public-environment details will be recorded when the synthetic Bronze implementation is recreated.
