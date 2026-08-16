## Exploration: SQLite → AWS RDS PostgreSQL Migration

### Current State

The ITMentorSoft FastAPI backend uses SQLite via `aiosqlite` for all data persistence. The database layer is built on SQLAlchemy 2.0 with a clean hexagonal (ports & adapters) architecture. The current stack:

- **Database**: SQLite (`sqlite+aiosqlite:///db/mentorsoft.db`)
- **ORM**: SQLAlchemy 2.0 async with `AsyncSession`, `DeclarativeBase`, `Mapped[T]`, `mapped_column()`
- **Session management**: `async_sessionmaker` with `autocommit=False`, `autoflush=False`, `expire_on_commit=False`
- **Migration system**: None — uses `Base.metadata.create_all` in `init_db()`
- **Connection pooling**: Not configured
- **DI architecture**: 9 abstract repository interfaces (ABC) wired to 9 concrete SQLite implementations

### SQLite-Specific Patterns Found

| Pattern | Location | Impact |
|---------|----------|--------|
| `autoincrement=True` on int PKs | 6 entities | PostgreSQL SERIAL/BIGSERIAL handles this natively |
| `datetime.now` Python defaults | 7 datetime columns | PostgreSQL prefers `server_default=func.now()` |
| `onupdate=datetime.now` | 2 entities (TopicResultEntity, ClassificationResultEntity) | Needs `server_onupdate` |
| Pipe-separated strings | 3 fields (related_topics, common_misconceptions, semantic_keywords) | No DB change needed — application-level |
| UUID as `String(uuid4().hex)` | Multiple entities | PostgreSQL has native UUID type |
| Enums stored as String | Multiple entities | No DB change needed — application-level |
| No connection pooling | Database config | PostgreSQL needs explicit pool config |
| No migration system | `init_db()` | Must add Alembic |

### File Inventory

#### Database Configuration
- `database/sqllite_database_session.py` — engine, sessionmaker, `get_db()`, `init_db()`

#### Model Entities (17 across 9 files)
- `features/user_management/models/sqllite_user_model.py`
- `features/user_management/models/sqllite_teacher_model.py`
- `features/user_management/models/sqllite_student_model.py`
- `features/content_management/models/sqllite_resource_content_model.py`
- `features/content_management/models/sqllite_topic_model.py`
- `features/assessments/models/sqllite_question_model.py`
- `features/assessments/models/sqllite_assessment_model.py`
- `features/assessments/models/sqllite_rubric_model.py`
- `features/reports/models/sqllite_topic_result_model.py`
- `features/reports/models/sqllite_classification_result_model.py`

#### Repositories (9 concrete implementations)
- `features/user_management/repositories/sqllite_user_repository.py`
- `features/user_management/repositories/sqllite_teacher_repository.py`
- `features/user_management/repositories/sqllite_student_repository.py`
- `features/content_management/repositories/sqllite_resource_content_repository.py`
- `features/content_management/repositories/sqllite_topic_repository.py`
- `features/assessments/repositories/sqllite_questions_repository.py`
- `features/assessments/repositories/sqllite_assessment_repository.py`
- `features/assessments/repositories/sqllite_rubric_repository.py`
- `features/reports/repositories/sqllite_topic_result_repository.py`

#### Dependency Injection Wiring
- `features/user_management/dependency.py`
- `features/reports/dependency.py`
- `features/content_management/dependency.py`
- `features/assessments/dependency.py`

#### Entry Points
- `main.py` — imports `init_db` and `sqllite_seeder`

### Approaches

1. **Big Bang Replacement** — Swap all `sqllite_*` files to `postgres_*` in one change
   - Pros: Fastest path, single PR, no dual-maintenance
   - Cons: High risk, no incremental validation, large review surface
   - Effort: Medium

2. **Strangler Fig Pattern** — Introduce PostgreSQL alongside SQLite, route traffic incrementally
   - Pros: Lower risk, can validate per-feature, easier rollback
   - Cons: Requires dual database setup during transition, more complex CI
   - Effort: High

3. **Phased Migration** — One domain at a time (e.g., user_management → content_management → assessments → reports)
   - Pros: Manageable review size, each phase is independently verifiable
   - Cons: Longer total timeline, dual code paths during transition
   - Effort: Medium

4. **Abstraction Layer Injection** — Introduce a database-agnostic repository base, then swap implementations
   - Pros: Cleanest separation, easiest to test, future-proof
   - Cons: Significant refactoring to add abstraction layer
   - Effort: High

### Recommendation

**Phased Migration with Alembic** — Given the clean hexagonal architecture, the swap is isolated to infrastructure layer + DI wiring. Recommended approach:

1. Add Alembic for migration management
2. Create PostgreSQL-compatible models (minimal changes — SERIAL, server_default, UUID type)
3. Phase per feature domain: user_management → content_management → assessments → reports
4. Use feature flags or environment-based routing during transition if zero-downtime is needed

This keeps each PR under 400 lines, validates each domain independently, and leaves a migration trail.

### Risks

- **Data migration**: Moving existing SQLite data to PostgreSQL requires a migration script with proper UUID handling and datetime normalization
- **Connection string secrets**: AWS RDS credentials must not be committed; needs environment variables or AWS Secrets Manager
- **Enum handling**: PostgreSQL enum types differ from SQLite; String storage is safer but loses DB-level constraints
- **Transaction behavior**: SQLite and PostgreSQL have different isolation levels; verify transaction boundaries
- **NULL handling**: SQLite treats NULL differently in some contexts; review NOT NULL constraints
- **String PKs**: Entities using `String` for UUIDs may need type coersion on queries

### Ready for Proposal

**Yes** — The codebase analysis is complete. The hexagonal architecture isolates the database swap to infrastructure layer + DI wiring. Recommend moving to `sdd-propose` to formalize scope, rollback plan, and delivery strategy.

Key decisions needed from proposal phase:
1. Zero-downtime requirement? (affects approach)
2. Data migration strategy (live migration vs. maintenance window)
3. AWS RDS setup (existing instance or new?)
4. Review budget — 4 feature domains suggest chained PRs per domain
