from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    ErrorResponse,
    PostCreate,
    PostResponse,
    PostStatusLiteral,
    PostUpdate,
    SubmitResponse,
)
import app.crud as crud

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post(
    "/",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new draft post",
    responses={
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)
@router.post(
    "",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
def create_post(
    post_in: PostCreate,
    db: Session = Depends(get_db),
) -> PostResponse:
    """Create a new post in draft status.

    Title must be 1-200 non-blank characters. Content can be up to 10,000 characters.
    Moderation length rules (50-2000 chars) are enforced at submit time.
    """
    db_post = crud.create_post(db, post_in=post_in)
    return PostResponse.model_validate(db_post)


@router.put(
    "/{post_id}",
    response_model=PostResponse,
    summary="Update an existing post",
    responses={
        404: {"model": ErrorResponse, "description": "Post not found"},
        409: {"model": ErrorResponse, "description": "Invalid state transition"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)
@router.put(
    "/{post_id}/",
    response_model=PostResponse,
    include_in_schema=False,
)
def update_post(
    post_id: int,
    post_in: PostUpdate,
    db: Session = Depends(get_db),
) -> PostResponse:
    """Update post title and/or content.

    Resets post status back to 'draft' and clears flagged reasons.
    Published posts cannot be edited and return 409 Conflict.
    """
    db_post = crud.get_post(db, post_id)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found.",
        )

    if db_post.status == "published":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Published posts are read-only",
        )

    updated = crud.update_post(db, post=db_post, post_in=post_in)
    return PostResponse.model_validate(updated)


@router.post(
    "/{post_id}/submit/",
    response_model=SubmitResponse,
    status_code=status.HTTP_200_OK,
    summary="Submit post for AI moderation",
    responses={
        404: {"model": ErrorResponse, "description": "Post not found"},
        409: {"model": ErrorResponse, "description": "Invalid state transition"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)
@router.post(
    "/{post_id}/submit",
    response_model=SubmitResponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
def submit_post(
    post_id: int,
    db: Session = Depends(get_db),
) -> SubmitResponse:
    """Submit a post for automated AI content moderation.

    Allowed only from 'draft' or 'flagged' status (re-submitting a flagged post is allowed).
    Evaluates profanity, content length (50-2000 characters), and AI tone.
    Transitions status to 'approved' or 'flagged'.
    """
    db_post = crud.get_post(db, post_id)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found.",
        )

    if db_post.status == "published":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Published posts are read-only",
        )

    if db_post.status == "approved":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot submit post with status 'approved'. Only 'draft' or 'flagged' posts can be submitted for moderation.",
        )

    updated_post, reasons, message = crud.submit_for_moderation(db, post=db_post)
    return SubmitResponse(
        id=updated_post.id,
        status=updated_post.status,
        reasons=reasons,
        message=message,
    )


@router.get(
    "/",
    response_model=List[PostResponse],
    summary="List all posts",
    responses={
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)
@router.get(
    "",
    response_model=List[PostResponse],
    include_in_schema=False,
)
def list_posts(
    status_filter: Optional[PostStatusLiteral] = Query(
        None,
        alias="status",
        description="Filter posts by status (draft, flagged, approved, published)",
    ),
    current_user: Optional[str] = Query(
        None,
        description="Current logged-in username for author-scoped queries (drafts/flagged)",
    ),
    db: Session = Depends(get_db),
) -> List[PostResponse]:
    """Retrieve all posts ordered newest first (ID descending).

    Supports optional status filtering against allowed statuses.
    Enforces privacy: flagged & draft posts are scoped to the current_user.
    """
    posts = crud.get_posts(db, status=status_filter, current_user=current_user)
    return [PostResponse.model_validate(p) for p in posts]


@router.patch(
    "/{post_id}/publish/",
    response_model=PostResponse,
    summary="Publish an approved post",
    responses={
        404: {"model": ErrorResponse, "description": "Post not found"},
        409: {"model": ErrorResponse, "description": "Invalid state transition"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)
@router.patch(
    "/{post_id}/publish",
    response_model=PostResponse,
    include_in_schema=False,
)
def publish_post(
    post_id: int,
    db: Session = Depends(get_db),
) -> PostResponse:
    """Publish an approved post.

    Only posts currently in 'approved' status can be published.
    Once published, the post becomes read-only and immutable.
    """
    db_post = crud.get_post(db, post_id)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found.",
        )

    if db_post.status == "published":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Published posts are read-only",
        )

    if db_post.status != "approved":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot publish post with status '{db_post.status}'. Only 'approved' posts can be published.",
        )

    published_post = crud.publish_post(db, post=db_post)
    return PostResponse.model_validate(published_post)


@router.get(
    "/{post_id}",
    response_model=PostResponse,
    summary="Get single post by ID",
    responses={
        404: {"model": ErrorResponse, "description": "Post not found"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)
@router.get(
    "/{post_id}/",
    response_model=PostResponse,
    include_in_schema=False,
)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
) -> PostResponse:
    """Retrieve full details of a single post by its ID."""
    db_post = crud.get_post(db, post_id)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found.",
        )
    return PostResponse.model_validate(db_post)
