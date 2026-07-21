from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_active_verified_user
from backend.app.models.models import User
from backend.app.schemas.schemas import EntrepreneurialMilestoneCreate, EntrepreneurialMilestoneRead
from backend.app.services import crud

router = APIRouter(prefix="/entrepreneurial", tags=["Entrepreneurial Sector"])

DEFAULT_USER_ID = 1

@router.get("/", response_model=list[EntrepreneurialMilestoneRead])
async def read_entrepreneurial_milestones(db: AsyncSession = Depends(get_db)):
    """
    Get all entrepreneurial milestones for the default profile user.
    """
    return await crud.get_entrepreneurial_milestones(db, user_id=DEFAULT_USER_ID)

@router.post("/", response_model=EntrepreneurialMilestoneRead, status_code=201)
async def add_entrepreneurial_milestone(
    milestone: EntrepreneurialMilestoneCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_verified_user)
):
    """
    Create a new entrepreneurial milestone. Protected: Requires DUNITE verified user authentication.
    """
    return await crud.create_entrepreneurial_milestone(db, milestone, user_id=current_user.id)
