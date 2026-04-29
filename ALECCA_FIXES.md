# Alecca Fix Log

Tracks bugs originally reported by Alecca (Kim) in 2003 and gameplay issues
relevant to showing her a working build. Updated as fixes land.

---

## ✅ Fixed

### BUG-019 — Cursed player following someone can still recall
- **Fixed:** 0.4.41 (2026-04-29)
- **Original report:** "when following someone, if you are cursed you can still recall"
- **What changed:** Curse check now gates recall even when the player is in a follow chain.

---

## 🔴 Open — originally reported by Alecca

### BUG-018 — Chill touch on weapon causes invincible AC after combat
- **Status:** open
- **Original report:** "BUG: with chill touch on weaps you get INVINCIBLE ac after a fight" (May 2003)
- **What's wrong:** AC modifier from chill touch weapon proc isn't cleaned up after combat, leaving extreme negative AC.

### BUG-021 — Paradox events not ticking
- **Status:** open (Code investigating)
- **Why it matters for Alecca:** Paradox is core to the Grace/Souls economy she helped design. Until it ticks, the escalation mechanic (Grace bonuses suspended during Paradox) can't be tested.

---

## 🟡 Related — not Alecca-reported but affects her experience

### BUG-020 — Monk/Shaolin/Sensei not selectable
- **Status:** fix-staged (0.4.41) — needs Kyle QA
- **Why it matters:** Class selection was silently broken; affects any new character creation session.

### BUG-016 — Ticks not firing (affect durations, travel cooldown)
- **Status:** fix-staged — needs Kyle QA
- **Why it matters:** Spells expiring correctly is table stakes for any playtest session.

---

## When to show Alecca

Kyle's milestone (from session notes 2026-04-29): show her a working build
once known bugs from the recovered file index are patched through. Priority:
- BUG-018 (chill touch AC) fixed
- BUG-021 (Paradox ticking) fixed
- Staged QA items above passing
