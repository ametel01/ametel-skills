---
name: hackerone-bug-hunt-submission
description: Use this skill when doing HackerOne bounty triage, in-scope asset validation, source-code bug hunting, PoCs, attachments, or report drafting.
---

# HackerOne Bug Hunt Submission

## Purpose

Find credible HackerOne bounty targets, verify scope and reward eligibility, produce reproducible evidence, and prepare a complete submission without fabricated claims.

## Ground Rules

- Browse current program pages or reliable scope mirrors before relying on scope, rewards, accepted weaknesses, or asset names.
- Prefer official HackerOne program pages and the target repository `SECURITY.md`; use mirrors such as bbscope only as supporting evidence when HackerOne pages are inaccessible.
- Do not submit reports for the user unless explicitly authorized and the platform/tooling supports it.
- Do not overstate impact. Mark local-only, user-interaction, race, or privileged preconditions clearly.
- Do not include real secrets, live tokens, private keys, or third-party data in PoCs. Use dummy values.
- Treat pre-submission checker warnings as useful but verify them against the actual form state.
- Treat local symlink, link-following, and TOCTOU bugs as high-duplicate/high-informative risk unless the exploit crosses a strong trust boundary or works in a default/common workflow.

## Workflow

1. **Choose a target**
   - Start from paid HackerOne opportunities with source-code or testable web/API assets.
   - Record program name, report URL, asset URL, asset type, reward eligibility, and any exclusions.
   - If the user says they already submitted to a program, pivot to a different program.

2. **Validate scope**
   - Match the exact HackerOne asset string where possible.
   - Confirm the repo or app is owned by the program and listed as in scope.
   - Read `SECURITY.md`, bug bounty policy, and out-of-scope findings before testing.

3. **Audit and prove**
   - Clone or inspect only in-scope code.
   - Look for security-sensitive surfaces: injection, auth bypass, SSRF, path traversal, symlink/link following, secret handling, archive extraction, template rendering, deserialization, command execution, update/install scripts, webhooks, CI, and permission boundaries.
   - Before investing in local file bugs, search recent duplicate patterns in the program and ask whether the victim must opt into a beta/diagnostic mode, use an attacker-writable per-user directory, or manually package/upload data. Those facts often reduce bounty value.
   - Create the smallest deterministic PoC that demonstrates exploitability.
   - Add a regression-style test when useful, but distinguish added test code from vulnerable source code.
   - Run focused verification commands and save exact command/result snippets.

4. **Package artifacts**
   - Create `reports/<program>-<bug-slug>.md` with the full report.
   - Create `reports/hackerone-submission-fields.md` with paste-ready form fields.
   - Create a PoC attachment such as `.patch`, `.py`, `.sh`, screenshots, logs, or a zip.
   - Zip only useful files: full report, field file, PoC/test patch, and minimal logs.

5. **Complete the HackerOne form**
   - Use the field checklist below.
   - Replace every default boilerplate marker such as `[add step]` and `Describe impact here.`
   - Run pre-submission checks if available.
   - Fix blocking issues first: default title, missing weakness, empty required fields, invalid asset, missing severity.

## Required HackerOne Fields

Always provide these fields in the final answer and in `reports/hackerone-submission-fields.md`:

- **Title**: Specific vulnerable component + bug class + consequence.
  - Example: `Doppler CLI mount path replacement can disclose mounted secrets to an attacker-controlled file`
- **Asset**: Exact in-scope asset URL or hostname from the program.
  - Include asset type when known: `SOURCE_CODE`, `URL`, `API`, `MOBILE_APP`, etc.
- **Weakness**: Best matching CWE/category accepted by HackerOne.
  - Include fallbacks when the form cannot find the ideal weakness.
- **Severity**: Informational, Low, Medium, High, or Critical.
  - Include CVSS vector when useful, but do not force a higher rating than the demonstrated preconditions support.
- **Description**: Paste-ready Markdown with `Summary`, `Description`, `Steps To Reproduce`, and `Supporting Material/References`.
- **Impact**: Concrete attacker capability and affected data/systems. Include prerequisites and limits.
- **Attachments**: Absolute local path(s) to the zip, patch, script, screenshots, or logs to upload.

## Report Template

Use this structure for `reports/hackerone-submission-fields.md`:

````markdown
# HackerOne submission fields

## Title

<descriptive title>

## Asset

<exact in-scope asset>

Asset type: <SOURCE_CODE / URL / API / other>

## Weakness

<primary CWE/category>

Fallbacks if the form cannot find it:
1. <fallback CWE/category>
2. <broader weakness category>

## Severity

<severity>

Suggested CVSS vector:

`<CVSS vector if applicable>`

Rationale: <one paragraph explaining prerequisites and impact>

## Description

