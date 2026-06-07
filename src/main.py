from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.features.assessments.shared.questions_seeder import seed_questions
from src.features.user_management.shared.init import router as user_management_router
from src.features.content_management.shared.init import (
    router as content_management_router,
)
from src.features.assessments.shared.init import router as assessments_router
from src.infrastructure.database.sqllite.shared.sqllite_database_session import init_db
from src.infrastructure.database.sqllite.shared.sqllite_seeder import seed_database
from src.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up the application...")
    await init_db()
    await seed_database(BcryptPasswordHasher())
    await seed_questions()
    yield
    print("Shutting down the application...")


app = FastAPI(lifespan=lifespan)

app.include_router(user_management_router, prefix="/users", tags=["users"])
app.include_router(content_management_router, prefix="/content", tags=["content"])
app.include_router(assessments_router, prefix="/assessments", tags=["assessments"])
