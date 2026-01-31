from meeting_os.lib.integrations.perplexity import PerplexityClient

class DocRetriever:
    """
    Retrieves technical documentation using Perplexity.
    Used to keep the Agent Builder up-to-date with external APIs.
    """
    
    def __init__(self):
        self.perplexity = PerplexityClient()
        
    def get_api_docs(self, tool_name, specific_feature):
        """
        Ask Perplexity for the latest API documentation or JSON schema.
        
        Args:
            tool_name: e.g. "n8n", "Notion", "Linear"
            specific_feature: e.g. "Create Database Page Node Schema", "Issue Create Mutations"
            
        Returns:
            str: The documentation snippet or JSON schema found.
        """
        query = f"Provide the official technical documentation and JSON schema for {tool_name}'s '{specific_feature}'. Output strictly the JSON structure if available, or a technical summary of parameters."
        
        print(f"📚 Retrieving docs for: {tool_name} -> {specific_feature}...")
        try:
            result = self.perplexity.research(query, model="sonar-pro")
            return result
        except Exception as e:
            print(f"❌ Doc Retrieval Failed: {e}")
            return None

if __name__ == "__main__":
    retriever = DocRetriever()
    # Test: Get n8n Notion Node docs
    docs = retriever.get_api_docs("n8n", "Notion Node Create Page Properties")
    print(docs[:500] + "...")
