from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.schemas.schemas import ProfessionalMilestoneCreate, ProfessionalMilestoneRead
from backend.app.services import crud

router = APIRouter(prefix="/professional", tags=["Professional Sector"])

DEFAULT_USER_ID = 1

@router.get("/", response_model=list[ProfessionalMilestoneRead])
async def read_professional_milestones(db: AsyncSession = Depends(get_db)):
    """
    Get all professional milestones for the default profile user.
    """
    return await crud.get_professional_milestones(db, user_id=DEFAULT_USER_ID)

@router.post("/", response_model=ProfessionalMilestoneRead, status_code=201)
async def add_professional_milestone(
    milestone: ProfessionalMilestoneCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new professional milestone (corporate role, industry placement).
    """
    return await crud.create_professional_milestone(db, milestone, user_id=DEFAULT_USER_ID)
