# Translation Check

Reviews reusable translation segments for meaning fidelity and exact coverage of a bounded terminology list.

## Why GenLayer

Validators semantically compare source and translation and return both a quality enum and an ordered terminology bitmask.

## Reusable workflow

A client adds source segments and required terms, locks the document, the translator submits each segment, and consensus accepts it or permits one revision. Constructor parameters create a new independent instance, so the code is reusable; state is not shared between deployments.

The contract is deliberately non-custodial. It records a decision, entitlement, score, or approval signal and never transfers GEN.

## Evidence boundary

Only the source segment, required terms, submitted translation, language labels, and fixed standard are judged. The contract performs no dictionary or web lookup.

## Verify locally

```powershell
genvm-lint check contracts/translation_check.py
genvm-lint typecheck contracts/translation_check.py
pytest tests/direct -q
python tests/run_glsim.py --validators 5
```

With GLSim running in another terminal:

```powershell
gltest tests/integration/test_glsim_consensus.py --network localnet -q
```

The live smoke test requires fresh test-only keys in `GENLAYER_PRIVATE_KEY`, `GENLAYER_SECONDARY_PRIVATE_KEY`. Never commit a `.env` file or use a production wallet.

```powershell
gltest tests/integration/test_studionet_smoke.py --network studionet -s -q --default-wait-interval=6000 --default-wait-retries=240
```

Use the documented 6-second StudioNet polling interval to stay comfortably below public endpoint limits.

See `ARCHITECTURE.md`, `SOURCE_POLICY.md`, `SECURITY.md`, `AUDIT.md`, and `deployments/studionet.json` for the review boundary and exact public evidence.
