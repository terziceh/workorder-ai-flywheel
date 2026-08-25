# 11 — CI/CD and Deployment

## Current CI

The repository-level workflow runs on pushes and pull requests to `main`:

- Install the project
- Check formatting
- Run linting
- Run unit and integration tests
- Generate a small synthetic-data fixture

## Planned progression

### After Silver and Gold

- Synthetic Bronze-to-Gold integration test
- Data-contract and quality assertions

### After baseline modeling

- Small-fixture training and inference smoke test
- Structured prediction validation
- Minimum regression thresholds where justified

### After reviewer application

- Application build
- Deployment to the selected public environment
- Health check
- Release/version recording

## Principle

Do not create deployment automation for an application that has not been built and validated.
