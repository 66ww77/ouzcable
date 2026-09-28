# -*- coding: utf-8 -*-
"""Universal page builder: generates a marketing page (same style as solutions/ai-computing)
from a PAGE data module. Reuses CSS/topbar/contact/footer/JS framework from ai-computing.html
and the contact/footer i18n keys from it."""
import json, re, sys

SRC = 'ai-computing.html'

def load_src():
    html = open(SRC, encoding='utf-8').read()
    style = html[html.find('<style>'):html.find('</style>') + 8]
    topbar = html[html.find('<div class="topbar">'):html.find('</div>\n</div>', html.find('<div class="topbar">')) + 15]
    contact = html[html.find('<section class="section" id="contact">'):html.find('</section>', html.find('<section class="section" id="contact">')) + 10]
    footer = html[html.find('<footer>'):html.find('</footer>') + 9]
    applyjs = html[html.find('<script>\nvar I18N'):html.find('</script>', html.find('<script>\nvar I18N')) + 9]
    return style, topbar, contact, footer, applyjs

def extract_common_i18n(html):
    """Extract contact.* + cta.email/phone/whatsapp/telegram + footer.* keys for 11 langs from ai-computing.html"""
    m = re.search(r'var I18N=.*?\n\};', html, re.S)
    js = m.group(0)
    langs = ['en','ru','es','ar','zh','fr','uk','tr','de','pt','mn']
    common_keys = ['cta.email','cta.phone','cta.whatsapp','cta.telegram',
                   'contact.email','contact.phone','contact.whatsapp','contact.telegram',
                   'contact.hq','contact.hqval','contact.web','footer.back','footer.rights']
    out = {}
    for lang in langs:
        start = js.find(f'{lang}:{{')
        end = js.find(f'\n{langs[langs.index(lang)+1]}:{{') if langs.index(lang)+1 < len(langs) else js.find('\nfunction setLang')
        seg = js[start:end]
        d = {}
        for k in common_keys:
            pat = re.search(rf'"{k}":"((?:[^"\\]|\\.)*)"', seg)
            if pat:
                d[k] = pat.group(1).replace('\\"', '"').replace('\\u2019', '\u2019').replace('\\u2018', '\u2018').replace('\\u2014', '\u2014').replace('\\u00e9', '\u00e9').replace('\\u00e8', '\u00e8').replace('\\u00e0', '\u00e0').replace('\\u00ee', '\u00ee').replace('\\u2019', '\u2019').replace('\\u2014', '\u2014')
            else:
                print('MISSING common key', k, 'in', lang)
        out[lang] = d
    return out

def jsval(s):
    return json.dumps(s, ensure_ascii=False)

def build_hero(cfg, d):
    return f'''<section class="hero">
  <div class="container">
    <span class="eyebrow" data-i18n="hero.eyebrow">{d.get('hero.eyebrow','')}</span>
    <h1 data-i18n="hero.title">{d.get('hero.title','')}</h1>
    <div class="sub" data-i18n="hero.sub">{d.get('hero.sub','')}</div>
    <p class="lead" data-i18n="hero.lead">{d.get('hero.lead','')}</p>
    <div class="hero-cta">
      <a class="btn" href="#contact" data-i18n="hero.cta1">{d.get('hero.cta1','')}</a>
      <a class="btn btn-outline" href="{cfg['cta2_href']}" data-i18n="hero.cta2">{d.get('hero.cta2','')}</a>
    </div>
  </div>
</section>'''

def build_cards(sec, d):
    n = int(sec.get('n', 4))
    out = [f'''<section class="section">
  <div class="container">
    <h2 data-i18n="{sec['title']}">{d.get(sec['title'],'')}</h2>
    <p data-i18n="{sec['p']}">{d.get(sec['p'],'')}</p>
    <div class="grid">''']
    for i in range(1, n+1):
        out.append(f'''      <div class="card">
        <div class="num">0{i}</div>
        <div class="t" data-i18n="{sec['c']}{i}t">{d.get(f"{sec['c']}{i}t",'')}</div>
        <div class="d" data-i18n="{sec['c']}{i}d">{d.get(f"{sec['c']}{i}d",'')}</div>
      </div>''')
    out.append('  </div>\n  </div>\n</section>')
    return '\n'.join(out)

def build_table(sec, d):
    cols = sec.get('cols', 2)
    out = [f'''<section class="section">
  <div class="container">
    <h2 data-i18n="{sec['title']}">{d.get(sec['title'],'')}</h2>
    <p data-i18n="{sec['p']}">{d.get(sec['p'],'')}</p>
    <table>''']
    if sec.get('th'):
        ths = []
        for i in range(1, cols+1):
            k = f"{sec['th']}{i}"
            ths.append(f'<th data-i18n="{k}">{d.get(k,"")}</th>')
        out.append('  <tr>' + ''.join(ths) + '</tr>')
    for row in sec['rows']:
        tds = []
        for i, k in enumerate(row):
            tds.append(f'<td data-i18n="{k}">{d.get(k,"")}</td>')
        out.append('  <tr>' + ''.join(tds) + '</tr>')
    out.append('  </table>\n  </div>\n</section>')
    return '\n'.join(out)

