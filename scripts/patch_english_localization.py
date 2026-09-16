from pathlib import Path

p = Path('scripts/build_english_mirror.py')
s = p.read_text(encoding='utf-8')

s = s.replace(
    "    # Preserve the Hebrew page's RTL layout direction so the English design is visually identical.\n    # English characters still render left-to-right naturally inside their text runs.\n",
    "    # English keeps the same Stitch components, spacing and imagery, but uses natural LTR flow.\n    # Fine-grained English-only CSS handles longer copy without changing the Hebrew master.\n"
)
s = s.replace("'dir=\"rtl\"'", "'dir=\"ltr\"'")

old = '''    out = out.replace('href="enhancements.css"', 'href="../enhancements.css"')
    out = out.replace('src="enhancements.js"', 'src="../enhancements.js"')
    out = out.replace('src="assets/', 'src="../assets/')
    out = out.replace('href="assets/', 'href="../assets/')

    # Do NOT alter layout classes such as text-right/text-left: the English page must retain
    # the same visual composition as the Hebrew Stitch master.
    return out
'''

new = '''    out = out.replace('href="enhancements.css"', 'href="../enhancements.css"')
    out = out.replace('src="enhancements.js"', 'src="../enhancements.js"')
    out = out.replace('src="assets/', 'src="../assets/')
    out = out.replace('href="assets/', 'href="../assets/')

    # English-specific layout polish: preserve the design system while giving English natural LTR flow.
    out = out.replace('href="../enhancements.css" rel="stylesheet"/>', 'href="../enhancements.css" rel="stylesheet"/>\\n<link href="../english.css" rel="stylesheet"/>')
    out = out.replace('<body class="', '<body class="gt-en-page ', 1)
    out = out.replace('text-right', 'text-left')

    # The homepage hero and trust badges need a little more room for English copy.
    if filename == 'index.html':
        out = out.replace('max-w-3xl text-white">', 'max-w-4xl text-white gt-en-hero-copy">', 1)
        out = out.replace('grid grid-cols-2 sm:grid-cols-4 gap-4 text-white/90', 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-white/90', 1)
        out = out.replace('>arrow_back<', '>arrow_forward<', 1)

    return out
'''

if old not in s:
    raise SystemExit('Expected generator block not found; refusing to patch blindly')
s = s.replace(old, new)
p.write_text(s, encoding='utf-8')
print('Patched English mirror generator for natural LTR localization')
