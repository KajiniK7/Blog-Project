-- ============================================================================
-- Seed Data for Content Moderation & Publishing Platform
-- To load this seed data into the database:
--   sqlite3 posts.db < seed_data.sql
-- Or in Windows PowerShell:
--   Get-Content seed_data.sql | sqlite3 posts.db
-- ============================================================================

INSERT INTO posts (title, content, status, flagged_reasons)
VALUES (
    'Drafting Guidelines for Community Discussion',
    'Working on new rules for respectful, high-quality discussion across our platform.',
    'draft',
    NULL
);

INSERT INTO posts (title, content, status, flagged_reasons)
VALUES (
    'Upcoming Architecture Overhaul RFC',
    'Proposing modular service boundaries and database indexing optimizations for next quarter.',
    'draft',
    NULL
);

INSERT INTO posts (title, content, status, flagged_reasons)
VALUES (
    'Get Rich Quick Miracle Token',
    'Click here to buy guaranteed crypto coins now idiot! Guaranteed 1000x return overnight.',
    'flagged',
    '["Spam or promotional content detected", "Banned words detected: idiot"]'
);

INSERT INTO posts (title, content, status, flagged_reasons)
VALUES (
    'Hi',
    'Yo',
    'flagged',
    '["Content too short", "Insufficient descriptive body"]'
);

INSERT INTO posts (title, content, status, flagged_reasons)
VALUES (
    'Understanding Clean Architecture in Python',
    'Writing maintainable software requires clear domain separation, explicit schemas, and strong test coverage.',
    'approved',
    NULL
);

INSERT INTO posts (title, content, status, flagged_reasons)
VALUES (
    'Welcome to the Moderation & Publishing Hub',
    'We are excited to launch our automated AI-assisted moderation queue and editorial workflow.',
    'approved',
    NULL
);

INSERT INTO posts (title, content, status, flagged_reasons)
VALUES (
    'Building Robust Web Services with FastAPI',
    'FastAPI leverages standard Python type hints and Pydantic validation to deliver high developer velocity and speed.',
    'published',
    NULL
);

INSERT INTO posts (title, content, status, flagged_reasons)
VALUES (
    'The Evolution of Asynchronous Web Applications',
    'Modern ASGI servers and event loops enable single-thread high concurrency with minimal CPU and memory overhead.',
    'published',
    NULL
);
