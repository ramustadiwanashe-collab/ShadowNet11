# ShadowNet 9.0

A free technology learning platform starter built with Flask.

## Included in this release
- Account registration and login with password hashing
- Student dashboard and profile
- Course catalogue and lesson progress
- Safe simulated Linux terminal (does not execute OS commands)
- IPv4 subnet calculator
- Introductory cybersecurity lessons and knowledge challenges
- PostgreSQL support through `DATABASE_URL`
- Render Blueprint deployment configuration

## Deploy to Render
1. Extract this ZIP.
2. Upload the **contents** of the `shadownet-9` folder to the root of a GitHub repository. `app.py`, `requirements.txt` and `render.yaml` must be at repository root.
3. Create a PostgreSQL database with a provider that supports your chosen plan.
4. Copy its internal connection URL.
5. In Render, create a Blueprint from your GitHub repository.
6. When prompted, set `DATABASE_URL` to the PostgreSQL connection URL. Keep the generated `SECRET_KEY`.
7. Deploy and open the service URL shown by Render.

The Render Blueprint deliberately leaves `DATABASE_URL` as a manual secret. A SQLite database on a free web service may be lost when the instance restarts or redeploys.

## Local run
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```
Open http://127.0.0.1:5000.

## Important scope
This is a deployable foundation, not a finished full cyber range:
- ShadowTerminal is a safe command simulator. It does not execute real Linux commands.
- Networking currently includes an IPv4 subnet calculator, not a full topology simulator.
- Cybersecurity includes introductory learning challenges, not real penetration-testing targets.
- ShadowAI is not connected to an AI provider.
- Add isolated lab workers, network emulation, advanced course content, monitoring, backups and security testing before offering real execution environments to the public.

## Security
Never execute user-supplied shell commands inside the Flask web process. Real terminal and vulnerable-lab environments must run in separately isolated containers or virtual machines with strict resource and network controls.
