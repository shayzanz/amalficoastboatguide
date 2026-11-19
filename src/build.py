#!/usr/bin/env python3
"""Static site generator for amalficoastboatguide.com.

Usage:  python3 build.py            -> writes ../site/ (upload that folder with Netlify Drop)

All content lives in content/<lang>.py. Shared facts (routes, prices, scores)
live in data.py so every language shows the same numbers.
"""
import html, importlib, json, os, re, shutil, sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from data import (DOMAIN, SITE_NAME, GYG_PID, GA4_ID, VIATOR_PID, VIATOR_MCID, WHATSAPP,
                  INDEXNOW_KEY, OWNER_NAME, OWNER_EMAIL, STOPS, TOURS, GUIDES,
                  PARTNER_ORDER, TOUR_PARTNER, PARTNER_NAME, GYG_TOUR_IDS, VIATOR_WIDGETS, IMAGES,
                  CRITERIA, overall)

OUT = os.path.normpath(os.path.join(HERE, '..', 'site'))
LANGS = os.environ.get('LANGS', 'en,it,es,de,fr').split(',')
DEFAULT = 'en'
TODAY = date.today().isoformat()
MONTHS = {'en': 'January February March April May June July August September October November December',
          'it': 'gennaio febbraio marzo aprile maggio giugno luglio agosto settembre ottobre novembre dicembre',
          'es': 'enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre',
          'de': 'Januar Februar März April Mai Juni Juli August September Oktober November Dezember',
          'fr': 'janvier février mars avril mai juin juillet août septembre octobre novembre décembre'}


def hdate(l):
    d = date.today(); m = MONTHS[l].split()[d.month - 1]
    return {'en': f'{m} {d.year}', 'de': f'{m} {d.year}', 'it': f'{m} {d.year}', 'es': f'{m} de {d.year}', 'fr': f'{m} {d.year}'}[l]
C = {l: importlib.import_module('content.' + l).L for l in LANGS}
LOCALE = {'en': 'en_US', 'it': 'it_IT', 'es': 'es_ES', 'de': 'de_DE', 'fr': 'fr_FR'}
GYG_LOCALE = {'en': 'en-US', 'it': 'it-IT', 'es': 'es-ES', 'de': 'de-DE', 'fr': 'fr-FR'}
GYG_HOST = {'en': 'www.getyourguide.com', 'it': 'www.getyourguide.it', 'es': 'www.getyourguide.es',
            'de': 'www.getyourguide.de', 'fr': 'www.getyourguide.fr'}
LANG_LABEL = {'en': 'English', 'it': 'Italiano', 'es': 'Español', 'de': 'Deutsch', 'fr': 'Français'}

esc = lambda s: html.escape(str(s), quote=True)


# ---------------------------------------------------------------- URLs
def prefix(l):
    return '/' if l == DEFAULT else f'/{l}/'


def url(l, key, item=None):
    s = C[l]['slugs']
    p = prefix(l)
    if key == 'home':
        return p
    if key == 'tour':
        return f"{p}{s['tours']}/{C[l]['tours'][item]['slug']}/"
    if key == 'guide':
        return f"{p}{s['guides']}/{C[l]['guides'][item]['slug']}/"
    if key == 'guides':
        return f"{p}{s['guides']}/"
    return f"{p}{s[key]}/"


def absu(path):
    return f'https://{DOMAIN}{path}'


def gyg_link(l, q, cmp):
    from urllib.parse import quote
    return f"https://{GYG_HOST[l]}/s/?q={quote(q)}&partner_id={GYG_PID}&cmp={quote(cmp)}"


def viator_link(q):
    from urllib.parse import quote
    return (f"https://www.viator.com/searchResults/all?text={quote(q)}"
            f"&pid={VIATOR_PID}&mcid={VIATOR_MCID}&medium=link")


def wa_link(l, extra=''):
    from urllib.parse import quote
    msg = C[l]['ui']['wa_msg'] + (f' ({extra})' if extra else '')
    return f"https://wa.me/{WHATSAPP}?text={quote(msg)}"


# ---------------------------------------------------------------- pieces
def money(l, lo, hi, unit):
    u = C[l]['ui']
    sep = {'en': ',', 'fr': '\u202f'}.get(l, '.')
    n = lambda v: f"{v:,}".replace(',', sep)
    s = f"{n(lo)}–{n(hi)}"
    s = f"€{s}" if l == 'en' else f"{s} €"
    return f"{s} {u['per_person'] if unit == 'pp' else u['per_boat']}"


def dur(l, a, b):
    h = C[l]['ui']['hours']
    return f"{a}–{b} {h}" if a != b else f"{a} {h}"


def score_bar(v):
    return f'<span class="bar"><span style="width:{v*10:.0f}%"></span></span><b>{v:.1f}</b>'


