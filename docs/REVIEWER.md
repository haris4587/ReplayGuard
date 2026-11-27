# Reviewer walkthrough

Website: https://replayguard.mohamedansaf222.chatgpt.site

Contract explorer: https://explorer-studio.genlayer.com/address/0xf6A55682019D16592B8639A32b8798ba3c07bd58

## Inspect without a wallet

1. Open the public website and select **Evidence & receipts**.
2. Enter `RG-LIVE-001`, then **Load & verify**.
3. Expect `IDEMPOTENT`, two duplicate attempts, hash-verified event/execution documents, three grounded PERMITTED semantic findings, and the transition timeline.
4. The audit includes initial review, one challenge and independent reassessment. After owner finalization the timeline has six receipts: REGISTERED, SUBMITTED, REVIEWED, CHALLENGED, REVIEWED, FINALIZED.
5. Select **Export receipts** to download the record and complete chain. All displayed evidence comes from actual contract reads, not a static result substitute. The browser recomputes commitments before displaying a verified chain.

## Exercise writes

Use **Verification desk** with a fresh ID and a supported injected wallet on Studionet. Register the selected policy, lock evidence, request review and wait for each successful finalization. For an existing deployment's built-in wallet, use Studio as described in the README. Only the audit owner may submit evidence or finalize; review and the single challenge are permissionless.

Use the safe, repeated-charge or permitted-audit-entry pack. The expected deterministic results are covered by local adversarial tests. Only the `RG-LIVE-001` lifecycle is claimed as live verified in this release; fixtures are not presented as production traffic.

## Reproduce the checks

```sh
npm ci
npm test
npm run build
npm run schema
npm run verify -- RG-LIVE-001
```

Schema and live verification need access to the hosted network. Local tests mock retrieval and consensus; transaction records and the live verification report provide the separate hosted evidence. Wallet rejection, retained hashes after a polling timeout, failed execution and receipt tampering are covered by frontend logic tests. The browser test checked missing-wallet handling; an installed MetaMask extension signing test was not performed.
