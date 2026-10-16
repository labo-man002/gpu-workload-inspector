from typing import Literal
from pydantic import BaseModel, Field

class Node(BaseModel):
    uid: str
    name: str
    gpu_allocatable: int = Field(ge=0)
    gpu_requested: int = Field(ge=0)
    zone: str | None = None

class Workload(BaseModel):
    uid: str
    name: str
    phase: Literal['Pending', 'Running', 'Succeeded', 'Failed']
    gpu_request: int = Field(ge=0)
    node_uid: str | None = None

class Insight(BaseModel):
    rule: str
    subject_uid: str
    title: str
    evidence: dict[str, int]
    limitation: str

class Snapshot(BaseModel):
    schema_version: str = '0.1'
    dataset_id: Literal['gpu-demo'] = 'gpu-demo'
    snapshot_id: str
    observed_at: str
    provenance: Literal['synthetic'] = 'synthetic'
    scenario: str
    nodes: list[Node]
    workloads: list[Workload]
    insights: list[Insight] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
