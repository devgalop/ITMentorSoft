# Database Migrations Specification

## Purpose

Introduces Alembic async migration system to manage PostgreSQL schema evolution with versioned migrations, replacing `Base.metadata.create_all` for production-ready schema management.

---

## ADDED Requirements

### Requirement: Alembic Initialization

The system SHALL run `alembic init` to create the `alembic/` directory with async configuration.

The `alembic.ini` file MUST configure `sqlalchemy.url` from the `DATABASE_URL` environment variable.

### Requirement: Async Engine in Alembic Environment

The `alembic/env.py` MUST use `AsyncEngine` from `sqlalchemy.ext.asyncio` and pass `async_engine_from_config()` to Alembic.

The migration context MUST invoke `run_async_migrations()` correctly.

### Requirement: Migration Directory Structure

The system SHALL maintain:
- `alembic/versions/` — versioned migration scripts (auto-generated)
- `alembic/env.py` — async engine configuration
- `alembic/script.py.mako` — migration script template

### Requirement: Auto-Generation of Initial Migration

The system SHALL run `alembic revision --autogenerate -m "initial"` to generate the baseline migration from existing model metadata after model updates are applied.

### Requirement: Upgrade and Downgrade Migrations

Each migration file MUST define both `upgrade()` and `downgrade()` functions.

`alembic upgrade head` MUST create all tables.
`alembic downgrade -1` MUST roll back the most recent migration.

### Requirement: Migration Status Command

The system SHALL provide a way to verify migration state via `alembic current` and `alembic history`.

---

## Scenarios

#### Scenario: Initial migration creates all tables

- GIVEN models are updated for PostgreSQL compatibility (no `autoincrement`, `server_default=func.now()`)
- WHEN `alembic revision --autogenerate -m "initial"` runs
- THEN a migration file is generated with `create_table` statements for all 17 entities
- AND `alembic upgrade head` successfully creates all tables on PostgreSQL

#### Scenario: Migration run on clean PostgreSQL instance

- GIVEN a fresh PostgreSQL instance with no tables
- WHEN `alembic upgrade head` executes
- THEN all 17 tables are created
- AND `alembic current` reports the latest revision

#### Scenario: Downgrade rolls back last migration

- GIVEN `alembic upgrade head` has been applied
- WHEN `alembic downgrade -1` executes
- THEN the most recent migration's `downgrade()` is called
- AND `alembic current` reports the previous revision

#### Scenario: Migration detects schema drift

- GIVEN the database has tables but migration history is empty
- WHEN `alembic upgrade head` runs
- THEN Alembic detects drift and raises `InconsistentMigrationError`
- AND the operator must resolve manually before proceeding

#### Scenario: Migration with asyncpg connection failure

- GIVEN `DATABASE_URL` points to an unreachable PostgreSQL instance
- WHEN `alembic upgrade head` runs
- THEN `OperationalError` is raised with a connection-related message
- AND no migration state is recorded

#### Scenario: Empty migration (no model changes)

- GIVEN no changes to model metadata since last migration
- WHEN `alembic revision --autogenerate -m "no changes"` runs
- THEN autogenerate produces an empty migration (no ops)
- AND the empty migration is still valid (can upgrade/downgrade with no effect)
