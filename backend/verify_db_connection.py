"""
Verification script for database connection module.

This script demonstrates:
- Database initialization
- Connection health check
- Creating and querying data
"""

import os
import sys

# Set up path to import from app
sys.path.insert(0, os.path.dirname(__file__))

from app.models.db_connection import init_db, check_db_connection, SessionLocal
from app.models.database import User, PronunciationAttempt, GameScore

def main():
    print("=" * 60)
    print("Database Connection Module Verification")
    print("=" * 60)
    
    # Set database URL for testing
    os.environ["DATABASE_URL"] = "sqlite:///./test_verification.db"
    
    # Initialize database
    print("\n1. Initializing database...")
    init_db()
    print("   ✓ Database initialized successfully")
    
    # Check connection
    print("\n2. Checking database connection...")
    if check_db_connection():
        print("   ✓ Database connection is healthy")
    else:
        print("   ✗ Database connection failed")
        return
    
    # Create a test user
    print("\n3. Creating test user...")
    db = SessionLocal()
    try:
        user = User(username="test_user")
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"   ✓ Created user: {user}")
        
        # Create a pronunciation attempt
        print("\n4. Creating pronunciation attempt...")
        attempt = PronunciationAttempt(
            user_id=user.id,
            target_word="hello",
            transcribed_text="hello",
            accuracy_score=95.5,
            expected_phonemes="HH AH L OW",
            actual_phonemes="HH AH L OW",
            mode="audio"
        )
        db.add(attempt)
        db.commit()
        db.refresh(attempt)
        print(f"   ✓ Created attempt: {attempt}")
        
        # Create a game score
        print("\n5. Creating game score...")
        score = GameScore(
            user_id=user.id,
            total_score=850,
            words_attempted=10
        )
        db.add(score)
        db.commit()
        db.refresh(score)
        print(f"   ✓ Created score: {score}")
        
        # Query data
        print("\n6. Querying data...")
        users = db.query(User).all()
        attempts = db.query(PronunciationAttempt).all()
        scores = db.query(GameScore).all()
        print(f"   ✓ Found {len(users)} users")
        print(f"   ✓ Found {len(attempts)} pronunciation attempts")
        print(f"   ✓ Found {len(scores)} game scores")
        
        # Test foreign key relationships
        print("\n7. Testing relationships...")
        user_with_data = db.query(User).first()
        print(f"   ✓ User has {len(user_with_data.pronunciation_attempts)} attempts")
        print(f"   ✓ User has {len(user_with_data.game_scores)} game scores")
        
    finally:
        db.close()
    
    print("\n" + "=" * 60)
    print("All verifications passed! ✓")
    print("=" * 60)
    
    # Clean up test database
    if os.path.exists("test_verification.db"):
        os.remove("test_verification.db")
        print("\nTest database cleaned up.")

if __name__ == "__main__":
    main()
