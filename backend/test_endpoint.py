"""
Quick test script to verify the evaluate endpoint works
"""
import requests
import base64
import json
from pathlib import Path

def test_evaluate_endpoint():
    """Test the pronunciation evaluation endpoint"""
    
    # Create a simple test audio (silence)
    # In real scenario, you'd use actual audio
    test_audio = b'\x00' * 1000  # Simple test data
    
    # Encode to base64
    audio_base64 = base64.b64encode(test_audio).decode('utf-8')
    
    # Prepare request
    url = "http://localhost:8000/api/pronunciation/evaluate"
    payload = {
        "audio": audio_base64,
        "target_word": "hello",
        "user_id": 1,
        "mode": "audio",
        "audio_format": "wav"
    }
    
    print("Testing pronunciation evaluation endpoint...")
    print(f"URL: {url}")
    print(f"Target word: {payload['target_word']}")
    print()
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print()
        
        if response.status_code == 200:
            print("✅ SUCCESS! Endpoint is working")
            print()
            print("Response:")
            print(json.dumps(response.json(), indent=2))
        else:
            print("❌ ERROR! Endpoint returned error")
            print()
            print("Response:")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR!")
        print("Cannot connect to http://localhost:8000")
        print()
        print("Make sure the backend server is running:")
        print("  cd backend")
        print("  .\\venv\\Scripts\\Activate.ps1")
        print("  python start_server.py")
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    test_evaluate_endpoint()
