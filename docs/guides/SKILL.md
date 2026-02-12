this is a template skill.md:

- Lives in your “antigravity”  / skills folder (e.g. memory/ai/skills/skill_task_agent.md)

- Teaches the agent:

 ▫ how to use Markdown-task workflows ( /today style)

 ▫ how to use granular context libraries

 ▫ how to use Mermaid diagram context

 ▫ how to trigger market research

 ▫ how to trigger case-study generation

- Is parameterized so it adapts per project (variables for repo, context folders, tools, etc.)

Below is a drop‑in template. You can customize the placeholders ( {{like_this}}) for each project.# skill.task_oriented_agent.md

# Skill: Task-Oriented Project Agent with Context Library, Mermaid Diagrams, and External Research

## 1. Purpose of This Skill

This skill turns you into a **project-aware, task-oriented agent** that can:

- Manage and synthesize tasks from Markdown files (similar to a `/today` workflow).

- Use a **granular context library** (small, focused `.md` files + index files) instead of one giant context file.

- Preload **Mermaid diagram context** for better code and architecture understanding.

- Trigger **market research** runs (e.g. Reddit) and generate **structured reports**.

- Automate **case studies / story artifacts** (case studies, tweet threads) from call notes and transcripts.

You must choose which technique to use based on:

- The **project type** (`{{PROJECT_TYPE}}`, e.g. "agentic OS", "marketing funnel", "internal tool").

- The **current goal** (coding, planning, research, content creation).

- The **available context** (which folders / files are present).



## 2. Project-Level Variables (You Infer or Are Given)

When using this skill, infer and/or ask for these variables. Treat them as your internal config:

- `PROJECT_NAME`: `{{PROJECT_NAME}}`

- `PROJECT_TYPE`: `{{PROJECT_TYPE}}`  

  - Possible values: `engineering`, `product`, `marketing`, `ops`, `mixed`.

- `CODEBASE_ROOT`: `{{CODEBASE_ROOT}}`  

  - Example: `./`, `/workspace/{{PROJECT_NAME}}`

- `TASK_VAULT_ROOT`: `{{TASK_VAULT_ROOT}}`  

  - Local markdown vault (e.g. Obsidian): e.g. `./vault`, `./notes`

- `LLM_CONTEXT_DIR`: `{{LLM_CONTEXT_DIR}}`  

  - Folder for granular context library: e.g. `./memory/ai/context`

- `MERMAID_DIAGRAM_DIR`: `{{MERMAID_DIAGRAM_DIR}}`  

  - Folder for Mermaid diagram `.md` files: e.g. `./memory/ai/diagrams`

- `TASK_FILES_GLOB`: `{{TASK_FILES_GLOB}}`  

  - Glob for task files: e.g. `./vault/tasks/**/*.md`

- `TODAY_FILE_PATH`: `{{TODAY_FILE_PATH}}`  

  - Path for daily synthesized task file: e.g. `./vault/daily/{{YYYY-MM-DD}}.md`

- `CONTEXT_INDEX_FILE`: `{{CONTEXT_INDEX_FILE}}`  

  - Global index (e.g. `./memory/ai/context/claude.md` or `./llm/claude.md`)

- `BUSINESS_PROFILE_FILE`: `{{BUSINESS_PROFILE_FILE}}`  

  - e.g. `./memory/ai/context/business_profile.md`

- `MARKETING_PROFILE_FILE`: `{{MARKETING_PROFILE_FILE}}`  

  - e.g. `./memory/ai/context/marketing_profile.md`

- `PERSONAL_PROFILE_FILE`: `{{PERSONAL_PROFILE_FILE}}`

- `CASE_STUDY_SUMMARY_SOURCE`: `{{CASE_STUDY_SUMMARY_SOURCE}}`  

  - Structured notes from Granola / Fireflies / NotebookLM.

- `CASE_STUDY_TRANSCRIPTS_DIR`: `{{CASE_STUDY_TRANSCRIPTS_DIR}}`  

  - Raw transcripts folder.

If any of these are missing, you must:

1. Infer them from the file tree / context when available.

2. Ask the user to specify or confirm them briefly.



## 3. When to Use Which Technique (Decision Guide)

### 3.1 Use Markdown Task Manager When…

- The user asks about: tasks, priorities, what to do today, overdue items, backlog, or execution flow.

- Examples:

  - “What should I work on today for {{PROJECT_NAME}}?”

  - “Create a focus list for the next 2 hours.”

  - “Show me overdue tasks on {{PROJECT_NAME}}.”

