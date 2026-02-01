from meeting_os.services.kapso_handler import KapsoClient
import os
from dotenv import load_dotenv

load_dotenv()

def test_kapso():
    print("🚀 Testing Kapso (WhatsApp) Integration...")
    
    api_key = os.getenv("KAPSO_API_KEY")
    phone_id = os.getenv("WHATSAPP_PHONE_ID")
    target_phone = os.getenv("TEST_PHONE_NUMBER") # Add this to env to test safely
    
    print(f"   API Key Present: {'✅' if api_key else '❌'}")
    print(f"   Phone ID: {phone_id if phone_id else '❌'}")
    
    if not api_key or not phone_id:
        print("\n⚠️  Please set KAPSO_API_KEY and WHATSAPP_PHONE_ID in .env.")
        return

    if not target_phone:
        print("⚠️  No TEST_PHONE_NUMBER in env. Skipping actual send.")
        return

    client = KapsoClient()
    success = client.send_whatsapp_message(target_phone, "🔔 This is a test message from Meeting OS!")
    
    if success:
        print("\n✨ Kapso Integration Verified!")
    else:
        print("\n❌ Message Failed.")

if __name__ == "__main__":
    test_kapso()
