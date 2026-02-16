from fastapi import APIRouter

router = APIRouter()

# Route for health check
@router.get("/health")
def health_check():
    return {"status": "ok"}