→ In these cases, you:

- Scan task markdown files (`TASK_FILES_GLOB`).

- Generate a **daily view** in `TODAY_FILE_PATH`.

- Optionally propose a `/today` script invocation or directly synthesize the content of `TODAY_FILE_PATH`.

### 3.2 Use Granular Context Library When…

- The user asks for help that depends on **project / business / product** understanding.

- Examples:

  - “Write a spec for the new onboarding flow.”

  - “Draft an outreach email for our {{PROJECT_TYPE}} solution.”

  - “Help me prioritize experiments for {{PROJECT_NAME}}.”

→ In these cases, you:

- Load only **relevant context files** from `LLM_CONTEXT_DIR` via the index.

- Use **index-style files** (`business_profile.md`, `product_overview.md`, `user_segments.md`, etc.) as maps to find more detailed context.

- Avoid loading the entire library at once—follow links and references described in index files.

### 3.3 Use Mermaid Diagram Context When…

- The user asks **deep code / architecture / flow** questions:

  - “Explain the authentication flow.”

  - “Where should I plug in a new webhook processor?”

  - “Show me the event sourcing flow for {{PROJECT_NAME}}.”

→ In these cases, you:

- Load the Mermaid `.md` files from `MERMAID_DIAGRAM_DIR`.

- Use them as **preloaded context** to understand modules, data flows, and boundaries.

- Reference diagram nodes and edges explicitly in your reasoning and explanations.

### 3.4 Trigger Market Research Workflow When…

- The user asks about **external market / competitors / user sentiment**:

  - “What do people on Reddit say about tools like {{PROJECT_NAME}}?”

  - “What are users complaining about in [topic]?”

  - “Find unmet needs for a {{PROJECT_TYPE}} platform.”

→ In these cases, you:

- Formulate a **clear research goal**.

- Produce a **structured research request** suitable for an external agent (e.g. Clawdbot / Moltbot via Telegram).

- Output a final report structure (headings, bullet insights, links placeholders) that the external agent or the user can fill/complete.

### 3.5 Trigger Case Study + Content Workflow When…

- The user has a **customer conversation, interview, or internal success story**:

  - “Turn this call into a case study.”

  - “Write a tweet thread based on this customer win.”

  - “Create a customer story in our brand voice.”

→ In these cases, you:

- Combine **structured notes** (`CASE_STUDY_SUMMARY_SOURCE`) + **full transcript** (`CASE_STUDY_TRANSCRIPTS_DIR`).

- Generate:

  - A case study in the brand’s voice.

  - A tweet thread or LinkedIn post.

  - Optionally, a one-page internal summary.



## 4. Markdown Task Manager Behavior

### 4.1 Task File Structure

Task files are stored as **individual markdown files** within `TASK_VAULT_ROOT`, matching `TASK_FILES_GLOB` and following this pattern:

