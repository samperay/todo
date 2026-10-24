# Content audit — v6 review edition

## Verified by construction

- 230 original lesson files preserved; 20 module indexes.
- Duplicate legacy appendix sections removed, except rich queue v4 content promoted to main Lesson 03.02.
- 10 technology tracks linked from relevant module indexes, each with Learn, Integrate and Operate chapters; baseline phase 00 points to Modules 01/02.
- `personal notes (optional)/` directory removed.

### Important unresolved quality work

The v5 legacy lessons often reused generic Python models for unrelated topics (e.g., permissions model for vulnerability scanning). This edition labels such models as conceptual prerequisites; it **does not** claim all 230 lessons have topic-specific verified labs. Those require further manual editorial development and actual execution. Some technology Learn chapters provide prerequisite checks rather than full integrations. The SDD integration chapters are plans, not implemented features.

### Acceptance gates for a fully verified edition

1. Unique topic-specific runnable labs and annotated output for each lesson.
2. Read-through for accuracy and security; fix misleading generic models.
3. Link audit passes, with no removed progress references.
4. All integration instructions reconciled to current Todo branch and actual tests.
5. Operational labs have safe cleanup and recovery evidence.
