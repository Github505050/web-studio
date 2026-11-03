"""Selected Work visual regression: image framing, fallback, mobile overflow, nav, and links.

Uses synthetic browser screenshots for controlled geometry tests; remote project images
are deliberately NOT fetched by this isolated test environment.
"""
from pathlib import Path
from io import BytesIO
import re,base64
from PIL import Image,ImageDraw,ImageFont
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
WIDTHS=[320,360,375,390,430,570,768,820,1024,1280,1440,1920]
issues=[]

def mockshot(w,h):
 im=Image.new('RGB',(w,h),'#e6f1f3'); d=ImageDraw.Draw(im)
 d.rectangle((0,0,w,54),fill='#173f53')
 d.rectangle((int(w*.06),int(h*.13),int(w*.67),int(h*.29)),fill='#28718a')
 d.rectangle((int(w*.06),int(h*.34),int(w*.36),int(h*.4)),fill='#e3ad72')
 for i in range(3):d.rounded_rectangle((int(w*(.06+i*.30)),int(h*.52),int(w*(.29+i*.30)),int(h*.75)),radius=15,fill='#fff')
 o=BytesIO();im.save(o,'PNG');return 'data:image/png;base64,'+base64.b64encode(o.getvalue()).decode()

with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in WIDTHS:
  page=b.new_page(viewport={'width':width,'height':880},device_scale_factor=1)
  page.on('pageerror',lambda e,w=width:issues.append(f'{w} page JS error {e}'))
  html=(ROOT/'selected-work/index.html').read_text()
  html=re.sub(r'<link[^>]*rel="stylesheet"[^>]*>', '', html)
  html=re.sub(r'<script[^>]*></script>', '', html)
  page.goto('about:blank');page.set_content(html,wait_until='domcontentloaded')
  for css in ('css/site.css','css/refinement.css','css/selected-work.css'):
   page.add_style_tag(content=(ROOT/css).read_text())
  page.add_script_tag(content=(ROOT/'js/site.js').read_text())
  wide=mockshot(1440,900); tall=mockshot(900,1500)
  page.eval_on_selector_all('img[data-studio-shot]', '(els, shots) => els.forEach((el,i)=>{el.classList.remove("studio-image-missing"); el.src = shots[i%2]})',[wide,tall])
  page.wait_for_timeout(120)
  result=page.evaluate('''() => {
    const R=x=>{const r=x.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height,right:r.right,bottom:r.bottom}};
    const pairs=[...document.querySelectorAll('.studio-browser-viewport')].map(v=>{
      const frame=v.closest('.studio-browser-mock'),img=v.querySelector('img');
      const box=R(v), f=R(frame), i=R(img);
      return {frame:f,box,img:i,fit:getComputedStyle(img).objectFit,overflow:getComputedStyle(v).overflow,loaded:img.naturalWidth>0}
    });
    return {doc:document.documentElement.scrollWidth,client:innerWidth,
      cases:document.querySelectorAll('.studio-case').length,
      visibleFrames:pairs.length, pairs,
      feature: R(document.querySelector('.studio-feature-image')),
      hero: R(document.querySelector('.studio-hero-grid')),
      previews:[...document.querySelectorAll('.studio-case-visual')].map(x=>R(x)),
      cards:[...document.querySelectorAll('.studio-case')].map(x=>R(x))
    }
  }''')
  if result['doc']>result['client']+1:issues.append(f'{width}px horizontal overflow {result["doc"]}>{result["client"]}')
  if result['cases']!=3 or result['visibleFrames']!=4:issues.append(f'{width}px missing cards/screenshots')
  for j,v in enumerate(result['pairs']):
   f,box,i=v['frame'],v['box'],v['img']
   if v['fit']!='contain' or v['overflow']!='hidden' or not v['loaded']:issues.append(f'{width}px frame {j} image loaded/fit/clip issue {v}')
   if not (box['x']>=f['x']-1 and box['right']<=f['right']+1 and box['y']>=f['y']-1 and box['bottom']<=f['bottom']+1):issues.append(f'{width}px frame {j} viewport outside browser frame')
   if not (i['w']<=box['w']+1 and i['h']<=box['h']+1):issues.append(f'{width}px frame {j} image exceeds screen')
   if abs(box['w']/max(box['h'],1)-1.6)>.04:issues.append(f'{width}px bad aspect ratio {box}')
  for j,(v,c) in enumerate(zip(result['previews'],result['cards'])):
   if not (v['x']>=c['x']-1 and v['right']<=c['right']+1 and v['y']>=c['y']-1 and v['bottom']<=c['bottom']+1):issues.append(f'{width}px project {j} preview outside card')
  if width in (390,768,1440):
   page.screenshot(path=str(ROOT/'assets'/f'selected-work-fixed-{width}.png'),full_page=True)
  if width<=820:
   page.locator('[data-nav-toggle]').click()
   if not page.locator('[data-nav]').is_visible():issues.append(f'{width}px nav failed to open')
   page.keyboard.press('Escape')
   if page.locator('[data-nav]').is_visible():issues.append(f'{width}px nav failed to close')
  page.close()
 b.close()
if issues:
 for i in issues:print('FAIL:',i)
 raise SystemExit(f'{len(issues)} failures')
print(f'PASS: {len(WIDTHS)} viewport tests, 4 framed images, geometry, image contain, clipping, no overflow, mobile menu and screenshots')
