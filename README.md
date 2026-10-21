# oracle-ai-lab

A learning project: Oracle 26ai + Python + Gemma 4 + MCP.

The goal is a local "ask your database" assistant. Gemma 4 runs on my own
machine, data and vectors live in Oracle 26ai, and an MCP server lets an
AI agent query the database safely.

## Tools
- Oracle 26ai (Docker)
- SQL Developer
- PyCharm Community
- Python (python-oracledb)
- Ollama + Gemma 4 (coming in Phase 1)

## Setup
1. Copy `.env.example` to `.env` and fill in your own values.
2. Create a virtual environment: `python3 -m venv .venv`
3. Activate it: `source .venv/bin/activate`
4. Install packages: `pip install -r requirements.txt`
5. Run: `python phase0/01_connect.py`

## Progress
- [x] Phase 0: Connect Python to Oracle
- [x] Phase 1: Talk to Gemma 4 through Ollama
- [x] Phase 2: Vector search and RAG
- [ ] Phase 3: REST API with FastAPI
- [ ] Phase 4: Oracle MCP server
- [ ] Phase 5: Agent capstone