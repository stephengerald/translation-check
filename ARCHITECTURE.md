# Architecture

## State machine

A client adds source segments and required terms, locks the document, the translator submits each segment, and consensus accepts it or permits one revision.

The relevant roles are translation client and translator. Write methods enforce role, phase, uniqueness, and bounded-storage rules before any state transition.

## Consensus boundary

Validators semantically compare source and translation and return both a quality enum and an ordered terminology bitmask. The leader returns a small JSON schema; validators independently rerun the same decision function and accept only exact enum or bitmask values. Malformed model output raises a tagged model error and writes no decision.

## Deterministic boundary

Enrollment, authorization, commitments, counters, phase changes, caps, masks, and any score or credit arithmetic are deterministic contract logic. Only semantic interpretation of the stored evidence occurs inside `run_nondet_unsafe`.

## Off-chain boundary

Wallet custody, identity verification, indexing, notifications, private file storage, source authentication, money movement, legal process, and user-interface behavior are outside this repository. This is not certified legal, medical, or safety-critical translation review. Dialect choice, specialized terminology, and cultural suitability still need qualified human review.
