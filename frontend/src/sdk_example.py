"""
Example usage of the generated Python SDK (OpenAPI Generator CLI).

How to run:
  1. Install the SDK:        pip install ./moderation_sdk
  2. Start the backend:      python main.py
  3. Run this script:        python sdk_example.py
"""
from moderation_sdk import ApiClient, Configuration
from moderation_sdk.api.posts_api import PostsApi
from moderation_sdk.models.post_create import PostCreate
from moderation_sdk.exceptions import ApiException

config = Configuration(host="http://localhost:8000")

GOOD_CONTENT = (
    "Learning FastAPI has been a rewarding experience. The framework makes it easy "
    "to build clean, well-documented APIs, and the automatic OpenAPI generation "
    "saves a lot of time when creating client SDKs."
)

with ApiClient(config) as client:
    api = PostsApi(client)
    try:
        # 1. Create a polite draft
        good = api.create_post(PostCreate(title="My FastAPI Journey", content=GOOD_CONTENT))
        print(f"Created post {good.id}, status: {good.status}")

        # 2. Submit it for moderation
        result = api.submit_post(good.id)
        print(f"Moderation result: {result.status}, reasons: {result.reasons}")

        # 3. Create a short ALL-CAPS post and submit it (should be flagged)
        bad = api.create_post(PostCreate(title="Angry post", content="THIS IS TERRIBLE!!!"))
        bad_result = api.submit_post(bad.id)
        print(f"Bad post result: {bad_result.status}")
        for reason in bad_result.reasons:
            print("  -", reason)

        # 4. List posts by status
        for status in ("approved", "flagged"):
            posts = api.list_posts(status=status)
            print(f"{status} posts: {[p.id for p in posts]}")

        # 5. Publish the approved post
        published = api.publish_post(good.id)
        print(f"Published post {published.id}, status: {published.status}")

        # 6. Get it again to confirm
        fetched = api.get_post(good.id)
        print(f"Fetched: {fetched.title} ({fetched.status})")

    except ApiException as e:
        print(f"API error {e.status}: {e.body}")