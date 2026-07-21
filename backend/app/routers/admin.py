from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.core.database import get_db
from backend.app.schemas.schemas import (
    AdminSubmissionItem,
    AdvanceSubmissionRequest,
    AdvanceSubmissionResponse,
    MediaRoutingResult,
)
from backend.app.services import crud
from backend.app.services.media_packager import generate_press_kit
from backend.app.services.media_router import route_media_package

router = APIRouter(prefix="/admin", tags=["Admin Review Pipeline"])

@router.get("/submissions", response_model=list[AdminSubmissionItem])
async def list_submissions(
    status: Optional[str] = Query(None, description="Filter by status: pending_validation, editorial_review, approved, rejected"),
    domain: Optional[str] = Query(None, description="Filter by domain: academic, professional, entrepreneurial, social-impact, personal"),
    db: AsyncSession = Depends(get_db)
):
    """
    List milestone submissions across all five sectors, with optional filtering by status or domain.
    """
    return await crud.list_admin_submissions(db, status_filter=status, domain_filter=domain)

@router.post("/advance", response_model=AdvanceSubmissionResponse)
async def advance_submission(
    payload: AdvanceSubmissionRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Advance a submission through the 3-Stage Content Review Pipeline:
    - Stage 1 (stage1_pass): Automated Completeness & Identity Check -> moves to editorial_review
    - Stage 2/3 (stage2_pass / stage3_approve): Editorial Fact Verification & Final Approval -> moves to approved
    - Reject (reject): Rejects submission

    When a milestone is approved, a full press kit and media routing result is generated
    on-the-fly and returned in the `media_package` field of the response.
    """
    try:
        res = await crud.advance_submission_stage(
            db,
            domain=payload.domain,
            submission_id=payload.submission_id,
            action=payload.action
        )
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/press-kit/{domain}/{submission_id}", response_model=MediaRoutingResult)
async def preview_press_kit(
    domain: str = Path(..., description="Domain: academic, professional, entrepreneurial, social-impact, personal"),
    submission_id: int = Path(..., description="Milestone submission ID"),
    db: AsyncSession = Depends(get_db)
):
    """
    Preview a generated press kit and media routing result for any approved milestone.
    The press kit is generated dynamically on-the-fly (not persisted in DB).
    Returns 404 if submission is not found, 400 if not yet approved.
    """
    if domain not in crud.DOMAIN_MODEL_MAP:
        raise HTTPException(status_code=400, detail=f"Invalid domain '{domain}'.")

    model_cls, title_attr = crud.DOMAIN_MODEL_MAP[domain]
    result = await db.execute(select(model_cls).where(model_cls.id == submission_id))
    item = result.scalars().first()

    if not item:
        raise HTTPException(status_code=404, detail=f"Submission {submission_id} not found in domain '{domain}'.")

    if item.status != "approved":
        raise HTTPException(
            status_code=400,
            detail=f"Press kit is only available for approved milestones. Current status: '{item.status}'."
        )

    # Build details dict
    details = {c.name: getattr(item, c.name) for c in item.__table__.columns}
    for k, v in details.items():
        if hasattr(v, "isoformat"):
            details[k] = str(v)

    press_kit = generate_press_kit(
        domain=domain,
        details=details,
        contact_name="Default Profile User",
        contact_email="developer@dain.local",
    )
    routing_result = route_media_package(
        domain=domain,
        details=details,
        press_kit=press_kit,
    )
    return routing_result

