# Contributing

## Delivery workflow

1. Select or create a GitHub issue with acceptance criteria.
2. Create a branch such as `feature/synthetic-data-generator`.
3. Make the smallest complete change that satisfies the issue.
4. Add or update tests and documentation.
5. Run `make check` locally.
6. Open a pull request and complete the checklist.
7. Merge only after CI succeeds.

## Definition of done

- Code is reusable and does not expose sensitive information.
- Relevant tests pass.
- Table grain or interface contract is documented.
- The decision log is updated for meaningful tradeoffs.
- Evidence of completion is included in the pull request.

## Commit style

Use concise imperative commits, for example:

```text
feat: add configurable synthetic work-order generator
test: validate generated work-order contract
docs: document Bronze ingestion grain
```
