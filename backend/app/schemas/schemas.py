from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Any

# ----------------------------------------------------
# USER SCHEMAS
# ----------------------------------------------------
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str = "student"  # student, alumni, admin

class UserCreate(UserBase):
    password: str | None = None

class UserRead(UserBase):
    id: int
    is_verified: bool = False
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ----------------------------------------------------
# ACADEMIC MILESTONE SCHEMAS
# ----------------------------------------------------
class AcademicMilestoneBase(BaseModel):
    type: str  # publication, research, cgpa, other
    title: str
    institution: str
    value: str | None = None
    date: str | None = None  # YYYY-MM-DD
    description: str | None = None
    status: str = "pending_validation"

class AcademicMilestoneCreate(AcademicMilestoneBase):
    pass

class AcademicMilestoneRead(AcademicMilestoneBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ----------------------------------------------------
# PROFESSIONAL MILESTONE SCHEMAS
# ----------------------------------------------------
class ProfessionalMilestoneBase(BaseModel):
    company: str
    role: str
    location: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    industry_sector: str | None = None
    description: str | None = None
    status: str = "pending_validation"

class ProfessionalMilestoneCreate(ProfessionalMilestoneBase):
    pass

class ProfessionalMilestoneRead(ProfessionalMilestoneBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ----------------------------------------------------
# ENTREPRENEURIAL MILESTONE SCHEMAS
# ----------------------------------------------------
class EntrepreneurialMilestoneBase(BaseModel):
    venture_name: str
    role: str
    stage: str  # ideation, mvp, funding, scaling, exited, other
    funding_amount: float = 0.0
    funding_source: str | None = None
    launch_date: str | None = None
    description: str | None = None
    status: str = "pending_validation"

class EntrepreneurialMilestoneCreate(EntrepreneurialMilestoneBase):
    pass

class EntrepreneurialMilestoneRead(EntrepreneurialMilestoneBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ----------------------------------------------------
# SOCIAL IMPACT MILESTONE SCHEMAS
# ----------------------------------------------------
class SocialImpactMilestoneBase(BaseModel):
    organization: str
    cause_area: str
    role: str
    hours_volunteered: float = 0.0
    initiatives_led: int = 0
    scale_metric: str | None = None
    date: str | None = None
    description: str | None = None
    status: str = "pending_validation"

class SocialImpactMilestoneCreate(SocialImpactMilestoneBase):
    pass

class SocialImpactMilestoneRead(SocialImpactMilestoneBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ----------------------------------------------------
# PERSONAL MILESTONE SCHEMAS
# ----------------------------------------------------
class PersonalMilestoneBase(BaseModel):
    category: str  # extracurricular, skill, hobby, other
    title: str
    date_achieved: str | None = None
    description: str | None = None
    status: str = "pending_validation"

class PersonalMilestoneCreate(PersonalMilestoneBase):
    pass

class PersonalMilestoneRead(PersonalMilestoneBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ----------------------------------------------------
# ADMIN REVIEW PIPELINE SCHEMAS
# ----------------------------------------------------
class AdminSubmissionItem(BaseModel):
    id: int
    user_id: int
    domain: str  # academic, professional, entrepreneurial, social-impact, personal
    title: str
    status: str  # pending_validation, editorial_review, approved, rejected
    created_at: datetime
    details: dict[str, Any]

    model_config = ConfigDict(from_attributes=True)

class AdvanceSubmissionRequest(BaseModel):
    domain: str  # academic, professional, entrepreneurial, social-impact, personal
    submission_id: int
    action: str  # stage1_pass, stage2_pass, stage3_approve, reject, or target status

class AdvanceSubmissionResponse(BaseModel):
    message: str
    domain: str
    submission_id: int
    previous_status: str
    new_status: str
    details: dict[str, Any]
    media_package: dict[str, Any] | None = None  # Populated when status becomes 'approved'

# ----------------------------------------------------
# PRESS KIT & MEDIA ROUTING SCHEMAS
# ----------------------------------------------------
class ContactInfo(BaseModel):
    name: str
    email: str
    domain: str

class PressKitPayload(BaseModel):
    headline: str
    executive_summary: str
    detailed_story: str
    media_assets: list[str]
    contact_info: ContactInfo
    generated_at: str

class MediaRoutingResult(BaseModel):
    press_kit: PressKitPayload
    target_tiers: list[str]
    channels: list[str]
    generated_at: str

# ----------------------------------------------------
# AUTHENTICATION SCHEMAS
# ----------------------------------------------------
class UserRegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "student"  # student, alumni, admin

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead

class UserProfile(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_verified: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


