# AI Workflow Principles
**Author:** Kyle Webb
**Started:** 2026-04-29
**Purpose:** Personal reference for AI-assisted project work. Lessons learned
across sessions — what works, what wastes time, how to think about the tools.
Intended to carry forward to future projects beyond DS:R.

---

## The Core Principle: Cheap vs. Expensive Computation

**LLMs are expensive reasoning engines. Computers are cheap counting machines.
Never use the expensive thing to do the cheap thing's job.**

Everything a script can do deterministically — searching, counting, sorting,
pattern matching, format conversion, status aggregation — should be done by
a script. The LLM's context window (its working memory) is finite and costly.
Fill it with judgment problems, not file scanning.

```
Script/compute owns:    indexing, scanning, aggregating, status tracking,
                        format conversion, repetitive pattern matching,
                        file search, data extraction

LLM owns:              judgment calls, design decisions, spec writing,
                        interpreting ambiguous information, creative work,
                        coordination between humans, reasoning about tradeoffs
```

---

## Token Economy

### Context window is working memory — treat it like RAM
Every file you ask an LLM to read costs tokens. Every large document loaded
at session start costs tokens before a single useful thought is had.
Design your workflow so the LLM receives **pre-digested summaries**, not raw
source material, wherever possible.

### The briefing pattern
Instead of having the LLM re-read 5 large docs every session, write a script
that generates a one-page session briefing:
- Current build version
- Open blockers (count + titles only)
- Pending decisions (list only)
- Next recommended action

The LLM reads 200 tokens instead of 5,000. Saves reasoning budget for
actual reasoning.

### Aggregate first, reason second
When working with bulk data (logs, player files, source files, area files):
1. Script extracts and aggregates the data
2. Script outputs a clean summary
3. LLM reasons about the summary

This is what made the player file analysis session work well — 155 player
files became a clean stats table before the LLM ever saw it. The LLM didn't
read player files; it read a spreadsheet and made judgments.

### Pre-built indexes > repeated searches
Any time you find yourself asking the LLM to search for the same things
across sessions (function locations, vnum ranges, skill table entries,
command table entries), that's a signal to build an index once and hand
it to the LLM as a reference. A JSON index of all `do_*` functions and
their file locations is a 5-minute script that saves tokens every session
forever.

---

## Multi-Agent Coordination

### Handoff docs are the protocol
When multiple agents (or humans) are working in parallel on the same project,
shared documents ARE the communication protocol. Keep them tight:
- One source of truth per topic
- Decisions recorded with rationale (not just outcomes)
- Open questions clearly flagged so the right person answers them

Ambiguity in handoff docs multiplies into wasted work across all agents.

### Separation of concerns between agents
In DS:R this looks like:
- **Code (Claude Code):** source implementation, disasm interpretation,
  build/deploy. Owns the C files.
- **Cowork (this agent):** design decisions, spec writing, documentation,
  cross-session memory. Owns the .md files.
- **Rex:** parallel class work (Morpheous). Owns his branch.

Each agent should be asking: "Is this my job, or is this someone else's
job that I'm doing inefficiently?" Code shouldn't be making design calls;
Cowork shouldn't be writing C.

### Version control is not optional for multi-agent work
Without Git, agents drift. Code writes a file, the other agent can't see
it, both proceed on stale assumptions. Push after every meaningful unit of
work — even if it's just a snapshot branch. Pull before every session that
touches shared files.

---

## Context Management

### Summarization checkpoints
Long-running projects accumulate context faster than any LLM can hold.
Build natural summarization checkpoints — end-of-session summaries, handoff
docs, decision logs. The goal is that a fresh session starting from the
summary should be nearly as effective as one with full history.

In practice: DECISIONS.md, CODE_HANDOFF.md, BUGS.md, and IDEAS.md together
serve as the project's "compressed context." They should always be current
enough that a new session reading only those files can pick up where the
last left off.

