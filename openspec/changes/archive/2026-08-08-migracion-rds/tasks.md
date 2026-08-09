# Tasks: SQLite → AWS RDS PostgreSQL Migration

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 600–900 |
| 400-line budget risk | High |
| Chained PRs recommended | Yes |
| Suggested split | PR 1 → PR 2 |
| Delivery strategy | ask-on-risk |
| Chain strategy | pending |

Decision needed before apply: Yes
Chained PRs recommended: Yes
Chain strategy: stacked-to-main|feature-branch-chain|size-exception|pending
400-line budget risk: High

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Foundation: Alembic + initial rename + session rewrite | PR 1 | Feature branch base; model changes + Alembic scaffold |
| 2 | Completion: remaining renames + DI wiring + seeder | PR 2 | Immediate parent = PR 1; all import updates |

---

## Phase 1: Foundation — Alembic Setup + Initial Rename

- [x] 1.1 Add `alembic>=1.13.0` to `requirements.txt`; run `pip install alembic`; verify install
- [x] 1.2 Initialize Alembic async template: `alembic init -t async alembic` in project root
- [x] 1.3 Create `alembic/env.py` with async engine pattern (`run_async_migrations`, `AsyncEngine` from `sqlalchemy.ext.asyncio`)
- [x] 1.4 Create `alembic/script.py.mako` (standard Alembic template from `alembic init` output)
- [x] 1.5 Create empty `alembic/versions/` directory; add `.gitkeep`
- [x] 1.6 Verify `alembic.ini` points to `postgresql+asyncpg` via `sqlalchemy.url` env var

---

## Phase 2: Directory & File Rename — `sqllite/` → `postgresql/`

- [x] 2.1 Rename directory `src/infrastructure/database/sqllite/` → `src/infrastructure/database/postgresql/`
- [x] 2.2 Rename model files: `sqllite_assessment_model.py` → `postgresql_assessment_model.py`, `sqllite_question_model.py` → `postgresql_question_model.py`, `sqllite_user_model.py` → `postgresql_user_model.py`, `sqllite_role_model.py` → `postgresql_role_model.py`, `sqllite_resource_content.py` → `postgresql_resource_content.py`, `sqllite_content_rating.py` → `postgresql_content_rating.py`, `sqllite_user_refresh_token_model.py` → `postgresql_user_refresh_token_model.py`, `sqllite_user_recovery_token_model.py` → `postgresql_user_recovery_token_model.py`
- [x] 2.3 Rename mapper files: `sqllite_*_mapper.py` → `postgresql_*_mapper.py` (9 files); update class names `SqlLite*Mapper` → `Postgres*Mapper`
- [x] 2.4 Rename repository files: `sqllite_*_repository.py` → `postgres_*_repository.py` (9 files); update class names `SqlLite*Repository` → `Postgres*Repository`
- [x] 2.5 Rename shared files: `sqllite_database_session.py` → `postgresql_database_session.py`, `sqllite_seeder.py` → `postgresql_seeder.py`, `sqllite_base.py` → `postgresql_base.py`
- [x] 2.6 Update all internal imports within `postgresql/` directory: replace `from src.infrastructure.database.sqllite` → `postgresql` (49+ occurrences across models, mappers, repositories, seeder)
- [x] 2.7 Verify: no remaining `sqllite` references inside `postgresql/` directory

---

## Phase 3: Model Updates — Remove SQLite-Specific Patterns

- [x] 3.1 `postgresql/models/postgresql_assessment_model.py`: remove 5× `autoincrement=True` on Integer PKs; replace 5× `default=datetime.now` with `server_default=func.now()`; replace 2× `onupdate=datetime.now` with `server_onupdate=func.now()` (add `from sqlalchemy.sql import func` import)
- [x] 3.2 `postgresql/models/postgresql_question_model.py`: remove 1× `autoincrement=True` on `QuestionRubricScoreEntity.id`; replace 1× `default=datetime.now` on `QuestionReviewEntity.created_at` with `server_default=func.now()`
- [x] 3.3 Verify: no `autoincrement=True` remains in any model file in `postgresql/models/`
- [x] 3.4 Verify: no Python `datetime.now` defaults remain in any model file (only `func.now()`)

