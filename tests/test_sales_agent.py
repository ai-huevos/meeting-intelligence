
import unittest
import os
import sys
from unittest.mock import MagicMock, patch
import json

# Ensure we can import from root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meeting_os.agents.sales_agent import SalesAgent
from meeting_os.core.tenancy.vault_context import TenantContext

class TestSalesAgent(unittest.TestCase):
    def setUp(self):
        # Mock Vault Context
        TenantContext.set_vault("test_vault_sales", "user_sales_test")
        
        # Initialize Agent (dependencies are handled in __init__ but we mock the expensive ones)
        self.agent = SalesAgent()
        
    @patch('meeting_os.core.base_agent.BaseAgent.call_llm')
    def test_extraction(self, mock_call_llm):
        """Test extraction logic with mocked LLM response."""
        
        # Define what the LLM *would* return
        mock_llm_response = json.dumps({
            "deal_info": {
                "stage": "Discovery",
                "probability": 0.5,
                "deal_value": 50000
            },
            "key_people": ["Leia Organa", "Mon Mothma"],
            "next_steps": ["Schedule follow-up"]
        })
        
        mock_call_llm.return_value = mock_llm_response
        
        # Test Input
        transcript_snippet = "We are interested in the enterprise plan. Budget is 50k."
        
        # Run SUT
        result = self.agent.extract_info("test_meeting_id", transcript_snippet)
        
        # Assertions
        self.assertIn("deal_info", result)
        self.assertEqual(result["deal_info"]["stage"], "Discovery")
        self.assertEqual(result["deal_info"]["deal_value"], 50000)
        self.assertEqual(len(result["key_people"]), 2)
        
        # Verify LLM was called with some prompt
        mock_call_llm.assert_called_once()
        print("\n✅ SalesAgent Extraction Test (Mocked) Passed!")

if __name__ == "__main__":
    unittest.main()