### Don't re-derive what you've already decided
Every time a design question gets re-litigated from scratch, you're paying
for reasoning you already did. Log decisions with rationale immediately.
DECISIONS.md exists for this reason — when a question comes up again, the
answer is there and the LLM doesn't need to re-reason it from first
principles.

### Prune before it grows
Documents like CODE_HANDOFF.md can become bloated as history accumulates.
Periodically archive resolved sections so the active document stays tight.
A 37,000-token document that's 70% resolved history is waste every time
it gets loaded.

---

## What to Script, What to Ask

### Script it if:
- You'll need the answer again in a future session
- The answer is deterministic (same input → same output every time)
- It involves reading more than a few files
- It's a count, search, sort, filter, or format operation
- A human (or LLM) would make no judgment in producing it

### Ask the LLM if:
- The answer requires weighing tradeoffs
- Multiple valid answers exist and context determines which is right
- It involves interpreting ambiguous or incomplete information
- It's a design, naming, or framing decision
- It requires synthesizing information from multiple domains

### The "should this be a script?" test
Ask: "If I ran this exact task 10 times with slightly different inputs,
would the answer always follow the same pattern?" If yes — script it.
The LLM is expensive pattern-matching at scale. Scripts are cheap
pattern-matching at scale. Use the right tool.

---

## Prompting Patterns That Work

### Give context up front, not at the end
LLMs read prompts in order. Relevant context buried at the end of a long
prompt is less useful than the same context at the beginning. Lead with
what the LLM needs to know, then ask the question.

### Constrain the output format
"List the open blockers" gets prose. "List the open blockers as a numbered
list with one sentence each" gets what you can scan in 10 seconds. Be
specific about format when you know what you need.

### Positive and negative examples
When asking for something where "almost right" isn't good enough (code,
specs, decisions), show an example of what you want AND an example of
what you don't want. Removes ambiguity faster than describing it in prose.

### Say what matters, not what to do
"I need to explain this to my PM who doesn't know C" is more useful than
"make this simpler." The LLM can infer what "simpler" means for a PM
better than it can infer it from the word "simpler" alone.

### Step-by-step for complex reasoning
For multi-step problems, explicitly ask the LLM to reason step by step
before giving an answer. This surfaces the reasoning so you can catch
errors in intermediate steps, not just the conclusion.

---

## Lessons from DS:R Specifically

**The player file analysis** is the model session. 155 files, Python does
the aggregation, LLM sees clean tables and makes design judgments. Zero
wasted tokens on file reading.

**CODE_HANDOFF.md growing too large** is the anti-pattern. At 37k tokens
it's becoming expensive to load. Should be pruned to open items only;
resolved history moves to an archive. Generate a "current state" view
with a script rather than loading the full document.

**Grep loops in session** are a smell. When 3+ session turns involve
searching source files for related things, that's a pre-built source
index that should have existed. One script run at project start, JSON
output, referenced forever.

**Decision logging pays compound interest.** Every decision logged in
DECISIONS.md is a future token saved — the question never gets re-reasoned.
Logging is never the bottleneck; not logging always is.

---

## Tools & Their Roles (DS:R Context)

| Tool | Role | Don't use it for |
|------|------|-----------------|
| Python scripts | Bulk file ops, indexing, aggregation, status tracking | Design decisions, spec writing |
| Cowork (Claude) | Design, specs, docs, cross-session memory, coordination | Searching source files repeatedly, reading large files that could be pre-summarized |
| Code (Claude Code) | C implementation, disasm interpretation, build/deploy | Making design calls, writing documentation |
| Git/GitHub | Version control, backup, multi-contributor sync | Anything synchronous — async by nature |
| DECISIONS.md | Locking in design choices with rationale | Day-to-day task tracking |
| CODE_HANDOFF.md | Code↔Cowork protocol | Permanent history — archive resolved sections regularly |
| BUGS.md / IDEAS.md | Tracking open work | Resolved items — move them to Done, don't leave them in Open |
