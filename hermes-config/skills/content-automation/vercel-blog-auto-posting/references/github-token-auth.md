# GitHub Personal Access Token — Quick Auth Guide

Use this when the agent needs to push code to a user's GitHub repo.

## Token creation (user-side, 30 seconds)

1. Go to [github.com/settings/tokens](https://github.com/settings/tokens) (must be logged in)
2. **Generate new token** → **Generate new token (classic)**
3. Fill in:
   - Note: `hermes-agent` (any name)
   - Expiration: `90 days` or `No expiration`
   - Scopes: ✅ check `repo` (top-level checkbox — auto-selects sub-items)
4. Click **Generate token** → **Copy immediately** (shown only once!)

## Agent-side usage

```bash
# 1. Verify token works + get username
curl -s -H "Authorization: token THE_TOKEN" "https://api.github.com/user"

# 2. Create repo if needed
curl -s -H "Authorization: token THE_TOKEN" \
  -H "Content-Type: application/json" \
  -X POST "https://api.github.com/user/repos" \
  -d '{"name":"repo-name","description":"...","private":false}'

# 3. Setup git remote with token embedded
git remote add origin "https://USERNAME:TOKEN@github.com/USERNAME/repo.git"

# 4. Push
git add -A
git commit -m "message"
git branch -M main
git push -u origin main
```

## Windows git-bash quirks

- Use URL-embedded auth (not credential manager) — most reliable on MSYS/git-bash
- `git config user.name` / `user.email` must be set before first commit
- LF→CRLF warnings are harmless noise; commit proceeds normally

## Security note

After the session, recommend the user revoke the token at [github.com/settings/tokens](https://github.com/settings/tokens) — agent tokens should be short-lived and scoped only to `repo`.