def build_steps(sec, d):
    out = [f'''<section class="section">
  <div class="container">
    <h2 data-i18n="{sec['title']}">{d.get(sec['title'],'')}</h2>
    <p data-i18n="{sec['p']}">{d.get(sec['p'],'')}</p>
    <div class="steps">''']
    for i in range(1, sec.get('n',5)+1):
        out.append(f'''      <div class="step"><div class="t" data-i18n="{sec['s']}{i}t">{d.get(f"{sec['s']}{i}t",'')}</div><div class="d" data-i18n="{sec['s']}{i}d">{d.get(f"{sec['s']}{i}d",'')}</div></div>''')
    out.append('  </div>\n  </div>\n</section>')
    return '\n'.join(out)

def build_highlight(sec, d):
    return f'''<section class="section">
  <div class="container">
    <h2 data-i18n="{sec['title']}">{d.get(sec['title'],'')}</h2>
    <div class="highlight-box" data-i18n="{sec['p']}">{d.get(sec['p'],'')}</div>
  </div>
</section>'''

def build_faq(sec, d):
    out = [f'''<section class="section">
  <div class="container">
    <h2 data-i18n="{sec['title']}">{d.get(sec['title'],'')}</h2>''']
    for i in range(1, sec.get('n',5)+1):
        out.append(f'''    <div class="faq-item">
      <div class="q" data-i18n="faq.q{i}">{d.get(f'faq.q{i}','')}</div>
      <div class="a" data-i18n="faq.a{i}">{d.get(f'faq.a{i}','')}</div>
    </div>''')
    out.append('  </div>\n</section>')
    return '\n'.join(out)

def build_body(cfg, d):
    parts = []
    for sec in cfg['sections']:
        t = sec['type']
        if t == 'hero': parts.append(build_hero(cfg, d))
        elif t == 'cards': parts.append(build_cards(sec, d))
        elif t == 'table': parts.append(build_table(sec, d))
        elif t == 'steps': parts.append(build_steps(sec, d))
        elif t == 'highlight': parts.append(build_highlight(sec, d))
        elif t == 'faq': parts.append(build_faq(sec, d))
    return '\n'.join(parts)

def build(cfg, data_module):
    style, topbar, contact, footer, applyjs = load_src()
    common = extract_common_i18n(load_src()[0] and open(SRC, encoding='utf-8').read())
    langs = ['en','ru','es','ar','zh','fr','uk','tr','de','pt','mn']

    # merge per-page i18n with common
    merged = {}
    for lang in langs:
        d = dict(data_module.I18N.get(lang, {}))
        d.update(common[lang])
        merged[lang] = d

    # head
    alt = ''.join(f'<link rel="alternate" hreflang="{l}" href="https://ouzcable.com/{cfg["file"]}?lang={l}">\n' for l in langs)
    head = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{cfg['title']}</title>
<meta name="description" content="{cfg['desc']}">
<meta name="keywords" content="{cfg['keywords']}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="OUZHI Cable">
<link rel="canonical" href="https://ouzcable.com/{cfg['file']}">
{alt}<link rel="alternate" hreflang="x-default" href="https://ouzcable.com/{cfg['file']}">
<link rel="icon" type="image/png" href="favicon.png">
'''
    head += style
    head += '</head>\n<body>\n'

    body = build_body(cfg, data_module.I18N['en'])

    # I18N JS
    i18n_parts = []
    for lang in langs:
        pairs = [f'"{k}":{jsval(v)}' for k, v in merged[lang].items()]
        i18n_parts.append(f'{lang}:{{\n' + ',\n'.join(pairs) + '\n}')
    i18n_js = 'var I18N={\n' + ',\n'.join(i18n_parts) + '\n};\n'
    new_script = '<script>\n' + i18n_js + applyjs[applyjs.find('function setLang'):]

    ld = f'''<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":"{cfg['ld_headline']}","url":"https://ouzcable.com/{cfg['file']}","author":{{"@type":"Organization","name":"OUZHI Cable","alternateName":"欧智电缆"}},"publisher":{{"@type":"Organization","name":"OUZHI Cable","logo":"https://ouzcable.com/logo-en.png"}},"description":"{cfg['ld_desc']}","mainEntity":{{"@type":"Organization","name":"OUZHI Cable","email":"info@ouzcable.com","telephone":"+998998516999"}}}}
</script>'''

    page = head + topbar + '\n' + body + contact + '\n' + footer + '\n' + new_script + '\n' + ld + '\n</body>\n</html>\n'
    out = cfg['file']
    open(out, 'w', encoding='utf-8').write(page)
    print('written', out, len(page), 'bytes')

if __name__ == '__main__':
    mod = sys.argv[1].replace('.py', '')
    import importlib.util
    spec = importlib.util.spec_from_file_location(mod, sys.argv[1])
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    build(m.CFG, m)
