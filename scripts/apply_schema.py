import sys
import os

# Add parent directory to path to import meeting_os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from meeting_os.lib.db import db

def apply_schema():
    print("🚀 Applying Schema to Supabase...")
    
    schema_path = os.path.join(os.path.dirname(__file__), "../meeting_os/schema.sql")
    if not os.path.exists(schema_path):
        print(f"❌ Schema file not found at: {schema_path}")
        return

    with open(schema_path, "r") as f:
        sql = f.read()

    try:
        # Split by statements just in case, but usually execute_sql can handle blocks if supported
        # psycopg2 execute() can handle multiple statements in one string usually
        db.execute_sql(sql)
        print("✅ Schema applied successfully!")
    except Exception as e:
        print(f"❌ Failed to apply schema: {e}")

if __name__ == "__main__":
    apply_schema()
