---
applyTo: "**"
---
# Instructions

## 1. Core Mission
We are building a multi-agent LLM app. The project is currently in active development; prioritize flexibility and scalable architecture over fixed legacy patterns.


## 2. Global Standards & Sub-Instructions (Mandatory)
- **Primary Sources:**
	- `.github/instructions/clean-code-standards.instructions.md`: Mandatory Python Clean Code rules (SOLID, DRY, KISS, PEP 8+, error handling, security, etc.).
	- `.github/instructions/python-clean-code-standards.instructions.md`: Extended Python clean code and architecture principles for senior engineers.
	- `.github/instructions/code-framework.instructions.md`: Framework-specific rules for AutoGen AgentChat (v0.4.x), agent/team design, workflows, tools, and memory.
- **Python Formatting:** You MUST follow all formatting and line length rules in `.github/instructions/python-format.instructions.md`.
- **Precedence:** If a framework-specific rule conflicts with general clean code rules, the framework specification takes precedence.
- **Compliance Check:** Before finalizing any code, verify it against all relevant instructions above and the Python formatting instructions.

## 3. Framework & Technical Constraints
- **Cost/Token Tracking:** Ensure every LLM response is processed for token/cost metrics using available utility patterns.
- **Environment:** Secrets must stay in `.env.local` (never hardcode keys).

## 4. Coding Behavior
- **Senior Engineer Analysis:** Before and after every task, provide a concise analysis and summary from a senior software engineer perspective. This should include:
	- Pre-task: Reasoning, risks, architectural/contextual impact, and expected outcome.
	- Post-task: What was changed, why, any trade-offs, and how the result aligns with best practices and project goals.
- **Refactoring:** Proactively suggest refactors for "Legacy" or "Messy" code based on our Clean Code standards.
- **Language:** All new code, docstrings, and comments must be in **English**.
- **Efficiency:** Prioritize readability and maintainability as defined in the primary standards file.