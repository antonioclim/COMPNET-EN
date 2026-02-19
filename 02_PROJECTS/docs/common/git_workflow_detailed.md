# 🔀 Git Workflow Guide
## Computer Networks Projects — ASE Bucharest, CSIE

> **Purpose:** Version control best practices for team projects.  
> **Applies to:** All projects P01-P20

---

## Repository Setup

### Initial Setup (Team Leader)

```bash
# Create repository on GitHub, then:
git clone https://github.com/[username]/retele-proiect-XX.git
cd retele-proiect-XX

# Create initial structure
mkdir -p docs src docker tests artifacts
touch README.md .gitignore CHANGELOG.md

# Initial commit
git add .
git commit -m "Initial project structure"
git push origin main
```

### Join Repository (Team Members)

```bash
# Clone the repository
git clone https://github.com/[username]/retele-proiect-XX.git
cd retele-proiect-XX

# Verify setup
git remote -v
git branch -a
```

---

## Branching Strategy

### Branch Types

| Branch | Purpose | Naming |
|--------|---------|--------|
| `main` | Production-ready code | Protected |
| `develop` | Integration branch | `develop` |
| `feature/*` | New functionality | `feature/add-firewall-rules` |
| `fix/*` | Bug fixes | `fix/socket-timeout` |
| `docs/*` | Documentation | `docs/update-readme` |

### Branch Flow

```
main ─────────────────────────────────────────► (releases only)
       │                               ▲
       └──► develop ─────────────────────────► (integration)
                 │           ▲       ▲
                 ├──► feature/X ─────┘       │
                 └──► feature/Y ─────────────┘
```

### Creating a Feature Branch

```bash
# Make sure you're on develop and up to date
git checkout develop
git pull origin develop

# Create and switch to new branch
git checkout -b feature/add-packet-capture

# Work on your feature...
# Then push to remote
git push -u origin feature/add-packet-capture
```

---

## Commit Message Conventions

### Format

```
<type>: <short description>

[optional body]

[optional footer]
```

### Types

| Type | When to use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code change that doesn't fix or add |
| `test` | Adding tests |
| `chore` | Build, config, dependencies |

### Examples

```bash
# Good commits
git commit -m "feat: add TCP packet filtering"
git commit -m "fix: resolve socket timeout on slow networks"
git commit -m "docs: update installation instructions"
git commit -m "test: add unit tests for packet parser"

# Bad commits (avoid these)
git commit -m "update"
git commit -m "fix stuff"
git commit -m "WIP"
git commit -m "asdfasdf"
```

### Multi-line Commit

```bash
git commit -m "feat: implement SDN controller

- Add flow rule installation
- Add packet-in handler
- Add topology discovery

Closes #12"
```

---

## Stage-Specific Workflow

### Stage E1 (Design)

```bash
# Create design branch
git checkout -b docs/e1-design

# Add specification files
git add docs/specificatii.md docs/diagrame/
git commit -m "docs: add E1 specifications and diagrams"

# Merge to develop
git checkout develop
git merge docs/e1-design
git push origin develop

# Tag the release
git tag -a e1-design -m "Stage E1 complete"
git push origin --tags
```

### Stage E2 (Prototype)

```bash
# Work on features in parallel
git checkout -b feature/basic-server   # Member 1
git checkout -b feature/client-module  # Member 2

# After completing features, merge to develop
git checkout develop
git pull origin develop
git merge feature/basic-server
git merge feature/client-module
git push origin develop

# Tag
git tag -a e2-prototype -m "Stage E2 complete"
git push origin --tags
```

### Stage E3 (Final)

```bash
# Final integration and testing
git checkout develop
git pull origin develop

# Run all tests
python -m pytest tests/

# Merge to main
git checkout main
git merge develop
git push origin main

# Final tag
git tag -a v1.0-final -m "Final version"
git push origin --tags
```

---

## Merge Conflicts

