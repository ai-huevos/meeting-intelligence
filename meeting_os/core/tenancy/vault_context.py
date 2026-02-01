import threading
from typing import Optional

class TenantContext:
    """Thread-local storage for tenant context"""
    
    _context = threading.local()
    
    @classmethod
    def set_vault(cls, vault_id: str, user_id: str):
        """Set current vault context (call at request start)"""
        cls._context.vault_id = vault_id
        cls._context.user_id = user_id
    
    @classmethod
    def get_vault(cls) -> str:
        """Get current vault ID"""
        vault_id = getattr(cls._context, 'vault_id', None)
        if not vault_id:
            # Raise exception? Or return default?
            # Spec says raise RuntimeError.
            # But during local testing or non-request context, maybe default?
            # For strict security, raise.
            raise RuntimeError("Tenant context not set. Call TenantContext.set_vault() first.")
        return vault_id
    
    @classmethod
    def get_user(cls) -> str:
        """Get current user ID"""
        user_id = getattr(cls._context, 'user_id', None)
        if not user_id:
            raise RuntimeError("User context not set.")
        return user_id
    
    @classmethod
    def clear(cls):
        """Clear context (call at request end)"""
        cls._context.vault_id = None
        cls._context.user_id = None