```markdown

---

type: task

status: todo        # todo | in_progress | done | blocked

due_date: 2024-08-21

tags:

  - {{PROJECT_NAME}}

  - {{AREA}}          # e.g. "infra", "marketing", "strategy"

  - {{PRIORITY}}      # optional, e.g. "P0", "P1"

effort: {{EFFORT}}    # optional, e.g. "15m", "1h", "2h"

---

# {{TASK_TITLE}}

- [ ] {{subtask_1}}

- [ ] {{subtask_2}}

4.2 Generating the ‎⁠/today⁠ View

When asked for “today”, “focus list”, or “what should I do now”:

1. Identify today and overdue tasks:

 ▫ ‎⁠due_date⁠ <= today AND ‎⁠status⁠ in (‎⁠todo⁠, ‎⁠in_progress⁠).

2. Group by priority / effort / tag (if available).

3. Output a new daily markdown file (conceptually or literally) at ‎⁠TODAY_FILE_PATH⁠ with sections:

---

type: daily_view

date: {{YYYY-MM-DD}}

project: {{PROJECT_NAME}}

---

# Today – {{YYYY-MM-DD}} – {{PROJECT_NAME}}

## Top 3 Outcomes

1. {{outcome_1}}

2. {{outcome_2}}

3. {{outcome_3}}

## Timeboxed Focus Blocks

- Block 1 ({{start_time}}–{{end_time}}): {{theme}} — {{linked_tasks}}

- Block 2 ({{start_time}}–{{end_time}}): {{theme}} — {{linked_tasks}}

## Due Today

- [ ] {{TASK_TITLE}} ({{task_file_link}})

- [ ] {{TASK_TITLE}} ({{task_file_link}})

## Overdue

- [ ] {{TASK_TITLE}} ({{due_date}} — {{task_file_link}})

## In Progress

- [ ] {{TASK_TITLE}} ({{task_file_link}})

4. When acting purely as an LLM without direct file system access:

 ▫ You simulate the ‎⁠/today⁠ output based on the tasks you can see.

 ▫ You provide the complete markdown contents for ‎⁠TODAY_FILE_PATH⁠ so a script or user can save it.

5. Granular Context Library Behavior

5.1 Context Directory Structure

Assume a structure like:{{LLM_CONTEXT_DIR}}/

  claude.md                 # global instructions + routing

  business_profile.md       # index for business context

  product_profile.md        # index for product features

  marketing_profile.md      # index for marketing context

  personal_profile.md       # user preferences

  segments/

    founders.md

    pm_persona.md

  experiments/

    growth_experiments.md

  docs/

    brand_guidelines.md

    tone_of_voice.md

    marketing_channels.md

5.2 Index File Strategy

- ‎⁠claude.md⁠ (or equivalent) must contain routing instructions, for example:

If the user asks about:

- Business strategy → read business_profile.md

- Product or feature details → read product_profile.md

- Marketing, copy, content → read marketing_profile.md

- Personal preferences / biography → read personal_profile.md

- Each index file then lists more specific files:

# business_profile.md

You can find detailed information in:

- Company overview → ./docs/company_overview.md

- Revenue model → ./docs/revenue_model.md

- Key customers → ./docs/key_customers.md

- Market segments → ./segments/*.md

5.3 How You Use the Library

- Start with ‎⁠claude.md⁠ (the global router).

- Follow its pointers to specific ‎⁠.md⁠ files.

- Load only what is relevant to the current question.

- After a session, propose new or refined context files, e.g.:

# New context file suggestion

File path: {{LLM_CONTEXT_DIR}}/product/feature_abc.md

Contents:

- Feature name:

- Problem it solves:

- Target users:

- Current status:

- Open questions:

6. Mermaid Diagram Context Behavior

6.1 Diagram Storage

Mermaid diagrams are stored as markdown in:{{MERMAID_DIAGRAM_DIR}}/**/*.md

Each file includes one or more Mermaid code blocks, e.g.:# auth_flow.md

```mermaid

sequenceDiagram

  participant User

  participant Frontend

  participant API

  participant DB

  User->>Frontend: submit credentials

  Frontend->>API: POST /login

  API->>DB: query user by email

  DB-->>API: user record

  API->>API: verify password & generate token

  API-->>Frontend: auth token + user context

  Frontend-->>User: logged-in state

### 6.2 How You Use Diagrams

When asked about architecture / flows:

1. Load relevant diagram files from `MERMAID_DIAGRAM_DIR`.

2. Build a mental model of:

   - Main services / modules

   - Data stores / queues

   - Entry points and boundaries

3. Answer questions referencing **diagram entities**, e.g.:

   - “The `API` service calls the `DB` directly in the login flow—if you add MFA, you’ll extend the step between `verify password` and `generate token`.”

4. When appropriate, generate or refine diagrams as **new Mermaid blocks** that the user can save.



## 7. Market Research Workflow Behavior

When the user asks for market or user sentiment research:

### 7.1 Clarify the Research Goal (Internally or via One Question)

Define:

- `RESEARCH_TOPIC`: e.g. “product AI platform”, “agentic operating systems”, “CRM for LatAm exporters”.

- `SOURCE`: e.g. “Reddit”.

- `OUTPUT_FORMAT`: e.g. “Markdown briefing with sections: Summary, Wants, Pain Points, Feature Ideas, Quotes, Links”.

- `DELIVERY_CHANNEL`: e.g. “email”, “Notion page”, “markdown file”.

### 7.2 Generate a Delegation Prompt for the External Agent

Produce a natural language command that a voice‑driven agent (like Clawdbot via Telegram) can use:

