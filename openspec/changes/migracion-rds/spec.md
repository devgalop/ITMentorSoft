# Delta: SQLite → PostgreSQL Infrastructure Migration

## Scope

This delta covers the infrastructure layer swap from SQLite (`aiosqlite`) to PostgreSQL (`asyncpg`) across models, repositories, DI wiring, and entry points. Business logic remains unchanged.

---

## MODIFIED Requirements

### Requirement: Directory Rename — `sqllite/` → `postgresql/`

The entire directory `src/infrastructure/database/sqllite/` SHALL be renamed to `src/infrastructure/database/postgresql/`.

All import paths referencing the old directory MUST be updated to the new path.

(Previously: `src/infrastructure/database/sqllite/` — no PostgreSQL infrastructure existed)

#### Scenario: Directory renamed and imports updated

- GIVEN the directory is renamed from `sqllite` to `postgresql`
- WHEN any Python file imports from the old `sqllite` path
- THEN the import fails with `ModuleNotFoundError`
- AND CI/import checks catch any remaining `sqllite` references

---

### Requirement: Database Session — SQLite Engine → PostgreSQL Engine

`src/infrastructure/database/postgresql/shared/postgresql_database_session.py` SHALL replace `sqllite_database_session.py`:

- `create_async_engine` MUST use `postgresql+asyncpg://` driver
- Connection pool config MUST be applied: `pool_size=5`, `max_overflow=10`, `pool_timeout=30`, `pool_pre_ping=True`, `pool_recycle=3600`
- `Base.metadata.create_all` in `init_db()` MUST be replaced by Alembic migration calls

(Previously: SQLite engine with no pooling, `create_all` at startup)

#### Scenario: PostgreSQL engine initializes with pool

- GIVEN `DATABASE_URL` is set to a valid PostgreSQL connection string
- WHEN the application starts
- THEN `create_async_engine` creates an engine with `pool_size=5`
- AND `async_sessionmaker` binds to that engine

#### Scenario: Database unreachable at startup

- GIVEN `DATABASE_URL` points to an unreachable host
- WHEN `init_db()` or any DB operation runs
- THEN `AsyncEngine` raises `OperationalError` or `OSError`
- AND the application lifespan fails with a clear error

---

### Requirement: Model Compatibility — Remove SQLite-Specific Patterns

The following patterns MUST be removed from all model files in `src/infrastructure/database/postgresql/models/`:

| Pattern | Action | Files |
|---------|--------|-------|
| `autoincrement=True` on `Integer` PKs | Remove (PostgreSQL SERIAL handles this) | `sqllite_assessment_model.py` (5 fields), `sqllite_question_model.py` (1 field) |
| `default=datetime.now` Python callable | Replace with `server_default=func.now()` | 7 datetime columns across 3 files |
| `onupdate=datetime.now` | Replace with `server_onupdate=func.now()` | 2 columns: `TopicResultEntity.updated_at`, `ClassificationResultEntity.updated_at` |

(Previously: Python-side `datetime.now` defaults; `autoincrement=True` explicit)

#### Scenario: Integer PK without autoincrement

- GIVEN `AssessmentQuizEntity.id` has `Integer, primary_key=True, autoincrement=True`
- WHEN the migration autogenerates
- THEN the resulting column is `id SERIAL PRIMARY KEY` (not `INTEGER AUTOINCREMENT`)
- AND insert operations work without explicit ID

#### Scenario: Datetime with server-side default

- GIVEN `AssessmentEntity.created_at` uses `default=datetime.now`
- WHEN the migration autogenerates
- THEN the column uses `DEFAULT now()` at the DB level
- AND new rows get a DB-generated timestamp even if app is slow

#### Scenario: Datetime with server_onupdate

- GIVEN `TopicResultEntity.updated_at` uses `onupdate=datetime.now`
- WHEN an UPDATE statement modifies the row
- THEN the `updated_at` column uses `DEFAULT now()` on UPDATE via `server_onupdate`
- AND the application does NOT send `updated_at` in the UPDATE statement

---

### Requirement: Repository Rename — `sqllite_*` → `postgres_*`

9 repository files in `src/infrastructure/database/postgresql/repository/` SHALL be renamed:

