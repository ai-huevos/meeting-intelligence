import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

def check_http_connection():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    if not url or not key:
        print("❌ Missing credentials in .env")
        return

    print(f"🌐 Testing HTTP Connection to {url}...")
    try:
        supabase: Client = create_client(url, key)
        # Try a simple read (even if table missing, it should return 400 or 200 empty)
        # We query a non-existent table just to check potential handshake
        response = supabase.table("event_log").select("*").limit(1).execute()
        print("✅ HTTP Connection Successful!")
        print(f"   Response: {response}")
    except Exception as e:
        print(f"❌ HTTP Connection Failed: {e}")

if __name__ == "__main__":
    check_http_connection()
