# Sukhjindra Web Studio

A premium static portfolio and interactive frontend demonstration library for an independent web designer. The business and people inside sample demonstrations are fictional. This is not a website claiming paid-client work, years of experience, guaranteed results or AI abilities without a model integration.

## Features

- Homepage, four dedicated service pages, working demo library, selected project case studies, About, FAQ and a custom 404 page
- Three distinct and fully navigable landing-page examples: consulting, wellness, SaaS
- Responsive iframe preview with desktop/tablet/mobile controls
- Four isolated before/after frontend repair examples
- Guided deterministic FAQ chatbot with 3 business knowledge bases (33 supported topics), quick replies, conversation display and fallback handling
- Three real, table-based HTML email signature variants with editable sample data, live preview, clipboard HTML and downloaded HTML file
- Mobile navigation, accessible FAQ accordions, demo filtering, keyboard support and reduced-motion CSS
- Static SEO fundamentals, `sitemap.xml`, `robots.txt`, meta descriptions and per-page canonical URLs

## Technology

Pure HTML5, CSS and ES module JavaScript; no framework, npm install, paid API, database or secret keys required. Hosted images for example signatures are authored in `assets/`.

## Structure

```text
index.html, 404.html, sitemap.xml, robots.txt
services/{landing-pages,bug-fixes,chatbots,email-signatures}/index.html
live-demos/index.html
selected-work/index.html
about/index.html
faq/index.html
demos/{consulting,wellness,saas}/index.html
css/site.css
assets/demo.css, sample-avatar.png, sample-logo.png, favicon.svg
js/site.js, chatbot.js, signature.js, sample-pages.js
build.py, make_demos.py          page generators
 tests/                           browser + source tests
```

## Local preview

GitHub Pages project URLs are based on `/web-studio/`. To simulate this locally, serve the parent folder of `web-studio`:

```bash
cd ..
python3 -m http.server 8000
```

Open `http://localhost:8000/web-studio/`.

## Publish on GitHub Pages (free)

1. Create a **new public repository** called `web-studio` under `Github505050`—do **not** overwrite any existing repository.
2. Upload the **contents** of this folder to its `main` branch, preserving the structure; do not upload only the ZIP file.
3. Open `Settings → Pages → Build and deployment → Deploy from a branch → main → /(root) → Save`.
4. Once Pages has finished deploying, open `https://github505050.github.io/web-studio/`.
5. Verify the demo routes, signature images, clipboard action on HTTPS, responsive preview, chatbot, and mobile navigation on the public URL.

## Quality checks

`python tests/site_audit.py` verifies page links, metadata, XML, JavaScript syntax via Node and other static properties. `python tests/browser_smoke.py` performs **isolated** Chromium interface checks by injecting the generated HTML, local CSS and JavaScript into a browser document. The automated browser environment blocks direct local navigation, so these are not full live-site network tests. These checks use fictional test data and are not a substitute for testing actual email client rendering or deployed GitHub Pages.

## Limitations and future work

- Default chatbot is a local guided FAQ assistant, **not** a generative AI model or connection to orders, student records, or agents. A protected server would be needed for real system integrations.
- Signatures use public hosted image URLs for Gmail/Outlook-friendly HTML; these images require this repository to be deployed on GitHub Pages. Rendering varies by email client; test in the actual email apps before production delivery.
- The responsive iframe preview is an illustration of breakpoint behavior, not a replacement for testing physical phones and tablets.
- The 404 page is provided; GitHub Pages may show its route directly when it handles missing pages.
- Local prototype features do not save real appointments, purchases, payments or emails.
- Case studies are descriptions of existing independent GitHub repositories. Their features and limitations should be reviewed after future source changes.
- Future additions: screenshots captured from deployed examples, optimized media, real-browser visual regression tests, internationalization, contact only through Upwork.

## Attribution and ethical presentation

Sample businesses (Northstar, Solace, OrbitFlow, Morrow, Alder, Brightpath) and sample signature identities are fictional. Screenshots for the three original landing-page demos were captured locally from the actual HTML/CSS in isolated Chromium. Selected-work screenshots are referenced from existing public repository files on GitHub, not invented project visuals. Descriptions of the external French Classroom, Northline and personal portfolio projects are based on their public repository READMEs. All initial professional inquiries related to Upwork projects should remain on Upwork before a contract begins.

## November 3, 2026 — cohesive studio showcase refresh

The public studio uses a calm slate / teal / warm-white system in `css/refinement.css`, layered over the original shared CSS. The refined layout covers the homepage, About, FAQ, Landing Pages, Bug Fixes, Selected Work, Live Demos, Chatbots and Email Signatures. The three separate fictional landing-page designs intentionally retain their distinct visual identities.

### Updated pages
- **Selected Work:** honest independent-project evidence with working external links and explicit limitations. Project imagery is sourced from public project repositories; if external images are unavailable, CSS illustrates a fallback and the source project links remain accessible. These are not paid-client case studies.
- **Live Demos:** six-category-aware demo cards with filters, selectable iframe preview, desktop/tablet/mobile frame controls, and real page links. The phone link opens full pages rather than requiring interaction through a narrow embedded iframe.
- **Chatbots:** three switchable structured FAQ knowledge bases, suggested prompts, unknown-question fallback, conversation reset, browser-only history and clear notice that the demonstration is deterministic, not a generative AI model.
- **Email Signatures:** three editable table-based templates, example contact details, selectable muted accent colours, editable HTTPS website link, email/phone hyperlinks, clipboard copy, source reveal, and HTML download. Generated sample artwork URLs refer to this public site's fictional images. Always test generated markup in actual email clients before real business use.

### How to test
`python tests/site_audit.py` checks syntax, links and metadata.
`python tests/bug_fixes_interactions.py` checks the repair lab.
`python tests/browser_smoke.py` runs a lightweight mobile sanity check. Run `python tests/studio_qa.py` and `python tests/demo_qa.py` separately for the complete isolated-browser interaction checks. Direct local and external network navigation is unavailable in the test environment, so images fetched from public repositories and GitHub Pages delivery must be checked on the deployed website separately.

`build.py` and `make_demos.py` are older generators: running them may overwrite the manually refined HTML. Review generated diffs and retain the November 2026 enhancements before rebuilding any page.
