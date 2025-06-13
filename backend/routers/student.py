from fastapi import APIRouter

router = APIRouter(prefix="/student", tags=["student"])

# Placeholder routes

@router.get("/dashboard")
async def student_dashboard():
    return {"msg": "Student dashboard - routes to be implemented"}