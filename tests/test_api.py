"""Unit and integration tests for FastAPI posts API endpoints."""

import pytest


def test_create_post_success(client):
    """Create post -> 201, status draft."""
    payload = {
        "title": "Initial Draft Architecture",
        "content": "Designing resilient microservices with event loops and async processing.",
    }
    response = client.post("/posts/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["title"] == payload["title"]
    assert data["content"] == payload["content"]
    assert data["status"] == "draft"
    assert data["flagged_reasons"] is None
    assert data["created_at"] is not None


def test_create_post_empty_title_or_blank_content_422(client):
    """Create with empty title / blank content -> 422."""
    # Blank / whitespace-only title
    res1 = client.post("/posts/", json={"title": "   ", "content": "Valid body text here."})
    assert res1.status_code == 422

    # Empty title
    res2 = client.post("/posts/", json={"title": "", "content": "Valid body text here."})
    assert res2.status_code == 422

    # Blank / whitespace-only content
    res3 = client.post("/posts/", json={"title": "Valid Title", "content": "   "})
    assert res3.status_code == 422

    # Missing fields
    res4 = client.post("/posts/", json={})
    assert res4.status_code == 422


def test_submit_good_post_and_bad_post(client, create_draft_post):
    """Submit good post -> approved; submit bad post -> flagged with reasons."""
    # 1. Good post (polite, >50 characters)
    good_post = create_draft_post(
        title="High Performance Python Systems",
        content="Writing maintainable software requires clean schemas, strict typing, and comprehensive test coverage.",
    )
    good_id = good_post["id"]

    good_res = client.post(f"/posts/{good_id}/submit/")
    assert good_res.status_code == 200
    good_data = good_res.json()
    assert good_data["id"] == good_id
    assert good_data["status"] == "approved"
    assert good_data["reasons"] == []
    assert "approved" in good_data["message"].lower()

    # Verify persisted state via GET
    get_good = client.get(f"/posts/{good_id}")
    assert get_good.status_code == 200
    assert get_good.json()["status"] == "approved"
    assert get_good.json()["flagged_reasons"] is None

    # 2. Short post is flagged by the deterministic length rule.
    bad_post = create_draft_post(
        title="Rant on Coding",
        content="You idiot! Fix this now.",
    )
    bad_id = bad_post["id"]

    bad_res = client.post(f"/posts/{bad_id}/submit/")
    assert bad_res.status_code == 200
    bad_data = bad_res.json()
    assert bad_data["id"] == bad_id
    assert bad_data["status"] == "flagged"
    assert len(bad_data["reasons"]) >= 1
    assert any("too short" in r.lower() for r in bad_data["reasons"])

    # Verify persisted state via GET (reasons parsed as a list)
    get_bad = client.get(f"/posts/{bad_id}")
    assert get_bad.status_code == 200
    assert get_bad.json()["status"] == "flagged"
    assert isinstance(get_bad.json()["flagged_reasons"], list)
    assert len(get_bad.json()["flagged_reasons"]) >= 1


def test_groq_flag_is_returned_and_persisted(client, create_draft_post, monkeypatch):
    from app import crud
    from app.moderation import ModerationResult

    monkeypatch.setattr(
        crud,
        "moderate_with_groq",
        lambda title, content: ModerationResult(
            approved=False,
            reasons=["Profanity detected: 'fuck'"],
        ),
    )
    post = create_draft_post(
        title="Community feedback",
        content="This test contains fuck so the mocked moderation reason can be shown to the user.",
    )

    response = client.post(f"/posts/{post['id']}/submit/")

    assert response.status_code == 200
    assert response.json()["status"] == "flagged"
    assert response.json()["reasons"] == ["Profanity detected: 'fuck'"]
    fetched = client.get(f"/posts/{post['id']}").json()
    assert fetched["status"] == "flagged"
    assert fetched["flagged_reasons"] == ["Profanity detected: 'fuck'"]


def test_missing_groq_key_fails_closed_and_persists_flag(
    client, create_draft_post, monkeypatch
):
    from app import crud
    from app.moderation import moderate_with_groq

    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.setattr(crud, "moderate_with_groq", moderate_with_groq)
    post = create_draft_post(
        title="A Safe-Looking Draft",
        content="A sufficiently long and otherwise polite post for testing missing credentials.",
    )

    response = client.post(f"/posts/{post['id']}/submit/")

    assert response.status_code == 200
    assert response.json()["status"] == "flagged"
    assert any(
        "Groq" in reason and "not configured" in reason
        for reason in response.json()["reasons"]
    )
    fetched = client.get(f"/posts/{post['id']}").json()
    assert fetched["status"] == "flagged"
    assert fetched["flagged_reasons"] == response.json()["reasons"]


def test_resubmit_flagged_post_after_valid_draft(client, create_draft_post):
    """Re-submitting a flagged post after it is a valid draft again works as designed."""
    # Step 1: Create a bad post
    post = create_draft_post(
        title="Short bad post",
        content="You moron!",  # too short and banned word
    )
    post_id = post["id"]

    # Step 2: Submit it -> flagged
    sub1 = client.post(f"/posts/{post_id}/submit/")
    assert sub1.status_code == 200
    assert sub1.json()["status"] == "flagged"

    # Step 3: Update post with valid content -> turns back into draft
    update_res = client.put(
        f"/posts/{post_id}",
        json={
            "title": "Constructive Critique on Systems Architecture",
            "content": "This is a revised, polite, and constructive critique explaining why modular boundaries are vital.",
        },
    )
    assert update_res.status_code == 200
    assert update_res.json()["status"] == "draft"
    assert update_res.json()["flagged_reasons"] is None

    # Step 4: Re-submit -> now it passes and is approved!
    sub2 = client.post(f"/posts/{post_id}/submit/")
    assert sub2.status_code == 200
    assert sub2.json()["status"] == "approved"
    assert sub2.json()["reasons"] == []

    # Verify final state via GET
    get_final = client.get(f"/posts/{post_id}")
    assert get_final.json()["status"] == "approved"
    assert get_final.json()["flagged_reasons"] is None


def test_list_all_and_filter_by_each_status(client, create_draft_post):
    """List all, and filter by each status; invalid status -> 422."""
    # 1. Draft post
    p_draft = create_draft_post(title="Draft 1", content="Content for draft post 1.")["id"]

    # 2. Flagged post
    p_flagged = create_draft_post(title="Flagged 1", content="Short")["id"]
    client.post(f"/posts/{p_flagged}/submit/")

    # 3. Approved post
    p_approved = create_draft_post(
        title="Approved 1",
        content="Polite article with sufficient character count to easily pass moderation.",
    )["id"]
    client.post(f"/posts/{p_approved}/submit/")

    # 4. Published post
    p_published = create_draft_post(
        title="Published 1",
        content="Another polite article with sufficient character count to easily pass moderation.",
    )["id"]
    client.post(f"/posts/{p_published}/submit/")
    client.patch(f"/posts/{p_published}/publish/")

    # List all -> 4 posts, newest first
    res_all = client.get("/posts/")
    assert res_all.status_code == 200
    all_posts = res_all.json()
    assert len(all_posts) == 4
    assert [p["id"] for p in all_posts] == [p_published, p_approved, p_flagged, p_draft]

    # Filter by 'draft'
    res_draft = client.get("/posts/?status=draft")
    assert res_draft.status_code == 200
    assert len(res_draft.json()) == 1
    assert res_draft.json()[0]["id"] == p_draft

    # Filter by 'flagged'
    res_flagged = client.get("/posts/?status=flagged")
    assert res_flagged.status_code == 200
    assert len(res_flagged.json()) == 1
    assert res_flagged.json()[0]["id"] == p_flagged

    # Filter by 'approved'
    res_approved = client.get("/posts/?status=approved")
    assert res_approved.status_code == 200
    assert len(res_approved.json()) == 1
    assert res_approved.json()[0]["id"] == p_approved

    # Filter by 'published'
    res_published = client.get("/posts/?status=published")
    assert res_published.status_code == 200
    assert len(res_published.json()) == 1
    assert res_published.json()[0]["id"] == p_published

    # Invalid status filter -> 422
    res_invalid = client.get("/posts/?status=not_a_real_status")
    assert res_invalid.status_code == 422


def test_publish_approved_post_succeeds(client, create_draft_post):
    """Publish an approved post -> published."""
    post = create_draft_post(
        title="Valid Article Ready For Publication",
        content="High quality discussion regarding database indexing and concurrency optimizations.",
    )
    post_id = post["id"]

    # Submit to approve
    sub_res = client.post(f"/posts/{post_id}/submit/")
    assert sub_res.json()["status"] == "approved"

    # Publish
    pub_res = client.patch(f"/posts/{post_id}/publish/")
    assert pub_res.status_code == 200
    assert pub_res.json()["id"] == post_id
    assert pub_res.json()["status"] == "published"

    # Confirm via GET
    get_res = client.get(f"/posts/{post_id}")
    assert get_res.json()["status"] == "published"


def test_publish_draft_or_flagged_post_conflict_409(client, create_draft_post):
    """Publish a draft/flagged post -> 409 Conflict."""
    # 1. Draft post publish attempt
    draft_post = create_draft_post(title="Draft Title", content="Draft content")
    draft_id = draft_post["id"]

    res_pub_draft = client.patch(f"/posts/{draft_id}/publish/")
    assert res_pub_draft.status_code == 409
    assert "draft" in res_pub_draft.json()["detail"].lower()

    # 2. Flagged post publish attempt
    flagged_post = create_draft_post(title="Flagged Title", content="Too short")
    flagged_id = flagged_post["id"]
    client.post(f"/posts/{flagged_id}/submit/")  # Status is now flagged

    res_pub_flagged = client.patch(f"/posts/{flagged_id}/publish/")
    assert res_pub_flagged.status_code == 409
    assert "flagged" in res_pub_flagged.json()["detail"].lower()


def test_submit_or_publish_already_published_post_409(client, create_draft_post):
    """Submit or publish an already published post -> 409 (read-only)."""
    # Create, approve, and publish a post
    post = create_draft_post(
        title="Published Post Immutability",
        content="This article has been vetted and published for the platform readers.",
    )
    post_id = post["id"]
    client.post(f"/posts/{post_id}/submit/")
    client.patch(f"/posts/{post_id}/publish/")

    # Attempt to submit already published post -> 409
    res_sub = client.post(f"/posts/{post_id}/submit/")
    assert res_sub.status_code == 409
    assert res_sub.json()["detail"] == "Published posts are read-only"

    # Attempt to publish already published post -> 409
    res_pub = client.patch(f"/posts/{post_id}/publish/")
    assert res_pub.status_code == 409
    assert res_pub.json()["detail"] == "Published posts are read-only"

    # Attempt to edit/update already published post -> 409
    res_update = client.put(f"/posts/{post_id}", json={"title": "New Title"})
    assert res_update.status_code == 409
    assert res_update.json()["detail"] == "Published posts are read-only"


def test_get_existing_and_non_existent_404(client, create_draft_post):
    """Get existing post -> 200; non-existent id -> 404 (for get, submit, publish)."""
    # Existing post -> 200
    post = create_draft_post(title="Existing Post", content="Existing post body content.")
    post_id = post["id"]

    res_get = client.get(f"/posts/{post_id}")
    assert res_get.status_code == 200
    assert res_get.json()["id"] == post_id

    # Non-existent ID (99999) -> 404
    non_existent_id = 99999

    res_get_missing = client.get(f"/posts/{non_existent_id}")
    assert res_get_missing.status_code == 404
    assert str(non_existent_id) in res_get_missing.json()["detail"]

    res_submit_missing = client.post(f"/posts/{non_existent_id}/submit/")
    assert res_submit_missing.status_code == 404
    assert str(non_existent_id) in res_submit_missing.json()["detail"]

    res_publish_missing = client.patch(f"/posts/{non_existent_id}/publish/")
    assert res_publish_missing.status_code == 404
    assert str(non_existent_id) in res_publish_missing.json()["detail"]

    res_update_missing = client.put(f"/posts/{non_existent_id}", json={"title": "Title"})
    assert res_update_missing.status_code == 404
    assert str(non_existent_id) in res_update_missing.json()["detail"]


def test_root_health_check(client):
    """GET / returns health check response."""
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["status"] == "online"


@pytest.mark.parametrize("origin", ["http://localhost:3000", "http://127.0.0.1:3000"])
def test_cors_preflight_and_get_for_frontend_origin(client, origin):
    preflight = client.options(
        "/posts/",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )
    response = client.get("/posts/", headers={"Origin": origin})

    assert preflight.status_code == 200
    assert preflight.headers["access-control-allow-origin"] == origin
    assert "POST" in preflight.headers["access-control-allow-methods"]
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == origin


def test_generic_500_response_includes_cors_header(client, monkeypatch):
    from app import crud

    def fail_list_posts(*args, **kwargs):
        raise RuntimeError("Database failure")

    monkeypatch.setattr(crud, "get_posts", fail_list_posts)
    response = client.get("/posts/", headers={"Origin": "http://localhost:3000"})

    assert response.status_code == 500
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


def test_openapi_sdk_quality():
    """Verify OpenAPI operation IDs match clean SDK function names."""
    from app.main_app import app
    openapi = app.openapi()
    assert openapi["info"]["title"] == "AI-Assisted Content Moderation & Publishing API"

    paths = openapi["paths"]
    assert paths["/posts/"]["post"]["operationId"] == "create_post"
    assert paths["/posts/"]["get"]["operationId"] == "list_posts"
    assert paths["/posts/{post_id}/submit/"]["post"]["operationId"] == "submit_post"
    assert paths["/posts/{post_id}/publish/"]["patch"]["operationId"] == "publish_post"
    assert paths["/posts/{post_id}"]["get"]["operationId"] == "get_post"


def test_generic_500_handler(client, monkeypatch):
    """Verify unhandled exceptions return clean 500 JSON message."""
    from app import crud

    def mock_get_post(*args, **kwargs):
        raise RuntimeError("Database connection dropped")

    monkeypatch.setattr(crud, "get_post", mock_get_post)
    res = client.get("/posts/1")
    assert res.status_code == 500
    assert res.json() == {"detail": "An internal server error occurred."}


def test_database_get_db_generator():
    """Verify get_db generator dependency yields session and closes it."""
    from app.database import get_db
    gen = get_db()
    session = next(gen)
    assert session is not None
    try:
        next(gen)
    except StopIteration:
        pass


def test_post_creation_stores_author_username(client):
    """Creating a post with author_username correctly stores and returns it."""
    res = client.post(
        "/posts/",
        json={
            "title": "Author Owned Story",
            "content": "A story written specifically by user alice.",
            "author_username": "alice",
        },
    )
    assert res.status_code == 201
    data = res.json()
    assert data["author_username"] == "alice"


def test_flagged_posts_privacy_scoping(client):
    """Flagged posts are only visible to the user who authored them."""
    # Create draft for alice
    p_alice = client.post(
        "/posts/",
        json={"title": "Alice Title", "content": "Short", "author_username": "alice"},
    ).json()["id"]
    client.post(f"/posts/{p_alice}/submit/")  # Flagged

    # Create draft for bob
    p_bob = client.post(
        "/posts/",
        json={"title": "Bob Title", "content": "Short", "author_username": "bob"},
    ).json()["id"]
    client.post(f"/posts/{p_bob}/submit/")  # Flagged

    # Alice queries flagged posts -> only alice's post returned
    res_alice = client.get("/posts/?status=flagged&current_user=alice")
    assert res_alice.status_code == 200
    ids_alice = [p["id"] for p in res_alice.json()]
    assert p_alice in ids_alice
    assert p_bob not in ids_alice

    # Bob queries flagged posts -> only bob's post returned
    res_bob = client.get("/posts/?status=flagged&current_user=bob")
    assert res_bob.status_code == 200
    ids_bob = [p["id"] for p in res_bob.json()]
    assert p_bob in ids_bob
    assert p_alice not in ids_bob

    # Charlie (third user) queries flagged posts -> neither returned
    res_charlie = client.get("/posts/?status=flagged&current_user=charlie")
    assert res_charlie.status_code == 200
    assert len(res_charlie.json()) == 0


def test_published_posts_visible_to_all_users(client):
    """Published posts can be seen and read by any user, regardless of author."""
    # Alice creates, approves, and publishes a post
    p_alice = client.post(
        "/posts/",
        json={
            "title": "Alice Public Wisdom",
            "content": "This is a great long article explaining microservice architecture in depth.",
            "author_username": "alice",
        },
    ).json()["id"]
    client.post(f"/posts/{p_alice}/submit/")
    client.patch(f"/posts/{p_alice}/publish/")

    # Bob lists published posts -> alice's published post is visible
    res_bob = client.get("/posts/?status=published&current_user=bob")
    assert res_bob.status_code == 200
    ids_bob = [p["id"] for p in res_bob.json()]
    assert p_alice in ids_bob
    assert res_bob.json()[0]["author_username"] == "alice"

