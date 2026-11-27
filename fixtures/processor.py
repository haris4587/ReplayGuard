"""Reproducible isolated webhook processor; never contacts a payment service."""
import hashlib
import json
from pathlib import Path


def run(broken=False, retry_audit=False):
    state = {'charged_cents': 0, 'fulfillment_count': 0, 'audit_count': 0}
    processed = set()
    events, executions = [], []
    payload_hash = hashlib.sha256(b'{"order_id":"order-1042","amount_cents":2500}').hexdigest()
    for i in range(3):
        before = dict(state)
        duplicate = 'payment-1042' in processed
        if not duplicate or broken:
            state['charged_cents'] += 2500
            state['fulfillment_count'] += 1
            processed.add('payment-1042')
            outcome = 'processed'
            note = 'Charged 2500 cents and created one fulfillment for order-1042.'
        else:
            outcome = 'skipped'
            if retry_audit:
                state['audit_count'] += 1
                note = 'Duplicate delivery skipped; appended one retry audit entry. No payment or fulfillment repeated.'
            else:
                note = 'Duplicate delivery skipped. No payment, fulfillment, or audit state changed.'
        aid = 'attempt-' + str(i + 1)
        events.append({'seq': i + 1, 'attempt_id': aid, 'event_id': 'payment-1042', 'payload_sha256': payload_hash, 'outcome': outcome, 'note': note})
        executions.append({'attempt_id': aid, 'before': before, 'after': dict(state)})
    return events, executions


if __name__ == '__main__':
    root = Path(__file__).parent
    for name, options in [('safe', {}), ('broken', {'broken': True}), ('conditional', {'retry_audit': True})]:
        events, executions = run(**options)
        (root / (name + '-events.json')).write_text(json.dumps(events, indent=2) + '\n')
        (root / (name + '-executions.json')).write_text(json.dumps(executions, indent=2) + '\n')
