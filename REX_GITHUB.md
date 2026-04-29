# Rex — GitHub Workflow for DS:R

Hey Rex, here's how we're handling GitHub for the project so everyone
stays in sync and nothing gets stepped on.

---

## Repo access

You should already have access. If not, ask Kyle for the repo URL and
an invite. Clone it locally if you haven't:

```bash
git clone <repo-url>
cd <repo-folder>
```

---

## Your branch

Work exclusively on your own branch:

```
rex/morpheous
```

Create it if it doesn't exist yet:

```bash
git checkout -b rex/morpheous
git push -u origin rex/morpheous
```

Never commit directly to `main` or `code/builds`. Those are Kyle's to merge.

---

## What to commit

**Commit the actual modified `.c` and `.h` files directly.** Don't wrap
changes in Python patch scripts — git already tracks exactly what changed
line by line, which makes review much easier.

The files you're most likely touching for Morpheous:

- `recovered/devils/src/const.c` — class table, skill groups
- `recovered/devils/src/act_combat.c` — new skill functions (Code is building this file; coordinate before touching)
- `recovered/devils/src/interp.c` — command table entries
- `recovered/devils/src/skills.c` — any utility skills

If you have Python scripts that generate or apply changes, keep them in a
`patches/` folder on your branch — that's fine for reference or server
hotpatching. But the actual source changes should be committed as real
file edits so we can diff them cleanly.

---

## Commit cadence

Push whenever you finish a logical chunk of work — doesn't have to be
a complete feature. Small, focused commits are easier to review than one
giant drop.

```bash
git add recovered/devils/src/const.c recovered/devils/src/act_combat.c
git commit -m "rex: Morpheous class skeleton — const.c entries + interp wiring"
git push origin rex/morpheous
```

Good commit message format: `rex: <what you did in one line>`

---

## Watch for conflicts

Two files are high-collision risk because both you and Code will touch them:

- `const.c` — let Kyle know before you edit the class table or skill groups
- `act_combat.c` — Code is actively building this file; coordinate on which
  functions you're adding so you don't overwrite each other

When in doubt, pull the latest `code/builds` branch before you start a
session and check if those files changed:

```bash
git fetch origin
git diff origin/code/builds -- recovered/devils/src/const.c
```

---

## Getting your work reviewed

When Morpheous is ready to integrate, open a Pull Request on GitHub:

- **From:** `rex/morpheous`
- **Into:** `code/builds`

Kyle will review the diff and merge when it's confirmed clean. You don't
need to do anything special — just open the PR and Kyle takes it from there.

---

## Summary

1. Work on `rex/morpheous` only
2. Commit real `.c`/`.h` file edits, not just patch scripts
3. Push regularly — small commits are fine
4. Heads up to Kyle before touching `const.c` or `act_combat.c`
5. Open a PR when Morpheous is ready to merge

Questions — ask Kyle.
