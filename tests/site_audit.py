from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from xml.etree import ElementTree
import subprocess,re
base=Path(__file__).resolve().parent.parent
class Scan(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.titles=0;self.descriptions=0;self.main=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='title':self.titles+=1
  if tag=='main':self.main+=1
  if tag=='meta' and a.get('name')=='description':self.descriptions+=1
  for key in ('href','src'):
   if key in a:self.links.append((tag,key,a[key]))
errs=[]
for file in sorted(base.rglob('*.html')):
 scan=Scan();scan.feed(file.read_text())
 if scan.titles!=1 or scan.descriptions!=1:errs.append(f'{file}: title/meta description invalid')
 if scan.main!=1:errs.append(f'{file}: main region count {scan.main}')
 for tag,attr,url in scan.links:
  if url.startswith('https://') or url.startswith('http://') or url.startswith('mailto:') or url.startswith('tel:') or url.startswith('#') or url.startswith('data:'):continue
  if url.startswith('//'):continue
  path=urlsplit(url).path
  if not path:continue
  if path.startswith('/web-studio/'):
   target=base/unquote(path.removeprefix('/web-studio/'))
  elif path.startswith('/'):
   errs.append(f'{file}: unexpected root path {url}');continue
  else:target=file.parent/unquote(path)
  if target.is_dir():target=target/'index.html'
  if not target.exists():errs.append(f'{file}: missing {url}')
for file in sorted((base/'js').glob('*.js')):
 r=subprocess.run(['node','--check',str(file)],capture_output=True,text=True)
 if r.returncode:errs.append(f'{file}: {r.stderr.strip()}')
ElementTree.parse(base/'sitemap.xml')
print(f'Found {len(list(base.rglob("*.html")))} pages and {len(list((base/"js").glob("*.js")))} script files.')
if errs:print('\n'.join(errs));raise SystemExit(f'FAIL: {len(errs)} problems')
print('PASS: page metadata, local links, sitemap XML and JS syntax')
