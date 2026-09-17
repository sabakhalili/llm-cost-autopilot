# LLM Cost Autopilot

A demo LLM request router: it classifies a prompt's complexity, routes it to the cheapest model that can handle it, and tracks how much that saved versus always calling the flagship model.

Built as a portfolio project to demonstrate the difference between **routing mechanics** (well-understood, widely built) and **routing-correctness validation** (the part most tools skip — see Future Work below).

## How it works

1. **Query in** — a prompt hits `POST /api/chat`.
2. **Classify complexity** — a single cheap/fast LLM call (Claude Haiku) rates the prompt `simple` / `medium` / `hard`. Chosen over a trained classifier for build speed — no labeled data needed.
3. **Route to model** — the tier maps to a model via `backend/app/router/model_config.py`, plus hand-written override rules in `backend/app/router/rules.py` (v1 ships one: any prompt containing code is floored at `medium`, regardless of what the classifier said). Overrides only ever raise the tier, never lower it.
4. **Call model** — a provider-agnostic interface (`backend/app/router/providers/`) sends the request to OpenAI or Anthropic and captures tokens in/out, latency, and cost.
5. **Return response + metadata** — the reply plus routing metadata (model used, tier, cost vs. baseline, one-line reason) goes back to the UI.
6. **Log** — the full trace is written to SQLite, powering the savings ticker and an audit trail.

The routing engine (`backend/app/router/`) has no FastAPI or database imports — it's a standalone async Python package, callable from any future client, not just this chat UI.

## Running it

No API keys needed to try it — `MOCK_MODE=true` by default simulates realistic-ish latency, token counts, and replies behind the same interface real providers use.

Requires **Python 3.10+** (the codebase uses `X | None` union syntax). Check `python3 --version` first — on macOS the system Python is often 3.9, in which case install a newer one via `brew install python@3.12` and use `python3.12` below instead of `python3`.

```bash
# Backend
cd backend
python3 -m venv .venv && source .venv/bin/activate   # use python3.12 if system python3 is < 3.10
pip install -r requirements.txt
cp .env.example .env          # MOCK_MODE=true by default

# Frontend
cd ../frontend
npm install

# From project root, run both together
cd ..
npm install
npm run dev                   # backend on :8000, frontend on :3000
```

Open http://localhost:3000 and type a prompt — every message goes through the same classify → route → call → log path, live.

**Going live:** fill in `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` in `backend/.env`, set `MOCK_MODE=false`, restart the backend. Double-check the model IDs and pricing in `backend/app/router/model_config.py` and `backend/app/router/pricing.py` first — these drift over time.

## A known simplification

"Cost vs. baseline" is computed by pricing the *same observed token counts* against the baseline (flagship) model's rates, not by actually re-running the flagship model on every request. A real flagship response could tokenize differently. This is a deliberate, documented approximation — being upfront about it is part of the point.

## Future work (explicitly out of scope for v1)

- **Shadow-check validation** — sample a % of requests, fire a parallel call to a higher-tier model, and score both with an LLM judge to validate the routing decision was correct. Not built because full validation erodes the savings you're trying to prove, and it adds real engineering surface (parallel calls, judge scoring, comparison logic) that didn't fit this build's timeline. A production version would sample 5–10% and log divergence as a retraining signal.
- **Confidence self-report** — have the responding model self-report a confidence score in the same call, as a near-free proxy signal for "was this routing probably fine," without a second model call.
- **Outcome-based classifier recalibration** — retrain the complexity classifier on real task-success/escalation signals instead of a static rule set.
- **A second embeddable app** that imports the router as a dependency, to demonstrate it's reusable middleware rather than a single chat feature. The router package is already structured for this (no FastAPI/DB imports).
- **Local model tier (Ollama)** — cloud providers only for now.
