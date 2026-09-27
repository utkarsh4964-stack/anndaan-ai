# Anndaan.AI

AI-powered smart food waste reduction & sustainable redistribution ecosystem for
institutional kitchens and food processing units — built for **SIH 2026, Problem
Statement 26234**.

## Architecture

Five cooperating agents behind a FastAPI backend:

| Agent | File | Role |
|---|---|---|
| Demand Forecasting | `backend/app/agents/demand_forecast.py` | Predicts per-item demand from consumption history |
| Quality & Expiry Vision | `backend/app/agents/expiry_detection.py` | Flags near-expiry items (vision/IoT stub) |
| Redistribution Matching | `backend/app/agents/redistribution_matcher.py` | Finds nearest eligible NGO/shelter for surplus |
| Logistics Optimization | `backend/app/agents/logistics_optimizer.py` | Plans pickup windows |
| Sustainability & Analytics | `backend/app/agents/analytics.py` | Waste-prevented / CO2e / ESG metrics |

Each agent has a real, runnable heuristic implementation (not a mock) so the
whole pipeline — log surplus → assess → match → schedule pickup → see it in
analytics — works end to end today. Swap the heuristics for trained models as
you get real data (see the docstring in each agent file for what to replace).

## Repo layout

```
backend/    FastAPI + SQLAlchemy, SQLite locally / Postgres in prod
frontend/   Next.js dashboard (App Router)
```

## Local development

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

API docs at `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

Dashboard at `http://localhost:3000/dashboard`.

## Quick smoke test (backend)

```bash
curl -X POST localhost:8000/facilities/ -H "Content-Type: application/json" \
  -d '{"name":"Hostel Mess","type":"kitchen","latitude":28.568,"longitude":77.326}'
curl -X POST localhost:8000/facilities/ -H "Content-Type: application/json" \
  -d '{"name":"Local Food Bank","type":"ngo","latitude":28.570,"longitude":77.330,"capacity_kg":50}'
curl -X POST localhost:8000/surplus/ -H "Content-Type: application/json" \
  -d '{"facility_id":1,"item_name":"Rice & Dal","quantity_kg":15}'
curl -X POST "localhost:8000/surplus/1/assess?category=cooked_grain"
curl -X POST localhost:8000/redistribution/match/1
curl localhost:8000/analytics/summary
```

## Deploying on Render

### Backend (Web Service)

1. Push this repo to GitHub, then in Render: **New → Web Service**, connect
   the repo, set **root directory** to `backend`.
2. Build command: `pip install -r requirements.txt`
3. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add a **Render PostgreSQL** instance (New → PostgreSQL), then set the
   backend's `DATABASE_URL` env var to its Internal Connection String.
5. Deploy — `/health` should return `{"status": "healthy"}`.

### Frontend (Web Service or Static Site)

1. **New → Web Service**, root directory `frontend`.
2. Build command: `npm install && npm run build`
3. Start command: `npm run start`
4. Set env var `NEXT_PUBLIC_API_BASE` to your backend's Render URL
   (e.g. `https://anndaan-backend.onrender.com`).
5. Redeploy the frontend any time the backend URL changes.

### Notes

- Free-tier Render services spin down when idle — the first request after
  idle will be slow (~30-50s cold start). Fine for a demo, upgrade the plan
  before a live judging session if that matters.
- CORS is wide open (`allow_origins=["*"]`) in `main.py` for the MVP —
  restrict it to your deployed frontend origin before submission.

## Next steps toward a full SIH build

- Replace the demand-forecast heuristic with a trained time-series model
  once you have a few weeks of `ConsumptionLog` data.
- Wire `expiry_detection.py` to a real vision model (YOLOv8/CNN) fed by
  actual kitchen camera or photo uploads.
- Add an NGO/shelter self-registration flow instead of manually seeding
  `Facility` rows.
- Add SMS/WhatsApp notifications when a `RedistributionMatch` is created.
- Add a processing-unit-specific dashboard (downtime, overproduction,
  energy-use anomalies) — the PS explicitly asks for this alongside kitchens.
