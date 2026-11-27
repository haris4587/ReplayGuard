import hashlib, json, sys
from pathlib import Path
root = Path(__file__).resolve().parents[1]
commit = sys.argv[1]
for kind in ('safe', 'broken', 'conditional'):
    bundle = {}
    for role in ('events', 'executions'):
        path = 'fixtures/' + kind + '-' + role + '.json'
        raw = (root / path).read_bytes()
        bundle[role] = {'url': 'https://raw.githubusercontent.com/haris4587/ReplayGuard/' + commit + '/' + path, 'body': raw.decode(), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}
    p = {'schema': 'replayguard/v1', 'repository': 'haris4587/ReplayGuard', 'evidence_commit': commit, 'business_rule': 'Each payment event represents an order for 2500 cents. Charge exactly 2500 cents and create exactly one fulfillment on the first successful processing. Duplicate deliveries must not charge or fulfill again. Skipping a duplicate without changing business state is permitted.', 'retry_rule': 'A duplicate may append at most one audit entry per attempt. It must not charge money or create fulfillment again.' if kind == 'conditional' else '', 'state_rules': {'charged_cents': {'first_delta': 2500, 'retry_max': 0}, 'fulfillment_count': {'first_delta': 1, 'retry_max': 0}, 'audit_count': {'first_delta': 0, 'retry_max': 1 if kind == 'conditional' else 0}}, 'expected_attempts': 3, 'events_sha256': bundle['events']['sha256'], 'executions_sha256': bundle['executions']['sha256']}
    for key, value in [('policy', p), ('bundle', bundle)]:
        (root / 'public' / (kind + '-' + key + '.json')).write_text(json.dumps(value, indent=2) + '\n')
