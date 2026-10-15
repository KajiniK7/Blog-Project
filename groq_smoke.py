"""Manual live Groq moderation check; run directly, not through pytest."""

from app.moderation import GroqModerationError, moderate_with_groq


def main() -> int:
    title = "A note about learning"
    content = (
        "Learning a new skill takes patience and practice. Sharing helpful advice "
        "can make the process easier for everyone in the community."
    )

    try:
        result = moderate_with_groq(title, content)
    except GroqModerationError as exc:
        print(f"Groq smoke test failed: {exc}")
        return 1

    print(f"Groq smoke test passed: {result.status if hasattr(result, 'status') else 'approved' if result.approved else 'flagged'}")
    for reason in result.reasons:
        print(f"- {reason}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())