# 0006-vault-reference-integrity — Understanding Shifts

## Delta-1: entry-churn-not-vault-absence

The soft-reference contract's value is resilience to vault **evolution** — a consumer's referenced entry being renamed, retired, or re-homed while the vault and the consumer both keep working — **not** resilience to the vault being **absent**. A consumer keeps a self-sufficient inline floor because it is a runnable procedure in its own right (the vault entry is the *theory* behind it, a different kind of thing); when its one referenced entry moves, only the optional depth degrades.

Kills the prior framing that the inline floor's worth is that it "works with the vault absent." That scenario does not occur in practice: the tooling is an empty wrapper with no value absent the vault, and the installer deploys these consumers together with the recorded vault location — there is no real deployment where a consumer is present but the vault is gone. The swappable-vault case (an install pointed at a vault lacking the entry) still reduces to "the *specific referenced entry* is absent" — the same entry-level condition, never "the whole vault is gone." The Requirements Guarantee already grounded the contract correctly on "every vault rename break its consumers / cost of evolving the vault"; the weak "absent" wording drifted into the Outcome, Spec#C-2's first clause, and the architecture rule. The check (`check-refs`) and its code are unaffected — they already assert the entry-level condition; only the justifying prose over-claimed.

Scope-of-impact: Spec#C-2-soft-reference-integrity, Design#D-4-document-contract-in-architecture, Tasks#T:A1
