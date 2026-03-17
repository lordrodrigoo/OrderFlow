from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from src.api.dependencies import get_db

router = APIRouter()

@router.get("/health")
def health_check(db=Depends(get_db)):
    try:
        db.session.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "ok"}
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Service unhealthy") from exc
