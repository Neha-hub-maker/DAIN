from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.schemas.schemas import SocialImpactMilestoneCreate, SocialImpactMilestoneRead
from backend.app.services import crud

router = APIRouter(prefix="/social-impact", tags=["Social Impact Sector"])

DEFAULT_USER_ID = 1

@router.get("/", response_model=list[SocialImpactMilestoneRead])
async def read_social_impact_milestones(db: AsyncSession = Depends(get_db)):
    """
    Get all social impact milestones for the default profile user.
    """
    return await crud.get_social_impact_milestones(db, user_id=DEFAULT_USER_ID)

@router.post("/", response_model=SocialImpactMilestoneRead, status_code=201)
async def add_social_impact_milestone(
    milestone: SocialImpactMilestoneCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new social impact milestone (volunteer role, community scaling initiative).
    """
    return await crud.create_social_impact_milestone(db, milestone, user_id=DEFAULT_USER_ID)
