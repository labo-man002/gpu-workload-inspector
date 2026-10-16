# GPU Workload Inspector

A read-only Kubernetes/GPU observability project. This scaffold implements a runnable **synthetic GPU-count analysis** slice. It does not yet collect live Kubernetes state or hardware telemetry.

## Run locally

Requirements: Python 3.12+, Node 22+, npm.

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r backend/requirements-dev.txt -c backend/requirements.lock
PYTHONPATH=backend uvicorn app.main:app --reload --port 8000
```

In another terminal:

```bash
cd frontend
npm ci
npm run dev
```

Open http://localhost:5173. API documentation: http://localhost:8000/docs.

```bash
PYTHONPATH=backend .venv/bin/pytest backend/tests -q
cd frontend
npm run build
```

After the frontend build, restart the backend and open http://localhost:8000 to use the bundled frontend. Vite proxies `/api` during development; no permissive CORS configuration is needed.

## What works

- Typed snapshot contract and replaceable state-provider interface.
- Isolated synthetic GPU dataset with deterministic scenario timestamps.
- Fragmentation, shortage and GPU-count-fit analysis with supporting numbers.
- FastAPI snapshot/dataset endpoints; invalid datasets never silently fall back.
- React/TypeScript node overview, workload table, scenario selection and insights.
- Docker build and kind deployment manifests (runtime validation tracked separately).

Compare **Fragmented capacity** with **Capacity released**. Both nodes initially have two free GPU units; a pending four-GPU Pod cannot fit on either. Releasing two units on one node produces a count-fit candidate. This is not a full scheduling prediction.

## Not implemented yet

Live Kubernetes collection, effective Pod request calculation, SQLite history, GPU utilization time series, low-activity analysis, event collection, physical topology, KAI and Prometheus/DCGM adapters. Node allocation totals in fixtures are explicit scenario inputs; the live implementation must compute and validate them.

## Container / kind walkthrough

Requires Docker, kind and kubectl. Commands below are a reproducible deployment procedure, not a claim that deployment has already been tested.

```bash
docker build -t gpu-inspector:dev .
kind create cluster --name gpu-inspector
kind load docker-image gpu-inspector:dev --name gpu-inspector
kubectl --context kind-gpu-inspector apply -f deploy/kubernetes.yaml
kubectl --context kind-gpu-inspector rollout status deployment/gpu-inspector
kubectl --context kind-gpu-inspector port-forward service/gpu-inspector 8000:8000
```

Open http://localhost:8000. This deployment deliberately has no API credentials: live collection is not implemented. Add a dedicated read-only ServiceAccount when implementing the collector. No GPUs are required for the fixture demo.

## Repository map

- `backend/app/models.py`: normalized snapshot contract.
- `backend/app/providers/`: provider interface and fixture reader.
- `backend/app/analysis/`: pure explanation rules.
- `backend/app/main.py`: HTTP endpoints and optional static frontend.
- `backend/tests/`: rule boundaries and API isolation tests.
- `frontend/src/`: initial dashboard.
- `fixtures/`: deterministic scenarios.
- `deploy/`: single-replica Kubernetes deployment.
- `docs/IMPLEMENTATION_PLAN.md`: ordered milestones and acceptance gates.
- `TECHNICAL_SPEC.md`: broader proposed design; not an implementation inventory.

No license has been chosen yet. Select one before distributing the project as open source.
