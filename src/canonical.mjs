export function canonical(v) {
  if (v === null || typeof v !== 'object') return JSON.stringify(v).replace(/[\u007f-\uffff]/g,c=>'\\u'+c.charCodeAt(0).toString(16).padStart(4,'0'));
  if (Array.isArray(v)) return '['+v.map(canonical).join(',')+']';
  return '{'+Object.keys(v).sort().map(k=>canonical(k)+':'+canonical(v[k])).join(',')+'}';
}
export async function sha256(raw) {
  const bytes=typeof raw==='string'?new TextEncoder().encode(raw):raw;
  return Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes)),x=>x.toString(16).padStart(2,'0')).join('');
}
export const digest=v=>sha256(canonical(v));
export async function verifyChain(auditId,record,receipts) {
  if(receipts.length!==record.sequence) throw Error('Receipt count mismatch');
  let previous='0'.repeat(64);
  for (let i=0;i<receipts.length;i++) {
    const {hash,...body}=receipts[i];
    if(body.audit_id!==auditId || body.sequence!==i+1 || body.previous!==previous || await digest(body)!==hash) throw Error('Receipt integrity mismatch');
    previous=hash;
  }
  if(previous!==record.head) throw Error('Receipt head mismatch');
  if(await digest(record.policy)!==record.policy_hash) throw Error('Policy commitment mismatch');
  if(record.bundle && await digest(record.bundle)!==record.bundle_hash) throw Error('Evidence commitment mismatch');
  if(record.bundle) for (const e of Object.values(record.bundle)) {
    if(new TextEncoder().encode(e.body).length!==e.bytes || await sha256(e.body)!==e.sha256) throw Error('Evidence bytes mismatch');
  }
  const last=receipts.at(-1);
  if(last && await digest({...record,sequence:record.sequence-1,head:last.previous})!==last.state_hash) throw Error('State commitment mismatch');
  if(record.result) {
    const review=receipts.filter(x=>x.event==='REVIEWED').at(-1);
    if(!review || review.detail.result_hash!==await digest(record.result)) throw Error('Decision commitment mismatch');
  }
  return true;
}
