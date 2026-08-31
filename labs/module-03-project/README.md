# Module 3 project — three agents write an investment memo

This is the Hour 3 lab from Module 3, packaged so you can run it at home.
It is free. It needs no API key and no installs.

Three agents write one investment memo. Each agent has one job, and each one
hands its output to the next. The hand-offs are the lesson.

1. The Research Agent collects the company's facts.
2. The Analysis Agent computes the ratios and writes what they mean.
3. The Writing Agent turns both into a one-page memo.

You are the Reviewer. Check every number in the memo against the source
before you trust it.

## Route 1 — run the Python pipeline

You need Python 3. Nothing else.

```
python3 memo_pipeline.py
```

The script reads `company_facts.csv` and writes three files into `output/`:
`1_research_notes.md`, `2_analysis.md`, `3_investment_memo.md`. Read them in
order. That order is the hand-off.

The CSV ships with sample numbers for a made-up company. Replace them with a
real NSE company's numbers from its published results or screener.in, then
run the script again. Keep the same columns.

In class we run the same pipeline in Claude Code, where each agent is a real
AI agent instead of a Python function. The shape is identical.

## Route 2 — run the three agents in any free AI chat

Open `agent_prompts.md`. It carries three prompts. Paste Prompt 1 into any
free AI chat with your company's numbers, copy its answer into Prompt 2, and
copy that answer into Prompt 3. You have just run a sequential three-agent
pipeline by hand.

## What to submit

Bring the memo and your reviewer notes to the next session. Score three
things: every number carries a source, the view follows from the numbers,
and you would send it upstairs.

## Disclaimer

This project is a classroom exercise. Its output is not investment advice
and not research under SEBI regulations.
