# 0002-ship-practice-skills — Install a working metacognition system, not just a knowledge library

## Problem

Installing the metacognition framework hands an adopter the knowledge but not the means to use it. The framework already ships and surfaces its knowledge siblings — the codified practice an agent consults — but the skills that put that practice *into action* mid-session live outside the framework, in the author's personal setup. A second party who installs metacognition therefore gets an inert knowledge library, not a working system: the agent can look practice up, yet the moves that actually wield it — carrying a session across a context boundary, focusing a compaction — never travel with the install, and nothing brings them up at the moment they are needed.

Two parties feel it. The adopter inherits a last-mile gap that strands all the effort poured into the knowledge. And the maintainer is forced to keep the most valuable, in-action pieces personal instead of shippable — so the framework can never deliver the very thing it is about: metacognition in practice.

## Outcome

Installing the framework delivers a working metacognition system. The in-action practice skills travel with the knowledge, generalized so they work for anyone, and they come up at the moments that call for them. The framework owns these pieces end to end — the same way it already owns its knowledge siblings — while leaving the adopter's own material untouched. Scope is the practice skills that exist today plus the path that lets future ones ship the same way; it does not reach into how reliably a skill fires, which is a separate, already-owned concern.

User stories:

- **Practice ships with the knowledge** — installing metacognition brings the in-action skills along with the codified practice, not the knowledge alone: carrying a session across a context boundary (`/handoff`) and focusing a compaction (`/compact-focus`).
- **Works for any adopter** — the shipped skills carry no personal paths and no personal phrasing; someone who is not the author gets working skills with nothing to patch by hand.
- **Surfaces at its moment** — each shipped skill's activation travels with it and is maintained by the framework, so the skill comes up when its moment arrives rather than waiting to be named or hand-assembled by the adopter.

The signal that confirms it: a clean install performed by someone other than the author yields the practice skills present, working, and coming up at their moments — with no personal paths or phrasing left to patch. The install stops being a knowledge library the adopter must finish wiring themselves and becomes a working system out of the box.

## Guarantee

- **The framework owns what uses the knowledge, never the user's philosophy** — the boundary the framework holds continuously: it owns the pieces that *apply* its knowledge (the knowledge siblings, and the practice skills that wield them together with their activation), and it never absorbs the adopter's general operating frame — the personal working philosophy that merely *draws on* metacognition. The deciding test is whether a piece *uses the knowledge base* (owned by the framework) or is *general working philosophy* (left to the user). Spec owns the observable form of this split.

## Non-goals

- **The self-activation behavior.** Whether a skill fires on its own cue without being named — and proving that lift over a baseline — is a separate problem already owned by the self-initiated-skill-activation feature. This feature ships the skills and their activation; it does not re-solve or measure how reliably they fire.
- **The adopter's general operating frame.** The personal working philosophy that draws on metacognition but is not itself a use of the knowledge base stays with the user; the framework neither absorbs nor ships it.
- **Framework maintenance / doctor tooling.** Auditing or updating an existing install is a separate category that already exists as its own framework capability; shipping the practice skills does not extend or modify it.
