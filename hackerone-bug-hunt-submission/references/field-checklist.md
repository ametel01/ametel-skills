# HackerOne Field Checklist

Use this when the user is actively filling a HackerOne form.

Required paste-ready fields:

1. Title
2. Asset
3. Asset type
4. Weakness
5. Severity
6. Description
7. Impact
8. Attachments

Description must include:

1. Summary
2. Technical description/root cause
3. Steps to reproduce
4. Supporting material/references

Submission blockers to fix:

1. Default title still present
2. Weakness not selected
3. Severity not set
4. Asset not selected from scope
5. Placeholder text remains
6. Attachment referenced but not uploaded

Pre-submit quality gates:

1. Check whether the bug class is a known duplicate pattern for that program.
2. Flag local-only symlink, TOCTOU, beta, diagnostic, and support-bundle issues as high informative risk.
3. Continue only if impact crosses a meaningful trust boundary or the program explicitly rewards the class.
4. State all prerequisites in severity and impact.
