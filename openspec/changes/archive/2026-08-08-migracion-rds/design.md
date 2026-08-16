# Design: SQLite → AWS RDS PostgreSQL Migration

## Technical Approach

Replace the SQLite infrastructure adapter with PostgreSQL while preserving the hexagonal architecture. The swap is purely infrastructure-level: rename the `sqllite/` directory to `postgresql/`, update SQLAlchemy engine configuration, add Alembic for schema management, and fix model patterns that are SQLite-specific. Business logic (features layer) remains untouched — only DI wiring imports change.

Key insight from codebase analysis: **all 9 repositories use standard SQLAlchemy ORM** (`select`, `selectinload`, `session.add`, `session.commit`). Zero raw SQL. This makes the migration highly mechanical — a rename + config swap.

## Architecture Decisions

| Decision | Choice | Alternatives | Rationale |
|----------|--------|-------------|-----------|
| Migration strategy | Big Bang rename | Strangler Fig, Phased | No production data to migrate, single PR is simpler to review, hexagonal arch isolates change |
| Schema management | Alembic async | `create_all` (current) | `create_all` is dev-only; Alembic enables versioned migrations for production |
| `autoincrement=True` | Remove entirely | Keep (harmless on PG) | PostgreSQL SERIAL is automatic for `Integer` PKs; removing is cleaner |
| `datetime.now` defaults | `server_default=func.now()` | Keep Python-side defaults | Server-side defaults are authoritative, survive direct SQL inserts, timezone-safe |
| `onupdate=datetime.now` | `server_onupdate=func.now()` + keep Python-side fallback | Remove Python-side entirely | `server_onupdate` doesn't work reliably in all SQLAlchemy versions; keep `onupdate` as fallback |
| UUID type | Keep `String` | Native `UUID` type | Avoids cascading type changes across mappers and domain models; future optimization |
| Connection pool | Conservative defaults | Aggressive (pool_size=20) | Unknown RDS instance size; start safe, tune after load testing |
| Pipe-separated strings | No change | Normalize to junction tables | Application-level concern, out of scope for infrastructure migration |

## Data Flow

```
FastAPI Router
    │
    ▼
Handler (feature layer)
    │
    ▼
DI dependencies.py ──→ get_db() ──→ async_sessionmaker ──→ AsyncSession
    │                                                        │
    ▼                                                        ▼
Repository (abstract)                              PostgreSQL Engine
    │                                              (asyncpg + pool)
    ▼                                                        │
Repository (concrete)                                        │
    │                                                        │
    ▼                                                        ▼
SQLAlchemy ORM ────────────────────────────────────→ AWS RDS PostgreSQL
(select, selectinload, session.add)
```

## File Changes

### New Files

| File | Description |
|------|-------------|
| `alembic.ini` | Alembic configuration pointing to PostgreSQL `DATABASE_URL` |
| `alembic/env.py` | Async migration environment using `AsyncEngine` + `run_async_migrations()` |
| `alembic/script.py.mako` | Migration template (standard Alembic boilerplate) |
| `alembic/versions/` | Empty directory for migration scripts |
| `.env.example` | Template with all PostgreSQL connection variables |

### Renamed Directory

`src/infrastructure/database/sqllite/` → `src/infrastructure/database/postgresql/`

All 28 files within are renamed `sqllite_*` → `postgresql_*` (or `postgres_*` for repos).

### Modified Files

| File | Action | Changes |
|------|--------|---------|
| `postgresql/shared/postgresql_database_session.py` | Rewrite | Engine config: `postgresql+asyncpg://`, pool params, remove `create_all`, add Alembic `upgrade head` call |
| `postgresql/models/postgresql_assessment_model.py` | Modify | Remove 5× `autoincrement=True`; replace 5× `default=datetime.now` with `server_default=func.now()`; replace 2× `onupdate` with `server_onupdate=func.now()` |
| `postgresql/models/postgresql_question_model.py` | Modify | Remove 1× `autoincrement=True` on `QuestionRubricScoreEntity.id`; replace 1× `default=datetime.now` on `QuestionReviewEntity.created_at` |
| `postgresql/models/postgresql_user_model.py` | Rename only | Import path update for `Base` |
| `postgresql/models/postgresql_role_model.py` | Rename only | Import path update for `Base` |
| `postgresql/models/postgresql_resource_content.py` | Rename only | Import path update for `Base` |
| `postgresql/models/postgresql_content_rating.py` | Rename only | Import path update for `Base` |
| `postgresql/models/postgresql_user_refresh_token_model.py` | Rename only | Import path update for `Base` |
| `postgresql/models/postgresql_user_recovery_token_model.py` | Rename only | Import path update for `Base` |
| All 9 mapper files | Rename + import update | Class rename `SqlLite*` → `Postgres*`, update internal imports |
| All 9 repository files | Rename + import update | Class rename `SqlLite*` → `Postgres*`, update internal imports |
| `postgresql/shared/postgresql_seeder.py` | Rename + import update | Update all model/session imports |
| `src/features/user_management/shared/dependencies.py` | Modify | 9 import lines: `sqllite` → `postgresql`, class names `SqlLite*` → `Postgres*` |
| `src/features/content_management/shared/dependencies.py` | Modify | 4 import lines updated |
| `src/features/assessments/shared/dependencies.py` | Modify | 6 import lines updated |
| `src/features/reports/shared/dependencies.py` | Modify | 3 import lines updated |
| `src/features/assessments/shared/questions_seeder.py` | Modify | 2 import lines updated (discovered during analysis — not in original spec) |
| `src/main.py` | Modify | 2 import lines: `sqllite_database_session` → `postgresql_database_session`, `sqllite_seeder` → `postgresql_seeder` |
| `requirements.txt` | Modify | Add `alembic>=1.13.0`; `asyncpg` already present (`0.31.0`) |
| `.env` | Modify | Update `DATABASE_URL` to `postgresql+asyncpg://...` format |

