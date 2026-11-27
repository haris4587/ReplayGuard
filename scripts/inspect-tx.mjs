import {createClient,isSuccessful} from 'genlayer-js';
import {studionet} from 'genlayer-js/chains';
import fs from 'node:fs';
const client=createClient({chain:studionet});
for(const hash of process.argv.slice(2)){
 const tx=await client.getTransaction({hash});
 const fields=['hash','from_address','to_address','statusName','txExecutionResultName','lifecycle','created_at','leader_only','execution_mode','num_of_initial_validators','result_name','last_round'];
 const summary=Object.fromEntries(fields.map(k=>[k,tx[k]??null]));
 summary.receipt_summary=true;summary.consensus_votes=tx.consensus_data?.votes;
 const receipts=tx.consensus_data?.leader_receipt||[];
 summary.execution_receipts=(Array.isArray(receipts)?receipts:[receipts]).map(r=>Object.fromEntries(['mode','vote','execution_result','processing_time','contract_state_hash'].map(k=>[k,r[k]??null])));
 fs.writeFileSync('docs/tx-'+hash+'.json',JSON.stringify(summary,(_,v)=>typeof v==='bigint'?v.toString():v,2)+'\n');
 console.log(JSON.stringify({hash,status:tx.statusName,execution:tx.txExecutionResultName,successful:isSuccessful(tx),address:tx.toAddress||tx.to_address}));
}
