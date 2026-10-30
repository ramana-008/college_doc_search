"""
ProjectForge: Phase 0 - Connection & Environment Verification Test
Verifies Python 3.10+, python-dotenv configuration, and Google AI Studio API access.
"""

import os
import sys

# 1. Check Python version (3.10+ required)
major, minor = sys.version_info[:2]
print(f"[*] Detected Python runtime: {sys.version.split()[0]}")
if major < 3 or (major == 3 and minor < 10):
    print(f"[FAIL] Python 3.10 or higher is required. You are using Python {major}.{minor}.")
    sys.exit(1)

# 2. Check dotenv & load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("[*] Successfully loaded environment configuration (.env)")
except ImportError:
    print("[FAIL] 'python-dotenv' is not installed. Run: pip install python-dotenv")
    sys.exit(1)

# 3. Verify Gemini API key presence
api_key = os.getenv("GEMINI_API_KEY")
if not api_key or api_key == "paste_your_gemini_api_key_here":
    print("\n[ERROR] GEMINI_API_KEY is not set or still contains the placeholder!")
    print("Action required:")
    print("  1. Create a file named '.env' in this folder (same directory as test_connection.py).")
    print("  2. Add: GEMINI_API_KEY=\"AIzaSy...\" (get your free key from https://aistudio.google.com/apikey).")
    print("  3. Never commit .env to GitHub (it is already included in .gitignore).")
    sys.exit(1)

masked_key = api_key[:6] + "..." + api_key[-4:] if len(api_key) > 10 else "***"
print(f"[*] Found GEMINI_API_KEY: {masked_key}")

# 4. Test live connection to Google AI Studio
try:
    from google import genai
    print("[*] Initializing Google GenAI Client...")
    client = genai.Client(api_key=api_key)

    print("[*] Sending ping request to Gemini 2.5 Flash model...")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Say exactly: 'ProjectForge connection verified: Ready for Phase 1.'"
    )

    print("\n" + "=" * 60)
    print(" SUCCESS! Gemini API Connection Test PASSED.")
    print(" Model Response:")
    print(f"   {response.text.strip()}")
    print("=" * 60)
    print("\nYour Phase 0 setup is complete. You can now proceed to Phase 1: Document Ingestion.")

except Exception as err:
    print(f"\n[FAIL] Connection error occurred: {err}")
    print("\nLikely causes in order of probability:")
    print("  1. Invalid API Key: Check that you copied the complete key without trailing spaces.")
    print("  2. Network / Proxy: If you are behind college Wi-Fi/firewall, test on mobile hotspot.")
    print("  3. Quota / Location: Ensure your Google account has AI Studio access enabled.")
    sys.exit(1)