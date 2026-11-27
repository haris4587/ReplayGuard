# Deployment

Stable GenLayer Studionet, chain ID 61999, RPC `https://studio.genlayer.com/api`.

Contract: `0xf6A55682019D16592B8639A32b8798ba3c07bd58`.

Explorer: https://explorer-studio.genlayer.com/address/0xf6A55682019D16592B8639A32b8798ba3c07bd58

Deployment transaction: `0x45fbd8469a287eaade8e978bf65c68595fd3c2b78b71da890ecb955eb2af8c2b`.

Deployed through Studio's built-in account `0xcD72fA5B6A496d84B4A10bCFF31D3B7c12346a9e`, in normal full-consensus mode. No wallet private key was exported. The deployment finalized with `FINISHED_WITH_RETURN`.

To redeploy: import `contracts/replay_guard.py` into Studio, select Studionet and normal full consensus, then deploy with no constructor arguments. Point `public/deployment.json` at the returned finalized address. Fetch and compare deployed source before claiming a matching release.

`npm run schema` requests the real hosted GenVM schema. `npm run verify -- RG-LIVE-001` compares deployed source and validates all finalized audit commitments and receipts. `scripts/inspect-tx.mjs HASH...` saves transaction evidence and reports execution status.

The website is a static Vite application. Its tracked `.openai/hosting.json` selects `dist`. Run `npm run build` before publication; publish the exact built source revision. No backend model or wallet secrets are needed. Browser wallet calls estimate fees through the matching SDK, submit the estimated distribution/deposit, and track finalization. Fee estimation is used per call for the current developer workflow; measure and maintain fee profiles before larger-scale use.

For an alternative static host, deploy `dist` with HTTPS. The repository contains no host authentication tokens. An example Netlify configuration is included; `.netlify` is ignored.
