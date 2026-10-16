import json
from pathlib import Path
from app.models import Snapshot

FIXTURES = Path(__file__).resolve().parents[3] / 'fixtures'
SCENARIOS = ('fragmented', 'restored')

class FixtureProvider:
    async def collect(self, scenario: str) -> Snapshot:
        if scenario not in SCENARIOS:
            raise ValueError('Unknown scenario')
        return Snapshot.model_validate(json.loads((FIXTURES / f'{scenario}.json').read_text()))
