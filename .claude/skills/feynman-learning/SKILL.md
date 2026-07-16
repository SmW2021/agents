---
name: feynman-learning
description: "Feynman Learning Method — 4 prompts, 20 minutes, knowledge that actually sticks. Use after reading a book, finishing a course, preparing for an interview, or learning any new concept. Triggers: feynman, learn, remember, understand, study, explain."
---

# Feynman Learning Method

4 prompts. Twenty minutes. Knowledge that actually sticks.

## Why This Works

- **Forgetting Curve** (Ebbinghaus 1885): lose 42% in 20 min, 56% in 1 hour, 80% in 31 days
- **Protege Effect** (Koh 2018): teaching others scores 10–20% higher than just studying
- **Retrieval Practice** (Karpicke 2011, *Science*): pulling info OUT beats putting more IN
- **Desirable Difficulty** (Bjork 1994): if it feels easy, it's shallow; if it feels hard, it's deep

Reading is proof of attention. Explaining is proof of understanding. These are not the same thing.

## Workflow

When the user names a topic or provides learning material, guide them through these 4 steps:

### Step 1: Concept Map (3 min)

Identify the topic, then output:

```
📌 Topic: [user's topic]

Here are the 5 most important ideas you need to fully understand:

1. **[Idea Name]**
   - One-sentence definition (plain English, no jargon)
   - Why it matters in the real world
   - The one question you should be able to answer if you truly understand it

2. ... (5 total)
```

**Rule**: Pick only the 5 load-bearing ideas. Most topics have 50 facts. Only 5 matter.

### Step 2: The 12-Year-Old Test (7 min)

For each idea, write a model answer a 12-year-old could understand, then ask the user to write their own version:

```
📖 Idea 1: [Name]

MODEL ANSWER (12-year-old version):
[Plain explanation with no jargon]
Everyday example: [cooking, driving, sports, weather — pick one]

✏️ Your turn:
Explain this idea in your own words like you're teaching a 12-year-old.
No jargon. No shortcuts. Type it out and send it to me.
```

**Rules**:
- Wait for the user to write their own version before continuing
- The moment they type their version is the moment learning actually happens
- If they write all 5 at once, that's fine — proceed to Step 3

### Step 3: The Gap Finder (5 min)

Read the user's explanations. Evaluate each one honestly:

```
📋 Your Report Card:

Idea 1: [Name]
Rating: STRONG / WEAK / WRONG
[Be specific about what's confused. Do not be polite.]
Corrected version (different analogy): [new simple explanation]
Follow-up question: [1 question that would prove you now understand it]

... (every idea gets rated)

🎯 Restudy first: [the weakest idea] — this is your biggest gap. Fix this one before the others.
```

**Rules**:
- Strict but kind. Never grade on effort.
- Use a **different** analogy than Step 2 for corrections
- End with exactly 1 highest-leverage gap to fix

### Step 4: The Analogy Lock (5 min)

Build 2 analogy anchors per idea. Show where each analogy works AND where it breaks:

```
🔗 Idea 1: [Name] — Analogy Lock

ANALOGY 1 (everyday life: cooking, driving, sports, weather, family, money):
  ✅ Where it works: [...]
  ⚠️ Where it breaks down: [...] (all analogies break somewhere)

ANALOGY 2 (adult experience: working a job, using a phone, managing money, managing time):
  ✅ Where it works: [...]
  ⚠️ Where it breaks down: [...]

📝 One-sentence summary (read this tomorrow morning to recall everything):
[One clean sentence]
```

Then output the final takeaway:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 5 SENTENCES TO KEEP — Read these tomorrow morning and it all comes back:

1. [Idea 1]: [one sentence]
2. [Idea 2]: [one sentence]
3. [Idea 3]: [one sentence]
4. [Idea 4]: [one sentence]
5. [Idea 5]: [one sentence]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## How to Use

Type `/feynman-learning` or say "use the Feynman method on [topic]" to start.

- If the user provides specific material (article, notes, book excerpt), run the 4 steps directly on that material.
- If only a topic name is given, briefly outline the core framework first, then run the 4 steps.

## Guidelines

- **Language**: The prompts in this SKILL.md stay in English. When running, match the language the user is speaking in the terminal — if they write in Chinese, respond in Chinese; if English, respond in English.
- Do not skip Step 2's wait for the user's own writing — this is the entire point
- Step 3 must be honest — no "participation trophies"
- The "where it breaks" part of each analogy is as important as "where it works"
- If the user wants to switch topics mid-way, restart freely
