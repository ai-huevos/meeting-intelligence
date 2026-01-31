import os
import sys
import unittest
from dotenv import load_dotenv

# Ensure we can import from root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meeting_os.agents.sales_agent import SalesAgent
from meeting_os.lib.tenancy.vault_context import TenantContext

# Load env in case it's not loaded
load_dotenv()

class TestSalesAgent(unittest.TestCase):
    def setUp(self):
        TenantContext.set_vault("test_vault_sales", "user_sales_test")
        self.agent = SalesAgent()
        
        # Load sample transcript
        with open("meeting-transcripts/Pricing-AI-Huevos-2f72b1c3-4393.md", "r") as f:
            self.transcript = f.read()

    def test_extraction(self):
        print("\nRunning Sales Extraction Test...")
        result = self.agent.extract_info("test_sales_meeting_1", self.transcript)
        
        print("Extraction Result:")
        import json
        print(json.dumps(result, indent=2))
        
        # Assertions
        self.assertIn("deal_info", result)
        self.assertEqual(result["deal_info"].get("stage"), "Discovery") # Or whatever the LLM determines
        self.assertIn("key_people", result)
        self.assertTrue(len(result["key_people"]) > 0)

if __name__ == "__main__":
    unittest.main()
