import os
from supabase import create_client, Client
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DB:
    """
    Database wrapper for Supabase.
    Supports both REST API (via supabase-py) and Direct SQL (via psycopg2).
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DB, cls).__new__(cls)
            cls._instance._init_clients()
        return cls._instance
    
    def _init_clients(self):
        """Initialize Supabase and Postgres clients"""
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.database_url = os.getenv("DATABASE_URL")
        
        # REST Client (for simple CRUD + Realtime + Storage)
        if self.supabase_url and self.supabase_key:
            self.client: Client = create_client(self.supabase_url, self.supabase_key)
        else:
            print("⚠️ Warning: SUPABASE_URL or SUPABASE_KEY not found. REST client disabled.")
            self.client = None
            
        # SQL Client (for complex queries, migrations, analytics)
        # We don't keep a persistent connection for psycopg2 to handle thread safety/timeouts simply here.
        # For production, use a pool.
        
    def get_conn(self):
        """Get a raw Postgres connection"""
        if not self.database_url:
            raise ValueError("DATABASE_URL not set")
        return psycopg2.connect(self.database_url)
        
    def execute_sql(self, sql: str, params: tuple = None, fetch: bool = False):
        """Execute raw SQL safely"""
        conn = self.get_conn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, params)
                if fetch:
                    result = cur.fetchall()
                    conn.commit()
                    return result
                conn.commit()
                return None
        finally:
            conn.close()

    # --- Helper methods for Supabase REST Client ---
    
    def table(self, table_name: str):
        """Get a table builder from REST client"""
        if not self.client:
            raise RuntimeError("Supabase REST client not initialized")
        return self.client.table(table_name)

# Global DB Instance
db = DB()
