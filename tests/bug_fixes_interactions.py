"""Live DOM regression checks for the self-contained Bug Fixes interactive demos."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import re

ROOT = Path(__file__).resolve().parents[2]
SITE_ROOT = ROOT / 'web-studio'
HTML = (SITE_ROOT / 'services/bug-fixes/index.html').read_text()
CSS = (SITE_ROOT / 'css/site.css').read_text()
JS = (SITE_ROOT / 'js/site.js').read_text()
HTML = re.sub(r'<link rel="stylesheet"[^>]+>', '', HTML)
HTML = re.sub(r'<script[^>]*></script>', '', HTML)

def load(page):
    page.goto('about:blank')
    page.set_content(HTML, wait_until='domcontentloaded')
    page.add_style_tag(content=CSS)
    page.add_script_tag(content=JS)

errors=[]
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width in (320,375,390,768,1024,1440):
        page=browser.new_page(viewport={'width':width,'height':900})
        page.on('pageerror',lambda err:errors.append('JS '+str(err)))
        load(page)
        assert page.locator('[data-repair-card]').count()==4
        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),f'overflow {width}'
        if width==1440:
            (ROOT/'web-studio/assets/bug-fix-desktop-preview.png').parent.mkdir(parents=True,exist_ok=True)
            page.screenshot(path=str(ROOT/'web-studio/assets/bug-fix-desktop-preview.png'),full_page=True)
        if width==390:
            page.screenshot(path=str(ROOT/'web-studio/assets/bug-fix-mobile-preview.png'),full_page=True)
        if width==320:
            page.locator('[data-nav-toggle]').click()
            assert page.locator('[data-nav]').is_visible(), 'mobile navigation does not expand'
        page.close()

    page=browser.new_page(viewport={'width':1440,'height':900})
    page.on('pageerror',lambda err:errors.append('JS '+str(err)))
    load(page)
    cards=page.locator('[data-repair-card]')

    # Pricing: deliberately broken state then corrected state
    pricing=cards.nth(0)
    pricing.locator('[data-qty-action="plus"]').click()
    assert pricing.locator('[data-qty]').inner_text()=='3'
    assert pricing.locator('[data-total]').inner_text()=='$60', 'before pricing should be stale'
    pricing.locator('[data-repair="after"]').click()
    assert pricing.locator('[data-total]').inner_text()=='$84', 'after pricing not recalculated'
    pricing.locator('[data-qty-action="minus"]').click()
    assert pricing.locator('[data-total]').inner_text()=='$60'
    pricing.locator('[data-qty-action="minus"]').click()
    assert pricing.locator('[data-total]').inner_text()=='$36'
    pricing.locator('[data-qty-action="minus"]').click()
    assert pricing.locator('[data-qty]').inner_text()=='1', 'quantity minimum should be 1'

    # Filters: combined query + status must work, counts align
    filt=cards.nth(1)
    assert filt.locator('[data-ticket-count]').inner_text()=='4 issues'
    filt.locator('[data-repair="after"]').click()
    assert filt.locator('[data-ticket-count]').inner_text()=='2 issues'
    filt.locator('[data-ticket-filter="resolved"]').click()
    assert filt.locator('[data-ticket-count]').inner_text()=='0 issues'
    filt.locator('[data-ticket-search]').fill('billing')
    assert filt.locator('[data-ticket-count]').inner_text()=='1 issue'
    assert 'Billing table' in filt.locator('[data-ticket-list]').inner_text()
    filt.locator('[data-ticket-search]').fill('no-match')
    assert filt.locator('[data-ticket-count]').inner_text()=='0 issues'

    # Form: never sends a message; gives validation feedback
    form=cards.nth(2)
    form.locator('[data-repair-form] button[type="submit"]').click()
    assert 'generic failure' in form.locator('[data-form-status]').inner_text() or 'vague message' in form.locator('[data-form-status]').inner_text()
    form.locator('[data-repair="after"]').click()
    form.locator('[data-repair-form] button[type="submit"]').click()
    assert form.locator('[data-form-errors] span').count()==3
    form.locator('input[name="name"]').fill('Alex Morgan')
    form.locator('input[name="email"]').fill('alex@company.com')
    form.locator('textarea[name="summary"]').fill('The checkout summary stays out of sync with pricing.')
    form.locator('[data-repair-form] button[type="submit"]').click()
    assert 'Validation passed' in form.locator('[data-form-errors]').inner_text()
    assert 'no message was sent' in form.locator('[data-form-errors]').inner_text()

    # Tabs: toggles only in broken state; corrected state updates panel
    tabs=cards.nth(3)
    tabs.locator('[data-panel-tab="billing"]').click()
    assert tabs.locator('[data-panel-title]').inner_text()=='Overview'
    tabs.locator('[data-repair="after"]').click()
    assert tabs.locator('[data-panel-title]').inner_text()=='Billing'
    tabs.locator('[data-panel-tab="access"]').click()
    assert tabs.locator('[data-panel-title]').inner_text()=='Access'
    assert tabs.locator('[data-panel-tab="access"]').get_attribute('aria-pressed')=='true'
    page.locator('#bugfaqb0').click()
    assert page.locator('#bugfaq0').is_visible()
    browser.close()
if errors:
    raise SystemExit('Browser JS errors: '+ '; '.join(errors))
print('PASS: bug fix page at 320, 375, 390, 768, 1024 and 1440px; pricing, filtering, forms, tabs, FAQ and mobile navigation')