| Old Name | New Name |
|----------|----------|
| `sqllite_user_repository.py` | `postgres_user_repository.py` |
| `sqllite_role_repository.py` | `postgres_role_repository.py` |
| `sqllite_user_refresh_token_repository.py` | `postgres_user_refresh_token_repository.py` |
| `sqllite_user_recovery_token_repository.py` | `postgres_user_recovery_token_repository.py` |
| `sqllite_resource_content_repository.py` | `postgres_resource_content_repository.py` |
| `sqllite_questions_repository.py` | `postgres_questions_repository.py` |
| `sqllite_questions_assessment_repository.py` | `postgres_questions_assessment_repository.py` |
| `sqllite_assessment_repository.py` | `postgres_assessment_repository.py` |
| `sqllite_report_repository.py` | `postgres_report_repository.py` |

Class names within files SHALL also rename: `SqlLite*Repository` → `Postgres*Repository`, `SqlLite*Mapper` → `Postgres*Mapper`.

(Previously: SQLite repository implementations with `SqlLite` prefix)

#### Scenario: Repository renamed and imports updated

- GIVEN a repository file is renamed from `sqllite_user_repository.py` to `postgres_user_repository.py`
- WHEN `SqlLiteUserRepository` is referenced in DI or tests
- THEN the reference must be updated to `PostgresUserRepository`
- AND all imports in dependency files are updated

---

### Requirement: DI Wiring Updates — Point to New Repository Implementations

4 dependency files MUST update imports from `sqllite_*` to `postgres_*`:

- `src/features/user_management/shared/dependencies.py`
- `src/features/content_management/shared/dependencies.py`
- `src/features/assessments/shared/dependencies.py`
- `src/features/reports/shared/dependencies.py`

Each file MUST update:
- Import paths: `sqllite_database_session` → `postgresql_database_session`
- Repository class names: `SqlLite*Repository` → `Postgres*Repository`
- Mapper class names: `SqlLite*Mapper` → `Postgres*Mapper`

(Previously: `SqlLite*Repository` and `SqlLite*Mapper` injected via `get_db`)

#### Scenario: DI wiring updated in user_management

- GIVEN `features/user_management/shared/dependencies.py` is updated
- WHEN `get_user_repository()` is called
- THEN it returns `PostgresUserRepository(session_factory=session, user_mapper=PostgresUserMapper)`
- AND no `SqlLite*` references remain in the file

---

### Requirement: Entry Point Updates — `main.py`

`src/main.py` MUST be updated:

- Import `init_db` from `src/infrastructure/database/postgresql/shared/postgresql_database_session` (was `sqllite_database_session`)
- Import `seed_database` and `seed_assessments` from `src/infrastructure/database/postgresql/shared/postgresql_seeder` (was `sqllite_seeder`)
- The `seed_database` call MUST be updated to use `PostgresPasswordHasher` if the hasher has DB dependencies
- Remove or replace `sqllite_seeder` import and calls

(Previously: `sqllite_database_session`, `sqllite_seeder` imported and called)

#### Scenario: main.py updated for PostgreSQL

- GIVEN `main.py` imports from `postgresql/` paths
- WHEN the FastAPI lifespan runs
- THEN `init_db()` triggers Alembic migrations (not `create_all`)
- AND `seed_database()` seeds initial roles/admin via PostgreSQL

---

### Requirement: Seeder Renamed and Updated

`src/infrastructure/database/postgresql/shared/postgresql_seeder.py` SHALL replace `sqllite_seeder.py` with:
- Same seed logic (roles, admin user, assessments)
- All imports updated to PostgreSQL-compatible paths
- Uses `PostgresPasswordHasher` if needed

---

## RENAMED Requirements

### Requirement: `sqllite_seeder.py` → `postgresql_seeder.py`

The seeder module SHALL be renamed and updated to use PostgreSQL-compatible imports.

(Reason: Consistency with directory rename; seeder must use new repository implementations)

(Migration: Update `main.py` import path from `sqllite_seeder` to `postgresql_seeder`)

---

## Coverage Summary

| Category | Covered |
|----------|---------|
| Happy path — PostgreSQL connects and pools correctly | ✓ |
| Happy path — Alembic creates all tables | ✓ |
| Edge case — DB unreachable | ✓ |
| Edge case — Pool exhausted | ✓ |
| Edge case — Stale connection recycled | ✓ |
| Edge case — Autogenerate empty migration | ✓ |
| Error state — Migration on unreachable DB | ✓ |
| Error state — Directory rename with stale imports | ✓ |
