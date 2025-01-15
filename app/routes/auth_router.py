from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.database.config import get_db
from app.database.models.user_model import User

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/register")
async def register(db: Session = Depends(get_db)):
    db.query(User).all()
    return {"message": "Register"}