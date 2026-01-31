import os
import google.generativeai as genai
import logging
from dotenv import load_dotenv
from meeting_os.lib.tenancy.vault_context import TenantContext

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class LLMClient:
    """Wrapper for Google Gemini Client with observability Hooks."""
    
    def __init__(self, api_key=None, event_logger=None):
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            logger.warning("GOOGLE_API_KEY not found. Calls will fail.")
        else:
            genai.configure(api_key=self.api_key)
        
        self.event_logger = event_logger

    def generate(self, prompt, model="gemini-2.5-flash", temperature=0.0):
        """
        Generate text from prompt.
        """
        # Map legacy/Anthropic model names to Gemini if passed
        model_map = {
            "claude-3-haiku-20240307": "gemini-2.5-flash",
            "claude-3-sonnet-20240229": "gemini-2.5-pro",
            "claude-3-opus-20240229": "gemini-2.5-pro",
            "gemini-1.5-flash": "gemini-2.5-flash",
        }
        
        actual_model = model_map.get(model, model)

        # Log call start
        if self.event_logger:
            self.event_logger.log({
                "type": "llm.call",
                "payload": {"model": actual_model, "prompt_preview": prompt[:100]}
            })

        try:
            gemini_model = genai.GenerativeModel(actual_model)
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=8192,
            )
            
            response = gemini_model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            response_text = response.text
            
            # Log success
            if self.event_logger:
                 self.event_logger.log({
                    "type": "llm.response",
                    "payload": {"response_preview": response_text[:100]}
                })
            
            return response_text
            
        except Exception as e:
            logger.error(f"LLM Call Failed: {e}")
            if self.event_logger:
                self.event_logger.log({
                    "type": "llm.error",
                    "payload": {"error": str(e)},
                    "severity": "high"
                })
            raise