### When Conflicts Happen

Conflicts occur when two people edit the same lines. Git marks them like this:

```python
<<<<<<< HEAD
def process_packet(data):
    return parse_tcp(data)
=======
def process_packet(data):
    return parse_udp(data)
>>>>>>> feature/udp-support
```

### Resolving Conflicts

1. **Understand both changes** — What was each person trying to do?
2. **Decide the correct version** — Sometimes it's one, sometimes a combination
3. **Edit the file** — Remove markers, keep correct code
4. **Test** — Make sure it works
5. **Commit** — Mark conflict as resolved

```bash
# After manually fixing the file:
git add src/packet_handler.py
git commit -m "fix: merge conflict in packet handler"
```

### Prevention Tips

- Pull frequently (`git pull` before starting work)
- Communicate about who's working on what
- Keep changes small and focused
- Use feature branches

---

## Pull Request Template

When merging to develop, create a pull request with:

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation
- [ ] Refactoring

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Tests pass locally
- [ ] Documentation updated

## Testing
How did you test this change?

## Screenshots (if applicable)
```

---

## Code Review Checklist

When reviewing a teammate's code:

```
□ Code compiles/runs without errors
□ Logic is correct and handles edge cases
□ Code follows project style guide
□ Variable names are meaningful
□ No hardcoded values (use constants)
□ Error handling is appropriate
□ Comments explain "why", not "what"
□ No debug print statements left
□ Tests are included (if applicable)
```

---

## Common Git Commands

### Daily Workflow

```bash
# Start of day
git checkout develop
git pull origin develop

# Check status
git status
git log --oneline -5

# Stage and commit
git add .
git commit -m "feat: description"

# Push
git push origin [branch-name]
```

### Useful Commands

```bash
# See what changed
git diff
git diff --staged

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard local changes to a file
git checkout -- filename.py

# Stash work temporarily
git stash
git stash pop

# See commit history
git log --oneline --graph --all

# Find who wrote a line
git blame filename.py
```

### Emergency Commands

```bash
# Undo a pushed commit (creates new commit)
git revert HEAD
git push origin main

# Reset to remote state (DESTRUCTIVE)
git fetch origin
git reset --hard origin/main

# Recover deleted branch
git reflog
git checkout -b recovered-branch [commit-hash]
```

---

## .gitignore Template

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
.env
venv/
.venv/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Docker
docker-compose.override.yml

# Project specific
artifacts/*.pcap
artifacts/*.log
*.tmp

# OS
.DS_Store
Thumbs.db

# Secrets (NEVER commit these)
*.pem
*.key
secrets.json
.env.local
```

---

## Troubleshooting Git

### "Permission denied" when pushing

```bash
# Check remote URL
git remote -v

# If using HTTPS, try SSH
git remote set-url origin git@github.com:[user]/[repo].git

# Or use personal access token with HTTPS
```

### "Divergent branches" error

```bash
# Pull with rebase
git pull --rebase origin develop

# Or merge
git pull --no-rebase origin develop
```

### Accidentally committed to main

```bash
# Move commit to new branch
git branch feature/accidental-commit
git reset --hard HEAD~1
git checkout feature/accidental-commit
```

### Need to change last commit message

```bash
# Only if not pushed yet
git commit --amend -m "New message"

# If already pushed (careful!)
git commit --amend -m "New message"
git push --force origin [branch]
```

---

## GitHub Repository Settings

Recommended settings for project repositories:

| Setting | Value | Why |
|---------|-------|-----|
| Default branch | `main` | Industry standard |
| Branch protection on `main` | Enabled | Prevent accidental pushes |
| Require pull requests | Optional | Good for teams of 3 |
| Issues | Enabled | Track bugs and tasks |
| Wiki | Disabled | Use docs/ folder instead |

---

*Git Workflow Guide v1.0 — Computer Networks, ASE Bucharest*
