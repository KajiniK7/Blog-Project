from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routers.posts import router as posts_router
from app.routers.auth import router as auth_router


def custom_generate_unique_id(route: APIRoute) -> str:
    """Generate clean OpenAPI operationId matching the route function name.

    Ensures OpenAPI Generator CLI produces clean SDK method names such as
    `create_post`, `submit_post`, `list_posts`, `publish_post`, `get_post`.
    """
    return route.name


app = FastAPI(
    title="AI-Assisted Content Moderation & Publishing API",
    description="Backend API for managing posts, AI-assisted content moderation, and editorial publishing workflow.",
    version="1.0.0",
    generate_unique_id_function=custom_generate_unique_id,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Global 500 error handler returning clean JSON message
@app.exception_handler(Exception)
async def generic_500_exception_handler(request: Request, exc: Exception):
    # Pass through standard HTTP and validation errors without altering their status codes
    if isinstance(exc, (StarletteHTTPException, RequestValidationError)):
        raise exc
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred."},
    )


# Register posts & auth routers
app.include_router(posts_router)
app.include_router(auth_router)


@app.get("/", tags=["health"], summary="Health check")
def root():
    """Health check / root endpoint."""
    return {
        "status": "online",
        "service": "AI-Assisted Content Moderation & Publishing API",
        "version": "1.0.0",
    }


# Keep CORS outside FastAPI's error middleware so error responses also get CORS headers.
asgi_app = CORSMiddleware(
    app,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH"],
    allow_headers=["Content-Type"],
)
