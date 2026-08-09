# Proposal: SQLite → AWS RDS PostgreSQL Migration

## Intent

Replace SQLite (`aiosqlite`) with AWS RDS PostgreSQL to support concurrent connections, enable proper connection pooling, and introduce Alembic-based migration management. The current `Base.metadata.create_all` approach is unsuitable for production and prevents schema evolution.

## Scope

### In Scope
- PostgreSQL connection config via `.env` (asyncpg driver, connection pool settings)
- Alembic initialization with async support
- Model compatibility updates: `autoincrement` → SERIAL, `datetime.now` → `server_default=func.now()`, `onupdate` → `server_onupdate`
- Repository layer rename: `sqllite_*` → `postgres_*` (9 repositories)
- DI wiring updates (4 dependency files)
- Entry point updates (`main.py` — seeder, init_db)
- `.env.example` with all PostgreSQL connection variables

### Out of Scope
- Data migration from existing SQLite (fresh start)
- Schema changes beyond PostgreSQL compatibility
- Native PostgreSQL UUID type adoption (keep String for now)
- Native PostgreSQL enum types (keep String storage)
- AWS RDS infrastructure provisioning (instance assumed ready)

## Capabilities

### New Capabilities
- `database-connection`: PostgreSQL async connection pool configuration via asyncpg, environment-driven
- `database-migrations`: Alembic async migration system for schema versioning

### Modified Capabilities
- None — existing business requirements unchanged; only infrastructure layer swaps

## Approach

1. **Alembic setup** — `alembic init`, async config, env.py with `AsyncEngine`
2. **Connection layer** — Replace `database/sqllite_database_session.py` with PostgreSQL engine (`asyncpg`), `async_sessionmaker`, connection pool (`pool_size`, `max_overflow`, `pool_timeout`)
3. **Model compatibility** — Update 9 model files: remove `autoincrement=True`, add `server_default=func.now()`, add `server_onupdate` where applicable
4. **Repository rename** — 9 files: `sqllite_*` → `postgres_*`, update imports
5. **DI wiring** — 4 dependency files: point to new repository implementations
6. **Entry point** — `main.py`: update `init_db`, remove/replace seeder
7. **Environment** — `.env.example` with all connection variables

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `database/sqllite_database_session.py` | Replaced | New PostgreSQL engine + session + pool config |
| `features/*/models/sqllite_*.py` (9 files) | Modified | Remove SQLite-specific patterns, add server defaults |
| `features/*/repositories/sqllite_*.py` (9 files) | Renamed + Modified | Rename to `postgres_*`, update imports |
| `features/*/dependency.py` (4 files) | Modified | Wire new repository implementations |
| `main.py` | Modified | Update init_db call, seeder reference |
| `alembic/` | New | Alembic migration directory and config |
| `.env.example` | New | PostgreSQL connection template |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Asyncpg compatibility gap with existing ORM queries | Low | All repos use standard SQLAlchemy ORM — no raw SQL |
| Connection pool misconfiguration under load | Medium | Start conservative (pool_size=5, max_overflow=10), tune after load testing |
| Alembic async migration failures | Low | Test `alembic upgrade head` against local PostgreSQL before each domain phase |
| `.env` secrets exposure | Low | Template only in `.env.example`; actual values in secret manager |

## Rollback Plan

1. Revert branch to `migracion-rds` pre-migration commit
2. Restore `.env` to point back to SQLite connection string
3. Remove `alembic/` directory (no production data to preserve — fresh start)
4. No data recovery needed (no migration of existing data)

## Dependencies

- AWS RDS PostgreSQL instance provisioned and accessible
- PostgreSQL 14+ (asyncpg compatible)
- `asyncpg` and `alembic` packages added to `requirements.txt` / `pyproject.toml`

## Success Criteria

- [ ] `alembic upgrade head` creates all 17 tables on fresh PostgreSQL instance
- [ ] All 9 repositories pass existing test suite against PostgreSQL
- [ ] Application starts and serves requests with PostgreSQL backend
- [ ] Connection pool handles 10+ concurrent requests without errors
- [ ] `.env.example` contains all required connection variables with documentation
- [ ] No references to `sqllite_*` remain in codebase
