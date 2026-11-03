from pathlib import Path
from playwright.sync_api import sync_playwright
import re
root=Path(__file__).resolve().parents[1]
errors=[]
def load(page,route):
    page.goto('about:blank')
    fn=root/route/'index.html' if route else root/'index.html'
    html=fn.read_text()
    html=re.sub(r'<link rel="stylesheet"[^>]+>', '', html)
    html=re.sub(r'<script[^>]*></script>', '', html)
    page.set_content(html,wait_until='domcontentloaded')
    demo=route.startswith('demos/')
    page.add_style_tag(content=(root/('assets/demo.css' if demo else 'css/site.css')).read_text())
    for script in (['js/sample-pages.js'] if demo else ['js/site.js']+(['js/chatbot.js'] if route=='services/chatbots/' else [])+(['js/signature.js'] if route=='services/email-signatures/' else [])):
        js=(root/script).read_text()
        js=re.sub(r'\nexport \{[^}]*};\s*$', '', js)
        page.add_script_tag(content=js)
with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for width in [320,375,390,768,1024,1440]:
   page=browser.new_page(viewport={'width':width,'height':900},device_scale_factor=1)
   page.on('pageerror',lambda error:errors.append(str(error)))
   for route in ['', 'services/landing-pages/', 'services/bug-fixes/', 'services/chatbots/','services/email-signatures/','live-demos/','selected-work/','about/','faq/','demos/consulting/','demos/wellness/','demos/saas/']:
    load(page,route)
    page.wait_for_timeout(80)
    over=page.evaluate('document.documentElement.scrollWidth > window.innerWidth + 1')
    if over:errors.append(f'Horizontal overflow {route} width {width} scroll {page.evaluate("document.documentElement.scrollWidth")}')
    if not page.locator('main').count():errors.append(f'no main {route}')
    if width==1440 and route.startswith('demos/'):
     page.screenshot(path=str(root/'assets'/('demo-'+route.split('/')[1]+'.png')),full_page=False)
   page.close()
  page=browser.new_page(viewport={'width':1440,'height':900},accept_downloads=True)
  page.on('pageerror',lambda error:errors.append('JS '+str(error)))
  load(page,'services/landing-pages/')
  page.locator('[data-device="mobile"]').click()
  assert page.locator('[data-preview-frame]').get_attribute('data-device')=='mobile'
  page.locator('[data-demo-picker]').select_option('/web-studio/demos/saas/')
  assert page.locator('[data-demo-open]').get_attribute('href')=='/web-studio/demos/saas/'
  load(page,'services/bug-fixes/')
  assert page.locator('[data-repair-card]').count()==4
  first=page.locator('[data-repair-card]').first
  first.locator('[data-repair="after"]').click()
  assert 'is-before' not in first.locator('[data-repair-scene]').get_attribute('class')
  js=page.locator('[data-repair-card]').nth(2)
  js.locator('[data-repair="after"]').click()
  js.locator('[data-bug-action]').click()
  assert 'Success' in js.locator('[data-bug-output]').inner_text()
  load(page,'services/chatbots/')
  page.locator('[data-chat-input]').fill('What is your return policy?')
  page.locator('[data-chat-form] button').click()
  assert '30 days' in page.locator('[data-chat-log]').inner_text()
  page.locator('[data-chat-context]').select_option('education')
  page.locator('[data-chat-input]').fill('Do you track progress?')
  page.locator('[data-chat-form] button').click()
  assert 'progress' in page.locator('[data-chat-log]').inner_text().lower()
  load(page,'services/email-signatures/')
  page.locator('[data-signature-form] [name="name"]').fill('Sam Demo')
  page.locator('[data-signature-toggle]').click()
  assert 'Sam Demo' in page.locator('[data-signature-code]').inner_text()
  page.locator('[data-signature-form] [name="style"]').select_option('modern')
  assert 'sample-avatar.png' in page.locator('[data-signature-code]').inner_text()
  with page.expect_download() as download_info:page.locator('[data-signature-download]').click()
  assert download_info.value.suggested_filename=='sample-email-signature.html'
  load(page,'live-demos/')
  page.locator('[data-filter="chat"]').click()
  assert page.locator('[data-category="chat"]').is_visible()
  assert page.locator('[data-category="landing"]').first.is_hidden()
  load(page,'demos/wellness/')
  page.locator('[data-class-type="breath"]').click()
  assert 'Guided breathwork' in page.locator('[data-schedule]').inner_text()
  load(page,'demos/saas/')
  page.locator('[data-hours]').evaluate("el => {el.value='40';el.dispatchEvent(new Event('input',{bubbles:true}))}")
  assert '40 h' in page.locator('[data-savings]').inner_text()
  load(page,'')
  page.locator('.faq-item button').first.click()
  assert page.locator('.faq-answer').first.is_visible()
  page.evaluate('window.scrollTo(0,0)')
  page.screenshot(path=str(root/'assets'/'homepage-screenshot.png'),full_page=True)
  page=browser.new_page(viewport={'width':390,'height':844})
  load(page,'')
  page.locator('[data-nav-toggle]').click()
  assert page.locator('[data-nav]').is_visible()
  page.locator('[data-nav-toggle]').click()
  page.screenshot(path=str(root/'assets'/'mobile-home-screenshot.png'),full_page=True)
  browser.close()
if errors:print('\n'.join(errors));raise SystemExit('FAILED: '+str(len(errors))+' browser issues')
print('PASS: 12 isolated pages at 6 widths, no overflow, home nav/FAQ, demo preview, bug toggles, chatbot, signature export, filters, wellness schedule and SaaS calculator')
