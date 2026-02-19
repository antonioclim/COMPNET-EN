# 👥 Pair Programming Guide
## Computer Networks Projects — ASE Bucharest, CSIE

> **Purpose:** This guide helps you work effectively in pairs during project development.  
> **Applies to:** All projects P01-P20

---

## Why Pair Programming?

Working in pairs improves code quality, catches errors earlier and helps both partners learn from each other. Research shows that pair programming produces fewer bugs and better designs than solo work.

---

## Roles

| Role | Responsibilities | Focus |
|------|------------------|-------|
| **Driver** | Types code, controls keyboard and mouse | Implementation details, syntax |
| **Navigator** | Reviews code, thinks ahead, checks documentation | Big picture, logic, potential issues |

**Critical rule:** SWAP roles every 10-15 minutes. Set a timer!

---

## Session Structure

### Before You Start (5 minutes)

```
□ Both partners have access to the development environment
□ Decide who drives first
□ Review the task objectives together
□ Agree on the approach before typing any code
```

### During the Session

**Driver responsibilities:**
- Type code at a pace the Navigator can follow
- Explain your thinking out loud
- Ask for input on design decisions
- Stop when Navigator spots an issue

**Navigator responsibilities:**
- Watch for typos and syntax errors
- Think about edge cases
- Keep documentation open for reference
- Suggest improvements and alternatives
- Track the overall progress against objectives

### Swap Protocol

When the timer rings:
1. Driver commits current work (even if incomplete)
2. Partners physically swap positions
3. New Driver takes 30 seconds to review current state
4. Continue from where you left off

---

## Communication Phrases

### Navigator to Driver

| Situation | What to say |
|-----------|-------------|
| Spotted a bug | "I think there might be an issue on line X..." |
| Need clarification | "Could you explain what this section does?" |
| Have a suggestion | "What if we tried...?" |
| Found in docs | "The documentation says we should..." |
| Lost track | "Can you walk me through the logic again?" |

### Driver to Navigator

| Situation | What to say |
|-----------|-------------|
| Starting new section | "I'm going to implement the X part now" |
| Uncertain | "Does this approach look right to you?" |
| Stuck | "I'm not sure how to handle this case..." |
| Need research | "Can you look up how to do X?" |

---

## Conflict Resolution

Disagreements are normal and productive. Handle them professionally:

1. **State your position clearly** — "I think we should use approach A because..."
2. **Listen to the alternative** — Let your partner explain fully
3. **Try the simpler approach first** — When in doubt, start simple
4. **Time-box experiments** — "Let's try your way for 10 minutes"
5. **Escalate if stuck** — Ask the instructor if you cannot agree

---

## Remote Pair Programming

If working remotely:

| Tool | Purpose |
|------|---------|
| **VS Code Live Share** | Real-time code collaboration |
| **Discord/Teams** | Voice communication |
| **Screen share** | When Live Share is not available |

**Remote-specific rules:**
- Keep your microphone on (mute only for background noise)
- Verbalise more than you would in person
- Take more frequent breaks (every 25 minutes)
- Use screen annotations to point at code

---

## Pair Programming for Project Stages

### Stage E1 (Design)
- **Driver:** Creates diagrams and writes specifications
- **Navigator:** Checks requirements coverage, asks clarifying questions
- **Swap after:** Each major diagram or section

### Stage E2 (Prototype)
- **Driver:** Implements core functionality
- **Navigator:** Tests each function immediately, checks Docker config
- **Swap after:** Each completed function or module

### Stage E3 (Final)
- **Driver:** Writes tests and documentation
- **Navigator:** Reviews test coverage, checks edge cases
- **Swap after:** Each test file or documentation section

### Stage E4 (Presentation)
- **Both partners:** Practice the demo together
- **Take turns:** Presenting different sections
- **Quiz each other:** On potential questions

---

## Self-Assessment Checklist

After each session, both partners should honestly answer:

```
□ Did we swap roles regularly?
□ Did we communicate respectfully?
□ Did the Navigator stay engaged (not checking phone)?
□ Did the Driver explain their thinking?
□ Did we both understand all the code we wrote?
□ Did we handle disagreements professionally?
```

If you answered "No" to any question, discuss how to improve next time.

---

## Common Mistakes to Avoid

| Mistake | Why it's problematic | Solution |
|---------|---------------------|----------|
| Navigator takes over keyboard | Driver loses engagement | Use words, not grabbing |
| Driver ignores Navigator | Defeats the purpose | Stop and discuss |
| No role swapping | One person does all the work | Set a timer, enforce swaps |
| Silent Navigator | Missing the review benefit | Navigator must verbalise thoughts |
| Checking phone while navigating | Not actually reviewing | Put devices away |

---

## Contribution Tracking

For fair assessment, track contributions:

```markdown
## Pair Programming Log — [Date]

**Session duration:** X hours
**Partners:** [Name1], [Name2]

| Time | Driver | Task completed |
|------|--------|----------------|
| 14:00-14:15 | Name1 | Set up Docker environment |
| 14:15-14:30 | Name2 | Implemented socket server |
| ... | ... | ... |

**Challenges encountered:** [Brief description]
**Solutions found:** [Brief description]
```

Keep this log in your repository under `docs/pair_programming_log.md`.

---

*Pair Programming Guide v1.0 — Computer Networks, ASE Bucharest*
