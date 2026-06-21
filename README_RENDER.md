# Render deployment notes

This repository is prepared for deployment on Render.

Recommended Render settings:
- Branch: main
- Build command: pip install -r requirements.txt
- Start command: gunicorn app.main:app
- Python runtime: 3.10 or 3.11
- Recommended environment variable (to limit workers on low-memory plans):
  GUNICORN_CMD_ARGS="--workers=1 --threads=2 --timeout=60"
- Health check: HTTP: /health

After deploying, check the service logs for dependency installation issues or outbound network errors (WHOIS/DNS requests may fail or be rate-limited).
