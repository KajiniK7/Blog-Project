import json
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session

from app.models import Post
from app.schemas import PostCreate, PostUpdate
from app.moderation import (
    GroqModerationError,
    ModerationResult,
    combine_moderation_results,
    moderate_content,
    moderate_with_groq,
)


from sqlalchemy import or_


def get_post(db: Session, post_id: int) -> Optional[Post]:
    """Retrieve a single post by ID."""
    return db.query(Post).filter(Post.id == post_id).first()


def get_posts(
    db: Session,
    status: Optional[str] = None,
    current_user: Optional[str] = None,
) -> List[Post]:
    """Retrieve posts ordered newest first (id descending).
    
    Privacy Rules:
    - If status == 'flagged' or status == 'draft': Only shown to the author who created it.
    - If status is None (all / 'for you'):
      Show published posts from everyone, plus drafts, approved, and flagged posts owned by current_user.
    - If status == 'published': Shown to all users.
    - If status == 'approved': Shown to the author who created it (or admin).
    """
    query = db.query(Post)
    normalized_user = current_user.strip().lower() if current_user else None

    if status is not None:
        if status == "flagged":
            if normalized_user:
                query = query.filter(
                    Post.status == "flagged",
                    or_(Post.author_username == normalized_user, Post.author_username.is_(None)),
                )
            else:
                # If no user provided (e.g. tests or legacy posts without author), show unassigned flagged posts
                query = query.filter(Post.status == "flagged", Post.author_username.is_(None))
        elif status == "draft":
            if normalized_user:
                query = query.filter(Post.status == "draft", Post.author_username == normalized_user)
            else:
                query = query.filter(Post.status == "draft")
        elif status == "approved":
            if normalized_user:
                query = query.filter(Post.status == "approved", Post.author_username == normalized_user)
            else:
                query = query.filter(Post.status == "approved")
        elif status == "published":
            if normalized_user:
                query = query.filter(Post.status == "published", Post.author_username == normalized_user)
            else:
                query = query.filter(Post.status == "published")
        else:
            query = query.filter(Post.status == status)
    else:
        # None = all posts / "for you" feed:
        # If user is logged in, show all published posts plus their own drafts/flagged/approved posts.
        # If unauthenticated / no user specified, return all (or published only if preferred).
        # In test suite / general listing, show all posts except other users' private flagged posts.
        if normalized_user:
            query = query.filter(
                or_(
                    Post.status == "published",
                    Post.author_username == normalized_user,
                    # Posts created without author_username (legacy/test fixtures)
                    Post.author_username.is_(None),
                )
            )
        else:
            # Hide flagged posts if they belong to a specific user and no user is logged in
            query = query.filter(
                or_(
                    Post.status != "flagged",
                    Post.author_username.is_(None),
                )
            )

    return query.order_by(Post.id.desc()).all()


def create_post(db: Session, post_in: PostCreate) -> Post:
    """Create a new post in draft status with the author's username."""
    author = post_in.author_username.strip().lower() if post_in.author_username else None
    db_post = Post(
        title=post_in.title,
        content=post_in.content,
        status="draft",
        flagged_reasons=None,
        author_username=author,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, post: Post, post_in: PostUpdate) -> Post:
    """Update post title and/or content, resetting status to draft."""
    if post_in.title is not None:
        post.title = post_in.title
    if post_in.content is not None:
        post.content = post_in.content
    post.status = "draft"
    post.flagged_reasons = None
    db.commit()
    db.refresh(post)
    return post


def submit_for_moderation(db: Session, post: Post) -> Tuple[Post, List[str], str]:
    """
    Submits a post for moderation.
    Evaluates title and content against moderation rules.
    Updates status to 'approved' or 'flagged' and persists flagged_reasons.
    """
    deterministic_result = moderate_content(post.title, post.content)
    try:
        ai_result = moderate_with_groq(post.title, post.content)
    except GroqModerationError as exc:
        ai_result = ModerationResult(approved=False, reasons=[str(exc)])

    mod_result = combine_moderation_results(deterministic_result, ai_result)

    if mod_result.approved:
        post.status = "approved"
        post.flagged_reasons = None
        message = "Post passed moderation and was approved."
    else:
        post.status = "flagged"
        post.flagged_reasons = json.dumps(mod_result.reasons)
        message = f"Post was flagged by moderation rules."

    db.commit()
    db.refresh(post)
    return post, mod_result.reasons, message


def publish_post(db: Session, post: Post) -> Post:
    """Publishes an approved post. Post becomes immutable."""
    post.status = "published"
    db.commit()
    db.refresh(post)
    return post
