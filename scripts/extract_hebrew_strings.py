from pathlib import Path
import re

PAGES = [
    'index.html','spa.html','ice-bath.html','workshops.html',
    'healthy-bar.html','about.html','gallery.html','contact.html'
]

hebrew = re.compile(r'[\u0590-\u05FF]')
strings = []
seen = set()

for page in PAGES:
    text = Path(page).read_text(encoding='utf-8')
    # Text nodes between tags
    for m in re.finditer(r'>([^<>]+)<', text, flags=re.S):
        raw = m.group(1)
        clean = re.sub(r'\s+', ' ', raw).strip()
        if clean and hebrew.search(clean) and clean not in seen:
            seen.add(clean)
            strings.append((page, clean))
    # Common visible attributes
    for attr in ('alt','title','placeholder','aria-label','content'):
        for m in re.finditer(rf'{attr}="([^"]+)"', text):
            clean = re.sub(r'\s+', ' ', m.group(1)).strip()
            if clean and hebrew.search(clean) and clean not in seen:
                seen.add(clean)
                strings.append((page, clean))

out = []
for i,(page,s) in enumerate(strings,1):
    out.append(f'{i:04d}\t{page}\t{s}')
Path('hebrew-strings.txt').write_text('\n'.join(out)+'\n', encoding='utf-8')
print(f'Extracted {len(strings)} unique Hebrew strings')
