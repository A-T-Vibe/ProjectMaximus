# ProjectMaximus

## Project Overview
This project uses Claude Code to manage and improve a WordPress website hosted on a remote Linux server. Claude connects to the server via SSH and uses WP-CLI to make changes to WordPress.

## Connection Method
- **Protocol:** SSH (key-based auth, no password prompt)
- **Tool:** WP-CLI (`wp` command) on the remote server
- **Server details:** TBD — update this section once SSH connection is configured

## Common Commands
```bash
# Test SSH connection
ssh user@your-server.com "wp --info"

# List plugins
ssh user@your-server.com "wp plugin list"

# List themes
ssh user@your-server.com "wp theme list"

# Check WordPress version
ssh user@your-server.com "wp core version"
```

## Project Goals
- Improve and maintain a WordPress website via Claude Code
- Use SSH + WP-CLI for server-side changes
- Keep all changes version-controlled and recoverable via GitHub

## Repository
- **GitHub:** https://github.com/A-T-Vibe/ProjectMaximus
- **Backup strategy:** Changes are committed and pushed to GitHub after each session

## Change Log
| Date | Change |
|------|--------|
| 2026-04-21 | Project initialised, CLAUDE.md created, GitHub repo set up |
