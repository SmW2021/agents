# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Ed Donner's 6-week "Agentic AI Engineering" course. The top-level numbered directories (`1_foundations`, `2_openai`, `3_crew`, `4_langgraph`, `5_autogen`, `6_mcp`) each correspond to one week and one framework. Each week mixes Jupyter lab notebooks (`*_labN.ipynb`) with a runnable capstone in Python. `community_contributions/` (and similar) inside each week hold student-submitted variants and should generally be treated as read-only examples, not the canonical path.

This is teaching code, not production code. Defaults favor clarity over robustness.

## Environment & tooling

- Package manager is `uv` (Astral). The top-level `pyproject.toml` + `uv.lock` cover weeks 1, 2, 4, 5, 6 with `requires-python = ">=3.12"`.
- Install / refresh: `uv sync` at the repo root.
- Run a script: `uv run <path/to/script.py>` (never invoke bare `python`; the venv is uv-managed).
- Run notebooks: open in Cursor / VS Code with the uv-provided kernel, or `uv run jupyter lab`.
- Week 4 (LangGraph) needs Playwright browsers: `uv run playwright install` once.
- A single `.env` at the repo root is loaded by every script via `load_dotenv(override=True)`. Keys referenced in code include: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `DEEPSEEK_API_KEY`, `GOOGLE_API_KEY` (and an identical `GEMINI_API_KEY` for CrewAI Gemini), `GROK_API_KEY`, `OPENROUTER_API_KEY`, `POLYGON_API_KEY` (+ optional `POLYGON_PLAN`), `BRAVE_API_KEY`, `SERPER_API_KEY`, `PUSHOVER_TOKEN` / `PUSHOVER_USER`, SendGrid key for week 2 email. There is no test suite or linter configured.

## CrewAI (week 3) is different

Week 3 projects (`3_crew/coder`, `debate`, `engineering_team`, `financial_researcher`, `stock_picker`) are **standalone uv projects**, each with its own `pyproject.toml` and `uv.lock`, pinned to `>=3.10,<3.13`. They are not installed by the top-level `uv sync`.

- Install the CLI once: `uv tool install crewai==0.130.0 --python 3.12` (README pins this exact version; upgrade with `uv tool upgrade crewai==0.130.0 --python 3.12`).
- Run a crew: `cd 3_crew/<project>` then `crewai run`. Other entrypoints declared in each `pyproject.toml`: `train`, `replay`, `test`.
- Each crew follows the same layout: `src/<name>/config/agents.yaml` + `tasks.yaml` declare roles and tasks; `crew.py` wires them with `@agent` / `@task` / `@crew` decorators on a `@CrewBase` class; `main.py:run()` calls `Crew().kickoff(inputs=...)`.
- `stock_picker` is the most elaborate example — hierarchical `Process` with a separate manager agent, plus `LongTermMemory` (SQLite at `./memory/long_term_memory_storage.db`), `ShortTermMemory`, and `EntityMemory` backed by RAG storage using `text-embedding-3-small`.
- `engineering_team` writes generated code to `output/` (gitignored).

## Per-week architecture notes

**1_foundations** — Plain `openai` SDK chatbot. `app.py` builds a Gradio chat where the system prompt impersonates Ed Donner using `me/summary.txt` + `me/linkedin.pdf` (parsed by `pypdf`), with two tool-calls (`record_user_details`, `record_unknown_question`) that push to Pushover. The tool-call loop runs inline in `Me.chat`.

**2_openai** — OpenAI Agents SDK labs plus the `deep_research/` capstone. `ResearchManager` orchestrates a `planner_agent` → many `search_agent` runs (in parallel) → `writer_agent` → `email_agent` pipeline, streamed back to a Gradio UI in `deep_research.py`.

**4_langgraph** — `sidekick.py` defines a two-node graph: a `worker` LLM (gpt-4o-mini bound to Playwright + other tools from `sidekick_tools.py`) and an `evaluator` LLM (structured output via Pydantic). Edges: `worker` routes to `tools` while there are tool calls, otherwise to `evaluator`; `evaluator` either ends or sends control back to `worker`. State is persisted with `MemorySaver` keyed by a per-session `sidekick_id` (UUID). `app.py` is the Gradio frontend and owns Playwright browser cleanup via `free_resources`. SQLite checkpoint files (`memory.db*`) are gitignored.

**5_autogen** — Distributed AutoGen demo. `world.py` starts a `GrpcWorkerAgentRuntimeHost` on `localhost:50051`, registers a `Creator` agent, and dispatches `HOW_MANY_AGENTS` messages in parallel; each spawned agent writes its source to `agentN.py` and an idea to `ideaN.md` in the working directory. `creator.py` / `agent.py` / `messages.py` define the agent classes and message shapes.

**6_mcp (capstone trading floor)** — Four trader personas (Warren / George / Ray / Cathie) defined in `reset.py`; run `uv run reset.py` once before first launch to seed accounts and strategies. Architecture:
- `traders.py` — `Trader` builds an OpenAI Agents SDK `Agent` that has its own `Researcher` sub-agent attached **as a tool** (`agent.as_tool(...)`). Multi-provider model routing in `get_model()` covers OpenAI, DeepSeek, Grok, Gemini, and any `org/model` form on OpenRouter.
- `mcp_params.py` — declares MCP server stdio params. Trader stack: `accounts_server.py` + `push_server.py` + a market server (either local `market_server.py` or the Polygon MCP image, gated on `is_paid_polygon` / `is_realtime_polygon` in `market.py`). Researcher stack: `mcp-server-fetch`, Brave Search (npx), and per-trader libsql memory in `./memory/<name>.db`.
- `trading_floor.py` — long-running scheduler. Sleeps `RUN_EVERY_N_MINUTES`, gates on `is_market_open()` (override with `RUN_EVEN_WHEN_MARKET_IS_CLOSED=true`), and toggles each trader between trade / rebalance modes per cycle. `USE_MANY_MODELS=true` switches to the heterogeneous model lineup.
- `app.py` — Gradio dashboard. Reads accounts/logs through `database.py` (SQLite) and refreshes via `gr.Timer`. The dashboard does **not** run the agents; start `trading_floor.py` in a separate process for live activity.
- `accounts.py` / `database.py` — Pydantic `Account` model persisted to `accounts.db` (gitignored). Initial balance `$10,000`, spread `0.002`.
- `tracers.py` registers a `LogTracer` with the OpenAI Agents SDK so every agent/function/generation event lands in the SQLite log surfaced by the dashboard.

## Conventions worth knowing before editing

- All scripts assume CWD is their containing directory (relative paths like `./memory/`, `me/linkedin.pdf`, `output/`, MCP `uv run accounts_server.py`). Don't refactor to absolute paths without checking every caller.
- Multi-provider LLM access is done by pointing the OpenAI SDK at alternative base URLs (`DEEPSEEK_BASE_URL`, `GROK_BASE_URL`, `GEMINI_BASE_URL`, `OPENROUTER_BASE_URL`). When adding a new provider, follow this pattern rather than introducing a new SDK.
- Gradio UIs in `1_foundations/app.py`, `4_langgraph/app.py`, `6_mcp/app.py`, `2_openai/deep_research/deep_research.py` all call `.launch(inbrowser=True)` at import time. Don't import them from other modules.
- `community_contributions/` directories are independent student work and may use different conventions, dependencies, or even broken state. Treat them as examples, not as part of the canonical build.
