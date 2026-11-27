# Security and trust boundaries

ReplayGuard is a bounded documentary assessment, not a global exactly-once guarantee or a production control plane.

- Policies fix repository, exact commit, expected attempt count, evidence digests, business rules and retry counter limits. Submitted UTF-8 documents must match SHA-256 and byte counts and cannot be replaced.
- Only HTTPS raw.githubusercontent.com URLs under the locked repository and exact 40-character commit are accepted. Paths reject traversal, encoding, queries and fragments. Roles have 18,000-byte accepted-body limits. Retrieval may download a larger response before rejecting it; the host network service controls transport/redirect behavior. No claim of streaming network-size enforcement is made.
- Documents are producer-supplied. A committed document can be incomplete or dishonest. An application-specific trusted producer/export/signature adapter is needed to authenticate production observations. ReplayGuard does not implement that adapter.
- Processing is one contiguous, ordered trace. Event IDs form the idempotency scope of an audit. Attempt IDs are unique; identifiers reused with conflicting payload hashes violate the policy. Counters are integers between zero and 10^15. No floats, booleans-as-integers, nonfinite JSON or duplicate JSON keys are accepted by the contract.
- State continuity and first-processing exact deltas are deterministic. Other attempts may only use bounded nonnegative retry effects. Validators cannot override a deterministic violation. AI conclusions are grounded by exact quotations and independently checked decision vectors, but quotation presence alone does not prove an interpretation correct.
- Prompts treat evidence and challenge text as untrusted data, forbid executing embedded instructions, and return UNKNOWN after two invalid model-response attempts. Prompt-injection resistance is a mitigation, not a guarantee.
- GenLayer consensus or VM/provider failures can fail a transaction. Only a successfully committed review updates its budget. Callers must inspect both lifecycle status and execution result. Accepted/finalized status alone is insufficient.
- Owner submission and finalization checks isolate audits. Review and a single challenge are permissionless; the optional challenge can therefore be used first by another account. There is no escrow, timed challenge window or economic anti-spam guarantee.
- The frontend retains an outstanding transaction hash before polling. A timeout is not an invitation to resubmit. Resume the known hash. Browser storage is not a substitute for chain records and should not contain secrets.
- Never submit private payloads, keys, personal customer data or credentials. On-chain policy and evidence text are public.

Report a reproducible issue privately to the repository maintainer through GitHub's available private reporting channel; if unavailable, open an issue without sensitive details.
