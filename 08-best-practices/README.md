# ✨ AI Engineering Best Practices


This section summarizes the core principles I follow to ensure high-quality AI software development.

---

1.  *Prompt Versioning: Treat prompts as code. Always version your prompts and track their performance using tools like LangSmith or Brais.
2.  Deterministic Over Probabilistic: Use LLMs for reasoning, but use code (Python/SQL) for calculations. Never let an LLM do math if you can use an API call.
3.  Human-in-the-loop (HITL): Design systems where humans can review and override AI decisions, especially in sensitive industries like Finance or Health.
4.  Security First: Implement prompt injection detection and ensure sensitive PII is never sent to external LLM providers without masking.
5.  Modular Design: Build small, specialized agents instead of one giant "do-it-all" prompt. It's easier to debug, test, and scale.
```