from sqlalchemy import Column, Integer, Text, TIMESTAMP, CheckConstraint, text
from app.database import Base


class Post(Base):
    __tablename__ = "posts"
    __table_args__ = (
        CheckConstraint(
            "status IN ('draft','flagged','approved','published')",
            name="check_status_valid",
        ),
        {"sqlite_autoincrement": True},
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    status = Column(Text, nullable=False, server_default=text("'draft'"))
    flagged_reasons = Column(Text, nullable=True)
    author_username = Column(Text, nullable=True, index=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        {"sqlite_autoincrement": True},
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, unique=True, nullable=False, index=True)
    password_hash = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

