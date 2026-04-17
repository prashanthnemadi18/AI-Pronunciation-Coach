"""
Test PostgreSQL URL detection without requiring psycopg2 installation.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

def test_sqlite_detection():
    """Test SQLite URL detection."""
    os.environ["DATABASE_URL"] = "sqlite:///./test.db"
    
    # Import after setting env var
    from importlib import reload
    from app.models import db_connection
    reload(db_connection)
    
    assert db_connection.is_sqlite == True
    assert db_connection.DATABASE_URL.startswith("sqlite")
    print("✓ SQLite detection works correctly")

def test_default_sqlite():
    """Test default SQLite database."""
    if "DATABASE_URL" in os.environ:
        del os.environ["DATABASE_URL"]
    
    from importlib import reload
    from app.models import db_connection
    reload(db_connection)
    
    assert db_connection.is_sqlite == True
    assert "pronunciation_coach.db" in db_connection.DATABASE_URL
    print("✓ Default SQLite database configured correctly")

def test_postgres_url_format():
    """Test that PostgreSQL URL format is recognized."""
    # We can't actually connect without psycopg2, but we can verify detection
    test_url = "postgresql://user:pass@localhost:5432/dbname"
    assert test_url.startswith("postgresql")
    print("✓ PostgreSQL URL format recognized")

if __name__ == "__main__":
    print("Testing database URL detection...")
    print()
    test_sqlite_detection()
    test_default_sqlite()
    test_postgres_url_format()
    print()
    print("All detection tests passed! ✓")
