import asyncio
from fastapi.testclient import TestClient
from app.main import app
from app.providers.fixture import FixtureProvider
from app.analysis.placement import placement_insights

def fixture(name='fragmented'):
    return asyncio.run(FixtureProvider().collect(name))

def test_fragmentation_and_release():
    before, after = fixture(), fixture('restored')
    assert placement_insights(before)[0].rule == 'fragmentation'
    assert placement_insights(before)[0].evidence == {'requested':4,'total_free':4,'largest_node_free':2}
    assert placement_insights(after)[0].rule == 'count-fit'

def test_shortage_and_bound_pending():
    s=fixture();s.workloads[-1].gpu_request=5
    assert placement_insights(s)[0].rule == 'shortage'
    s.workloads[-1].node_uid='node-a'
    assert placement_insights(s)==[]

def test_inconsistent_accounting_has_no_advice():
    s=fixture();s.nodes[0].gpu_requested=9
    assert placement_insights(s)==[]

def test_api_isolation_and_scenario_validation():
    with TestClient(app) as c:
        assert c.get('/api/v1/datasets/local-kubernetes/snapshot').status_code==404
        assert c.get('/api/v1/datasets/gpu-demo/snapshot?scenario=bad').status_code==422
        body=c.get('/api/v1/datasets/gpu-demo/snapshot').json()
        assert body['provenance']=='synthetic'
        assert body['insights'][0]['rule']=='fragmentation'
