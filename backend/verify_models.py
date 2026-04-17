"""
Simple verification script to test database models.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, User, PronunciationAttempt, GameScore

# Create in-memory database
engine = create_engine("sqlite:///:memory:", echo=True)
Base.metadata.create_all(engine)

# Create session
Session = sessionmaker(bind=engine)
session = Session()

print("\n=== Testing User Model ===")
user = User(username="testuser")
session.add(user)
session.commit()
print(f"Created user: {user}")
print(f"User ID: {user.id}")
print(f"Username: {user.username}")
print(f"Created at: {user.created_at}")

print("\n=== Testing PronunciationAttempt Model ===")
attempt = PronunciationAttempt(
    user_id=user.id,
    target_word="hello",
    transcribed_text="hello",
    accuracy_score=95.5,
    expected_phonemes="HH AH L OW",
    actual_phonemes="HH AH L OW",
    mode="audio"
)
session.add(attempt)
session.commit()
print(f"Created attempt: {attempt}")
print(f"Attempt ID: {attempt.id}")
print(f"Target word: {attempt.target_word}")
print(f"Accuracy score: {attempt.accuracy_score}")
print(f"Mode: {attempt.mode}")

print("\n=== Testing GameScore Model ===")
game_score = GameScore(
    user_id=user.id,
    total_score=500,
    words_attempted=10
)
session.add(game_score)
session.commit()
print(f"Created game score: {game_score}")
print(f"Game score ID: {game_score.id}")
print(f"Total score: {game_score.total_score}")
print(f"Words attempted: {game_score.words_attempted}")

print("\n=== Testing Relationships ===")
print(f"User's pronunciation attempts: {len(user.pronunciation_attempts)}")
print(f"User's game scores: {len(user.game_scores)}")
print(f"Attempt belongs to user: {attempt.user.username}")
print(f"Game score belongs to user: {game_score.user.username}")

print("\n=== All Models Verified Successfully! ===")

session.close()
