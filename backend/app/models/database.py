"""
SQLAlchemy database models for AI Pronunciation Coach.

This module defines the database schema including:
- User: User information and authentication
- PronunciationAttempt: Individual pronunciation evaluation records
- GameScore: Game mode scoring records
"""

from datetime import datetime, UTC
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    """User model for storing user information."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    
    # Relationships
    pronunciation_attempts = relationship(
        "PronunciationAttempt",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    game_scores = relationship(
        "GameScore",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"


class PronunciationAttempt(Base):
    """Model for storing individual pronunciation evaluation attempts."""
    
    __tablename__ = "pronunciation_attempts"
    __table_args__ = (
        # Indexes for performance optimization
        {"sqlite_autoincrement": True}
    )
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    target_word = Column(String(100), nullable=False)
    transcribed_text = Column(String(200))
    accuracy_score = Column(Float, nullable=False)
    expected_phonemes = Column(Text)
    actual_phonemes = Column(Text)
    mode = Column(String(20), nullable=False)  # 'audio', 'image', 'game'
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False, index=True)
    
    # Relationships
    user = relationship("User", back_populates="pronunciation_attempts")
    
    def __repr__(self):
        return (
            f"<PronunciationAttempt(id={self.id}, user_id={self.user_id}, "
            f"target_word='{self.target_word}', score={self.accuracy_score})>"
        )


class GameScore(Base):
    """Model for storing game mode scores."""
    
    __tablename__ = "game_scores"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    total_score = Column(Integer, nullable=False)
    words_attempted = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="game_scores")
    
    def __repr__(self):
        return (
            f"<GameScore(id={self.id}, user_id={self.user_id}, "
            f"total_score={self.total_score}, words_attempted={self.words_attempted})>"
        )