def widget(l, q, cmp, n=3, tour=None):
    u = C[l]['ui']
    ids = GYG_TOUR_IDS.get(tour, '') if tour else ''
    W = VIATOR_WIDGETS.get(l, {})
    vi = W.get(tour) or W.get('default') if tour else W.get('default')
    vi_html = f'<template class="viator-tpl">{vi}</template>' if vi else ''
    return f'''<div class="gyg-wrap" data-q="{esc(q)}" data-cmp="{esc(cmp)}" data-n="{n}" data-ids="{esc(ids)}" data-locale="{GYG_LOCALE[l]}">{vi_html}
  <div class="gyg-consent">
    <p>{u['widget_consent']}</p>
    <button type="button" class="btn btn-primary js-gyg-accept">{u['widget_show']}</button>
    <a class="btn btn-ghost" rel="sponsored nofollow noopener" target="_blank" href="{esc(gyg_link(l, q, cmp))}">{u['open_gyg']}</a>
    <p class="small">{u['via']} GetYourGuide{' · Viator' if vi else ''}</p>
  </div>
</div>'''


def partner_links(l, q, cmp, tid=None):
    ps = [TOUR_PARTNER[tid]] if tid in TOUR_PARTNER else PARTNER_ORDER[:1]
    return [(p, gyg_link(l, q, cmp) if p == 'gyg' else viator_link(q)) for p in ps]


def partner_buttons(l, q, cmp, tid=None):
    u = C[l]['ui']; out = []
    for i, (p, href) in enumerate(partner_links(l, q, cmp, tid)):
        cls = 'btn-primary' if i == 0 else 'btn-secondary'
        label = u['book_now'] if i == 0 else u['compare_prices']
        out.append(f'<a class="btn {cls} btn-partner" rel="sponsored nofollow noopener" target="_blank" href="{esc(href)}">{label}<small>{u["via"]} {PARTNER_NAME[p]}</small></a>')
    return '\n  '.join(out)


def cta_row(l, t, cmp):
    u = C[l]['ui']
    q = t['q']
    return f'''<div class="cta-row">
  {partner_buttons(l, q, cmp, t['id'])}
  <a class="btn btn-wa" rel="noopener" target="_blank" href="{esc(wa_link(l, C[l]['tours'][t['id']]['name']))}">{u['ask_wa']}</a>
</div>'''


def img_src(e):
    s = e['src']
    return s if s.startswith('http') else '/assets/' + s


def credit_html(e):
    return ''  # credits listed on the privacy page instead


def _credit_inline(e):
    c = esc(e['credit'])
    return f'<span class="credit">© <a href="{esc(e["link"])}" rel="nofollow noopener" target="_blank">{c}</a></span>' if e.get('link') else f'<span class="credit">© {c}</span>'


def photo_attrs(tid):
    e = IMAGES['tours'].get(tid)
    i = [x['id'] for x in TOURS].index(tid) % 4
    cls = f'ph ph-{i}' if not e else ''
    style = f' style="background-image:url(\'{esc(img_src(e))}\')"' if e else ''
    return cls, style, e


def tour_card(l, t):
    u = C[l]['ui']
    tt = C[l]['tours'][t['id']]
    tags = [u['private'] if t['private'] else u['shared']]
    if t['capri']:
        tags.append('Capri')
    if t['grotto']:
        tags.append(C[l]['stops']['grotto'])
    tags_html = ''.join(f'<span class="tag">{esc(x)}</span>' for x in tags)
    cls, style, _ = photo_attrs(t['id'])
    return f'''<article class="card">
  <a class="card-img {cls}"{style} href="{url(l, 'tour', t['id'])}" aria-label="{esc(tt['name'])}"><span class="score" title="{u['our_score']}">{overall(t):.1f}</span></a>
  <div class="card-body">
  <div class="card-top">{tags_html}</div>
  <h3><a href="{url(l, 'tour', t['id'])}">{esc(tt['name'])}</a></h3>
  <p>{esc(tt['short'])}</p>
  <ul class="facts">
    <li><span>{u['from']}</span>{esc(', '.join(C[l]['stops'][d] for d in t['from']))}</li>
    <li><span>{u['duration']}</span>{dur(l, *t['hours'])}</li>
    <li><span>{u['typical_price']}</span>{money(l, *t['price'])}</li>
  </ul>
  <a class="btn btn-ghost" href="{url(l, 'tour', t['id'])}">{u['details']}</a>
  </div>
</article>'''


def route_svg(route):
    lats = [r['lat'] for r in route]; lngs = [r['lng'] for r in route]
    a, b_, c, d = min(lats), max(lats), min(lngs), max(lngs)
    W, H, P = 600, 340, 40
    sx = (W - 2 * P) / max(d - c, 1e-6); sy = (H - 2 * P) / max(b_ - a, 1e-6); s = min(sx, sy * 1.3)
    ox = (W - (d - c) * s) / 2; oy = (H - (b_ - a) * s / 1.3) / 2
    xy = lambda r: (ox + (r['lng'] - c) * s, H - (oy + (r['lat'] - a) * s / 1.3))
    pts = ' '.join(f'{x:.1f},{y:.1f}' for x, y in map(xy, route))
    dots, seen = '', set()
    for r in route:
        if r['stop'] and r['name'] not in seen:
            seen.add(r['name']); x, y = xy(r)
            dots += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="#fff" stroke="#0b4f6c" stroke-width="3"/><text x="{x+9:.1f}" y="{y-8:.1f}" font-size="13" fill="#083344">{esc(r["name"])}</text>'
    return (f'<svg class="route-svg" viewBox="0 0 {W} {H}" role="img"><rect width="{W}" height="{H}" fill="#cfe9f2"/>'
            f'<polyline points="{pts}" fill="none" stroke="#e76f51" stroke-width="3" stroke-dasharray="8 6"/>{dots}</svg>')


