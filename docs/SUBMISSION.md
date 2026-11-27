# ReplayGuard project submission

Project name: ReplayGuard

Suggested primary tag: Developer Tools (choose the closest available label).
Suggested topics: Infrastructure; Verification (choose matching options offered by the form).

## One-liner

Verify whether webhook retries and duplicate events cause unintended state changes using locked policies, deterministic checks and GenLayer validator consensus.

## Description

ReplayGuard helps software teams verify whether webhook retries and duplicate messages cause repeated charges, duplicate fulfillment or other unintended effects. Teams register immutable processing policies and commit-pinned event logs and execution reports. A GenLayer Intelligent Contract checks duplicate IDs, payload conflicts, state continuity and counter limits. Independent AI validators assess each attempt against business rules and permitted retry exceptions, grounding findings in exact evidence quotations. Verdicts are IDEMPOTENT, CONDITIONAL, VIOLATION or INCONCLUSIVE. The public application calls the contract, tracks transaction finalization, supports challenges and exports hash-linked receipts. A live Studionet audit covers registration, evidence locking, review, challenge, reassessment and finalization. Results cover the supplied trace and tracked counters, not unobserved production behavior.

## How-to

1. Inspect a live audit: Open the website, select Evidence & receipts, enter RG-LIVE-001 and click Load & verify. No wallet is needed to read.
2. Check the evidence: Inspect the verdict, per-attempt quotations and receipt timeline. Click Export receipts to download the verification record.
3. Create a verification: In Verification desk, connect a supported wallet to Studionet, choose a unique audit ID and an evidence pack or your own commit-pinned JSON. Register policy, lock evidence and request review, waiting for successful finalization after each write. Studio's built-in wallet can run the same methods inside Studio.
4. Review a dispute: After a review, submit one evidence-grounded challenge and request review again. The owner may finalize the audit.

## Expected verification outcome

RG-LIVE-001 displays IDEMPOTENT, two duplicate attempts, verified document hashes and three grounded PERMITTED findings. Its six hash-linked receipts show registration, evidence submission, review, challenge, reassessment and finalization. The browser verifies the receipt chain and commitments from finalized contract reads; Export receipts downloads the record.

Website: https://replayguard.mohamedansaf222.chatgpt.site
GitHub: https://github.com/haris4587/ReplayGuard
Contract: https://explorer-studio.genlayer.com/address/0xf6A55682019D16592B8639A32b8798ba3c07bd58
Logo PNG: https://replayguard.mohamedansaf222.chatgpt.site/logo.png
Video: leave blank; no YouTube or X video was published.

Evidence links: repository, docs/verification.json, docs/EVIDENCE.md and contract explorer.