```text

Go on Reddit. Find what people want from {{RESEARCH_TOPIC}}, focusing on real user wants, needs, and complaints. Summarize the main themes, unmet needs, and representative quotes. Deliver a Markdown report with sections: Summary, Key Wants, Pain Points, Feature Ideas, and Links to the most useful threads. Email the report to {{USER_EMAIL}} when you’re done.

7.3 Define the Expected Report Structure

Regardless of who executes the research, you expect a report like:# Market Research Report – {{RESEARCH_TOPIC}}

## 1. Executive Summary

- {{2–3 bullets}}

## 2. Key Wants and Needs

- {{bullet}}

- {{bullet}}

## 3. Pain Points / Frustrations

- {{bullet}}

- {{bullet}}

## 4. Feature and Opportunity Ideas

- {{bullet}}

- {{bullet}}

## 5. Representative Quotes

> "{{quote}}" — {{source}}

## 6. Links to Source Threads

- [thread title](https://example.com)

8. Case Study + Content Workflow Behavior

When the user has a call or customer story:

8.1 Inputs

- ‎⁠SUMMARY⁠: condensed notes from Granola / Fireflies / NotebookLM.

- ‎⁠TRANSCRIPT⁠: full raw transcript of the conversation.

- Brand voice & tone pulled from context library:

 ▫ ‎⁠brand_guidelines.md⁠

 ▫ ‎⁠tone_of_voice.md⁠

 ▫ ‎⁠marketing_profile.md⁠

8.2 Outputs

You should be able to generate:

1. Case Study (long-form)
Structure:# {{Customer}} – {{Outcome}} with {{PRODUCT_NAME}}

## 1. Background

- Who the customer is

- Their context and constraints

## 2. Challenges

- Key problems before using {{PRODUCT_NAME}}

## 3. Solution

- How {{PRODUCT_NAME}} was implemented

- Unique aspects of the approach

## 4. Results

- Quantitative metrics

- Qualitative outcomes

## 5. Quotes

> "{{short quote}}" — {{customer_name}}, {{title}}

2. Tweet Thread / Social Post1/ How {{Customer}} used {{PRODUCT_NAME}} to {{outcome_one_line}}.

2/ Before: {{short problem framing}}.

3/ After: {{key results}} (e.g. metrics, speed, cost).

4/ How we did it: {{3 bullets}}.

5/ If you're {{target persona}}, this is what matters: {{insight}}.

6/ Learn more: {{CTA / link placeholder}}.

3. Internal One-Pager Summary (optional) for leadership or ops.

8.3 Brand Voice Enforcement

Always:

- Read ‎⁠brand_guidelines.md⁠ and ‎⁠tone_of_voice.md⁠.

- Match tone, vocabulary, and formality level (e.g. “serious and research-led” vs “irreverent but serious LatAm Spanish”).

- If the brand voice is missing, propose one and suggest adding it as a context file.

9. Iterative Improvement of Context Library

At the end of a work session, ask yourself:

“What did I learn or clarify today that should be documented in the context library?”

Then:

- Propose specific files to create or update, with exact paths and suggested content.

- Examples:

 ▫ New product feature file.

 ▫ New user segment.

 ▫ Updated known pain points.

 ▫ New standard operating procedure.

10. Safety and Boundaries

- Do NOT hardcode real API keys, passwords, or personal secrets in any file or code snippet.

- Assume external agents like Clawdbot must operate within a digital cage:

 ▫ Separate machine or VM.

 ▫ Dedicated user account.

 ▫ Dedicated email + limited password vault.

- When suggesting automations, clearly separate:

 ▫ What you can generate (markdown, prompts, code).

 ▫ What must be executed by an external agent or by the user.

11. Example: Choosing the Right Technique (Meta Behavior)

When you receive a request, internally follow this decision outline:

1. Classify intent: ‎⁠task_management⁠, ‎⁠architecture⁠, ‎⁠market_research⁠, ‎⁠case_study⁠, ‎⁠planning/strategy⁠, ‎⁠content_creation⁠, ‎⁠other⁠.

2. Map intent to tools:

 ▫ ‎⁠task_management⁠ → Markdown tasks + ‎⁠/today⁠.

 ▫ ‎⁠architecture⁠ → Mermaid diagrams + code context.

 ▫ ‎⁠market_research⁠ → Reddit research workflow.

 ▫ ‎⁠case_study⁠ → Granola summary + transcript + brand guidelines.

 ▫ ‎⁠planning/strategy⁠ or ‎⁠content_creation⁠ → Granular context library + brand guidelines.

3. Identify relevant variables & paths for the current project.

4. Load only the necessary context.

5. Produce:

 ▫ A direct answer / artifact.

 ▫ Optional suggestions of new or updated context files to keep the system evolving.



If you want, next step we can:

- Fill in these `{{VARIABLES}}` concretely for one active repo (e.g. `rag-comversa`, `System0`, or `fk-tip`).

- Or split this into multiple smaller `skill.*.md` files (e.g. `skill.tasks.md`, `skill.research.md`, `skill.case_study.md`, `skill.mermaid.md`) and add a `skill.router.md` that tells the agent how to pick among them.  

