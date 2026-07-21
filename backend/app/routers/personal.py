from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_active_verified_user
from backend.app.models.models import User
from backend.app.schemas.schemas import PersonalMilestoneCreate, PersonalMilestoneRead
from backend.app.services import crud

router = APIRouter(prefix="/personal", tags=["Personal Sector"])

DEFAULT_USER_ID = 1

@router.get("/", response_model=list[PersonalMilestoneRead])
async def read_personal_milestones(db: AsyncSession = Depends(get_db)):
    """
    Get all personal milestones for the default profile user.
    """
    return await crud.get_personal_milestones(db, user_id=DEFAULT_USER_ID)

@router.post("/", response_model=PersonalMilestoneRead, status_code=201)
async def add_personal_milestone(
    milestone: PersonalMilestoneCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_verified_user)
):
    """
    Create a new personal milestone. Protected: Requires DUNITE verified user authentication.
    """
    return await crud.create_personal_milestone(db, milestone, user_id=current_user.id)
