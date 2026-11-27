# Verification evidence

## Real hosted execution

Network: stable Studionet, chain 61999. Contract: `0xf6A55682019D16592B8639A32b8798ba3c07bd58`.

| Action | Transaction |
| --- | --- |
| Deployment | `0x45fbd8469a287eaade8e978bf65c68595fd3c2b78b71da890ecb955eb2af8c2b` |
| Register RG-LIVE-001 | `0x0eedc794ff02053c1fcc323f689f3593ee5262975305c5d7fa2edc6c2bb6e885` |
| Lock evidence | `0x2fb7f7e40781c5f950d267e6dee28d9caa9ff4e5ed5186e8d0399e80de2b9d41` |
| Initial review | `0x8f3af937c0a5c86ce11dce2489fb1bd85f37ab234a3baeb417ff55f44e9db6e2` |
| Challenge | `0x68e215570f666a70088263eee7c3476a7121eda65bf95fce8899cf712eee0c1c` |
| Reassessment | `0xf2ccc337febe1d9387c902ace61fe059b79858305acec3c9aa6df8bdcdb87796` |
| Finalization | `0x958b186e141fea3b852e9d64b98b54edf7af29160fd8805ca76087ce0c604c54` |

The transaction JSON files record lifecycle and execution separately. `verification.json` compares deployed contract source byte-for-byte and recomputes finalized policy, evidence, result, state and receipt hashes. `RG-LIVE-001-record.json` and `RG-LIVE-001-receipts.json` are exported finalized reads. Normal full consensus was used, not leader-only execution.

The live trace consists of one isolated payment event delivered three times. The first charges 2500 cents and creates one fulfillment; two duplicate attempts are skipped with no counter changes. Both reviews returned IDEMPOTENT. The challenge alleged possible hidden repeat charges; reassessment used the locked counters and retained the supported verdict.

## Local verification

`npm test`: 31 Python contract/fixture tests and 5 JavaScript commitment/transaction tests. Network and VM boundaries are mocked locally. Adversarial cases cover repeated charges, conflicting payloads, discontinuous state, wrong first deltas, decrements, malformed/unknown model output, fabricated quotes, independent-validator disagreement, unavailable/substituted evidence, coverage, URL restrictions, hash/byte mismatches, booleans-as-integers, duplicate JSON keys, nonfinite JSON, authorization, immutability, receipt hashes, bounded challenges/retries and fixture reproducibility.

`npm run schema`: actual GenVM schema generation succeeded. This is not a claim of a separate GenVM linter pass.

`npm run build`: Vite production build succeeded.

## Browser verification

The public website was opened without sign-in, read RG-LIVE-001 through the real SDK, recomputed its commitments and receipt chain, rendered grounded findings and exported receipt JSON. The missing-injected-wallet state was tested. Live signing used the built-in Studio wallet; an installed MetaMask extension signing test was not performed. No published video or public social post is claimed.

## Data authority and limits

Documents are pinned to the exact GitHub commit `047ba8e3bf586003eec741200f8266ab23155d9c`. `fixtures/processor.py` reproduces the observed traces. These are isolated reproducible fixtures, not independently authenticated production event logs. See SECURITY.md for transport, producer trust, coverage, model and challenge limitations.
