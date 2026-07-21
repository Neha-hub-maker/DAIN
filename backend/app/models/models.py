from datetime import datetime
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    password_hash: Mapped[str | None] = mapped_column(String, nullable=True)
    role: Mapped[str] = mapped_column(String, default="student")  # student, alumni, admin
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    
    # Relationships
    academic_milestones: Mapped[list["AcademicMilestone"]] = relationship(
        "AcademicMilestone", back_populates="user", cascade="all, delete-orphan"
    )
    professional_milestones: Mapped[list["ProfessionalMilestone"]] = relationship(
        "ProfessionalMilestone", back_populates="user", cascade="all, delete-orphan"
    )
    entrepreneurial_milestones: Mapped[list["EntrepreneurialMilestone"]] = relationship(
        "EntrepreneurialMilestone", back_populates="user", cascade="all, delete-orphan"
    )
    social_impact_milestones: Mapped[list["SocialImpactMilestone"]] = relationship(
        "SocialImpactMilestone", back_populates="user", cascade="all, delete-orphan"
    )
    personal_milestones: Mapped[list["PersonalMilestone"]] = relationship(
        "PersonalMilestone", back_populates="user", cascade="all, delete-orphan"
    )

class AcademicMilestone(Base):
    __tablename__ = "academic_milestones"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)  # publication, research, cgpa, other
    title: Mapped[str] = mapped_column(String, nullable=False)
    institution: Mapped[str] = mapped_column(String, nullable=False)
    value: Mapped[str | None] = mapped_column(String, nullable=True)
    date: Mapped[str | None] = mapped_column(String, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String, default="pending_validation")  # pending_validation, editorial_review, approved, rejected
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="academic_milestones")

class ProfessionalMilestone(Base):
    __tablename__ = "professional_milestones"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    company: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[str | None] = mapped_column(String, nullable=True)
    start_date: Mapped[str | None] = mapped_column(String, nullable=True)
    end_date: Mapped[str | None] = mapped_column(String, nullable=True)
    industry_sector: Mapped[str | None] = mapped_column(String, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String, default="pending_validation")  # pending_validation, editorial_review, approved, rejected
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="professional_milestones")

class EntrepreneurialMilestone(Base):
    __tablename__ = "entrepreneurial_milestones"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    venture_name: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    stage: Mapped[str] = mapped_column(String, nullable=False)  # ideation, mvp, funding, scaling, exited, other
    funding_amount: Mapped[float] = mapped_column(Float, default=0.0)
    funding_source: Mapped[str | None] = mapped_column(String, nullable=True)
    launch_date: Mapped[str | None] = mapped_column(String, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String, default="pending_validation")  # pending_validation, editorial_review, approved, rejected
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="entrepreneurial_milestones")

class SocialImpactMilestone(Base):
    __tablename__ = "social_impact_milestones"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    organization: Mapped[str] = mapped_column(String, nullable=False)
    cause_area: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    hours_volunteered: Mapped[float] = mapped_column(Float, default=0.0)
    initiatives_led: Mapped[int] = mapped_column(Integer, default=0)
    scale_metric: Mapped[str | None] = mapped_column(String, nullable=True)
    date: Mapped[str | None] = mapped_column(String, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String, default="pending_validation")  # pending_validation, editorial_review, approved, rejected
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="social_impact_milestones")

class PersonalMilestone(Base):
    __tablename__ = "personal_milestones"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)  # extracurricular, skill, hobby, other
    title: Mapped[str] = mapped_column(String, nullable=False)
    date_achieved: Mapped[str | None] = mapped_column(String, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String, default="pending_validation")  # pending_validation, editorial_review, approved, rejected
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="personal_milestones")
