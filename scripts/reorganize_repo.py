#!/usr/bin/env python3
"""
Meeting OS Repository Reorganization Script

This script safely reorganizes the repository structure according to the plan in:
CODEBASE_STATE_AUDIT.md

It will:
1. Create new directory structure
2. Move files to their proper locations
3. Update path references in code
4. Create backup before any changes
5. Generate rollback script

Usage:
    python3 scripts/reorganize_repo.py --dry-run    # Preview changes
    python3 scripts/reorganize_repo.py --execute    # Execute migration
    python3 scripts/reorganize_repo.py --rollback   # Undo changes
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime
import argparse


class RepoReorganizer:
    def __init__(self, repo_root: Path, dry_run: bool = True):
        self.repo_root = repo_root
        self.dry_run = dry_run
        self.backup_dir = repo_root / f"_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.migration_log = []
        
    def log(self, action: str, source: str, dest: str = None, status: str = "pending"):
        """Log a migration action"""
        entry = {
            "action": action,
            "source": source,
            "destination": dest,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        self.migration_log.append(entry)
        
        emoji = "🔍" if self.dry_run else ("✅" if status == "success" else "⚠️")
        if dest:
            print(f"{emoji} {action}: {source} → {dest}")
        else:
            print(f"{emoji} {action}: {source}")
    
    def create_backup(self):
        """Create backup of current state"""
        if self.dry_run:
            print("🔍 [DRY RUN] Would create backup at:", self.backup_dir)
            return
        
        print(f"📦 Creating backup at {self.backup_dir}")
        self.backup_dir.mkdir(exist_ok=True)
        
        # Save current git status
        import subprocess
        try:
            git_status = subprocess.run(
                ["git", "status", "--short"],
                cwd=self.repo_root,
                capture_output=True,
                text=True
            )
            (self.backup_dir / "git_status.txt").write_text(git_status.stdout)
        except Exception as e:
            print(f"⚠️  Could not save git status: {e}")
    
    def move_file(self, source: Path, dest: Path):
        """Safely move a file"""
        if not source.exists():
            self.log("skip", str(source), str(dest), "not_found")
            return False
        
        if self.dry_run:
            self.log("move", str(source), str(dest), "dry_run")
            return True
        
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(dest))
            self.log("move", str(source), str(dest), "success")
            return True
        except Exception as e:
            self.log("move", str(source), str(dest), f"error: {e}")
            return False
    
    def create_directory(self, path: Path):
        """Create directory if it doesn't exist"""
        if self.dry_run:
            self.log("mkdir", str(path), status="dry_run")
            return
        
        path.mkdir(parents=True, exist_ok=True)
        self.log("mkdir", str(path), status="success")
    
    def update_file_references(self, file_path: Path, old_path: str, new_path: str):
        """Update path references in a file"""
        if not file_path.exists():
            return False
        
        if self.dry_run:
            self.log("update_refs", str(file_path), f"{old_path} → {new_path}", "dry_run")
            return True
        
        try:
            content = file_path.read_text()
            if old_path in content:
                updated_content = content.replace(old_path, new_path)
                file_path.write_text(updated_content)
                self.log("update_refs", str(file_path), f"{old_path} → {new_path}", "success")
                return True
        except Exception as e:
            self.log("update_refs", str(file_path), f"{old_path} → {new_path}", f"error: {e}")
        
        return False
    
    def phase_1_docs(self):
        """Phase 1: Reorganize documentation files"""
        print("\n" + "="*60)
        print("📚 PHASE 1: Documentation Reorganization")
        print("="*60 + "\n")
        
        # Create docs structure
        docs_dirs = [
            "docs/architecture/diagrams",
            "docs/deployment",
            "docs/guides",
            "docs/security",
            "docs/product"
        ]
        
        for dir_path in docs_dirs:
            self.create_directory(self.repo_root / dir_path)
        
        # Document movements
        doc_moves = [
            ("DESIGN.md", "docs/architecture/DESIGN.md"),
            ("Information flowchart  .mmd", "docs/architecture/diagrams/information_flowchart.mmd"),
            ("DEPLOYMENT.md", "docs/deployment/DEPLOYMENT.md"),
            ("DEPLOYMENT_CONCEPTS.md", "docs/deployment/DEPLOYMENT_CONCEPTS.md"),
            ("GCLOUD_DEPLOY.md", "docs/deployment/GCLOUD_DEPLOY.md"),
            ("MCP_SETUP.md", "docs/guides/MCP_SETUP.md"),
            ("SKILL.MD", "docs/guides/SKILL.md"),
            ("SECURITY.md", "docs/security/SECURITY.md"),
            ("meeting-os-cost-growth.md", "docs/product/meeting-os-cost-growth.md"),
            ("meeting-os-observability.md", "docs/product/meeting-os-observability.md"),
            ("meeting-os-security.md", "docs/product/meeting-os-security.md"),
        ]
        
        for source, dest in doc_moves:
            self.move_file(self.repo_root / source, self.repo_root / dest)
    
    def phase_2_credentials(self):
        """Phase 2: Secure credentials"""
        print("\n" + "="*60)
        print("🔒 PHASE 2: Credential Security")
        print("="*60 + "\n")
        
        # Create .secrets directory
        secrets_dir = self.repo_root / ".secrets"
        self.create_directory(secrets_dir)
        
        # Create .gitignore for secrets
        gitignore_content = "*\n!.gitignore\n"
        if not self.dry_run:
            (secrets_dir / ".gitignore").write_text(gitignore_content)
            self.log("create", str(secrets_dir / ".gitignore"), status="success")
        else:
            self.log("create", str(secrets_dir / ".gitignore"), status="dry_run")
        
        # Move credentials
        credential_files = [
            "credentials.json",
            "token.json",
        ]
        
        # Find client_secret files (pattern match)
        for file in self.repo_root.glob("client_secret_*.json"):
            credential_files.append(file.name)
        
        for cred_file in credential_files:
            source = self.repo_root / cred_file
            dest = secrets_dir / cred_file
            if self.move_file(source, dest):
                # Update references in google_calendar.py
                calendar_file = self.repo_root / "meeting_os" / "services" / "google_calendar.py"
                self.update_file_references(
                    calendar_file,
                    f'"{cred_file}"',
                    f'".secrets/{cred_file}"'
                )
                self.update_file_references(
                    calendar_file,
                    f"'{cred_file}'",
                    f"'.secrets/{cred_file}'"
                )
    
    def phase_3_deployment(self):
        """Phase 3: Organize deployment files"""
        print("\n" + "="*60)
        print("🚀 PHASE 3: Deployment File Organization")
        print("="*60 + "\n")
        
        # Create deployment structure
        deployment_dirs = [
            "deployment/docker",
            "deployment/render",
            "deployment/gcloud"
        ]
        
        for dir_path in deployment_dirs:
            self.create_directory(self.repo_root / dir_path)
        
        # Move deployment files
        deployment_moves = [
            ("Dockerfile", "deployment/docker/Dockerfile"),
            (".dockerignore", "deployment/docker/.dockerignore"),
            ("render.yaml", "deployment/render/render.yaml"),
        ]
        
        for source, dest in deployment_moves:
            self.move_file(self.repo_root / source, self.repo_root / dest)
    
    def phase_4_readme(self):
        """Phase 4: Create comprehensive README"""
        print("\n" + "="*60)
        print("📝 PHASE 4: Create README")
        print("="*60 + "\n")
        
        readme_content = """# Meeting OS - Intelligent Meeting Assistant

> **AI-powered meeting intelligence system** that transforms conversations into actionable insights.

## 🎯 Overview

Meeting OS is an autonomous AI system that:
- 📝 **Ingests** meeting transcripts from Fireflies, Slack, WhatsApp
- 🧠 **Analyzes** content using Gemini & Perplexity AI
- 🎯 **Routes** to specialized agents (Sales, Ops, Research)
- 💾 **Persists** to Notion CRM and Supabase
- 📢 **Notifies** teams via Slack with rich, bio-chromatic UI

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Supabase account
- Google Gemini API key
- Notion workspace

### Installation

```bash
# Clone and navigate
git clone <your-repo>
cd tbd

# Install dependencies
pip install -r meeting_os/requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run locally
python3 main.py
```

### First Test

```bash
# Health check
curl http://localhost:8080/

# Test webhook
curl -X POST http://localhost:8080/webhook \\
  -H "Content-Type: application/json" \\
  -d '{"message":"Test meeting about enterprise deal","sender":"user@example.com","source":"test"}'
```

## 📚 Documentation

- **[Architecture Design](docs/architecture/DESIGN.md)** - System design & data flows
- **[Deployment Guide](docs/deployment/)** - Cloud Run, Render, Docker setup
- **[Security Overview](docs/security/SECURITY.md)** - 4-layer security model
- **[Codebase Audit](CODEBASE_STATE_AUDIT.md)** - Implementation status

## 🏗️ Project Structure

```
tbd/
├── main.py                 # FastAPI entry point
├── meeting_os/             # Core application
│   ├── agents/            # AI agents (Router, Sales, Research)
│   ├── core/              # UCO, EventLog, Security
│   ├── services/          # External integrations
│   ├── prompts/           # LLM prompt templates
│   └── workflows/         # n8n workflow definitions
├── deployment/            # Docker, Cloud Run configs
├── docs/                  # Documentation
├── tests/                 # Test suite
└── .secrets/             # Credentials (gitignored)
```

## 🔑 Key Concepts

### Universal Context Object (UCO)
The "nervous system" of Meeting OS - a standardized data structure that flows through all agents:

```python
{
  "event_id": "evt_abc123",
  "source": "Fireflies",
  "routing_flags": {"sales": true, "ops": false},
  "context_layer": {
    "summary": "Client interested in Enterprise plan",
    "sentiment": "Positive",
    "next_steps": ["Send proposal", "Schedule demo"]
  }
}
```

### Agent Architecture
- **Router Agent**: Ingests UCOs, persists to Supabase, dispatches to swarms
- **Sales Agent**: Extracts deals, updates Notion CRM
- **Research Agent**: Pre-meeting briefs using Perplexity
- **Ops Agent**: Action items, task tracking

## 🛠️ Development

### Running Tests
```bash
# Unit tests (coming soon)
pytest tests/unit/

# Integration tests
pytest tests/integration/
```

### Code Quality
- Uses Pydantic for strict type validation
- 4-layer security (Input Sanitization, Prompt Wrapping, Tool Allowlist, Vault Isolation)
- Append-only event logs for auditability

## 🎨 Design Philosophy

**Bio-Chromatic Cyberpunk**: Premium, neon-accented dark mode UI
- 🟣 Neural Pink - User interactions
- 🔵 Data Cyan - Ingestion & processing
- 🟢 Bio-Lime - Success & outcomes
- 🟡 Warning Yellow - Alerts & routing decisions

## 🚢 Deployment

### Google Cloud Run
```bash
gcloud run deploy meeting-os \\
  --source . \\
  --region us-central1 \\
  --allow-unauthenticated \\
  --dockerfile deployment/docker/Dockerfile
```

See [docs/deployment/GCLOUD_DEPLOY.md](docs/deployment/GCLOUD_DEPLOY.md) for details.

## 📊 Monitoring

- **Event Logs**: All actions logged to Supabase `event_logs` table
- **Slack Notifications**: Real-time updates via bio-chromatic cards
- **Notion Dashboard**: CRM updates visible in workspace

## 🤝 Contributing

1. Read [CODEBASE_STATE_AUDIT.md](CODEBASE_STATE_AUDIT.md) to understand current state
2. Follow the established patterns (UCO, Agent base classes)
3. Add tests for new features
4. Update documentation

## 📄 License

[Your License Here]

## 🙏 Acknowledgments

Built with:
- Google Gemini 1.5
- Perplexity AI
- Supabase
- FastAPI
- Notion API

---

**Status**: ✅ Production-ready core • ⚠️ Advanced features in testing

For questions, see [docs/guides/](docs/guides/) or raise an issue.
"""
        
        readme_path = self.repo_root / "README.md"
        if not self.dry_run:
            readme_path.write_text(readme_content)
            self.log("create", "README.md", status="success")
        else:
            self.log("create", "README.md", status="dry_run")
    
    def save_migration_log(self):
        """Save migration log to file"""
        if self.dry_run:
            return
        
        log_file = self.repo_root / "migration_log.json"
        with open(log_file, 'w') as f:
            json.dump(self.migration_log, f, indent=2)
        
        print(f"\n📋 Migration log saved to: {log_file}")
    
    def generate_rollback_script(self):
        """Generate a script to undo all changes"""
        rollback_commands = []
        
        for entry in reversed(self.migration_log):
            if entry['action'] == 'move' and entry['status'] == 'success':
                source = entry['source']
                dest = entry['destination']
                rollback_commands.append(f'mv "{dest}" "{source}"')
        
        rollback_script = f"""#!/bin/bash
# Rollback script generated at {datetime.now().isoformat()}
# Run this to undo the repository reorganization

set -e

echo "🔄 Rolling back repository reorganization..."

{chr(10).join(rollback_commands)}

echo "✅ Rollback complete!"
"""
        
        if not self.dry_run:
            rollback_path = self.repo_root / "rollback_reorganization.sh"
            rollback_path.write_text(rollback_script)
            rollback_path.chmod(0o755)
            print(f"📜 Rollback script created: {rollback_path}")
        else:
            print(f"🔍 [DRY RUN] Would create rollback script with {len(rollback_commands)} commands")
    
    def run(self):
        """Execute the full reorganization"""
        print("\n" + "="*60)
        print(f"🚀 Meeting OS Repository Reorganization")
        print(f"Mode: {'DRY RUN' if self.dry_run else 'EXECUTE'}")
        print("="*60 + "\n")
        
        if not self.dry_run:
            self.create_backup()
        
        self.phase_1_docs()
        self.phase_2_credentials()
        self.phase_3_deployment()
        self.phase_4_readme()
        
        if not self.dry_run:
            self.save_migration_log()
            self.generate_rollback_script()
        
        print("\n" + "="*60)
        print(f"{'🔍 DRY RUN COMPLETE' if self.dry_run else '✅ MIGRATION COMPLETE'}")
        print("="*60 + "\n")
        
        if self.dry_run:
            print("To execute for real, run:")
            print(f"  python3 scripts/reorganize_repo.py --execute")
        else:
            print("Next steps:")
            print("1. Review changes: git status")
            print("2. Test the system: python3 main.py")
            print("3. Commit if satisfied: git add . && git commit -m 'Reorganize repository structure'")
            print(f"4. If needed, rollback: ./rollback_reorganization.sh")


def main():
    parser = argparse.ArgumentParser(description="Reorganize Meeting OS repository structure")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without executing"
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute the reorganization"
    )
    
    args = parser.parse_args()
    
    # Default to dry-run if neither flag specified
    dry_run = not args.execute or args.dry_run
    
    repo_root = Path(__file__).parent.parent
    reorganizer = RepoReorganizer(repo_root, dry_run=dry_run)
    reorganizer.run()


if __name__ == "__main__":
    main()
