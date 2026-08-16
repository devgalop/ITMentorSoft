# Database Connection Specification

## Purpose

Provides async PostgreSQL connection management with connection pooling, environment-driven configuration, and session lifecycle handling via SQLAlchemy 2.0 async + asyncpg.

---

## ADDED Requirements

### Requirement: Async PostgreSQL Engine

The system SHALL create an async PostgreSQL engine using `asyncpg` driver via `sqlalchemy.ext.asyncio.create_async_engine`.

The DATABASE_URL environment variable MUST be in the format `postgresql+asyncpg://user:pass@host:port/dbname`.

The engine MUST be instantiated once at module level and reused across all requests.

### Requirement: Connection Pool Configuration

The system SHALL configure the connection pool with the following settings:
- `pool_size=5` — minimum connections maintained
- `max_overflow=10` — additional connections allowed under load
- `pool_timeout=30` — seconds to wait for available connection
- `pool_pre_ping=True` — verify connection health before use
- `pool_recycle=3600` — recycle connections after 1 hour

### Requirement: Async Session Factory

The system SHALL create an `async_sessionmaker` bound to the engine with:
- `autocommit=False`
- `autoflush=False`
- `expire_on_commit=False`

### Requirement: Environment-Driven Configuration

All database configuration MUST be read from environment variables with no hardcoded values.

The system SHALL support the following environment variables:
- `DATABASE_URL` (required) — full connection string
- `DATABASE_ADMIN_USERNAME` (optional) — for seeder
- `DATABASE_ADMIN_PASSWORD` (optional) — for seeder

### Requirement: Database Session Dependency

The system MUST provide a `get_db()` async generator that yields an `AsyncSession` per request and handles cleanup via `async with`.

### Requirement: Directory Rename

The system SHALL rename `src/infrastructure/database/sqllite/` to `src/infrastructure/database/postgresql/`, updating all import paths accordingly.

---

## Scenarios

#### Scenario: Application starts with valid PostgreSQL connection

- GIVEN `DATABASE_URL` is set to a reachable PostgreSQL instance
- WHEN the FastAPI application starts
- THEN the async engine initializes with connection pool
- AND `alembic upgrade head` creates all tables successfully

#### Scenario: Application starts with unreachable database

- GIVEN `DATABASE_URL` points to an unreachable host or wrong port
- WHEN the FastAPI application starts or a request triggers DB access
- THEN an `OperationalError` or `OSError` is raised with a clear message
- AND the application does NOT start (lifespan fails)

#### Scenario: Connection pool exhausted under load

- GIVEN pool_size=5, max_overflow=10 (15 max connections)
- WHEN 16+ concurrent requests all need DB connections
- THEN requests wait up to `pool_timeout=30` seconds
- AND if no connection becomes available, `TimeoutError` is raised
- AND the system remains stable (no connection leaks)

#### Scenario: Stale connection reuse

- GIVEN a DB connection was idle for >1 hour (pool_recycle)
- WHEN a new request uses that connection from the pool
- THEN `pool_pre_ping=True` detects the stale connection
- AND the connection is replaced with a fresh one transparently

#### Scenario: Seeder uses admin credentials

- GIVEN `DATABASE_ADMIN_USERNAME` and `DATABASE_ADMIN_PASSWORD` are set
- WHEN the seeder runs at startup
- THEN it connects with admin credentials to create initial roles/users