def faq_html(l, faqs):
    u = C[l]['ui']
    items = ''.join(f'<details><summary>{esc(q)}</summary><div>{a}</div></details>' for q, a in faqs)
    return f'<section class="faq"><h2>{u["faq"]}</h2>{items}</section>'


def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": re.sub('<[^>]+>', '', re.sub(r'\{[^}]+\}', '', a))}} for q, a in faqs]}


def breadcrumbs(l, trail):
    u = C[l]['ui']
    full = [(u['home'], url(l, 'home'))] + trail
    vis = ' <span>/</span> '.join(
        f'<a href="{p}">{esc(n)}</a>' if i < len(full) - 1 else f'<span aria-current="page">{esc(n)}</span>'
        for i, (n, p) in enumerate(full))
    sch = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": absu(p)} for i, (n, p) in enumerate(full)]}
    return f'<nav class="crumbs" aria-label="breadcrumb">{vis}</nav>', sch


# ---------------------------------------------------------------- layout
def links(l, s):
    s = re.sub(r'\{(tour|guide):([\w-]+)\}', lambda m: url(l, m.group(1), m.group(2)), s)
    return re.sub(r'\{(best|about|contact|guides|privacy)\}', lambda m: url(l, m.group(1)), s)


def page(l, key, item, title, desc, body, schema=None, og_type='website', noindex=False):
    u = C[l]['ui']
    body = links(l, body)
    path = url(l, key, item) if key != '404' else prefix(l) + '404.html'
    alts = '' if key == '404' else ''.join(
        f'<link rel="alternate" hreflang="{x}" href="{absu(url(x, key, item))}">' for x in LANGS
    ) + f'<link rel="alternate" hreflang="x-default" href="{absu(url(DEFAULT, key, item))}">'
    graph = [
        {"@type": "Organization", "@id": absu('/#org'), "name": SITE_NAME, "url": absu('/'),
         "logo": absu('/apple-touch-icon.png'),
         "contactPoint": {"@type": "ContactPoint", "telephone": "+" + WHATSAPP, "contactType": "customer support",
                          "availableLanguage": ["English", "Italian", "Spanish", "German", "French"]}},
        {"@type": "WebSite", "@id": absu('/#website'), "name": SITE_NAME, "url": absu('/'),
         "inLanguage": l, "publisher": {"@id": absu('/#org')}},
    ] + (schema or [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    nav = ''.join(f'<a href="{url(l, k)}">{esc(u["nav_" + k])}</a>' for k in ['home', 'best', 'guides', 'contact'])
    switch = ''.join(
        f'<a href="{url(x, key, item) if key != "404" else prefix(x)}" hreflang="{x}" lang="{x}"'
        + (' aria-current="true"' if x == l else '') + f'>{x.upper()}</a>' for x in LANGS)
    guides_links = ''.join(f'<li><a href="{url(l, "guide", g["id"])}">{esc(C[l]["guides"][g["id"]]["nav"])}</a></li>'
                           for g in GUIDES)
    lang_links = ''.join(f'<li><a href="{url(x, key, item) if key != "404" else prefix(x)}" lang="{x}">{LANG_LABEL[x]}</a></li>' for x in LANGS)
    robots = 'noindex,follow' if noindex else 'index,follow,max-image-preview:large,max-snippet:-1'
    return path, f'''<!doctype html>
<html lang="{l}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
{'' if key == '404' else f'<link rel="canonical" href="{absu(path)}">'}
{alts}
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{absu(path)}">
<meta property="og:image" content="{absu('/og.jpg')}">
<meta property="og:locale" content="{LOCALE[l]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0b4f6c">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="stylesheet" href="/assets/style.css?v={TODAY}">
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">{u['skip']}</a>
<header class="site-header">
  <div class="wrap header-in">
    <a class="logo" href="{url(l, 'home')}" aria-label="{SITE_NAME}">
      <svg viewBox="0 0 40 40" width="34" height="34" aria-hidden="true"><circle cx="20" cy="20" r="20" fill="#0b4f6c"/><circle cx="28" cy="12" r="5" fill="#f2c94c"/><path d="M8 25h24l-4 6H12z" fill="#fff"/><path d="M19 9v15h-9z" fill="#fff" opacity=".9"/><path d="M4 33c4 0 4-2 8-2s4 2 8 2 4-2 8-2 4 2 8 2" stroke="#7fd1e8" stroke-width="2" fill="none"/></svg>
      <span>Amalfi Coast <b>Boat Guide</b></span>
    </a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mainnav">{u['menu']}</button>
    <nav id="mainnav" class="mainnav">{nav}<span class="langs">{switch}</span></nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap foot-grid">
    <div><p class="logo-text">Amalfi Coast <b>Boat Guide</b></p><p>{u['footer_about']}</p>
      <p class="small">{u['disclosure']} <a href="{url(l, 'about')}">{u['how_we_rate']}</a></p></div>
    <div><h4>{u['nav_guides']}</h4><ul>{guides_links}</ul></div>
    <div><h4>{u['site']}</h4><ul>
      <li><a href="{url(l, 'best')}">{esc(u['nav_best'])}</a></li>
      <li><a href="{url(l, 'about')}">{esc(u['nav_about'])}</a></li>
      <li><a href="{url(l, 'contact')}">{esc(u['nav_contact'])}</a></li>
      <li><a href="{url(l, 'privacy')}">{esc(u['nav_privacy'])}</a></li>
      <li><a href="#" class="js-consent-reset">{esc(u['cookie_settings'])}</a></li></ul>
      <h4>{u['language']}</h4><ul class="inline">{lang_links}</ul></div>
  </div>
  <p class="wrap small copy">© {date.today().year} {SITE_NAME} · {u['updated']} {hdate(l)}</p>
</footer>
<a class="wa-float" href="{esc(wa_link(l))}" target="_blank" rel="noopener" aria-label="WhatsApp">
  <svg viewBox="0 0 32 32" width="28" height="28" aria-hidden="true"><path fill="#fff" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.6c-2 0-4-.6-5.7-1.6l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 1 1 16 26.6zm5.8-7.9c-.3-.2-1.9-.9-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7 0a8.7 8.7 0 0 1-4.3-3.7c-.3-.6.3-.5 1-1.7.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6a1.2 1.2 0 0 0-.9.4 3.7 3.7 0 0 0-1.1 2.7 6.4 6.4 0 0 0 1.3 3.4 14.7 14.7 0 0 0 5.7 5c2.1.9 2.9 1 4 .8a3.4 3.4 0 0 0 2.2-1.6 2.8 2.8 0 0 0 .2-1.6c-.1-.2-.3-.3-.6-.5z"/></svg>
  <span>{u['wa_short']}</span>
</a>
<div class="consent" hidden role="dialog" aria-live="polite" aria-label="cookies">
  <p>{u['consent_text']} <a href="{url(l, 'privacy')}">{u['nav_privacy']}</a></p>
  <div><button type="button" class="btn btn-primary js-consent-yes">{u['consent_yes']}</button>
  <button type="button" class="btn btn-ghost js-consent-no">{u['consent_no']}</button></div>
</div>
<script>window.GYG_PID="{GYG_PID}";window.GA4_ID="{GA4_ID}";</script>
<script src="/assets/site.js?v={TODAY}" defer></script>
</body>
</html>'''


# ---------------------------------------------------------------- pages
def home(l):
    L = C[l]; u = L['ui']; h = L['home']
    data = [{
        'id': t['id'], 'name': L['tours'][t['id']]['name'], 'short': L['tours'][t['id']]['short'],
        'url': url(l, 'tour', t['id']), 'from': t['from'],
        'fromLabel': ', '.join(L['stops'][d] for d in t['from']),
        'private': t['private'], 'capri': t['capri'], 'grotto': t['grotto'], 'kids': t['kids'],
        'h1': t['hours'][0], 'h2': t['hours'][1], 'lo': t['price'][0], 'hi': t['price'][1], 'unit': t['price'][2],
        'img': (img_src(IMAGES['tours'][t['id']]) if IMAGES['tours'].get(t['id']) else ''), 'ph': photo_attrs(t['id'])[0], 'score': round(overall(t), 1), 'price': money(l, *t['price']), 'dur': dur(l, *t['hours']),
        'partners': [[PARTNER_NAME[p], h_] for p, h_ in partner_links(l, t['q'], 'home-compare', t['id'])],
    } for t in TOURS]
    deps = ''.join(f'<option value="{d}">{esc(L["stops"][d])}</option>' for d in ['positano', 'amalfi', 'sorrento', 'capri_port'])
    guides = ''.join(
        f'<a class="guide-tile" href="{url(l, "guide", g["id"])}"><b>{esc(L["guides"][g["id"]]["nav"])}</b><span>{esc(L["guides"][g["id"]]["teaser"])}</span></a>'
        for g in GUIDES)
    body = f'''
<section class="hero{' has-img' if IMAGES.get('hero') else ''}"{(' style="background-image:url(' + chr(39) + esc(img_src(IMAGES['hero'])) + chr(39) + ')"') if IMAGES.get('hero') else ''}>
  {credit_html(IMAGES.get('hero'))}
  <div class="wrap hero-in">
    <p class="eyebrow">{h['eyebrow']}</p>
    <h1>{h['h1']}</h1>
    <p class="lead">{h['lead']}</p>
    <div class="cta-row"><a class="btn btn-primary" href="#compare">{u['compare_now']}</a>
      <a class="btn btn-light" href="{url(l, 'best')}">{u['nav_best']}</a></div>
    <p class="hero-note">{u['updated']} {hdate(l)}</p>
  </div>
</section>
<section id="compare" class="wrap section">
  <h2>{h['compare_h2']}</h2>
  <p>{h['compare_intro']}</p>
  <form class="filters" id="filters" onsubmit="return false">
    <label>{u['from']}<select name="from"><option value="">{u['any']}</option>{deps}</select></label>
    <label>{u['type']}<select name="type"><option value="">{u['any']}</option><option value="private">{u['private']}</option><option value="shared">{u['shared']}</option></select></label>
    <label>{u['max_duration']}<select name="dur"><option value="">{u['any']}</option><option value="3">≤ 3 {u['hours']}</option><option value="6">≤ 6 {u['hours']}</option></select></label>
    <label>{u['sort']}<select name="sort"><option value="score">{u['sort_score']}</option><option value="price">{u['sort_price']}</option><option value="dur">{u['sort_dur']}</option></select></label>
    <label class="chk"><input type="checkbox" name="capri"> {u['f_capri']}</label>
    <label class="chk"><input type="checkbox" name="grotto"> {u['f_grotto']}</label>
    <label class="chk"><input type="checkbox" name="kids"> {u['f_kids']}</label>
  </form>
  <p class="count" id="count" aria-live="polite"></p>
  <div class="grid" id="results"></div>
  <noscript><div class="grid">{''.join(tour_card(l, t) for t in TOURS)}</div></noscript>
  <p class="small">{u['price_note']}</p>
</section>
<section class="band"><div class="wrap section">
  <h2>{h['live_h2']}</h2><p>{h['live_intro']}</p>
  {widget(l, h['live_q'], 'home-widget', 6)}
</div></section>
<section class="wrap section">
  <h2>{h['guides_h2']}</h2>
  <div class="guide-grid">{guides}</div>
</section>
<section class="wrap section prose">
  {h['body']}
</section>
<section class="wrap section">{faq_html(l, h['faq'])}</section>
<section class="wrap section wa-box"><h2>{u['wa_h2']}</h2><p>{u['wa_p']}</p>
  <a class="btn btn-wa" target="_blank" rel="noopener" href="{esc(wa_link(l))}">{u['ask_wa']}</a></section>
<script type="application/json" id="tour-data">{json.dumps(data, ensure_ascii=False)}</script>
<script type="application/json" id="ui-data">{json.dumps({k: u[k] for k in ['from', 'duration', 'typical_price', 'details', 'private', 'shared', 'results', 'no_results', 'our_score', 'book_now', 'compare_prices', 'via']}, ensure_ascii=False)}</script>
<script type="application/json" id="grotto-label">{json.dumps(L['stops']['grotto'], ensure_ascii=False)}</script>'''
    sch = [{"@type": "ItemList", "name": h['compare_h2'], "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": absu(url(l, 'tour', t['id'])), "name": L['tours'][t['id']]['name']}
        for i, t in enumerate(sorted(TOURS, key=overall, reverse=True))]}, faq_schema(h['faq'])]
    return page(l, 'home', None, h['title'], h['desc'], body, sch)


