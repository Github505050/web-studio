"""Isolated Chromium QA for the November 2026 studio redesign. CSS/JS injected locally; external image and live Pages requests are not validated."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
import re
from bs4 import BeautifulSoup
BASE='http://127.0.0.1:8012/web-studio'
ROUTES=['','services/landing-pages/','services/bug-fixes/','services/chatbots/','services/email-signatures/','live-demos/','selected-work/','about/','faq/',]
WIDTHS=[320,375,390,430,768,1024,1440]
issues=[]
root=Path(__file__).resolve().parents[1]
def check(condition,msg):
 if not condition:issues.append(msg)
def load(page,route):
 file = root / route / 'index.html' if route else root / 'index.html'
 content=file.read_text(encoding='utf-8')
 content=re.sub(r'<link[^>]*rel="stylesheet"[^>]*>', '', content)
 content=re.sub(r'<script[^>]*></script>', '', content)
 page.goto('about:blank')
 page.set_content(content, wait_until='domcontentloaded')
 demo=route.startswith('demos/')
 page.add_style_tag(content=(root / ('assets/demo.css' if demo else 'css/site.css')).read_text())
 if demo:
  name=route.split('/')[1]
  extra={'consulting':'assets/northstar.css','wellness':'assets/solace.css'}.get(name)
  if extra:page.add_style_tag(content=(root/extra).read_text())
 else:
  page.add_style_tag(content=(root/'css/refinement.css').read_text())
 scripts= (['js/sample-pages.js'] if demo else ['js/site.js']+(['js/showcase.js'] if route=='live-demos/' else [])+(['js/chatbot.js'] if route=='services/chatbots/' else [])+(['js/signature.js'] if route=='services/email-signatures/' else []))
 if demo:
  scripts += [('js/northstar.js' if name=='consulting' else 'js/solace.js') ] if name in ['consulting','wellness'] else []
 for script in scripts:
  js=(root/script).read_text()
  js=re.sub(r'\nexport \{[^}]*};\s*$', '', js)
  page.add_script_tag(content=js)

with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in WIDTHS:
  for route in ROUTES:
   page=browser.new_page(viewport={'width':width,'height':880},device_scale_factor=1)
   page.on('pageerror', lambda e,w=width:issues.append('JS '+str(w)+' '+str(e)))
   load(page,route)
   page.wait_for_timeout(80)
   check(True,f'{width} {route} loaded')
   try:
    scroll=page.evaluate('document.documentElement.scrollWidth')
    inner=page.evaluate('window.innerWidth')
    check(scroll<=inner+1,f'{width} {route} overflow {scroll} vs {inner}')
    check(page.locator('main').count()==1,f'{width} {route} missing/duplicate main')
    if route in ['selected-work/','live-demos/','services/chatbots/','services/email-signatures/']:
     check(page.evaluate('document.styleSheets.length >= 2'),f'{width} {route} no styling')
    if width==390 and route in ['selected-work/','live-demos/','services/chatbots/','services/email-signatures/']:
     page.screenshot(path=str(root/'assets'/('studio-'+route.strip('/').replace('/','-')+'-mobile.png')),full_page=True)
    if width==1440 and route in ['selected-work/','live-demos/','services/chatbots/','services/email-signatures/']:
     page.screenshot(path=str(root/'assets'/('studio-'+route.strip('/').replace('/','-')+'-desktop.png')),full_page=True)
   except Exception as e:issues.append(f'{width} {route} '+str(e))
   page.close()
 page=browser.new_page(viewport={'width':1440,'height':900},accept_downloads=True)
 page.on('pageerror',lambda e:issues.append('flow JS '+str(e)))
 load(page,'live-demos/')
 page.locator('[data-filter="chat"]').click()
 check(page.locator('[data-category="chat"]').is_visible(),'chat demo filter visible')
 check(page.locator('[data-category="landing"]').first.is_hidden(),'landing hidden after chat filter')
 check(page.locator('[data-demo-count]').inner_text()=='1 demonstration','filtered count correct')
 check(page.locator('[data-preview-link]').get_attribute('href')=='/web-studio/services/chatbots/','filter selects chat demo')
 page.locator('[data-filter="all"]').click()
 page.locator('[data-demo-url="/web-studio/demos/wellness/"] [data-preview-demo]').click()
 check('Solace' in page.locator('[data-preview-title]').inner_text(),'select demo title')
 check(page.locator('[data-preview-iframe]').get_attribute('src')=='/web-studio/demos/wellness/','iframe src selection')
 page.locator('[data-demo-device="mobile"]').click()
 check(page.locator('[data-device-frame]').get_attribute('data-device-frame')=='mobile','mobile preview mode')
 load(page,'services/chatbots/')
 check(page.locator('[data-chat-log]').count()==1,'chat loaded')
 page.locator('[data-chat-input]').fill('How long is shipping?')
 page.locator('[data-chat-form] button').click()
 check('3–5 business days' in page.locator('[data-chat-log]').inner_text(),'retail shipping answer')
 page.locator('[data-context-button="education"]').click()
 check(page.locator('[data-chat-context]').input_value()=='education','education context sync')
 page.locator('[data-chat-input]').fill('Do you track progress?')
 page.locator('[data-chat-form] button').click()
 check('progress tracking' in page.locator('[data-chat-log]').inner_text().lower(),'education progress answer')
 page.locator('[data-chat-unsupported]').click()
 check("reliable answer" in page.locator('[data-chat-log]').inner_text().lower(),'unsupported answer fallback')
 page.locator('[data-chat-reset]').click()
 check(page.locator('.message.user').count()==0,'chat reset')
 load(page,'services/email-signatures/')
 page.locator('[data-signature-form] [name="name"]').fill('Casey Demo')
 page.locator('[data-signature-form] [name="website"]').fill('mycompany.org')
 page.locator('[data-signature-form] [name="accent"]').select_option('bronze')
 page.locator('[data-signature-toggle]').click()
 code=page.locator('[data-signature-code]').inner_text()
 check('Casey Demo' in code,'signature edit name')
 check('https://mycompany.org' in code,'signature website link configurable')
 check('#a27a4a' in code,'signature accent selected')
 page.locator('[data-signature-form] [name="website"]').fill('javascript:alert(1)')
 code=page.locator('[data-signature-code]').inner_text()
 check('javascript:' not in code,'signature URL injection blocked')
 page.locator('[data-signature-form] [name="name"]').fill('<script>alert(1)</script>')
 check('&lt;script&gt;' in page.locator('[data-signature-code]').inner_text(),'signature html escaped')
 page.locator('[data-style-option="corporate"]').click()
 check('sample-logo.png' in page.locator('[data-signature-code]').inner_text(),'corporate style')
 page.locator('[data-style-option="modern"]').click()
 check('sample-avatar.png' in page.locator('[data-signature-code]').inner_text(),'modern style')
 with page.expect_download(timeout=10000) as info:page.locator('[data-signature-download]').click()
 check(info.value.suggested_filename=='sample-email-signature.html','signature download name')
 load(page,'services/bug-fixes/')
 check(page.locator('[data-repair-card]').count()==4,'bug examples retained')
 first=page.locator('[data-repair-card]').first
 first.locator('[data-repair="after"]').click()
 first.locator('[data-qty-action="plus"]').click()
 check('$84' in first.locator('[data-total]').inner_text(),'pricing repair still works')
 load(page,'selected-work/')
 check(page.locator('.studio-case').count()==3,'3 real project cards')
 check(page.locator('.studio-limit').count()==3,'3 clear scope notes')
 load(page,'faq/')
 page.locator('.faq-item button').first.click()
 check(page.locator('.faq-answer').first.is_visible(),'faq accordion')
 load(page,'services/landing-pages/')
 page.locator('[data-demo-picker]').select_option('/web-studio/demos/saas/')
 check(page.locator('[data-demo-open]').get_attribute('href')=='/web-studio/demos/saas/','landing picker retained')
 page.close()
 # real mobile navigation and minimum touch targets for key actions
 for width in (320,390):
  page=browser.new_page(viewport={'width':width,'height':844})
  for route in ['selected-work/','live-demos/','services/chatbots/','services/email-signatures/']:
   load(page,route)
   page.locator('[data-nav-toggle]').click()
   check(page.locator('[data-nav]').is_visible(),f'{width} {route} mobile menu')
   page.locator('[data-nav-toggle]').click()
   check(not page.locator('[data-nav]').is_visible(),f'{width} {route} mobile menu close')
  page.close()
 browser.close()
if issues:
 print('FAIL',len(issues))
 for x in issues:print(x)
 raise SystemExit(1)
print('PASS:',len(WIDTHS)*len(ROUTES),'isolated-browser viewport/page checks, no horizontal overflow, 4 redesigned page screenshots in 2 sizes, interactive demo filters, full preview, chat contexts/fallback, signature validation/security/export, legacy bug fixes and mobile navigation.')