## Interfaces / Contracts

### Connection Configuration (`.env` variables)

```
DATABASE_URL=postgresql+asyncpg://<user>:<password>@<host>:<port>/<dbname>
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600
```

### Engine Configuration (`postgresql_database_session.py`)

```python
engine = create_async_engine(
    DATABASE_URL,
    pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
    max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "10")),
    pool_timeout=int(os.getenv("DB_POOL_TIMEOUT", "30")),
    pool_pre_ping=True,
    pool_recycle=int(os.getenv("DB_POOL_RECYCLE", "3600")),
)
```

### Alembic Async `env.py` Pattern

```python
from sqlalchemy.ext.asyncio import create_async_engine

async def run_migrations_online():
    connectable = create_async_engine(config.get_main_option("sqlalchemy.url"))
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()
```

### Model Change Pattern (assessment_model example)

```python
# BEFORE (SQLite)
id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

# AFTER (PostgreSQL)
from sqlalchemy.sql import func
id: Mapped[int] = mapped_column(Integer, primary_key=True)  # SERIAL auto
created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=datetime.now, server_onupdate=func.now())
```

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | Model entity creation with server defaults | Verify entities instantiate without errors; `server_default` columns accept `None` |
| Integration | `alembic upgrade head` on local PostgreSQL | Run against Docker PostgreSQL; verify all 17 tables created |
| Integration | All 9 repositories CRUD operations | Run existing test suite (if any) against PostgreSQL; or manual smoke tests via API |
| E2E | Application startup + seeder | `uvicorn src.main:app` → verify lifespan completes, seed data exists |
| E2E | API endpoint smoke test | POST login, GET questions, POST assessment — verify full request cycle |

## Migration Execution Plan

**Order of operations for the implementer:**

1. **Add Alembic dependency**: `pip install alembic` → update `requirements.txt`
2. **Rename directory**: `src/infrastructure/database/sqllite/` → `src/infrastructure/database/postgresql/`
3. **Rename all files**: `sqllite_*` → `postgresql_*` (models, mappers) and `sqllite_*` → `postgres_*` (repositories)
4. **Rewrite session module**: `postgresql_database_session.py` with asyncpg engine + pool config
5. **Update model files**: Remove `autoincrement`, add `server_default=func.now()`, add `server_onupdate`
6. **Update all internal imports**: Within the renamed directory, fix all `from src.infrastructure.database.sqllite` → `postgresql`
7. **Update DI wiring**: 4 dependency files + `questions_seeder.py`
8. **Update `main.py`**: Import paths for `init_db` and seeders
9. **Initialize Alembic**: `alembic init -t async alembic`, configure `env.py` for async
10. **Update `.env`**: Change `DATABASE_URL` to PostgreSQL format
11. **Create `.env.example`**: Template with all variables
12. **Generate initial migration**: `alembic revision --autogenerate -m "initial schema"`
13. **Test**: `alembic upgrade head` → start app → verify endpoints

## `.env.example` Template

```env
# JWT Configuration
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DELTA_SECONDS=1800

# Token Configuration
RANDOM_TOKEN_EXPIRATION_DELTA_SECONDS=1800
REFRESH_TOKEN_EXPIRATION_DELTA_SECONDS=604800

# Database — PostgreSQL (AWS RDS)
DATABASE_URL=postgresql+asyncpg://<username>:<password>@<host>:<port>/<database>
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600

# Database Seeder
DATABASE_ADMIN_USERNAME=admin
DATABASE_ADMIN_PASSWORD=your-admin-password
DATABASE_ADMIN_EMAIL=admin@example.com
DEFAULT_STUDENT_PASSWORD=your-student-password
DEFAULT_TEACHER_PASSWORD=your-teacher-password
DEFAULT_USER_PASSWORD=your-user-password

# Email (Brevo)
BREVO_API_KEY=your-brevo-api-key
BREVO_BASE_API_URL=https://api.brevo.com/v3
EMAIL_DEFAULT_SENDER=noreply@example.com

# URLs
RECOVERY_URL_BASE=http://localhost:8000/reset-password
REVIEW_URL_BASE=http://localhost:8000/assessments/pending-approval-questions
LOGIN_URL_BASE=http://localhost:8000/login

# AI Services
GROQ_API_KEY=your-groq-api-key
OPENCODE_API_KEY=your-opencode-api-key
OPENCODE_API_URL=https://opencode.ai/zen/go/v1

# Application
ASSESSMENT_QUALIFICATION_CHUNK_SIZE=5
```

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| RDS SSL requirement | Add `connect_args={"ssl": "require"}` to engine if RDS enforces SSL; make configurable via env var |
| Pool exhaustion under load | Conservative defaults (5+10=15 max connections); monitor with `pool.status()`; tune via env vars |
| Stale connections after RDS failover | `pool_pre_ping=True` detects and replaces dead connections; `pool_recycle=3600` recycles hourly |
| `server_onupdate` not firing | Keep `onupdate=datetime.now` as Python-side fallback alongside `server_onupdate` |
| `questions_seeder.py` missed | Discovered during analysis — must update imports or seeder will crash at startup |
| Alembic async misconfiguration | Use `alembic init -t async` template; verify `run_async_migrations` pattern in `env.py` |

## Open Questions

- [ ] Does the RDS instance require SSL? If yes, add `connect_args` SSL configuration
- [ ] Should `alembic upgrade head` run automatically at startup (in `init_db()`) or only via CLI? Recommendation: CLI only for production, auto for dev
- [ ] Are there any existing tests that reference `sqllite_*` paths? Need to update test imports too
