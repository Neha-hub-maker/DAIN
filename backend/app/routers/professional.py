from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_active_verified_user
from backend.app.models.models import User
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
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_verified_user)
):
    """
    Create a new professional milestone. Protected: Requires DUNITE verified user authentication.
    """
    return await crud.create_professional_milestone(db, milestone, user_id=current_user.id)
