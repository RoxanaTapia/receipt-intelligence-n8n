# /verify Command

You are acting as the **verifier** agent.

Your task is to review the current changes or the latest work done in the project and provide a quality check.

## Instructions

1. Review the code changes or the current state of the relevant files.
2. Check doc changes against `.cursor/rules/documentation.mdc`.
3. Check code against `.cursor/rules/elegant-minimal-python.mdc`.
4. Run any relevant checks if possible (linting, tests, etc.).
5. Provide clear feedback using the verification format.

## Output Format

Structure your response like this:

```markdown
## Verification Summary

- **Status**: ✅ Pass / ⚠️ Issues found / ❌ Needs work
- **Checks performed**:
- **Issues found**:
  - ...
- **Suggestions**:
  - ...
```