from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.schemas.schemas import AcademicMilestoneCreate, AcademicMilestoneRead
from backend.app.services import crud

router = APIRouter(prefix="/academic", tags=["Academic Sector"])

# We default to user_id=1 for MVP simplicity
DEFAULT_USER_ID = 1

@router.get("/", response_model=list[AcademicMilestoneRead])
async def read_academic_milestones(db: AsyncSession = Depends(get_db)):
    """
    Get all academic milestones for the default profile user.
    """
    return await crud.get_academic_milestones(db, user_id=DEFAULT_USER_ID)

@router.post("/", response_model=AcademicMilestoneRead, status_code=201)
async def add_academic_milestone(
    milestone: AcademicMilestoneCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new academic milestone (publication, research, CGPA milestone).
    """
    return await crud.create_academic_milestone(db, milestone, user_id=DEFAULT_USER_ID)
