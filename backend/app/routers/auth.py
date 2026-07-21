from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.app.core.database import get_db
from backend.app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from backend.app.core.dependencies import get_current_user
from backend.app.models.models import User
from backend.app.schemas.schemas import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    UserRead,
    UserProfile,
)

router = APIRouter(prefix="/auth", tags=["DUNITE Authentication"])

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: UserRegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user on the platform.
    
    Automatic Student Verification Rule:
    - Emails ending in '@du.ac.bd' are automatically verified (is_verified = True).
    - Other emails default to unverified (is_verified = False) and require manual admin approval.
    """
    email_clean = payload.email.strip().lower()

    # Check for duplicate email
    result = await db.execute(select(User).where(User.email == email_clean))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists."
        )

    # Automatic DU student verification check
    is_verified_auto = email_clean.endswith("@du.ac.bd")

    hashed_pw = hash_password(payload.password)
    new_user = User(
        name=payload.name.strip(),
        email=email_clean,
        password_hash=hashed_pw,
        role=payload.role if payload.role in ("student", "alumni", "admin") else "student",
        is_verified=is_verified_auto,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Generate access token
    access_token = create_access_token({"sub": str(new_user.id)})

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserRead.model_validate(new_user)
    )

@router.post("/login", response_model=TokenResponse)
async def login_user(
    payload: UserLoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticate user with email & password, returning a JWT Bearer access token.
    """
    email_clean = payload.email.strip().lower()

    result = await db.execute(select(User).where(User.email == email_clean))
    user = result.scalars().first()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserRead.model_validate(user)
    )

@router.get("/me", response_model=UserProfile)
async def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user profile and verification status.
    """
    return UserProfile.model_validate(current_user)
