"""Lightweight smoke suite. Run studio_qa.py and demo_qa.py separately for full coverage."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
ROOT=Path(__file__).resolve().parents[1]
ROUTES=['','selected-work/','live-demos/','services/chatbots/','services/email-signatures/','services/bug-fixes/']
issues=[]
with sync_playwright() as playwright:
 browser=playwright.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for route in ROUTES:
  page=browser.new_page(viewport={'width':390,'height':844})
  html=(ROOT/route/'index.html' if route else ROOT/'index.html').read_text()
  html=re.sub(r'<link[^>]*rel="stylesheet"[^>]*>','',html)
  html=re.sub(r'<script[^>]*></script>','',html)
  page.set_content(html,wait_until='domcontentloaded')
  page.add_style_tag(content=(ROOT/'css/site.css').read_text())
  page.add_style_tag(content=(ROOT/'css/refinement.css').read_text())
  if page.evaluate('document.documentElement.scrollWidth > innerWidth+1'):issues.append(route+' overflow')
  if page.locator('main').count()!=1:issues.append(route+' missing main')
  page.close()
 browser.close()
if issues:
 print('FAIL',issues);raise SystemExit(1)
print('PASS: 6 primary routes checked for mobile overflow and main content.')
