# Security Protocols & Data Protection

## 1. Secrets Management
**Critical Rule**: Never commit secrets (API Keys, Token Files) to version control.

### Protocol
*   **Local Development**: Use `.env` file (listed in `.gitignore`).
*   **Production**: Use Environment Variables injected by the cloud provider (Render, Railway, AWS).
*   **Verification**: Run `grep -r "API_KEY" .` before pushing to ensure no hardcoded secrets exist.

## 2. Dependency Management
Minimizing vulnerability surface area.

### Protocol
*   **Locking**: Use `requirements.txt` with specific versions (e.g., `requests==2.31.0` not `requests>=2.0`).
*   **Auditing**: Run `pip list` or `safety check` quarterly.
*   **Virtual Environments**: Python `venv` must be excluded from git.

## 3. Data Privacy (PII)
Handling names, emails, and phone numbers.

### Protocol
*   **Logging**: Do not log full phone numbers or emails in `event_log.py`. Use UUIDs or masked strings (e.g., `+1***555`).
    *   *Correction Needed*: Current logs show full targets. Update `logging` config to mask PII.
*   **Retention**: Meeting transcripts should be retained only as long as necessary.
*   **WhatsApp**: Adhere to Meta's 24h conversation window policy. Messages must be user-initiated or use approved templates.

## 4. Access Control
*   **Google Calendar**: Limit scopes to `calendar.readonly` unless write access is explicitly authorized.
*   **Database**: Use Row Level Security (RLS) on Supabase if multi-tenancy is introduced.
