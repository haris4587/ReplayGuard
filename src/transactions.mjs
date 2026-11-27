import {isSuccessful} from 'genlayer-js';
export const PENDING_KEY='replayguard:pending:v1';
export async function submitAndTrack(client, call, storage, notify) {
  if(storage.getItem(PENDING_KEY)) throw Error('Resume the pending transaction before sending another.');
  notify({stage:'ESTIMATING',method:call.functionName});
  const estimate=await client.estimateTransactionFeesForWrite(call);
  notify({stage:'AWAITING_WALLET',method:call.functionName});
  const hash=await client.writeContract({...call,fees:{distribution:estimate.distribution,feeValue:estimate.feeValue}});
  const pending={hash,method:call.functionName,auditId:call.args?.[0]||'',createdAt:new Date().toISOString()};
  storage.setItem(PENDING_KEY,JSON.stringify(pending));
  return track(client,pending,storage,notify);
}
export async function track(client,pending,storage,notify) {
  notify({...pending,stage:'PENDING'});
  // Timeouts preserve the hash. Reconnect resumes this transaction; never resubmit.
  const tx=await client.waitForFinalization({hash:pending.hash,retries:90,interval:10000});
  const successful=isSuccessful(tx);
  storage.removeItem(PENDING_KEY);
  notify({...pending,stage:successful?'FINALIZED':'FAILED',tx});
  if(!successful) throw Error('Transaction failed: '+(tx.statusName||tx.status)+' / '+(tx.txExecutionResultName||tx.result));
  return tx;
}