def best(l):
    L = C[l]; u = L['ui']; b = L['best']
    ranked = sorted(TOURS, key=overall, reverse=True)
    crumbs, bsch = breadcrumbs(l, [(u['nav_best'], url(l, 'best'))])
    heads = ''.join(f'<th>{esc(L["criteria"][c])}</th>' for c, _ in CRITERIA)
    rows = ''.join(
        f'<tr><td>{i+1}</td><td><a href="{url(l, "tour", t["id"])}">{esc(L["tours"][t["id"]]["name"])}</a></td>'
        + ''.join(f'<td>{t["scores"][c]}</td>' for c, _ in CRITERIA)
        + f'<td><b>{overall(t):.1f}</b></td></tr>' for i, t in enumerate(ranked))
    blocks = ''
    for i, t in enumerate(ranked):
        tt = L['tours'][t['id']]
        cls, style, e = photo_attrs(t['id'])
        blocks += f'''<article class="rank-item" id="{t['id']}">
  <a class="card-img {cls}"{style} href="{url(l, 'tour', t['id'])}" aria-label="{esc(tt['name'])}"></a>
  <div class="rank-body">
  <h3><span class="rank">#{i+1}</span> {esc(tt['name'])} <span class="score">{overall(t):.1f}</span></h3>
  <p class="verdict"><b>{u['best_for']}:</b> {esc(tt['best_for'])}</p>
  <p>{tt['long']}</p>
  <div class="two"><div><h4>{u['why_we_like']}</h4><ul>{''.join(f'<li>{esc(x)}</li>' for x in tt['highlights'])}</ul></div>
  <div><h4>{u['watch_out']}</h4><ul>{''.join(f'<li>{esc(x)}</li>' for x in tt['watch'])}</ul></div></div>
  <p class="meta">{u['from']}: {esc(', '.join(L['stops'][d] for d in t['from']))} · {dur(l, *t['hours'])} · {money(l, *t['price'])}</p>
  <div class="cta-row"><a class="btn btn-ghost" href="{url(l, 'tour', t['id'])}">{u['details_map']}</a>
  {partner_buttons(l, t['q'], 'best-' + t['id'], t['id'])}</div>
  </div>
</article>'''
    body = f'''<div class="wrap section">{crumbs}
<h1>{b['h1']}</h1><p class="lead">{b['lead']}</p>
<p class="updated">{u['updated']} {hdate(l)} · <a href="{url(l, 'about')}">{u['how_we_rate']}</a></p>
<div class="table-wrap"><table class="rank-table"><thead><tr><th>#</th><th>{u['tour']}</th>{heads}<th>{u['overall']}</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="small">{b['method_short']}</p>
{blocks}
<h2>{b['live_h2']}</h2><p>{b['live_p']}</p>
{widget(l, b['live_q'], 'best-widget', 6)}
<div class="prose">{b['body']}</div>
{faq_html(l, b['faq'])}
</div>'''
    sch = [bsch, {"@type": "ItemList", "name": b['h1'], "itemListOrder": "https://schema.org/ItemListOrderDescending",
                  "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": absu(url(l, 'tour', t['id'])),
                                       "name": L['tours'][t['id']]['name']} for i, t in enumerate(ranked)]},
           {"@type": "Article", "headline": b['h1'], "inLanguage": l, "dateModified": TODAY,
            "author": {"@id": absu('/#org')}, "publisher": {"@id": absu('/#org')}},
           faq_schema(b['faq'])]
    return page(l, 'best', None, b['title'], b['desc'], body, sch, 'article')


