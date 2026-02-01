import os
import json
import logging
from notion_client import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SchemaDeployer:
    def __init__(self, token=None):
        self.token = token or os.environ.get("NOTION_API_KEY")
        if not self.token:
            raise ValueError("NOTION_API_KEY not found in environment variables.")
        self.client = Client(auth=self.token)
        self.db_ids = {}

    def load_template(self, name):
        """Load JSON template for database schema."""
        path = os.path.join(os.path.dirname(__file__), "templates", f"{name}.json")
        with open(path, "r") as f:
            return json.load(f)

    def create_database(self, parent_page_id, name, template_name=None):
        """Create a database in Notion."""
        template_name = template_name or name.lower()
        schema = self.load_template(template_name)
        
        logger.info(f"Creating database: {name}...")
        
        try:
            response = self.client.databases.create(
                parent={"page_id": parent_page_id},
                title=schema["title"],
                properties=schema["properties"]
            )
            db_id = response["id"]
            self.db_ids[name] = db_id
            logger.info(f"✅ Created {name} (ID: {db_id})")
            return db_id
        except Exception as e:
            logger.error(f"❌ Failed to create {name}: {e}")
            raise

    def add_relation(self, source_db_name, target_db_name, property_name, synced_property_name=None):
        """Add a relation property to a database."""
        source_id = self.db_ids.get(source_db_name)
        target_id = self.db_ids.get(target_db_name)
        
        if not source_id or not target_id:
            logger.error(f"❌ Cannot link {source_db_name} -> {target_db_name}: ID not found.")
            return

        logger.info(f"Linking {source_db_name} -> {target_db_name} as '{property_name}'...")
        
        properties = {
            property_name: {
                "relation": {
                    "database_id": target_id,
                    # "type": "dual_property" if synced_property_name else "single_property"
                    # Notion API default is dual if synced_property_name provided? 
                    # Actually keeping it simple: separate property update
                }
            }
        }
        
        # If we want dual-way sync (back-link), we need to specify it.
        # However, creating relation via API often requires simpler syntax initially.
        # Let's try basic relation first.
        
        try:
           self.client.databases.update(
                database_id=source_id,
                properties=properties
            )
           logger.info(f"✅ Relation added: {source_db_name}.{property_name}")
        except Exception as e:
            logger.error(f"❌ Failed to add relation {source_db_name}.{property_name}: {e}")
            raise

    def deploy(self, parent_page_id):
        """Deploy all core databases."""
        logger.info("🚀 Starting Schema Deployment...")
        
        # 1. Create Core DBs (Independent first)
        self.create_database(parent_page_id, "Company", "company")
        self.create_database(parent_page_id, "Person", "person")
        
        # 2. Create Dependent DBs
        self.create_database(parent_page_id, "Opportunity", "opportunity")
        self.create_database(parent_page_id, "Meeting", "meeting")
        
        # 3. Add Relations
        # Person -> Company
        self.add_relation("Person", "Company", "Company")
        
        # Opportunity -> Company
        self.add_relation("Opportunity", "Company", "Company")
        
        # Meeting -> Company
        self.add_relation("Meeting", "Company", "Company")
        
        # Meeting -> Participants (People)
        self.add_relation("Meeting", "Person", "Participants")
        
        # Meeting -> Opportunity
        self.add_relation("Meeting", "Opportunity", "Opportunity")
        
        logger.info("✨ Deployment Complete!")
        return self.db_ids

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Deploy Meeting OS Schema to Notion")
    parser.add_argument("--parent-id", required=True, help="ID of the parent page to create databases in")
    parser.add_argument("--api-key", help="Notion API Key (optional, defaults to env var)")
    
    args = parser.parse_args()
    
    deployer = SchemaDeployer(token=args.api_key)
    ids = deployer.deploy(args.parent_id)
    
    # Save IDs to a local file for reference
    with open("deployed_ids.json", "w") as f:
        json.dump(ids, f, indent=2)
    print("Database IDs saved to deployed_ids.json")
