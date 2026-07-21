from typing import Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.services.media_packager import generate_press_kit
from backend.app.services.media_router import route_media_package
from sqlalchemy.future import select
from backend.app.models.models import (
    User,
    AcademicMilestone,
    ProfessionalMilestone,
    EntrepreneurialMilestone,
    SocialImpactMilestone,
    PersonalMilestone,
)
from backend.app.schemas.schemas import (
    AcademicMilestoneCreate,
    ProfessionalMilestoneCreate,
    EntrepreneurialMilestoneCreate,
    SocialImpactMilestoneCreate,
    PersonalMilestoneCreate,
    AdminSubmissionItem,
)

# ----------------------------------------------------
# DEFAULT USER SEED LOGIC
# ----------------------------------------------------
async def seed_default_user(db: AsyncSession) -> User:
    """
    Ensure that a default user (id=1) exists in the database.
    This simplifies MVP API calls by eliminating complex authentication.
    """
    result = await db.execute(select(User).where(User.id == 1))
    user = result.scalars().first()
    if not user:
        user = User(
            id=1,
            name="Default Profile User",
            email="developer@dain.local",
            role="admin"
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        print("Successfully seeded default profile user (id=1)")
    return user

# ----------------------------------------------------
# ACADEMIC MILESTONES CRUD
# ----------------------------------------------------
async def get_academic_milestones(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(AcademicMilestone)
        .where(AcademicMilestone.user_id == user_id)
        .order_by(AcademicMilestone.id.desc())
    )
    return result.scalars().all()

async def create_academic_milestone(db: AsyncSession, milestone: AcademicMilestoneCreate, user_id: int):
    data = milestone.model_dump()
    if not data.get("status"):
        data["status"] = "pending_validation"
    db_milestone = AcademicMilestone(**data, user_id=user_id)
    db.add(db_milestone)
    await db.commit()
    await db.refresh(db_milestone)
    return db_milestone

# ----------------------------------------------------
# PROFESSIONAL MILESTONES CRUD
# ----------------------------------------------------
async def get_professional_milestones(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(ProfessionalMilestone)
        .where(ProfessionalMilestone.user_id == user_id)
        .order_by(ProfessionalMilestone.id.desc())
    )
    return result.scalars().all()

async def create_professional_milestone(db: AsyncSession, milestone: ProfessionalMilestoneCreate, user_id: int):
    data = milestone.model_dump()
    if not data.get("status"):
        data["status"] = "pending_validation"
    db_milestone = ProfessionalMilestone(**data, user_id=user_id)
    db.add(db_milestone)
    await db.commit()
    await db.refresh(db_milestone)
    return db_milestone

# ----------------------------------------------------
# ENTREPRENEURIAL MILESTONES CRUD
# ----------------------------------------------------
async def get_entrepreneurial_milestones(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(EntrepreneurialMilestone)
        .where(EntrepreneurialMilestone.user_id == user_id)
        .order_by(EntrepreneurialMilestone.id.desc())
    )
    return result.scalars().all()

async def create_entrepreneurial_milestone(db: AsyncSession, milestone: EntrepreneurialMilestoneCreate, user_id: int):
    data = milestone.model_dump()
    if not data.get("status"):
        data["status"] = "pending_validation"
    db_milestone = EntrepreneurialMilestone(**data, user_id=user_id)
    db.add(db_milestone)
    await db.commit()
    await db.refresh(db_milestone)
    return db_milestone

# ----------------------------------------------------
# SOCIAL IMPACT MILESTONES CRUD
# ----------------------------------------------------
async def get_social_impact_milestones(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(SocialImpactMilestone)
        .where(SocialImpactMilestone.user_id == user_id)
        .order_by(SocialImpactMilestone.id.desc())
    )
    return result.scalars().all()

async def create_social_impact_milestone(db: AsyncSession, milestone: SocialImpactMilestoneCreate, user_id: int):
    data = milestone.model_dump()
    if not data.get("status"):
        data["status"] = "pending_validation"
    db_milestone = SocialImpactMilestone(**data, user_id=user_id)
    db.add(db_milestone)
    await db.commit()
    await db.refresh(db_milestone)
    return db_milestone

# ----------------------------------------------------
# PERSONAL MILESTONES CRUD
# ----------------------------------------------------
async def get_personal_milestones(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(PersonalMilestone)
        .where(PersonalMilestone.user_id == user_id)
        .order_by(PersonalMilestone.id.desc())
    )
    return result.scalars().all()

async def create_personal_milestone(db: AsyncSession, milestone: PersonalMilestoneCreate, user_id: int):
    data = milestone.model_dump()
    if not data.get("status"):
        data["status"] = "pending_validation"
    db_milestone = PersonalMilestone(**data, user_id=user_id)
    db.add(db_milestone)
    await db.commit()
    await db.refresh(db_milestone)
    return db_milestone

# ----------------------------------------------------
# ADMIN REVIEW PIPELINE SERVICES
# ----------------------------------------------------
DOMAIN_MODEL_MAP = {
    "academic": (AcademicMilestone, "title"),
    "professional": (ProfessionalMilestone, "role"),
    "entrepreneurial": (EntrepreneurialMilestone, "venture_name"),
    "social-impact": (SocialImpactMilestone, "role"),
    "personal": (PersonalMilestone, "title"),
}

async def list_admin_submissions(
    db: AsyncSession,
    status_filter: Optional[str] = None,
    domain_filter: Optional[str] = None
) -> list[dict[str, Any]]:
    submissions = []
    
    target_domains = [domain_filter] if domain_filter in DOMAIN_MODEL_MAP else list(DOMAIN_MODEL_MAP.keys())
    
    for domain in target_domains:
        model_cls, title_attr = DOMAIN_MODEL_MAP[domain]
        query = select(model_cls)
        if status_filter:
            query = query.where(model_cls.status == status_filter)
        query = query.order_by(model_cls.id.desc())
        
        result = await db.execute(query)
        items = result.scalars().all()
        
        for item in items:
            title_val = getattr(item, title_attr, f"{domain.capitalize()} Item #{item.id}")
            details = {c.name: getattr(item, c.name) for c in item.__table__.columns}
            # Convert datetime objects in details dict to isoformat for serialization
            for k, v in details.items():
                if isinstance(v, AsyncSession) or hasattr(v, "isoformat"):
                    details[k] = str(v)

            submissions.append({
                "id": item.id,
                "user_id": item.user_id,
                "domain": domain,
                "title": str(title_val),
                "status": item.status,
                "created_at": item.created_at,
                "details": details
            })
            
    # Sort by created_at descending
    submissions.sort(key=lambda x: str(x["created_at"]), reverse=True)
    return submissions

async def advance_submission_stage(
    db: AsyncSession,
    domain: str,
    submission_id: int,
    action: str
) -> dict[str, Any]:
    if domain not in DOMAIN_MODEL_MAP:
        raise ValueError(f"Invalid domain '{domain}'. Must be one of: {list(DOMAIN_MODEL_MAP.keys())}")

    model_cls, title_attr = DOMAIN_MODEL_MAP[domain]
    result = await db.execute(select(model_cls).where(model_cls.id == submission_id))
    item = result.scalars().first()
    
    if not item:
        raise ValueError(f"Submission with ID {submission_id} not found in domain '{domain}'")
        
    previous_status = item.status

    # Action Mapping Rules
    # Stage 1: Automated Completeness / Identity Check -> pending_validation to editorial_review
    # Stage 2: Editorial Fact Verification -> editorial_review to approved
    # Stage 3: Final Approval -> approved
    # reject -> rejected
    if action in ("stage1_pass", "advance_to_editorial", "editorial_review"):
        # Automated completeness check
        title_val = getattr(item, title_attr, None)
        if not title_val or len(str(title_val).strip()) == 0:
            item.status = "rejected"
            msg = "Stage 1 Automated Check failed: Title/Role is empty."
        else:
            item.status = "editorial_review"
            msg = "Passed Stage 1 (Automated Completeness Check). Advanced to editorial_review."
            
    elif action in ("stage2_pass", "stage3_approve", "approve", "approved"):
        item.status = "approved"
        msg = "Passed Stage 2/3 (Editorial Verification & Final Approval). Status set to approved. Press kit generated."
        
    elif action in ("reject", "rejected"):
        item.status = "rejected"
        msg = "Submission rejected."
        
    elif action in ("pending_validation", "editorial_review", "approved", "rejected"):
        item.status = action
        msg = f"Submission status updated directly to {action}."
        
    else:
        raise ValueError(f"Unknown action '{action}'. Valid actions: stage1_pass, stage2_pass, stage3_approve, reject, pending_validation, editorial_review, approved, rejected.")

    await db.commit()
    await db.refresh(item)

    details = {c.name: getattr(item, c.name) for c in item.__table__.columns}
    for k, v in details.items():
        if hasattr(v, "isoformat"):
            details[k] = str(v)

    # Generate press kit on-the-fly when status becomes approved
    media_package = None
    if item.status == "approved":
        try:
            press_kit = generate_press_kit(
                domain=domain,
                details=details,
                contact_name="Default Profile User",
                contact_email="developer@dain.local",
            )
            media_package = route_media_package(
                domain=domain,
                details=details,
                press_kit=press_kit,
            )
        except Exception as e:
            # Don't fail the approval if packaging errors—log and continue
            media_package = {"error": f"Press kit generation failed: {str(e)}"}

    return {
        "message": msg,
        "domain": domain,
        "submission_id": item.id,
        "previous_status": previous_status,
        "new_status": item.status,
        "details": details,
        "media_package": media_package,
    }
