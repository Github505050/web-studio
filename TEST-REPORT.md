# Sukhjindra Web Studio — release test report

**Release candidate:** November 3, 2026, studio-wide showcase refresh

## Scope

Redesigned: Selected Work, Live Demos, Chatbots, Email Signatures.
Visual consistency: added `css/refinement.css` to the shared pages with warm white, deep slate, and muted teal, plus deliberate mobile layouts. Existing independent Northstar, Solace Studio and OrbitFlow demo designs remain distinct.

## Completed tests (before publication)

1. `python tests/site_audit.py`: page metadata, local links, sitemap and JavaScript syntax — PASS.
2. `python tests/bug_fixes_interactions.py`: repair lab interactions and responsive layout — PASS.
3. `python tests/studio_qa.py`: 9 shared-site pages × 7 viewport widths (320, 375, 390, 430, 768, 1024, 1440 px); no horizontal document overflow; mobile navigation; preview filtering/device selection; chatbot context, answer, reset and unsupported-question fallback; signature editing, HTML escaping, invalid URL handling, three style modes and download; preserved bug-fix pricing; selected-work cards; FAQ and landing-page picker — PASS.
4. `python tests/demo_qa.py`: three separately themed landing-page demos × 4 viewport widths (320, 390, 768, 1440 px), responsive layout, wellness schedule toggle and SaaS savings calculator — PASS.

## Design and content review

- Reviewed desktop and phone screenshots of the four redesigned pages.
- Demonstrations are labelled as fictional and independent builds; no fabricated paid-client testimonials, results or ratings are used.
- Chatbot remains accurately identified as deterministic FAQ matching, not live generative AI.
- Signature builder exports real HTML and warns about actual email-client compatibility; tests do not assert that Gmail or Outlook will render identically.
- Real project screenshots are referenced from public GitHub repositories. Local isolated browsers block external image access; a labelled fallback is provided and the live images must be inspected again after publication.

## Testing limitations

This test runner blocks direct local-server navigation and outbound requests. Browser QA therefore loads source HTML and injects the project's CSS and JavaScript in isolated Chromium documents. It checks rendering and interaction locally, but does not independently prove production GitHub Pages delivery, external project imagery, third-party links, client email app compatibility, server integrations, Firebase permissions, or production AI behaviour.

A successful GitHub Pages workflow confirms publishing, not an end-to-end user-path verification. Perform a live-browser review at https://github505050.github.io/web-studio/ after publishing, ideally on a real phone as well.
