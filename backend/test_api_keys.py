"""
Quick script to test if API keys are valid
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_api():
    """Test Gemini API key"""
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment")
        return False
    
    print(f"✓ GEMINI_API_KEY found: {api_key[:10]}...{api_key[-4:]}")
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        # Try to list models to verify key works
        models = genai.list_models()
        model_list = list(models)
        
        if model_list:
            print(f"✅ GEMINI_API_KEY is VALID - Found {len(model_list)} models")
            return True
        else:
            print("⚠️  GEMINI_API_KEY might be invalid - No models found")
            return False
            
    except Exception as e:
        print(f"❌ GEMINI_API_KEY is INVALID - Error: {str(e)}")
        return False

def test_groq_api():
    """Test Groq API key"""
    api_key = os.getenv('GROQ_API_KEY')
    
    if not api_key:
        print("❌ GROQ_API_KEY not found in environment")
        return False
    
    print(f"✓ GROQ_API_KEY found: {api_key[:10]}...{api_key[-4:]}")
    
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        
        # Try to list models to verify key works
        models = client.models.list()
        
        if models.data:
            print(f"✅ GROQ_API_KEY is VALID - Found {len(models.data)} models")
            return True
        else:
            print("⚠️  GROQ_API_KEY might be invalid - No models found")
            return False
            
    except Exception as e:
        print(f"❌ GROQ_API_KEY is INVALID - Error: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("API Key Validation Test")
    print("=" * 60)
    print()
    
    gemini_valid = test_gemini_api()
    print()
    groq_valid = test_groq_api()
    print()
    
    print("=" * 60)
    print("Summary:")
    print("=" * 60)
    
    if gemini_valid:
        print("✅ Gemini API: Image detection and feedback generation will work")
    else:
        print("❌ Gemini API: Image detection and feedback generation will NOT work")
    
    if groq_valid:
        print("✅ Groq API: Alternative LLM for feedback generation available")
    else:
        print("❌ Groq API: Alternative LLM not available")
    
    print()
    
    if not gemini_valid and not groq_valid:
        print("⚠️  WARNING: No valid API keys found!")
        print("   You need to get new API keys from:")
        print("   - Gemini: https://makersuite.google.com/app/apikey")
        print("   - Groq: https://console.groq.com/keys")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
