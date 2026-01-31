import re
from typing import Dict, Any, List
# from meeting_os.lib.observability.event_log import EventLog # Circular import? We'll inject logger.

class InputSanitizer:
    """Detects prompt injection and sanitizes untrusted input"""
    
    # Patterns that indicate prompt injection attempts
    INJECTION_PATTERNS = [
        r"ignore\s+(all\s+)?previous\s+instructions",
        r"system\s*:\s*you\s+are",
        r"<\|im_start\|>",
        r"<\|im_end\|>",
        r"forget\s+everything",
        r"new\s+instructions",
        r"disregard\s+(all\s+)?above",
        r"override\s+previous",
    ]
    
    # Maximum allowed input size (tokens)
    MAX_INPUT_TOKENS = 100_000
    
    def __init__(self, event_logger=None):
        self.event_logger = event_logger
        self.injection_regex = re.compile(
            "|".join(self.INJECTION_PATTERNS),
            re.IGNORECASE
        )
    
    def log_event(self, event):
        if self.event_logger:
            self.event_logger.log(event)
        else:
            print(f"[LOG] {event}")

    def sanitize_transcript(
        self,
        transcript: str,
        source_metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Sanitize meeting transcript and detect injection attempts
        
        Returns:
            {
                "sanitized": str,  # Cleaned transcript
                "quarantined": bool,  # True if suspicious
                "injection_patterns": List[str],  # Detected patterns
                "metadata": Dict  # Source info
            }
        """
        
        # Check size
        if len(transcript) > self.MAX_INPUT_TOKENS * 4:  # ~4 chars/token
            self.log_event({
                "type": "security.input.oversized",
                "payload": {
                    "length": len(transcript),
                    "max_allowed": self.MAX_INPUT_TOKENS * 4,
                    **source_metadata
                },
                "severity": "high"
            })
            # Truncate
            transcript = transcript[:self.MAX_INPUT_TOKENS * 4]
        
        # Detect injection patterns
        matches = self.injection_regex.findall(transcript.lower())
        
        if matches:
            self.log_event({
                "type": "security.input.injection_detected",
                "payload": {
                    "patterns": matches,
                    "transcript_preview": transcript[:200],
                    **source_metadata
                },
                "severity": "critical"
            })
            
            return {
                "sanitized": self._redact_injection_patterns(transcript),
                "quarantined": True,
                "injection_patterns": matches,
                "metadata": source_metadata
            }
        
        # Basic sanitization
        sanitized = self._basic_sanitize(transcript)
        
        return {
            "sanitized": sanitized,
            "quarantined": False,
            "injection_patterns": [],
            "metadata": source_metadata
        }
    
    def _basic_sanitize(self, text: str) -> str:
        """Remove potentially dangerous characters/sequences"""
        # Remove null bytes
        text = text.replace('\x00', '')
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove control characters (except newlines)
        text = re.sub(r'[\x01-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
        
        return text.strip()
    
    def _redact_injection_patterns(self, text: str) -> str:
        """Replace injection patterns with [REDACTED]"""
        return self.injection_regex.sub('[REDACTED]', text)
