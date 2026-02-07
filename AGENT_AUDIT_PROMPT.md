# 🕵️ Agent Audit Request Prompt (AOAgentDocs v1.1.0)

You are an expert **Software Architect & Documentation Auditor**.
Your task is to review the **Antigravity Standard Documentation System** (designed for AI Agent collaboration) and provide critical feedback.

## 1. Context
This documentation system (`AOAgentDocs`) is designed to standardize how AI Agents (Claude, Gemini, ChatGPT, etc.) onboard, collaborate, and develop software across multiple platforms (Android, Web, Server).

**Core Philosophy:**
- **Agent-First:** Instructions are optimized for LLM parsing (clear, structured, unambiguous).
- **Modular:** Rules are split into `COMMON` (Version Control, Ethics) and `PLATFORM` (Android, Web).
- **Enforceable:** A strict onboarding pipeline (Checklist -> Memory) ensures compliance.

## 2. Review Materials
Please analyze the following files in the provided repository/folder structure:
1.  **`CONTRIBUTING.md`**: The entry point. Does it effectively grab your attention and force you into the onboarding pipeline?
2.  **`RULES/000_CHECKLIST_TEMPLATE.md`**: The "Ritual". Is it clear where you should copy this and how to fill it out?
3.  **`RULES/000_INDEX.md`**: Does it clearly define priority (Platform > Common) to resolve conflicts?
4.  **`folder structure`**: Is the separation of `COMMON` vs `PLATFORM` logical and scalable?

## 3. Audit Criteria (What to check)
Please evaluate the system based on these 4 dimensions:

### A. 🛡️ Robustness (Onboarding)
- Can an agent "skip" the rules? Is the pipeline strict enough?
- Is the instruction to use *your own memory file* (e.g., `CLAUDE.md`) vs `docs/ONBOARDING.md` clear?

### B. 🧱 Scalability (Modularity)
- If we add a `rules/PLATFORM/WEB` folder later, will it break existing Android projects?
- Is the `MIGRATION_PROMPT.txt` logic sound for setting up new projects?

### C. 🧠 Clarity (LLM Optimization)
- Are there ambiguous instructions?
- Are the filenames and directory structures intuitive for an AI?

## 4. Output Format
Please provide your review in the following format:

```markdown
# 🧐 AOAgentDocs Audit Report

## ✅ Strengths
- (List 3 things that are well-designed)

## ⚠️ Potential Risks / Weaknesses
- (List areas where an agent might get confused or fail)

## 🎯 Suggestions for Improvement
- (Concrete actionable item 1)
- (Concrete actionable item 2)

## ⚖️ Final Verdict
- [ ] Approved (Ready for deployment)
- [ ] Needs Revision (Critical flaws exist)
```

---
*End of Prompt*
