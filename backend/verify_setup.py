"""
Comprehensive setup verification script
Checks all API keys, modules, and dependencies
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def check_env_variables():
    """Check if environment variables are set"""
    print_section("Environment Variables")
    
    env_vars = {
        'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
        'LLM_API_KEY': os.getenv('LLM_API_KEY'),
        'GROQ_API_KEY': os.getenv('GROQ_API_KEY'),
        'DATABASE_URL': os.getenv('DATABASE_URL'),
        'WHISPER_MODEL_SIZE': os.getenv('WHISPER_MODEL_SIZE', 'base'),
    }
    
    all_good = True
    for key, value in env_vars.items():
        if value:
            masked = f"{value[:10]}...{value[-4:]}" if len(value) > 14 else "***"
            print(f"✅ {key}: {masked}")
        else:
            print(f"❌ {key}: NOT SET")
            if key in ['GEMINI_API_KEY', 'LLM_API_KEY']:
                all_good = False
    
    return all_good

def check_modules():
    """Check if all modules can be imported"""
    print_section("Module Imports")
    
    modules = [
        ('audio_input', 'app.modules.audio_input', 'AudioInputModule'),
        ('audio_processor', 'app.modules.audio_processor', 'AudioProcessor'),
        ('speech_recognizer', 'app.modules.speech_recognizer', 'SpeechRecognizer'),
        ('phoneme_analyzer', 'app.modules.phoneme_analyzer', 'PhonemeAnalyzer'),
        ('scoring_engine', 'app.modules.scoring_engine', 'ScoringEngine'),
        ('feedback_generator', 'app.modules.feedback_generator', 'FeedbackGenerator'),
        ('image_detector', 'app.modules.image_detector', 'ImageDetector'),
    ]
    
    all_good = True
    for name, module_path, class_name in modules:
        try:
            module = __import__(module_path, fromlist=[class_name])
            getattr(module, class_name)
            print(f"✅ {name}: OK")
        except Exception as e:
            print(f"❌ {name}: FAILED - {str(e)}")
            all_good = False
    
    return all_good

def check_dependencies():
    """Check if required dependencies are installed"""
    print_section("Dependencies")
    
    dependencies = [
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'Uvicorn'),
        ('sqlalchemy', 'SQLAlchemy'),
        ('pydantic', 'Pydantic'),
        ('whisper', 'OpenAI Whisper'),
        ('pydub', 'PyDub'),
        ('nltk', 'NLTK'),
        ('PIL', 'Pillow'),
        ('google.generativeai', 'Google Generative AI'),
        ('groq', 'Groq'),
    ]
    
    all_good = True
    for module_name, display_name in dependencies:
        try:
            __import__(module_name)
            print(f"✅ {display_name}: Installed")
        except ImportError:
            print(f"❌ {display_name}: NOT INSTALLED")
            all_good = False
    
    return all_good

def check_api_keys():
    """Test if API keys are valid"""
    print_section("API Key Validation")
    
    # Test Gemini API
    gemini_key = os.getenv('GEMINI_API_KEY')
    if gemini_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            models = list(genai.list_models())
            if models:
                print(f"✅ Gemini API: VALID ({len(models)} models available)")
            else:
                print("⚠️  Gemini API: Key set but no models found")
        except Exception as e:
            print(f"❌ Gemini API: INVALID - {str(e)}")
    else:
        print("❌ Gemini API: Key not set")
    
    # Test Groq API
    groq_key = os.getenv('GROQ_API_KEY')
    if groq_key:
        try:
            from groq import Groq
            client = Groq(api_key=groq_key)
            models = client.models.list()
            if models.data:
                print(f"✅ Groq API: VALID ({len(models.data)} models available)")
            else:
                print("⚠️  Groq API: Key set but no models found")
        except Exception as e:
            print(f"❌ Groq API: INVALID - {str(e)}")
    else:
        print("⚠️  Groq API: Key not set (optional)")

def check_database():
    """Check database connection"""
    print_section("Database")
    
    try:
        from app.models.db_connection import check_db_connection
        if check_db_connection():
            print("✅ Database: Connected")
            return True
        else:
            print("❌ Database: Connection failed")
            return False
    except Exception as e:
        print(f"❌ Database: ERROR - {str(e)}")
        return False

def check_server():
    """Check if server is running"""
    print_section("Server Status")
    
    try:
        import requests
        response = requests.get('http://localhost:8000/api/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Server: Running")
            print(f"   Status: {data.get('status')}")
            print(f"   Services:")
            for service, status in data.get('services', {}).items():
                icon = "✅" if status == "healthy" else "❌"
                print(f"     {icon} {service}: {status}")
            return True
        else:
            print(f"⚠️  Server: Running but returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Server: NOT RUNNING")
        print("   Start with: python start_server.py")
        return False
    except Exception as e:
        print(f"❌ Server: ERROR - {str(e)}")
        return False

def main():
    """Run all checks"""
    print("\n" + "=" * 60)
    print("  AI Pronunciation Coach - Setup Verification")
    print("=" * 60)
    
    results = {
        'Environment Variables': check_env_variables(),
        'Dependencies': check_dependencies(),
        'Modules': check_modules(),
        'Database': check_database(),
        'API Keys': True,  # Will be checked separately
    }
    
    # Check API keys (doesn't affect overall status)
    check_api_keys()
    
    # Check server
    server_running = check_server()
    
    # Summary
    print_section("Summary")
    
    all_passed = all(results.values())
    
    if all_passed and server_running:
        print("✅ ALL CHECKS PASSED!")
        print("\nYour setup is complete and ready to use.")
        print("\nAccess the API at:")
        print("  - Swagger UI: http://localhost:8000/docs")
        print("  - Health Check: http://localhost:8000/api/health")
    else:
        print("❌ SOME CHECKS FAILED")
        print("\nPlease fix the issues above before using the application.")
        
        if not server_running:
            print("\n⚠️  Server is not running. Start it with:")
            print("  cd backend")
            print("  .\\venv\\Scripts\\Activate.ps1")
            print("  python start_server.py")
    
    print("=" * 60)
    print()

if __name__ == "__main__":
    main()
