from datetime import datetime
import json
from typing import Any, List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator


PostStatusLiteral = Literal["draft", "flagged", "approved", "published"]
SubmitStatusLiteral = Literal["approved", "flagged"]


class PostCreate(BaseModel):
    """Schema for creating a new post (starts in draft status)."""
    title: str = Field(
        ...,
        max_length=200,
        description="Title of the post (1-200 characters, non-blank)",
        examples=["Building Reliable Microservices with FastAPI"],
    )
    content: str = Field(
        ...,
        max_length=10000,
        description="Body content (non-blank, up to 10000 characters at creation)",
        examples=["Here is the full text of the article detailing best practices..."],
    )
    author_username: Optional[str] = Field(
        None,
        max_length=50,
        description="Author's username",
        examples=["kajini"],
    )

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Title cannot be blank or whitespace-only")
        if len(stripped) > 200:
            raise ValueError("Title must be between 1 and 200 characters")
        return stripped

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Content cannot be blank or whitespace-only")
        if len(v) > 10000:
            raise ValueError("Content cannot exceed 10000 characters")
        return v


class PostUpdate(BaseModel):
    """Schema for updating an existing post (resets status back to draft)."""
    title: Optional[str] = Field(
        None,
        max_length=200,
        description="Updated title (1-200 characters, non-blank)",
    )
    content: Optional[str] = Field(
        None,
        max_length=10000,
        description="Updated body content (non-blank, up to 10000 characters)",
    )

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        stripped = v.strip()
        if not stripped:
            raise ValueError("Title cannot be blank or whitespace-only")
        if len(stripped) > 200:
            raise ValueError("Title must be between 1 and 200 characters")
        return stripped

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        stripped = v.strip()
        if not stripped:
            raise ValueError("Content cannot be blank or whitespace-only")
        if len(v) > 10000:
            raise ValueError("Content cannot exceed 10000 characters")
        return v


class PostResponse(BaseModel):
    """Schema representing a post entity."""
    id: int = Field(..., description="Unique post ID", examples=[1])
    title: str = Field(..., description="Post title", examples=["Building Reliable Microservices"])
    content: str = Field(..., description="Post body content")
    status: PostStatusLiteral = Field(..., description="Current status in moderation lifecycle", examples=["draft"])
    flagged_reasons: Optional[List[str]] = Field(
        None,
        description="List of moderation violation reasons if flagged, otherwise null",
        examples=[["Content too short (24 characters, minimum 50)"]],
    )
    created_at: Optional[datetime] = Field(None, description="Post creation timestamp")
    author_username: Optional[str] = Field(None, description="Author's username")

    model_config = ConfigDict(from_attributes=True)

    @field_validator("flagged_reasons", mode="before")
    @classmethod
    def parse_flagged_reasons(cls, v: Any) -> Optional[List[str]]:
        if v is None:
            return None
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            trimmed = v.strip()
            if not trimmed:
                return None
            try:
                parsed = json.loads(trimmed)
                if isinstance(parsed, list):
                    return parsed
                return [str(parsed)]
            except json.JSONDecodeError:
                return [trimmed]
        return None


class SubmitResponse(BaseModel):
    """Response returned upon submitting a post for AI moderation."""
    id: int = Field(..., description="Post ID", examples=[1])
    status: SubmitStatusLiteral = Field(
        ...,
        description="New post status after moderation evaluation",
        examples=["approved"],
    )
    reasons: List[str] = Field(
        default_factory=list,
        description="List of moderation violation reasons if flagged (empty if approved)",
    )
    message: str = Field(
        ...,
        description="Human-readable summary of moderation outcome",
        examples=["Post passed moderation and was approved."],
    )


class ErrorResponse(BaseModel):
    """Standardized error response body."""
    detail: str = Field(
        ...,
        description="Error message explanation",
        examples=["Post with id 1 not found."],
    )


class UserRegister(BaseModel):
    """Schema for registering a new user."""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=4, max_length=100)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        s = v.strip().lower()
        if not s or len(s) < 3:
            raise ValueError("Username must be at least 3 characters")
        return s

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 4:
            raise ValueError("Password must be at least 4 characters")
        return v


class UserLogin(BaseModel):
    """Schema for logging in."""
    username: str
    password: str


class UserResponse(BaseModel):
    """Schema representing a user."""
    id: int
    username: str
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

