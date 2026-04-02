# Schema Wrapper (Python)

This package generates and tests Python wrapper classes for the Mosaic JSON schema.

## Prerequisites

- Use Python `>=3.9`.
- Run commands from `packages/schema-wrapper`.
- Use `uv` to create and manage the environment.

## Install Dependencies

```bash
uv sync --group dev
```

## Generate Wrapper Classes

Regenerate `schema_wrapper/generated_classes.py` from the schema version pinned in `schema_wrapper/generate_schema_wrapper.py` (`SCHEMA_VERSION`):

```bash
uv run generate.py
```

Note: `generate.py` currently does not accept a schema path argument; it reads from `docs/public/schema/<SCHEMA_VERSION>.json`.

## Run Tests

Run all schema-wrapper tests:

```bash
uv run --group dev pytest test/ -v
```

Run only the full round-trip tests:

```bash
uv run --group dev pytest test/test_full_round_trip.py -q
```

## Lint and Format

```bash
uv run --group dev ruff check
uv run --group dev ruff format
```

## Type Checking

```bash
uv run --group dev mypy
```

## Notebook Exploration

```bash
uv run --group dev jupyter lab
```

No example notebook is currently committed in this package; create a local notebook in this directory if you want to experiment interactively.