def tour_page(l, t):
    L = C[l]; u = L['ui']; tt = L['tours'][t['id']]
    crumbs, bsch = breadcrumbs(l, [(u['nav_best'], url(l, 'best')), (tt['name'], url(l, 'tour', t['id']))])
    route = [dict(STOPS[s], id=s, name=L['stops'].get(s, ''), stop=s in L['stops']) for s in t['route']]
    stops_list = ''.join(f'<li>{esc(r["name"])}</li>' for r in route if r['stop'])
    scores = ''.join(f'<li><span>{esc(L["criteria"][c])}</span>{score_bar(t["scores"][c])}</li>' for c, _ in CRITERIA)
    rel_guides = [g for g in GUIDES if t['id'] in g['tours']][:4]
    rel = ''.join(f'<li><a href="{url(l, "guide", g["id"])}">{esc(L["guides"][g["id"]]["nav"])}</a></li>' for g in rel_guides)
    others = ''.join(tour_card(l, o) for o in TOURS if o['id'] in t['related'])
    pcls, pstyle, pe = photo_attrs(t['id'])
    banner = f'<div class="tour-banner"{pstyle}>{credit_html(pe)}</div>' if pe else ''
    body = f'''<div class="wrap section">{crumbs}
{banner}
<div class="tour-head"><div>
<h1>{esc(tt['name'])}</h1>
<p class="lead">{esc(tt['short'])}</p></div>
<div class="score-big" title="{u['our_score']}"><b>{overall(t):.1f}</b><span>{u['our_score']}</span></div></div>
<section class="photos"><h2>{u['live_options']}</h2><p>{u['live_options_p']}</p>
{widget(l, t['q'], 'tour-' + t['id'], 3, t['id'])}</section>
<div class="tour-grid">
<div>
  <div id="map" class="map" data-route='{json.dumps([[r["lat"], r["lng"], r["name"] if r["stop"] else ""] for r in route], ensure_ascii=False)}' aria-label="{esc(u['map_label'])}">{route_svg(route)}</div>
  <p class="small">{u['map_note']}</p>
  <h2>{u['route']}</h2><ol class="stops">{stops_list}</ol>
  <div class="prose">{tt['long']}</div>
  <div class="two"><div><h3>{u['why_we_like']}</h3><ul>{''.join(f'<li>{esc(x)}</li>' for x in tt['highlights'])}</ul></div>
  <div><h3>{u['watch_out']}</h3><ul>{''.join(f'<li>{esc(x)}</li>' for x in tt['watch'])}</ul></div></div>
</div>
<aside class="side">
  <div class="box"><h2>{u['key_facts']}</h2><ul class="facts">
    <li><span>{u['type']}</span>{u['private'] if t['private'] else u['shared']}</li>
    <li><span>{u['from']}</span>{esc(', '.join(L['stops'][d] for d in t['from']))}</li>
    <li><span>{u['duration']}</span>{dur(l, *t['hours'])}</li>
    <li><span>{u['typical_price']}</span>{money(l, *t['price'])}</li>
    <li><span>{u['best_for']}</span>{esc(tt['best_for'])}</li></ul>
    <p class="small">{u['price_note']}</p>
    {cta_row(l, t, 'tour-' + t['id'])}
  </div>
  <div class="box"><h2>{u['our_rating']}</h2><ul class="scores">{scores}</ul>
    <p class="small"><a href="{url(l, 'about')}">{u['how_we_rate']}</a></p></div>
  {f'<div class="box"><h2>{u["related_guides"]}</h2><ul>{rel}</ul></div>' if rel else ''}
</aside>
</div>
<h2>{u['similar']}</h2><div class="grid">{others}</div>
</div>
<link rel="stylesheet" href="/assets/leaflet/leaflet.css">
<script src="/assets/leaflet/leaflet.js" defer></script>'''
    sch = [bsch, {"@type": "TouristTrip", "name": tt['name'], "description": tt['short'], "inLanguage": l,
                  "touristType": tt['best_for'],
                  "itinerary": {"@type": "ItemList", "itemListElement": [
                      {"@type": "ListItem", "position": i + 1,
                       "item": {"@type": "TouristAttraction", "name": r['name'],
                                "geo": {"@type": "GeoCoordinates", "latitude": r['lat'], "longitude": r['lng']}}}
                      for i, r in enumerate([r for r in route if r['stop']])]},
                  "provider": {"@id": absu('/#org')}}]
    return page(l, 'tour', t['id'], tt['title'], tt['desc'], body, sch, 'article')


