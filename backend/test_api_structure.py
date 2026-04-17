"""
Test API structure without running the full app
"""

def test_api_structure():
    """Test that the API endpoints are properly defined"""
    
    # Check that main.py has the required endpoints
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Check for required endpoints
    required_endpoints = [
        '@app.post("/api/pronunciation/evaluate"',
        '@app.post("/api/pronunciation/image"',
        '@app.get("/api/user/{user_id}/history"',
        '@app.get("/api/leaderboard"',
        '@app.get("/api/health"'
    ]
    
    for endpoint in required_endpoints:
        assert endpoint in content, f"Missing endpoint: {endpoint}"
    
    # Check for CORS middleware
    assert 'CORSMiddleware' in content, "Missing CORS middleware"
    
    # Check for database initialization
    assert 'init_db()' in content, "Missing database initialization"
    
    # Check for module imports
    required_modules = [
        'AudioInputModule',
        'AudioProcessor',
        'SpeechRecognizer',
        'PhonemeAnalyzer',
        'ScoringEngine',
        'FeedbackGenerator',
        'ImageDetector'
    ]
    
    for module in required_modules:
        assert module in content, f"Missing module import: {module}"
    
    print("✓ All API structure checks passed!")
    print("✓ POST /api/pronunciation/evaluate endpoint defined")
    print("✓ POST /api/pronunciation/image endpoint defined")
    print("✓ GET /api/user/{user_id}/history endpoint defined")
    print("✓ GET /api/leaderboard endpoint defined")
    print("✓ GET /api/health endpoint defined")
    print("✓ CORS middleware configured")
    print("✓ Database initialization included")
    print("✓ All processing modules imported")

if __name__ == "__main__":
    test_api_structure()
