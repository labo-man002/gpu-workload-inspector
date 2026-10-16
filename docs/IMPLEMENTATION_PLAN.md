# Implementation plan

## Current checkpoint: runnable fixture scaffold

Implemented: typed models, provider seam, deterministic fragmented/restored scenarios, GPU-count analysis, HTTP endpoints, dashboard, focused tests and deployment templates.

The technical specification describes the target product. This document and the README describe actual implementation status. The four-hour budget below is a target for the next MVP session, assuming Docker/kind work locally; environment setup may consume that budget.

## 1. Real Kubernetes state — 55 minutes

Add a `local-kubernetes` dataset and `KubernetesStateProvider`. Use the official Python client with explicit kubeconfig context or in-cluster credentials. Poll Nodes, Pods, Jobs and core Events with deadlines. Normalize UIDs, owners, phases, allocatable resources, labels and timestamps. Publish only complete successful collections; retain the last successful snapshot with visible failure/staleness status.

Start CPU/memory and conventional exclusive GPU resource accounting with supported request semantics. Mark unsupported init/sidecar, sharing, MIG or DRA cases incomplete until handled; never emit confident placement advice from incomplete data. Keep all synthetic data in `gpu-demo`.

Acceptance: local nodes and Jobs appear with live provenance; API outage is visible; no synthetic fallback. Unit tests cover bound Pending and terminal Pods, missing resources and partial-list failures.

## 2. Deploy and exercise operations — 35 minutes

Build the image, load into kind and deploy. Introduce a dedicated ServiceAccount and narrowly scoped get/list permissions for Nodes, Pods, Jobs and Events. No Secrets access or write permissions. Verify readiness, resource requests, logs, and port-forwarding.

Run a tiny CPU Job and one deliberately unschedulable CPU request. Inspect the Pending event, adjust the workload manually, and observe completion. Record commands, outcome and a screenshot in a short demo report.

Acceptance: actual deployment and failure diagnosis documented; this is the first concrete hands-on Kubernetes milestone.

## 3. Snapshot history and event evidence — 35 minutes

Add SQLite with one writer and immutable snapshot IDs. Poll at 15 seconds; retain 24 hours with a bounded database policy. Persist observed Events, deduplicated by UID/count rather than inventing a complete event history. Snapshot-pin drill-downs. Make ephemeral versus persistent storage explicit.

Acceptance: a workload transition can be replayed; missing collection windows remain missing; details cannot accidentally use a newer snapshot than the overview.

## 4. Synthetic GPU telemetry — 40 minutes

Define metric samples, quality flags and timestamped explicit device assignments. Add deterministic sustained-low-activity and missing-data scenarios. Implement a five-minute low-activity rule only for stable exclusive assignments with adequate sample coverage. Preserve null values; never substitute zero for missing measurements.

Acceptance: allocation and utilization are separately displayed; insufficient samples yield unknown; low activity is presented as an investigation lead, not wasted capacity or a measured optimization result.

## 5. Frontend investigation workflow — 45 minutes

Add workload selection, snapshot-pinned details, event timeline, one utilization chart and node-to-workload placement links. Display source, freshness, rule evidence and limitations. Extend the data contract rather than implementing scheduling logic in React.

Acceptance: select a Pending workload and explain the relevant resource state in under a minute. No inferred NVLink/InfiniBand topology from zone labels.

## 6. Verification and demo — 30 minutes

Run contract/rule tests, frontend build and the local deployment walkthrough. Capture one short fragmented-to-restored scenario and one real Kubernetes Pending-to-completed investigation. Pin tested dependency resolutions. Document tested commands, failures, limitations and next steps.

Acceptance: a fresh checkout has a reproducible run procedure and explicit implementation inventory. The CV can then describe exactly what was built and deployed.

## Scope cuts if time runs short

Keep live collection/deployment, provenance and trustworthy accounting. Cut the history selector, advanced topology visualization, extra charts and KAI panel first. Do not describe a scaffold or fixture-only run as cluster-operations experience.

## Following iterations

1. Prometheus query adapter using an explicit metric allowlist and bounded range queries.
2. DCGM data integration, GPU UUID mapping and exporter schema verification.
3. KAI scheduler metrics for queue allocation/fair-share context, separate from hardware activity.
4. Resilient watch/relist, supported scheduling constraints, persistent deployment and authentication.

`rea` is not a core dependency. Evaluate it separately after the collector works; the MVP does not need an autonomous agent to explain deterministic evidence.
