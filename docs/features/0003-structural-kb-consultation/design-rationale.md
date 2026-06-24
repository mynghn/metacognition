# 0003-structural-kb-consultation — Design Rationale

## D-1: kb-consultation-agents-block

The framework already has a provider-neutral place to put standing behavior: the shared `AGENTS.md` spans that `install` upserts surgically. Reusing that surface keeps ownership in Metacognition, works for both supported runtimes, and avoids inventing a scheduler or background process.

Runtime hooks were rejected as the spine. They may be useful later for a runtime-specific enhancement, but a hook-first design would either be Claude-only / Codex-specific or would require two separate mechanisms that could drift. Description tuning was also rejected as the spine: the reported failure is precisely that description matching is framing-gated, and the `0001` worktree has measured evidence that trigger-first ordering can hurt scoped-skill activation.

Invalidation: if the marker is present and the installed block still gets ignored in realistic runs, the next candidate should be a runtime-specific enforcement layer, but that would be a separate design with an explicit provider gap.

## D-2: checkpoint-marker-protocol

The marker turns "notice that this authoring step is also a KB moment" into a procedure step. That is the narrow structural move the failure report asked for. It keeps nonmatching work quiet because nothing fires unless a supported workflow declares a checkpoint, and it keeps consumer workflows thin because they declare intent IDs rather than copying Metacognition policy.

A broad every-turn checklist was rejected. `0001` shows that a standing checkpoint can help, but this feature's precision requirement is sharper: ordinary coding and local investigation should not see KB surfacing just because the global prompt says to consider skills. A marker gives the workflow author a deterministic place to say "this is the moment" without making the agent rediscover it.

Invalidation: if early adopters overuse markers until they become noise, the registry should split intents more narrowly or require workflow-local criteria next to the marker.

## D-4: kb-consultation-eval-gate

The project exists because plausible activation changes have failed. The `0001` worktree is the useful prior: it made the miss countable, established a baseline, and found that a standing checkpoint lifted one scoped skill while description reordering hurt. This feature should reuse that evaluation stance, not just its conclusion.

The new scorer is specialized because the observable is different. `0001` asks whether a scoped skill self-activated on a no-cue moment. This feature asks whether a declared KB authoring checkpoint produced the expected consultation or a reviewable skip, and whether ordinary nonmatching work stayed silent. Those are close enough to share transcript-reading ideas, but different enough to deserve separate labels and rates.

Invalidation: if transcript evidence cannot reliably show selected KB entries across both runtimes, the marker format becomes the canonical observation and the checker scores the marker rather than attempting to infer entry reads from tool traces.
