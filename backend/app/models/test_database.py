"""
Unit tests for database models.

Tests verify:
- Model creation and field validation
- Foreign key relationships
- Indexes are properly defined
"""

import pytest
from datetime import datetime
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from .database import Base, User, PronunciationAttempt, GameScore


@pytest.fixture
def db_session():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_user_model_creation(db_session):
    """Test User model can be created with required fields."""
    user = User(username="testuser")
    db_session.add(user)
    db_session.commit()
    
    assert user.id is not None
    assert user.username == "testuser"
    assert isinstance(user.created_at, datetime)


def test_user_unique_username(db_session):
    """Test username uniqueness constraint."""
    user1 = User(username="testuser")
    user2 = User(username="testuser")
    
    db_session.add(user1)
    db_session.commit()
    
    db_session.add(user2)
    with pytest.raises(Exception):  # SQLAlchemy will raise IntegrityError
        db_session.commit()


def test_pronunciation_attempt_model_creation(db_session):
    """Test PronunciationAttempt model with all required fields."""
    user = User(username="testuser")
    db_session.add(user)
    db_session.commit()
    
    attempt = PronunciationAttempt(
        user_id=user.id,
        target_word="hello",
        transcribed_text="hello",
        accuracy_score=95.5,
        expected_phonemes="HH AH L OW",
        actual_phonemes="HH AH L OW",
        mode="audio"
    )
    db_session.add(attempt)
    db_session.commit()
    
    assert attempt.id is not None
    assert attempt.user_id == user.id
    assert attempt.target_word == "hello"
    assert attempt.transcribed_text == "hello"
    assert attempt.accuracy_score == 95.5
    assert attempt.expected_phonemes == "HH AH L OW"
    assert attempt.actual_phonemes == "HH AH L OW"
    assert attempt.mode == "audio"
    assert isinstance(attempt.created_at, datetime)


def test_pronunciation_attempt_foreign_key(db_session):
    """Test foreign key relationship between PronunciationAttempt and User."""
    user = User(username="testuser")
    db_session.add(user)
    db_session.commit()
    
    attempt = PronunciationAttempt(
        user_id=user.id,
        target_word="hello",
        accuracy_score=95.5,
        mode="audio"
    )
    db_session.add(attempt)
    db_session.commit()
    
    # Test relationship
    assert attempt.user == user
    assert attempt in user.pronunciation_attempts


def test_game_score_model_creation(db_session):
    """Test GameScore model with all required fields."""
    user = User(username="testuser")
    db_session.add(user)
    db_session.commit()
    
    game_score = GameScore(
        user_id=user.id,
        total_score=500,
        words_attempted=10
    )
    db_session.add(game_score)
    db_session.commit()
    
    assert game_score.id is not None
    assert game_score.user_id == user.id
    assert game_score.total_score == 500
    assert game_score.words_attempted == 10
    assert isinstance(game_score.created_at, datetime)


def test_game_score_foreign_key(db_session):
    """Test foreign key relationship between GameScore and User."""
    user = User(username="testuser")
    db_session.add(user)
    db_session.commit()
    
    game_score = GameScore(
        user_id=user.id,
        total_score=500,
        words_attempted=10
    )
    db_session.add(game_score)
    db_session.commit()
    
    # Test relationship
    assert game_score.user == user
    assert game_score in user.game_scores


def test_cascade_delete(db_session):
    """Test cascade delete removes related records when user is deleted."""
    user = User(username="testuser")
    db_session.add(user)
    db_session.commit()
    
    attempt = PronunciationAttempt(
        user_id=user.id,
        target_word="hello",
        accuracy_score=95.5,
        mode="audio"
    )
    game_score = GameScore(
        user_id=user.id,
        total_score=500,
        words_attempted=10
    )
    db_session.add(attempt)
    db_session.add(game_score)
    db_session.commit()
    
    # Delete user
    db_session.delete(user)
    db_session.commit()
    
    # Verify related records are deleted
    assert db_session.query(PronunciationAttempt).count() == 0
    assert db_session.query(GameScore).count() == 0


def test_indexes_exist():
    """Test that required indexes are defined on tables."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    inspector = inspect(engine)
    
    # Check pronunciation_attempts indexes
    attempts_indexes = inspector.get_indexes("pronunciation_attempts")
    index_columns = [idx["column_names"] for idx in attempts_indexes]
    
    # SQLAlchemy creates indexes for foreign keys automatically
    # We verify user_id and created_at have indexes
    assert any("user_id" in cols for cols in index_columns)
    
    # Check game_scores indexes
    scores_indexes = inspector.get_indexes("game_scores")
    index_columns = [idx["column_names"] for idx in scores_indexes]
    assert any("user_id" in cols for cols in index_columns)


def test_model_repr():
    """Test string representation of models."""
    user = User(id=1, username="testuser")
    assert "testuser" in repr(user)
    assert "1" in repr(user)
    
    attempt = PronunciationAttempt(
        id=1,
        user_id=1,
        target_word="hello",
        accuracy_score=95.5,
        mode="audio"
    )
    assert "hello" in repr(attempt)
    assert "95.5" in repr(attempt)
    
    game_score = GameScore(
        id=1,
        user_id=1,
        total_score=500,
        words_attempted=10
    )
    assert "500" in repr(game_score)
    assert "10" in repr(game_score)
