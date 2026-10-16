from app.models import Insight, Snapshot

def placement_insights(snapshot: Snapshot) -> list[Insight]:
    """Whole exclusive GPU counts only; fixtures declare all nodes eligible."""
    if any(n.gpu_requested > n.gpu_allocatable for n in snapshot.nodes):
        return []  # inconsistent accounting must not produce placement advice
    free = [n.gpu_allocatable - n.gpu_requested for n in snapshot.nodes]
    total, largest = sum(free), max(free, default=0)
    findings = []
    for job in snapshot.workloads:
        if job.phase != 'Pending' or job.node_uid or job.gpu_request == 0:
            continue
        if not free:
            rule, title = 'no-nodes', 'No candidate nodes'
        elif total < job.gpu_request:
            rule, title = 'shortage', 'Insufficient total free GPU units'
        elif largest < job.gpu_request:
            rule, title = 'fragmentation', 'Free GPU units are split across nodes'
        else:
            rule, title = 'count-fit', 'A node has enough free GPU units'
        findings.append(Insight(rule=rule, subject_uid=job.uid, title=title,
            evidence={'requested': job.gpu_request, 'total_free': total, 'largest_node_free': largest},
            limitation='GPU-count check only. Assumes all fixture nodes eligible; CPU, memory, affinity, taints, MIG, sharing and gang constraints are not evaluated. Count fit does not guarantee scheduling.'))
    return findings
