import {createClient} from 'genlayer-js';
import {studionet} from 'genlayer-js/chains';
import fs from 'node:fs';
const client=createClient({chain:studionet});
const schema=await client.getContractSchemaForCode(fs.readFileSync('contracts/replay_guard.py','utf8'));
fs.writeFileSync('docs/contract-schema.json',JSON.stringify(schema,null,2)+'\n');
console.log(JSON.stringify(schema,null,2));
