from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UserRegister, UserLogin, UserResponse, ErrorResponse
import app.auth_service as auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    responses={
        400: {"model": ErrorResponse, "description": "Username already exists"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    """Registers a new user and persists their username & hashed password in SQLite."""
    existing_user = auth_service.get_user_by_username(db, user_in.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken. Please choose another username.",
        )
    user = auth_service.create_user(db, user_in)
    return UserResponse.model_validate(user)


@router.post(
    "/login/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate a user",
    responses={
        401: {"model": ErrorResponse, "description": "Invalid credentials"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)
@router.post(
    "/login",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    """Authenticates username and password against SQLite database records."""
    user = auth_service.get_user_by_username(db, user_in.username)
    if not user or not auth_service.verify_password(user.password_hash, user_in.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )
    return UserResponse.model_validate(user)
