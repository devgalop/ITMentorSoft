# Environment Variables

This document lists all environment variables required to run the IT MentorSoft backend. Copy `.env.example` to `.env` and fill in the values.

> **Security notice:** Never commit real secret values to version control. Use a secrets manager or local `.env` file excluded via `.gitignore`.

---

## Authentication & JWT

| Variable | Example | Description |
|---|---|---|
| `JWT_SECRET_KEY` | `<your-secret-key>` | Secret key used to sign and verify JWT tokens. Must be a strong, unpredictable string. |
| `JWT_ALGORITHM` | `HS256` | Algorithm used for JWT signing. Supported: `HS256`, `HS384`, `HS512`. |
| `JWT_EXPIRATION_DELTA_SECONDS` | `1800` | Access token lifetime in seconds (default: 1800 = 30 min). |
| `RANDOM_TOKEN_EXPIRATION_DELTA_SECONDS` | `1800` | Lifetime in seconds for one-time random tokens (e.g. email verification, password recovery links). |
| `REFRESH_TOKEN_EXPIRATION_DELTA_SECONDS` | `604800` | Refresh token lifetime in seconds (default: 604800 = 7 days). |

---

## Database

| Variable | Example | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite+aiosqlite:///db/mentorsoft.db` | SQLAlchemy async connection string. Supports SQLite (dev) or PostgreSQL (prod). |
| `DATABASE_ADMIN_USERNAME` | `admin` | Username for the admin account created by the database seeder on first run. |
| `DATABASE_ADMIN_PASSWORD` | `<strong-password>` | Password for the seeded admin account. |
| `DATABASE_ADMIN_EMAIL` | `admin@example.com` | Email for the seeded admin account. |
| `DEFAULT_STUDENT_PASSWORD` | `<default-password>` | Default password assigned to student accounts created by the seeder. |
| `DEFAULT_TEACHER_PASSWORD` | `<default-password>` | Default password assigned to teacher accounts created by the seeder. |

---

## Email Notifications (Brevo)

| Variable | Example | Description |
|---|---|---|
| `BREVO_API_KEY` | `<your-brevo-api-key>` | API key for the Brevo (ex-Sendinblue) transactional email service. |
| `BREVO_BASE_API_URL` | `https://api.brevo.com/v3` | Base URL of the Brevo REST API. |
| `EMAIL_DEFAULT_SENDER` | `noreply@example.com` | Default "From" address used in outgoing notification emails. |

---

## URL Bases (Email Links)

| Variable | Example | Description |
|---|---|---|
| `RECOVERY_URL_BASE` | `http://localhost:8000/reset-password` | Base URL embedded in password-recovery emails. The frontend appends the recovery token to this path. |
| `REVIEW_URL_BASE` | `http://localhost:8000/assessments/pending-approval-questions` | Base URL embedded in assessment-review notification emails. Teachers use it to reach pending approval questions. |

---

## LLM Qualifier Services

| Variable | Example | Description |
|---|---|---|
| `GROQ_API_KEY` | `<your-groq-api-key>` | API key for the Groq inference platform, used as one of the LLM qualifier backends for assessment grading. |
| `OPENCODE_API_KEY` | `<your-opencode-api-key>` | API key for the OpenCode LLM endpoint, alternative qualifier backend. |
| `OPENCODE_API_URL` | `https://opencode.ai/zen/go/v1` | Full URL of the OpenCode LLM API endpoint. |

---

## Assessment Configuration

| Variable | Example | Description |
|---|---|---|
| `ASSESSMENT_QUALIFICATION_CHUNK_SIZE` | `5` | Number of questions sent to the LLM qualifier in a single batch. Controls throughput vs. cost trade-off during automated assessment grading. |
