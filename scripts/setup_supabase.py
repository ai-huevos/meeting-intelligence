import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def setup_supabase():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ DATABASE_URL not found. Please set it in .env (Supabase Connection String).")
        return

    print("🚀 Connecting to Supabase...")
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Create Tables
        print("   Creating Tables...")
        
        # 1. Event Log
        cur.execute("""
        CREATE TABLE IF NOT EXISTS event_log (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            timestamp TIMESTAMP DEFAULT NOW(),
            type VARCHAR(50),
            agent VARCHAR(50),
            payload JSONB,
            severity VARCHAR(20)
        );
        """)
        
        # 2. Meetings (Mirror of Notion for faster Retrieval)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS meetings (
            id VARCHAR(100) PRIMARY KEY, -- Notion ID or Fireflies ID
            title TEXT,
            transcript TEXT,
            summary TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        );
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Supabase Schema Initialized.")
        
    except Exception as e:
        print(f"❌ Database Error: {e}")

if __name__ == "__main__":
    setup_supabase()
