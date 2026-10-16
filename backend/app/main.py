from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from app.providers.fixture import FixtureProvider, SCENARIOS
from app.analysis.placement import placement_insights
from app.models import Snapshot

app = FastAPI(title='GPU Workload Inspector', version='0.1.0')
provider = FixtureProvider()

@app.get('/healthz')
@app.get('/readyz')
def health():
    return {'status': 'ok', 'mode': 'fixture'}

@app.get('/api/v1/datasets')
def datasets():
    return [{'id': 'gpu-demo', 'mode': 'fixture', 'scenarios': SCENARIOS,
             'capabilities': ['snapshot', 'gpu-count-analysis']}]

@app.get('/api/v1/datasets/{dataset_id}/snapshot', response_model=Snapshot)
async def snapshot(dataset_id: str, scenario: str = 'fragmented'):
    if dataset_id != 'gpu-demo':
        raise HTTPException(404, 'Dataset unavailable; live Kubernetes is not implemented yet')
    if scenario not in SCENARIOS:
        raise HTTPException(422, 'Unknown scenario')
    result = await provider.collect(scenario)
    result.insights = placement_insights(result)
    return result

frontend = Path(__file__).resolve().parents[2] / 'frontend' / 'dist'
if frontend.is_dir():
    app.mount('/', StaticFiles(directory=frontend, html=True), name='frontend')
