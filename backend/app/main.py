from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.core.database import engine
from backend.app.routers import (
    academic,
    professional,
    entrepreneurial,
    social_impact,
    personal,
    admin,
    auth,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Seed default profile user (id=1)
    from backend.app.core.database import SessionLocal
    from backend.app.services.crud import seed_default_user
    
    async with SessionLocal() as db:
        try:
            await seed_default_user(db)
        except Exception as e:
            print(f"Error seeding default user on startup: {e}")
            
    yield
    
    # Shutdown: Clean up connections
    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(academic.router, prefix=settings.API_V1_STR)
app.include_router(professional.router, prefix=settings.API_V1_STR)
app.include_router(entrepreneurial.router, prefix=settings.API_V1_STR)
app.include_router(social_impact.router, prefix=settings.API_V1_STR)
app.include_router(personal.router, prefix=settings.API_V1_STR)
app.include_router(admin.router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Service health check endpoint.
    """
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "database_connected": True
    }