def guide_page(l, g):
    L = C[l]; u = L['ui']; gg = L['guides'][g['id']]
    crumbs, bsch = breadcrumbs(l, [(u['nav_guides'], url(l, 'guides')), (gg['nav'], url(l, 'guide', g['id']))])
    cards = ''.join(tour_card(l, t) for t in TOURS if t['id'] in g['tours'])
    others = ''.join(f'<li><a href="{url(l, "guide", o["id"])}">{esc(L["guides"][o["id"]]["nav"])}</a></li>'
                     for o in GUIDES if o['id'] != g['id'])
    body = f'''<div class="wrap section narrow">{crumbs}
<h1>{gg['h1']}</h1>
<p class="lead">{gg['lead']}</p>
<p class="updated">{u['updated']} {hdate(l)} · {u['byline']}</p>
<p class="answer">{gg['answer']}</p>
<div class="prose">{gg['body']}</div>
<h2>{u['tours_for_this']}</h2>
</div>
<div class="wrap"><div class="grid">{cards}</div></div>
<div class="wrap section narrow">
<h2>{u['live_options']}</h2><p>{u['live_options_p']}</p>
{widget(l, g['q'][l] if isinstance(g['q'], dict) else g['q'], 'guide-' + g['id'], 3)}
{faq_html(l, gg['faq'])}
<div class="wa-box"><h2>{u['wa_h2']}</h2><p>{u['wa_p']}</p><a class="btn btn-wa" target="_blank" rel="noopener" href="{esc(wa_link(l, gg['nav']))}">{u['ask_wa']}</a></div>
<h2>{u['more_guides']}</h2><ul class="cols">{others}</ul>
</div>'''
    sch = [bsch, {"@type": "Article", "headline": gg['h1'], "description": gg['desc'], "inLanguage": l,
                  "dateModified": TODAY, "datePublished": TODAY, "image": absu('/og.jpg'),
                  "author": {"@id": absu('/#org')}, "publisher": {"@id": absu('/#org')},
                  "mainEntityOfPage": absu(url(l, 'guide', g['id']))}, faq_schema(gg['faq'])]
    return page(l, 'guide', g['id'], gg['title'], gg['desc'], body, sch, 'article')