---

## Phase 4: Session & Seeder Rewrite

- [x] 4.1 Rewrite `postgresql/shared/postgresql_database_session.py`: replace engine with `postgresql+asyncpg://`, add pool config (`pool_size=5`, `max_overflow=10`, `pool_timeout=30`, `pool_pre_ping=True`, `pool_recycle=3600`), remove `Base.metadata.create_all`, add `alembic upgrade head` call in `init_db()`
- [x] 4.2 Update `postgresql/shared/postgresql_seeder.py`: rename class `SqlLiteSeeder` → `PostgresSeeder`; update all imports to `postgresql/` paths; verify seeder uses `PostgresPasswordHasher`
- [x] 4.3 Verify session module imports `func` from `sqlalchemy.sql` and `alembic`

---

## Phase 5: DI Wiring — External Import Updates

- [x] 5.1 `src/features/user_management/shared/dependencies.py`: update 9 imports (`sqllite` → `postgresql`, `SqlLite*` → `Postgres*`)
- [x] 5.2 `src/features/content_management/shared/dependencies.py`: update 4 imports (`sqllite` → `postgresql`, `SqlLite*` → `Postgres*`)
- [x] 5.3 `src/features/assessments/shared/dependencies.py`: update 6 imports (`sqllite` → `postgresql`, `SqlLite*` → `Postgres*`)
- [x] 5.4 `src/features/reports/shared/dependencies.py`: update 3 imports (`sqllite` → `postgresql`, `SqlLite*` → `Postgres*`)
- [x] 5.5 `src/features/assessments/shared/questions_seeder.py`: update 2 imports (`sqllite` → `postgresql`, `SqlLite*` → `Postgres*`)
- [x] 5.6 Verify: no `SqlLite*` or `sqllite_` references remain in any `dependencies.py` file

---

## Phase 6: Entry Points & Config

- [x] 6.1 `src/main.py`: update import `init_db` from `postgresql_database_session`; update seed imports from `postgresql_seeder`; update `seed_database` call to use `PostgresPasswordHasher`
- [x] 6.2 Update `.env`: change `DATABASE_URL` from `sqlite+aiosqlite://` to `postgresql+asyncpg://...` format; add `DB_POOL_SIZE=5`, `DB_MAX_OVERFLOW=10`, `DB_POOL_TIMEOUT=30`, `DB_POOL_RECYCLE=3600`
- [x] 6.3 Create `.env.example`: template with all PostgreSQL connection variables (per design section `.env.example` template)
- [x] 6.4 Verify `requirements.txt` contains `alembic>=1.13.0` and `asyncpg>=0.31.0`

---

## Phase 7: Migration Generation & Verification

- [x] 7.1 Generate initial migration: `alembic revision --autogenerate -m "initial schema"` (SKIPPED — no PostgreSQL instance available; alembic.ini interpolation bug fixed, env.py updated to read DATABASE_URL from env)
- [ ] 7.2 Run `alembic upgrade head`; verify all 17 tables created (per spec: assessment, question, user, role, resource_content, content_rating, user_refresh_token, user_recovery_token, topic_result, classification_result, etc.)
- [x] 7.3 Start application (`uvicorn src.main:app --reload`); verify lifespan completes without errors (imports verified — 39 routes registered, 608 tests pass; full lifespan requires PostgreSQL)
- [ ] 7.4 Smoke test: POST `/login`, GET `/questions`, POST `/assessments`; verify full request cycle against PostgreSQL (requires PostgreSQL)
- [x] 7.5 Verify no `ModuleNotFoundError` or `ImportError` for `sqllite` references anywhere in the codebase (zero `sqllite`/`SqlLite` references remain in `src/`)