```markdown
## Summary:

<one concise paragraph>

## Description:

<technical details with affected file/function/endpoint and root cause>

## Steps To Reproduce:

1. <step>
2. <step>
3. <step>
4. <observed result>

## Supporting Material/References:

* Affected source: `<file/function/line if known>`
* Verified on commit/version: `<commit/version>`
* Verification command: `<command>`
* Attached PoC: `<filename>`
```

## Impact

```markdown
<impact text>
```

## Attachments

Upload:

`<absolute path to zip or PoC>`
````

## Weakness Selection Guidance

- SQL injection: `CWE-89: Improper Neutralization of Special Elements used in an SQL Command`
- OS command injection: `CWE-78: Improper Neutralization of Special Elements used in an OS Command`
- SSRF: `CWE-918: Server-Side Request Forgery`
- Path traversal: `CWE-22: Improper Limitation of a Pathname to a Restricted Directory`
- Symlink/link following: try `CWE-61: UNIX Symbolic Link Following`, then `CWE-59: Improper Link Resolution Before File Access`, then `Link Following`
- Sensitive file/data disclosure: `CWE-200: Exposure of Sensitive Information to an Unauthorized Actor`
- Broken authorization/IDOR: `CWE-639: User-Controlled Key in Authorization Decision`, or `CWE-862: Missing Authorization`
- XSS: `CWE-79: Improper Neutralization of Input During Web Page Generation`
- CSRF: `CWE-352: Cross-Site Request Forgery`
- Insecure deserialization: `CWE-502: Deserialization of Untrusted Data`
- Archive extraction slip: `CWE-22` or `CWE-59`, depending on the primitive.

If HackerOne cannot find the exact CWE, choose the closest broader category and state the exact CWE in the report body.

## Duplicate and Informative Risk

Deprioritize or heavily qualify findings with these traits:

- Local-only symlink traversal in installers, skill/plugin copy logic, archives, cache folders, fallback files, or mount/FIFO paths.
- TOCTOU path replacement where the attacker needs write access to the same per-user directory and victim timing/cooperation.
- Opt-in hidden beta, diagnostic, support, or telemetry packaging commands where the user must manually generate and upload the artifact.
- Findings that disclose files only from the reporting user's own machine with no privilege escalation, remote attacker path, or default multi-user boundary.
- Bugs matching common public duplicate chains: missing `O_NOFOLLOW`, `fs.cp(..., dereference: true)`, unguarded archive symlink extraction, or diagnostic zips that dereference logs.

Only continue with those classes when at least one stronger factor is present:

- Remote or unauthenticated trigger.
- Default workflow with no hidden/beta flags.
- Cross-user, sandbox/container escape, CI runner, production secret, or privilege boundary.
- Program-specific policy explicitly rewards local CLI issues.
- Clear evidence the same root cause has not already been reported.

## Severity Guidance

- **Critical**: unauthenticated remote code execution, full account takeover at scale, broad production secret compromise.
- **High**: network-exploitable injection/auth bypass with high confidentiality or integrity impact.
- **Medium**: meaningful data disclosure or write primitive with local access, user interaction, race/timing, or scoped prerequisites.
- **Low**: limited information disclosure, self-impact, hard-to-exploit local issue, or low-value data.
- **Informational**: hardening-only or no clear security boundary crossed.

Always include prerequisites: authentication, local access, same machine, writable directory, victim interaction, race timing, required feature flag, or privileged role.

## Submission Troubleshooting

- **Default title blocker**: Replace `Report Intent #...` with the vulnerability title.
- **Asset cannot be matched**: Re-select the exact asset from the program asset list. If the asset is a GitHub repository, use the exact repository URL and asset type `SOURCE_CODE`.
- **Weakness not found**: Search by CWE number first, then by short phrase, then use a broader data exposure or authorization category and explain the exact weakness in the report.
- **Severity not accepted**: Use manual severity if CVSS is unavailable; include CVSS in the body if the form supports only manual values.
- **Required fields incomplete**: Check for untouched boilerplate markers: `[add summary]`, `[add step]`, `[attachment / reference]`, `Describe impact here`.
- **Attachment missing**: Provide the exact local path to the zip or PoC file and list its contents.

## Completion Checklist

Before telling the user the report is ready:

- Scope/reward checked against current sources.
- Duplicate/informative risk assessed, especially for local file, symlink, TOCTOU, beta, diagnostic, and support-bundle bugs.
- Exact asset and asset type identified.
- Weakness selected with fallbacks.
- Severity and rationale written.
- Description includes summary, root cause, reproduction steps, and supporting material.
- Impact states attacker capability, affected data, prerequisites, and limits.
- PoC is deterministic and uses dummy data.
- Verification command was run and result recorded.
- Attachment path exists and zip contents were inspected.
- No placeholders remain in the report fields.
