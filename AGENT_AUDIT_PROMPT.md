# 🕵️ Agent Audit Request Prompt (AOAgentDocs v1.1.1)

You are an expert **Software Architect & Documentation Auditor**.
Your task is to review the **Antigravity Standard Documentation System** (designed for AI Agent collaboration) and provide critical feedback.

## 1. Context
This documentation system (`AOAgentDocs`) is designed to standardize how AI Agents (Claude, Gemini, ChatGPT, etc.) onboard, collaborate, and develop software across multiple platforms (Android, Web, Server).

**Core Philosophy:**
- **Agent-First:** Instructions are optimized for LLM parsing (clear, structured, unambiguous).
- **Dual-Track Communication:** Uses `WRK` (Work Reports) for progress and `ISS` (Issues) for problem-solving.
- **Hash-Based ID:** Uses 6-digit hex hashes (SHA-256) for unique, collision-free document IDs.
- **Enforceable:** A strict onboarding pipeline (Checklist -> Memory) ensures compliance.

## 2. Review Materials
Please analyze the following files in the provided repository/folder structure:
1.  **`CONTRIBUTING.md`**: The entry point. Does it effectively grab your attention and force you into the onboarding pipeline?
2.  **`RULES/COMMON/COMMUNICATION.md`**: The core communication rules. Is the WRK+ISS hash system clear and collision-proof?
3.  **`UPGRADE_PROMPT.txt`**: The automated upgrade script. Is the logic sound for refactoring existing projects?
4.  **`folder structure`**: Is the separation of `works/`, `issues/`, and `END/` logical and scalable?

## 3. Audit Criteria (What to check)
Please evaluate the system based on these 4 dimensions:

### A. 🛡️ Robustness (Onboarding & ID)
- Can an agent "skip" the rules? Is the pipeline strict enough?
- Is the hash generation rule (`YYMMDD+HHMMSS+random` SHA-256 prefix) sufficient to prevent collisions?

### B. 🧱 Scalability (Modularity & Archive)
- If we add a `rules/PLATFORM/WEB` folder later, will it break existing Android projects?
- Does the `END/` archive strategy effectively manage long-term project history?

### C. 🧠 Clarity (LLM Optimization)
- Are there ambiguous instructions in `WRK` vs `ISS` templates?
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
