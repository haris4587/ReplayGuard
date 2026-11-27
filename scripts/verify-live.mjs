import {createClient} from 'genlayer-js';
import {studionet} from 'genlayer-js/chains';
import {TransactionHashVariant} from 'genlayer-js/types';
import fs from 'node:fs';
import {verifyChain,sha256} from '../src/canonical.mjs';
const config=JSON.parse(fs.readFileSync('public/deployment.json','utf8'));
if(!config.address)throw Error('No deployment recorded');
const client=createClient({chain:studionet});
const source=fs.readFileSync('contracts/replay_guard.py','utf8');
if(await client.getContractCode(config.address)!==source)throw Error('Deployed source mismatch');
const read=async(functionName,args)=>JSON.parse(await client.readContract({address:config.address,transactionHashVariant:TransactionHashVariant.LATEST_FINAL,functionName,args}));
const ids=process.argv.slice(2);if(!ids.length)ids.push('RG-LIVE-001');
const records=[];
for(const id of ids){
 const record=await read('get_audit',[id]);const receipts=[];
 for(let i=1;i<=record.sequence;i++)receipts.push(await read('get_receipt',[id,i]));
 await verifyChain(id,record,receipts);
 fs.writeFileSync('docs/'+id+'-record.json',JSON.stringify(record,null,2)+'\n');
 fs.writeFileSync('docs/'+id+'-receipts.json',JSON.stringify(receipts,null,2)+'\n');
 records.push({id,status:record.result?.status,phase:record.phase,head:record.head,receipts:record.sequence,attempts:record.attempts});
}
const report={checked_at:new Date().toISOString(),network:config.network,chain_id:config.chain_id,contract:config.address,source_sha256:await sha256(source),deployed_source_matches:true,finalized_reads:true,records};
fs.writeFileSync('docs/verification.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
