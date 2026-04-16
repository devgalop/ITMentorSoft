from fastapi import FastAPI
from src.features.user_management.shared.init import router as user_management_router

app = FastAPI()
app.include_router(user_management_router, prefix="/users", tags=["users"])
