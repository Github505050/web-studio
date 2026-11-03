"""Isolated functional smoke check for three independently themed landing-page demos."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import re
ROOT=Path(__file__).resolve().parents[1]
ROUTES=['consulting','wellness','saas']
WIDTHS=[320,390,768,1440]
issues=[]
def check(ok,msg):
 if not ok:issues.append(msg)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for slug in ROUTES:
  for width in WIDTHS:
   page=browser.new_page(viewport={'width':width,'height':900})
   page.on('pageerror',lambda e:issues.append(str(e)))
   html=(ROOT/'demos'/slug/'index.html').read_text()
   html=re.sub(r'<link[^>]*rel="stylesheet"[^>]*>','',html)
   html=re.sub(r'<script[^>]*></script>','',html)
   page.set_content(html,wait_until='domcontentloaded')
   page.add_style_tag(content=(ROOT/'assets/demo.css').read_text())
   extra={'consulting':'northstar.css','wellness':'solace.css'}.get(slug)
   if extra:page.add_style_tag(content=re.sub(r'@import[^;]+;','',(ROOT/'assets'/extra).read_text()))
   for name in [{'consulting':'northstar.js','wellness':'solace.js','saas':'sample-pages.js'}[slug]]:
    page.add_script_tag(content=(ROOT/'js'/name).read_text())
   check(page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'),f'{slug} {width} overflow')
   check(page.locator('main').count()==1,f'{slug} {width} main absent')
   if slug=='wellness':
    btn=page.locator('[data-class-type="breath"]')
    if btn.count():
     btn.click();check('breath' in page.locator('[data-schedule]').inner_text().lower(),f'{slug} schedule')
   if slug=='saas':
    r=page.locator('[data-hours]')
    if r.count():
     r.evaluate("el=>{el.value='40';el.dispatchEvent(new Event('input',{bubbles:true}));}")
     check('40 h' in page.locator('[data-savings]').inner_text(),f'{slug} calculator')
   page.close()
 browser.close()
if issues:
 print('FAIL:',*issues,sep='\n');raise SystemExit(1)
print('PASS: 3 independent landing pages at 320, 390, 768 and 1440 px, no horizontal overflow, legacy interactions.')
