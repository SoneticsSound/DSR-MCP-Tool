# Stance System — DS:R Help File Draft

*Source status: weapon flag mappings confirmed from fight.c / bit.h / const.c.
do_stance mana costs and stat modifiers pending disasm port (1479b).*

---

## HELP STANCE

```
Syntax:  stance <name>
         stance none

Monks, Shaolin, and Sensei may adopt a fighting stance that channels
their training into every blow they land. Each stance imparts a
different weapon property to your attacks for as long as it is held.

Only one stance may be active at a time. Entering combat while
maintaining a stance costs mana each round. Use 'stance none' to
return to normal posture.

STANCES
-------
Dragon    Your strikes crackle with electric force, adding a jolt of
          lightning damage to each blow.

Crane     The precision of the crane finds gaps in any defence. Your
          attacks carry a chance to strike a killing blow outright
          (vorpal).

Scorpion  You coat every strike with a venom drawn from perfect
          stillness. Victims may be poisoned on each hit.

Leopard   The cold patience of the leopard runs through your fists.
          Attacks carry a frost bite that chills and slows.

Phoenix   Your strikes burn with inner fire, adding flame damage to
          each blow landed.

Monkey    Unpredictable and relentless, the monkey stance spreads
          rot and decay through each hit.

Rabbit    The rabbit is an ill omen. Strikes may curse the victim,
          souring their luck in combat.

Leech     The most draining stance. Each hit siphons vitality from
          the victim (vampiric) while also drawing on their essence
          (osmosis). Costly in mana but self-sustaining in a long
          fight.

Skunk     A jinx runs through every strike. Victims find their
          fortunes turning against them.

See also: MONK, SHAOLIN, SENSEI, SKILLS
```

---

## Design Notes (internal — not for in-game help)

- **Rabbit** is NOT a dodge stance — it applies WEAPON_ACCURSED. Kyle's
  dodge/extra-attack instinct was a good design idea but not the original.
  Consider a separate "evasion stance" idea if that niche needs filling.
- **Leech** is the only dual-flag stance (OSMOSIS + VAMPIRIC). Likely the
  most mana-intensive. Worth flagging for Code when tuning mana-per-round cost.
- **Skunk** applies WEAPON_JINX, not plague. Monkey covers the disease/rot angle.
- Mana costs per round unknown until `do_stance` (1479b) is disasm-ported.
  Placeholder for help file: "Costs mana each round."
- Stat bonuses (AC, hitroll, etc.) from stances are also unknown — the fight.c
  hooks only show the weapon flag injection, not any passive modifiers.