def guides_index(l):
    L = C[l]; u = L['ui']; gi = L['guides_index']
    crumbs, bsch = breadcrumbs(l, [(u['nav_guides'], url(l, 'guides'))])
    tiles = ''.join(
        f'<a class="guide-tile" href="{url(l, "guide", g["id"])}"><b>{esc(L["guides"][g["id"]]["nav"])}</b><span>{esc(L["guides"][g["id"]]["teaser"])}</span></a>'
        for g in GUIDES)
    body = f'<div class="wrap section">{crumbs}<h1>{gi["h1"]}</h1><p class="lead">{gi["lead"]}</p><div class="guide-grid">{tiles}</div></div>'
    return page(l, 'guides', None, gi['title'], gi['desc'], body, [bsch])


def simple(l, key):
    L = C[l]; u = L['ui']; p = L[key]
    crumbs, bsch = breadcrumbs(l, [(u['nav_' + key], url(l, key))])
    extra = ''
    if key == 'contact':
        extra = f'<p><a class="btn btn-wa" target="_blank" rel="noopener" href="{esc(wa_link(l))}">{u["ask_wa"]} · +39 393 855 2086</a></p>'
    if key == 'about':
        rows = ''.join(f'<li><b>{esc(L["criteria"][c])}</b> ({int(w*100)}%): {esc(L["criteria_desc"][c])}</li>' for c, w in CRITERIA)
        extra = f'<h2>{u["criteria_h"]}</h2><ul>{rows}</ul>'
    if key == 'privacy':
        H = {'en': 'Photo credits', 'it': 'Crediti foto', 'es': 'Créditos de las fotos', 'de': 'Bildnachweise', 'fr': 'Crédits photo'}
        T = {'en': 'Photos on this site come from Unsplash and are used under the Unsplash License. Thanks to:',
             'it': 'Le foto del sito vengono da Unsplash e sono usate con la licenza Unsplash. Grazie a:',
             'es': 'Las fotos del sitio son de Unsplash y se usan con la licencia de Unsplash. Gracias a:',
             'de': 'Die Fotos auf dieser Seite stammen von Unsplash und werden unter der Unsplash-Lizenz verwendet. Danke an:',
             'fr': "Les photos du site viennent d'Unsplash et sont utilisées sous la licence Unsplash. Merci à :"}
        seen = {}
        for e in [IMAGES.get('hero')] + list(IMAGES['tours'].values()):
            if e and e.get('credit'): seen[e['link']] = e['credit']
        items = ''.join(f'<li><a href="{esc(k)}" rel="nofollow noopener" target="_blank">{esc(v)}</a></li>' for k, v in seen.items())
        extra += f'<h2>{H[l]}</h2><p>{T[l]}</p><ul>{items}</ul>' if items else ''
    bodytxt = p['body'].replace('{OWNER}', esc(OWNER_NAME or SITE_NAME)).replace(
        '{EMAIL}', f'<a href="mailto:{OWNER_EMAIL}">{OWNER_EMAIL}</a>' if OWNER_EMAIL else 'WhatsApp +39 393 855 2086')
    body = f'<div class="wrap section narrow">{crumbs}<h1>{p["h1"]}</h1><div class="prose">{bodytxt}{extra}</div></div>'
    return page(l, key, None, p['title'], p['desc'], body, [bsch], noindex=(key == 'privacy'))


