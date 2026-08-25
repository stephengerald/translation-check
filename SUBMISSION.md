# Submission: Translation Check

Project name: Translation Check

Repository: https://github.com/stephengerald/translation-check

StudioNet contract: https://explorer-studio.genlayer.com/address/0x9d83b747102ea11Db9B76028c883a3b614AFcf69

Deployment transaction: https://explorer-studio.genlayer.com/tx/0xb660daeafaacc4e74478480834caa082e4b1129879dd858b10cd2653265829c8

Intelligent transaction: https://explorer-studio.genlayer.com/tx/0x935f0972215a695a0d257366bc0e76f659874db0360182fb8e31294328b74f24

Summary: Reviews reusable translation segments for meaning fidelity and exact coverage of a bounded terminology list.

Why it is GenLayer-native: Validators semantically compare source and translation and return both a quality enum and an ordered terminology bitmask.

Evidence/source model: Only the source segment, required terms, submitted translation, language labels, and fixed standard are judged. The contract performs no dictionary or web lookup.

Declared scope: Reusable, non-custodial prototype. This is not certified legal, medical, or safety-critical translation review. Dialect choice, specialized terminology, and cultural suitability still need qualified human review.

Review evidence: `AUDIT.md`, `SECURITY.md`, `SOURCE_POLICY.md`, and `deployments/studionet.json` bind the reviewed source hash to the public live result.
