import { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './style.css';
type Snapshot = {snapshot_id:string;observed_at:string;nodes:{uid:string;name:string;gpu_allocatable:number;gpu_requested:number;zone:string|null}[];workloads:{uid:string;name:string;phase:string;gpu_request:number;node_uid:string|null}[];insights:{rule:string;title:string;evidence:Record<string,number>;limitation:string}[];warnings:string[]};
function App(){
 const [scenario,setScenario]=useState('fragmented');
 const [data,setData]=useState<Snapshot|null>(null);
 const [error,setError]=useState('');
 useEffect(()=>{const controller=new AbortController();setData(null);setError('');
 fetch(`/api/v1/datasets/gpu-demo/snapshot?scenario=${scenario}`,{signal:controller.signal})
 .then(r=>{if(!r.ok)throw new Error(`API returned ${r.status}`);return r.json()})
 .then(setData).catch(e=>{if(e.name!=='AbortError')setError(e.message)});
 return ()=>controller.abort();},[scenario]);
 return <main><header><div><small>CLUSTER OPERATIONS / PROTOTYPE</small><h1>GPU Workload Inspector</h1><p>From resource allocation to placement explanations.</p></div><span className="badge">Synthetic GPU dataset</span></header>
 <label>Scenario <select value={scenario} onChange={e=>setScenario(e.target.value)}><option value="fragmented">Fragmented capacity</option><option value="restored">Capacity released</option></select></label>
 {error&&<p role="alert">{error} — check that the backend is running.</p>}
 {!data&&!error&&<p>Loading snapshot…</p>}
 {data&&<><p className="muted">Scenario time: {data.observed_at} · Snapshot {data.snapshot_id}</p>
 <section className="nodes">{data.nodes.map(n=><article key={n.uid}><small>{n.zone??'Unknown zone'}</small><h2>{n.name}</h2><strong>{n.gpu_allocatable-n.gpu_requested} / {n.gpu_allocatable}</strong><p>GPU units free by request accounting</p><meter min={0} max={n.gpu_allocatable} value={n.gpu_requested}/><p>{n.gpu_requested} requested · measured utilization unavailable</p></article>)}</section>
 <h2>Workloads</h2><div className="table"><table><thead><tr><th>Name</th><th>Phase</th><th>GPU request</th><th>Placement</th></tr></thead><tbody>{data.workloads.map(w=><tr key={w.uid}><td>{w.name}</td><td>{w.phase}</td><td>{w.gpu_request}</td><td>{w.node_uid??'Unassigned'}</td></tr>)}</tbody></table></div>
 <h2>Placement insights</h2>{data.insights.map(i=><article key={i.rule}><span className="badge">{i.rule}</span><h3>{i.title}</h3><p>Requested: {i.evidence.requested} · Total free: {i.evidence.total_free} · Largest free on one node: {i.evidence.largest_node_free}</p><p className="muted">{i.limitation}</p></article>)}
 <footer>{data.warnings.join(' ')}</footer></>}
 </main>
}
createRoot(document.getElementById('root')!).render(<App/>);
