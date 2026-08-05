# Personal AI Playbook

## When I reach for AI first

I use AI first when the task is structured and reviewable: drafting user stories, comparing small architecture options, writing strict prompts, generating test cases from acceptance criteria, reviewing a diff, checking a Dockerfile, or asking for a security review of specific files. AI helped most when I gave it exact files, exact constraints, and a clear output format.

## When I do not reach for AI first

I slow down before using AI when the task involves private data, secrets, customer information, unclear requirements, or decisions that would change the project scope. I also do not ask AI to rewrite the whole project when a small targeted fix is needed. For learning tasks, I need to understand the result before accepting it.

## My non-negotiables

I never paste real `.env` values, tokens, credentials, production logs, or personal/customer data into AI tools. I do not submit generated code that I cannot explain. I do not hide failing tests, skip pytest, or use CI shortcuts such as `continue-on-error` or `|| true`. AI output is always a draft until I inspect it, run it, test it, and record important decisions.

## My review rules

For code, I read the diff before running it, check that it changes only the intended files, and confirm it does not add out-of-scope features. For debugging, I use real error messages and ask for targeted fixes, not vague “fix everything” prompts. For review findings, I grade them as Useful, Noise, or Wrong. For security findings, I grade them as Valid, False Positive, or Noise and decide whether to fix, document, or reject.

## What I am still figuring out

I am still figuring out how much AI review evidence is enough for a team without making documentation too heavy. I also want better habits for deciding when to use a terminal-based AI tool versus a chat-based tool. The main rule I will keep is that AI can speed up drafting and checking, but I remain responsible for the final code and explanation.

## Decision Card

| Situation | My rule |
|---|---|
| New feature | Start with user stories and acceptance criteria before code. |
| Code review | Ask AI for comments, then grade each one instead of accepting all. |
| Debugging | Paste the exact error and relevant file only; request a narrow fix. |
| Infrastructure | Verify commands locally and in CI; no hidden shortcuts. |
| Never-paste | No secrets, credentials, production logs, or personal/customer data. |
| One rule | If I cannot explain it, I do not submit it. |
