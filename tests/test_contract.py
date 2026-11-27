"""Local harness: real contract logic, mocked network and consensus boundaries."""
import copy, hashlib, importlib.util, json, pathlib, sys, types, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
class Return:
    def __init__(self, value): self.calldata = value
class Map:
    def __class_getitem__(cls, key): return dict
identity = lambda f: f
gl = types.SimpleNamespace(Contract=object, public=types.SimpleNamespace(write=identity, view=identity), message=types.SimpleNamespace(sender_address='owner'), vm=types.SimpleNamespace(Return=Return))
sys.modules['genlayer'] = types.SimpleNamespace(gl=gl, TreeMap=Map, u256=int)
spec = importlib.util.spec_from_file_location('contract', ROOT/'contracts/replay_guard.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
spec2 = importlib.util.spec_from_file_location('processor', ROOT/'fixtures/processor.py')
processor = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(processor)

class ContractTests(unittest.TestCase):
    def setUp(self):
        gl.message.sender_address = 'owner'
        self.c = m.ReplayGuard(); self.c.records = {}; self.c.receipts = {}
        self.p = {'schema': m.SCHEMA, 'repository': 'haris4587/ReplayGuard', 'evidence_commit': 'a'*40, 'business_rule': 'Charge once.', 'retry_rule': '', 'state_rules': {'charged_cents': {'first_delta': 2500, 'retry_max': 0}, 'fulfillment_count': {'first_delta': 1, 'retry_max': 0}, 'audit_count': {'first_delta': 0, 'retry_max': 0}}, 'expected_attempts': 3}
        self.events, self.executions = processor.run()
        self.refresh()
        self.decisions = ['PERMITTED']*3
        self.prompts = 0
        def get(url):
            body = next(e['body'].encode() for e in self.b.values() if e['url'] == url)
            return types.SimpleNamespace(status=200, body=body)
        def prompt(_):
            self.prompts += 1
            return m.canonical({'cases': [{'attempt_id': e['attempt_id'], 'decision': d, 'reason': 'The operation follows the policy.', 'quote': e['note'][:80]} for e, d in zip(self.events, self.decisions)]})
        gl.nondet = types.SimpleNamespace(web=types.SimpleNamespace(get=get), exec_prompt=prompt)
        gl.eq_principle = types.SimpleNamespace(strict_eq=lambda f:f())
        def run(f,v):
            answer=f()
            if not v(Return(answer)): raise ValueError('Consensus rejected')
            return answer
        gl.vm.run_nondet_unsafe = run
    def refresh(self):
        self.b = {}
        for role, value in [('events', self.events), ('executions', self.executions)]:
            body = m.canonical(value); sha = hashlib.sha256(body.encode()).hexdigest()
            self.p[role+'_sha256'] = sha
            self.b[role] = {'url': 'https://raw.githubusercontent.com/haris4587/ReplayGuard/'+'a'*40+'/'+role+'.json', 'body': body, 'sha256': sha, 'bytes': len(body.encode())}
    def submit(self):
        self.c.register_policy('audit', m.canonical(self.p)); self.c.submit_evidence('audit', m.canonical(self.b))
    def record(self): return json.loads(self.c.get_audit('audit'))
    def review(self): self.submit(); self.c.review('audit'); return self.record()['result']
    def test_safe_independent_validators(self):
        self.assertEqual(self.review()['status'], 'IDEMPOTENT'); self.assertEqual(self.prompts, 2)
    def test_duplicate_charge_cannot_be_excused(self):
        self.events, self.executions = processor.run(broken=True); self.refresh()
        self.assertEqual(self.review()['status'], 'VIOLATION'); self.assertEqual(self.prompts, 0)
    def test_allowed_retry_effect(self):
        self.events, self.executions = processor.run(retry_audit=True); self.p['retry_rule']='One audit append per retry allowed.'; self.p['state_rules']['audit_count']['retry_max']=1; self.refresh()
        self.assertEqual(self.review()['status'], 'CONDITIONAL')
    def test_no_rule_no_exception(self):
        self.events, self.executions = processor.run(retry_audit=True); self.p['state_rules']['audit_count']['retry_max']=1; self.refresh()
        self.assertEqual(self.review()['status'], 'INCONCLUSIVE')
    def test_conflicting_payload(self):
        self.events[1]['payload_sha256']='b'*64; self.refresh()
        self.assertIn('attempt-2:IDENTIFIER_PAYLOAD_CONFLICT', self.review()['deterministic']['failures'])
    def test_discontinuous_state(self):
        self.executions[1]['before']['charged_cents']=10; self.refresh()
        self.assertEqual(self.review()['status'], 'VIOLATION')
    def test_missing_first_effect(self):
        for x in self.executions: x['before']['charged_cents']=0; x['after']['charged_cents']=0
        self.refresh(); self.assertEqual(self.review()['status'], 'VIOLATION')
    def test_decrement_violation(self):
        self.executions[2]['after']['charged_cents']=0; self.refresh(); self.assertEqual(self.review()['status'], 'VIOLATION')
    def test_semantic_forbidden(self):
        self.decisions[1]='FORBIDDEN'; self.assertEqual(self.review()['status'], 'VIOLATION')
    def test_semantic_unknown(self):
        self.decisions[1]='UNKNOWN'; self.assertEqual(self.review()['status'], 'INCONCLUSIVE')
    def test_fabricated_quote(self):
        gl.nondet.exec_prompt=lambda _:m.canonical({'cases':[{'attempt_id':e['attempt_id'],'decision':'PERMITTED','reason':'ok','quote':'invented quote'} for e in self.events]})
        self.assertEqual(self.review()['status'], 'INCONCLUSIVE')
    def test_bad_model_json(self):
        gl.nondet.exec_prompt=lambda _:'not json'; self.assertEqual(self.review()['status'], 'INCONCLUSIVE')
    def test_validator_disagreement(self):
        self.submit()
        def run(f,v):
            leader=f(); self.decisions[1]='FORBIDDEN'; self.assertFalse(v(Return(leader))); raise ValueError('Consensus rejected')
        gl.vm.run_nondet_unsafe=run
        with self.assertRaises(ValueError): self.c.review('audit')
        self.assertEqual(self.record()['attempts'],0)
    def test_no_retrieval_no_verdict(self):
        gl.nondet.web.get=lambda _:types.SimpleNamespace(status=404,body=b'')
        self.assertEqual(self.review()['status'], 'INCONCLUSIVE'); self.assertEqual(self.prompts,0)
    def test_substituted_remote(self):
        gl.nondet.web.get=lambda _:types.SimpleNamespace(status=200,body=b'substituted')
        self.assertEqual(self.review()['status'], 'INCONCLUSIVE')
    def test_retrieval_exception(self):
        def fail(_): raise RuntimeError('network')
        gl.nondet.web.get=fail; self.assertEqual(self.review()['status'],'INCONCLUSIVE')
    def test_coverage_count(self):
        self.events.pop(); self.refresh()
        with self.assertRaises(AssertionError): self.submit()
    def test_unique_attempts(self):
        self.events[1]['attempt_id']=self.events[0]['attempt_id']; self.refresh()
        with self.assertRaises(AssertionError): self.submit()
    def test_no_duplicate_coverage(self):
        for i,e in enumerate(self.events): e['event_id']='unique-'+str(i)
        # Each unique first process needs a real effect; skipped unseen events remain incomplete.
        self.refresh(); self.assertEqual(self.review()['status'],'INCONCLUSIVE')
    def test_commit_pinning(self):
        self.b['events']['url']=self.b['events']['url'].replace('a'*40,'main')
        with self.assertRaises(AssertionError): self.submit()
    def test_unsafe_urls(self):
        for suffix in ('../x','%2e%2e/x','x?token=1','x#fragment'):
            self.b['events']['url']='https://raw.githubusercontent.com/haris4587/ReplayGuard/'+'a'*40+'/'+suffix
            with self.assertRaises(AssertionError): self.submit()
    def test_hash_binding(self):
        self.b['events']['body']+=' '
        with self.assertRaises(AssertionError):self.submit()
    def test_bytes_binding(self):
        self.b['events']['bytes']+=1
        with self.assertRaises(AssertionError):self.submit()
    def test_boolean_not_integer(self):
        self.p['expected_attempts']=True
        with self.assertRaises(AssertionError):self.submit()
    def test_duplicate_keys(self):
        with self.assertRaises(AssertionError):m.parse('{"a":1,"a":2}')
    def test_nan(self):
        with self.assertRaises(ValueError):m.parse('{"a":NaN}')
    def test_owner_and_immutable(self):
        self.c.register_policy('audit',m.canonical(self.p)); gl.message.sender_address='other'
        with self.assertRaises(AssertionError):self.c.submit_evidence('audit',m.canonical(self.b))
        gl.message.sender_address='owner'; self.c.submit_evidence('audit',m.canonical(self.b))
        with self.assertRaises(AssertionError):self.c.submit_evidence('audit',m.canonical(self.b))
        with self.assertRaises(AssertionError):self.c.register_policy('audit',m.canonical(self.p))
    def test_receipts_and_finalization(self):
        self.review(); self.c.finalize('audit'); r=self.record(); previous=m.ZERO
        for i in range(1,r['sequence']+1):
            receipt=json.loads(self.c.get_receipt('audit',i)); claimed=receipt.pop('hash'); self.assertEqual(m.digest(receipt),claimed); self.assertEqual(receipt['previous'],previous); previous=claimed
        self.assertEqual(previous,r['head']); last=json.loads(self.c.get_receipt('audit',r['sequence'])); before={**r,'sequence':r['sequence']-1,'head':last['previous']}; self.assertEqual(m.digest(before),last['state_hash'])
        with self.assertRaises(AssertionError):self.c.review('audit')
    def test_challenge_once_reassess(self):
        self.review(); gl.message.sender_address='reviewer'; self.c.challenge('audit','Please check duplicate payments.'); self.c.review('audit')
        self.assertEqual(self.record()['attempts'],2)
        with self.assertRaises(AssertionError):self.c.challenge('audit','again')
        with self.assertRaises(AssertionError):self.c.finalize('audit')
    def test_retry_budget(self):
        self.decisions=['UNKNOWN']*3; self.submit()
        for _ in range(3):self.c.review('audit')
        with self.assertRaises(AssertionError):self.c.review('audit')
    def test_fixture_reproducible(self):
        for kind, kwargs in [('safe',{}),('broken',{'broken':True}),('conditional',{'retry_audit':True})]:
            e,x=processor.run(**kwargs)
            self.assertEqual(json.loads((ROOT/'fixtures'/f'{kind}-events.json').read_text()),e)
            self.assertEqual(json.loads((ROOT/'fixtures'/f'{kind}-executions.json').read_text()),x)
