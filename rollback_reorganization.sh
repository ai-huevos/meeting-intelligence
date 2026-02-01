#!/bin/bash
# Rollback script generated at 2026-02-01T09:02:51.266072
# Run this to undo the repository reorganization

set -e

echo "🔄 Rolling back repository reorganization..."

mv "/Users/tatooine/Documents/Development/tbd/deployment/render/render.yaml" "/Users/tatooine/Documents/Development/tbd/render.yaml"
mv "/Users/tatooine/Documents/Development/tbd/deployment/docker/.dockerignore" "/Users/tatooine/Documents/Development/tbd/.dockerignore"
mv "/Users/tatooine/Documents/Development/tbd/deployment/docker/Dockerfile" "/Users/tatooine/Documents/Development/tbd/Dockerfile"
mv "/Users/tatooine/Documents/Development/tbd/.secrets/client_secret_161599347588-be1moeq82k4750lko3vgp76r62pltvuh.apps.googleusercontent.com.json" "/Users/tatooine/Documents/Development/tbd/client_secret_161599347588-be1moeq82k4750lko3vgp76r62pltvuh.apps.googleusercontent.com.json"
mv "/Users/tatooine/Documents/Development/tbd/.secrets/token.json" "/Users/tatooine/Documents/Development/tbd/token.json"
mv "/Users/tatooine/Documents/Development/tbd/.secrets/credentials.json" "/Users/tatooine/Documents/Development/tbd/credentials.json"
mv "/Users/tatooine/Documents/Development/tbd/docs/product/meeting-os-security.md" "/Users/tatooine/Documents/Development/tbd/meeting-os-security.md"
mv "/Users/tatooine/Documents/Development/tbd/docs/product/meeting-os-observability.md" "/Users/tatooine/Documents/Development/tbd/meeting-os-observability.md"
mv "/Users/tatooine/Documents/Development/tbd/docs/product/meeting-os-cost-growth.md" "/Users/tatooine/Documents/Development/tbd/meeting-os-cost-growth.md"
mv "/Users/tatooine/Documents/Development/tbd/docs/security/SECURITY.md" "/Users/tatooine/Documents/Development/tbd/SECURITY.md"
mv "/Users/tatooine/Documents/Development/tbd/docs/guides/SKILL.md" "/Users/tatooine/Documents/Development/tbd/SKILL.MD"
mv "/Users/tatooine/Documents/Development/tbd/docs/guides/MCP_SETUP.md" "/Users/tatooine/Documents/Development/tbd/MCP_SETUP.md"
mv "/Users/tatooine/Documents/Development/tbd/docs/deployment/GCLOUD_DEPLOY.md" "/Users/tatooine/Documents/Development/tbd/GCLOUD_DEPLOY.md"
mv "/Users/tatooine/Documents/Development/tbd/docs/deployment/DEPLOYMENT_CONCEPTS.md" "/Users/tatooine/Documents/Development/tbd/DEPLOYMENT_CONCEPTS.md"
mv "/Users/tatooine/Documents/Development/tbd/docs/deployment/DEPLOYMENT.md" "/Users/tatooine/Documents/Development/tbd/DEPLOYMENT.md"
mv "/Users/tatooine/Documents/Development/tbd/docs/architecture/diagrams/information_flowchart.mmd" "/Users/tatooine/Documents/Development/tbd/Information flowchart  .mmd"
mv "/Users/tatooine/Documents/Development/tbd/docs/architecture/DESIGN.md" "/Users/tatooine/Documents/Development/tbd/DESIGN.md"

echo "✅ Rollback complete!"
