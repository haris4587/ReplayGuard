# ReplayGuard

Event-processing idempotency verification powered by a real GenLayer Intelligent Contract.

**Website:** https://replayguard.mohamedansaf222.chatgpt.site

**Contract:** [0xf6A55682019D16592B8639A32b8798ba3c07bd58](https://explorer-studio.genlayer.com/address/0xf6A55682019D16592B8639A32b8798ba3c07bd58) — Studionet, chain 61999.

ReplayGuard helps teams investigate whether duplicate webhook deliveries, queue messages and retries caused repeated business effects. It locks a processing policy and exact event/execution documents, verifies counter invariants, asks independent GenLayer validators to assess business semantics, and records hash-linked transition receipts. It does not modify the system under review.

## Run

```sh
npm ci
npm test
npm run build
npm run dev
```

Requires Node 22+ and Python 3.11+. There are no paid API keys in the frontend; AI execution happens through GenLayer consensus. `genlayer-js` is pinned to 2.0.0. Modern browsers supporting ES2022 are required.

## Review the live audit

Open **Evidence & receipts**, enter `RG-LIVE-001`, and select **Load & verify**. The app reads finalized contract state and all receipts, then recomputes the policy, evidence, decision, state and receipt hashes in the browser. An isolated payment handler processed three deliveries of one payment event; only the first charged 2500 cents and created one fulfillment.

## Create an audit

1. Use **Verification desk**. Choose a unique audit identifier.
2. Pick a reproducible evidence pack, or replace the policy and evidence JSON with your own commit-pinned documents. Policies support 2–64 attempts and 1–8 named nonnegative integer counters.
3. Connect MetaMask or another injected EIP-1193 wallet to Studionet. Select **Register policy**, **Lock evidence**, then **Request review**, waiting for successful finalization after each write.
4. Optionally challenge a reviewed result with an evidence-grounded objection and request review again. The owner can finalize the audit.
5. Export the complete record and receipt chain from **Evidence & receipts**.

**Studio alternative:** The built-in Studio wallet signs inside [GenLayer Studio](https://studio.genlayer.com). Import `contracts/replay_guard.py`, select the existing contract address, and call the same methods with `public/safe-policy.json` and `public/safe-bundle.json`. Never export a Studio private key into this app. Live lifecycle testing used Studio's built-in account; a live MetaMask extension signing test is not claimed.

## Why GenLayer

Counter arithmetic alone cannot establish whether an operation described in a processing note satisfies a business rule or falls within a permitted retry exception. Every validator independently interprets the locked evidence and rules, produces an ordered per-attempt decision vector and exact supporting quotations, and checks the leader's decision vector against its own. This uses `gl.vm.run_nondet_unsafe` with a validating callback, not a server-side model API. Remote document hash checks use `gl.eq_principle.strict_eq`. Deterministic violations take precedence over semantic reasoning.

| Verdict | Meaning |
| --- | --- |
| IDEMPOTENT | Duplicate coverage exists, every event eventually processes, all invariants hold, all semantic cases are permitted, and retries change no tracked state. |
| CONDITIONAL | All checks hold, but retries produce bounded effects expressly permitted by the locked retry rule. |
| VIOLATION | Deterministic counter/payload/continuity checks fail or semantic review identifies a forbidden operation. |
| INCONCLUSIVE | Evidence retrieval or hash verification fails, coverage is insufficient, or semantic support is unknown. |

## State and API

`REGISTERED → SUBMITTED → REVIEWED / RETRYABLE → FINALIZED`, with an optional `CHALLENGED → review` transition. The policy and evidence are immutable. Anyone may review or challenge; only the owner submits evidence and finalizes. One challenge and at most three successful review executions per audit are allowed. Finalization is owner-controlled and has no promised timed challenge window.

Writes: `register_policy(audit_id, policy_json)`, `submit_evidence(audit_id, bundle_json)`, `review(audit_id)`, `challenge(audit_id, reason)`, `finalize(audit_id)`.

Views: `get_audit(audit_id)`, `get_receipt(audit_id, sequence)`, `get_count()`.

## Evidence and limits

Fixtures come from executing [fixtures/processor.py](fixtures/processor.py); regenerate with `python fixtures/processor.py`. They represent isolated safe, faulty and permitted-audit-entry handlers, not customer production traffic. Documents are pinned to GitHub commit `047ba8e3bf586003eec741200f8266ab23155d9c`. The commit identifies the producer's documents; it does not authenticate a production service or establish complete logging. Hidden effects, omitted events, concurrent traces, negative deltas and arbitrary state transformations are outside this counter model.

Local tests mock network and VM consensus boundaries. Live receipts separately demonstrate hosted execution. See [verification evidence](docs/EVIDENCE.md), [reviewer steps](docs/REVIEWER.md), [deployment](docs/DEPLOYMENT.md), [submission text](docs/SUBMISSION.md) and [security](SECURITY.md).