def notfound(l):
    L = C[l]; u = L['ui']
    body = f'<div class="wrap section narrow"><h1>{u["nf_h1"]}</h1><p>{u["nf_p"]}</p><p><a class="btn btn-primary" href="{url(l, "home")}">{u["home"]}</a> <a class="btn btn-ghost" href="{url(l, "best")}">{u["nav_best"]}</a></p></div>'
    return page(l, '404', None, u['nf_h1'] + ' | ' + SITE_NAME, u['nf_p'], body, noindex=True)


# ---------------------------------------------------------------- write
def write(path, content):
    fp = os.path.join(OUT, path.lstrip('/'))
    if fp.endswith('/'):
        fp += 'index.html'
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)


def strip(h):
    h = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', h, flags=re.S)
    h = re.sub(r'<li>', '- ', h)
    h = re.sub(r'</(p|h\d|li|tr|div|section|article|summary)>', '\n', h)
    h = re.sub('<[^>]+>', '', h)
    h = html.unescape(h)
    return re.sub(r'\n\s*\n+', '\n\n', h).strip()


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(HERE, 'assets'), os.path.join(OUT, 'assets'))
    for f in os.listdir(os.path.join(HERE, 'root')):
        shutil.copy(os.path.join(HERE, 'root', f), OUT)
    pages = []  # (key, item)
    for l in LANGS:
        out = [home(l), best(l), guides_index(l), simple(l, 'about'), simple(l, 'contact'), simple(l, 'privacy')]
        out += [tour_page(l, t) for t in TOURS] + [guide_page(l, g) for g in GUIDES]
        for p, h in out:
            write(p, h)
        p, h = notfound(l)
        write(p, h)
    keys = [('home', None), ('best', None), ('guides', None), ('about', None), ('contact', None)] + \
           [('tour', t['id']) for t in TOURS] + [('guide', g['id']) for g in GUIDES]
    # sitemap with hreflang
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    allurls = []
    for k, i in keys:
        for l in LANGS:
            u_ = absu(url(l, k, i)); allurls.append(u_)
            alts = ''.join(f'<xhtml:link rel="alternate" hreflang="{x}" href="{absu(url(x, k, i))}"/>' for x in LANGS)
            alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{absu(url(DEFAULT, k, i))}"/>'
            sm.append(f'<url><loc>{u_}</loc><lastmod>{TODAY}</lastmod>{alts}</url>')
    sm.append('</urlset>')
    write('/sitemap.xml', '\n'.join(sm))
    # IndexNow
    write(f'/{INDEXNOW_KEY}.txt', INDEXNOW_KEY)
    with open(os.path.join(OUT, '..', 'indexnow-payload.json'), 'w') as f:
        json.dump({"host": DOMAIN, "key": INDEXNOW_KEY, "keyLocation": absu(f'/{INDEXNOW_KEY}.txt'),
                   "urlList": allurls}, f, indent=1)
    # llms.txt + llms-full.txt
    en = C['en']
    lines = [f'# {SITE_NAME}', '', f'> {en["llms_summary"]}', '',
             'Independent comparison guide. Ratings are editorial scores from a published method, not customer reviews. '
             'Prices are indicative ranges; live prices and availability come from GetYourGuide and Viator. '
             f'Custom requests: WhatsApp +39 393 855 2086.', '',
             'Languages: English (/), Italiano (/it/), Español (/es/), Deutsch (/de/), Français (/fr/).', '',
             '## Key pages', f'- [Compare boat tours]({absu("/")}): filterable comparison of tour types',
             f'- [Best boat tours, ranked]({absu(url("en", "best"))}): ranking with scores per criterion',
             f'- [How we rate]({absu(url("en", "about"))}): method and affiliate disclosure', '', '## Guides']
    lines += [f'- [{en["guides"][g["id"]]["h1"]}]({absu(url("en", "guide", g["id"]))}): {en["guides"][g["id"]]["desc"]}' for g in GUIDES]
    lines += ['', '## Tours']
    lines += [f'- [{en["tours"][t["id"]]["name"]}]({absu(url("en", "tour", t["id"]))}): {en["tours"][t["id"]]["short"]}' for t in TOURS]
    lines += ['', '## Other languages']
    for l in LANGS[1:]:
        lines.append(f'- [{LANG_LABEL[l]}]({absu(prefix(l))}) · [{C[l]["best"]["h1"]}]({absu(url(l, "best"))})')
    lines += ['', '## Optional', f'- [Full text of English pages]({absu("/llms-full.txt")})']
    write('/llms.txt', '\n'.join(lines) + '\n')
    full = []
    for k, i in keys:
        fp = os.path.join(OUT, url('en', k, i).lstrip('/'), 'index.html')
        with open(fp, encoding='utf-8') as f:
            h = f.read()
        m = re.search(r'<main id="main">(.*)</main>', h, re.S)
        full.append(f'# {absu(url("en", k, i))}\n\n' + strip(m.group(1)))
    write('/llms-full.txt', '\n\n---\n\n'.join(full) + '\n')
    n = sum(len(files) for _, _, files in os.walk(OUT))
    print(f'Built {n} files into {OUT}')


if __name__ == '__main__':
    main()
