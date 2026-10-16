from typing import Protocol
from app.models import Snapshot

class StateProvider(Protocol):
    async def collect(self, scenario: str) -> Snapshot: ...

# MetricProvider and TopologyProvider contracts will be introduced with their
# normalized models. Do not treat node labels as physical fabric inventory.
