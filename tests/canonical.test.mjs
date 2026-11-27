import test from 'node:test';
import assert from 'node:assert/strict';
import {canonical,digest,verifyChain} from '../src/canonical.mjs';
import {PENDING_KEY,submitAndTrack,track} from '../src/transactions.mjs';
const storage=()=>{const m=new Map();return {getItem:k=>m.get(k)||null,setItem:(k,v)=>m.set(k,v),removeItem:k=>m.delete(k)}};
test('canonical matches Python ordering, ASCII escapes, integer-like keys',()=>assert.equal(canonical({'10':2,'2':1,z:'é😀',a:[1,true,null]}),'{"10":2,"2":1,"a":[1,true,null],"z":"\\u00e9\\ud83d\\ude00"}'));
test('pending hash survives wait failure; second submit blocked',async()=>{
 const s=storage();let sent=0;const c={estimateTransactionFeesForWrite:async()=>({distribution:[],feeValue:0n}),writeContract:async()=>{sent++;return '0x123'},waitForFinalization:async()=>{throw Error('timeout')}};
 await assert.rejects(submitAndTrack(c,{functionName:'review',args:['a']},s,()=>{}),/timeout/);
 assert.equal(JSON.parse(s.getItem(PENDING_KEY)).hash,'0x123');
 await assert.rejects(submitAndTrack(c,{},s,()=>{}),/Resume/);assert.equal(sent,1);
});
test('wallet rejection never creates pending operation',async()=>{
 const s=storage();await assert.rejects(submitAndTrack({estimateTransactionFeesForWrite:async()=>({distribution:[],feeValue:0n}),writeContract:async()=>{throw Error('rejected')}},{},s,()=>{}),/rejected/);assert.equal(s.getItem(PENDING_KEY),null);
});
test('terminal failed execution clears pending and reports failure',async()=>{
 const s=storage();s.setItem(PENDING_KEY,'hash');const stages=[];
 await assert.rejects(track({waitForFinalization:async()=>({statusName:'FINALIZED',txExecutionResultName:'VM_ERROR'})},{hash:'0x1'},s,x=>stages.push(x.stage)),/failed/);
 assert.equal(s.getItem(PENDING_KEY),null);assert.equal(stages.at(-1),'FAILED');
});
test('tampered receipt rejected',async()=>{
 const p={schema:'x'};const r={sequence:1,head:'bad',policy:p,policy_hash:await digest(p)};
 await assert.rejects(verifyChain('x',r,[{hash:'bad',audit_id:'x',sequence:1,previous:'0'.repeat(64)}]),/integrity/);
});
