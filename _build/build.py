# -*- coding: utf-8 -*-
"""Generates index.html and /services/<slug>/index.html for the AI AutoTech redesign.
Run from the repo root:  python3 _build/build.py
(Folder starts with "_" so GitHub Pages/Jekyll does not publish it.)"""
import json, math, os, sys
from html import escape
from urllib.parse import quote
sys.path.insert(0, os.path.dirname(__file__))
from content import SERVICES, STACK, ORCH_NODES, WHO_KEYS, BOOK, TEAMS, TEAM_PRICE, TEAM_PRICE_NOTE

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = "20260925d"
LASTMOD = "2026-09-25"
SITE = "https://aiautotech.co.za"
WA_NUM = "27646863803"
BYSLUG = {s["slug"]: s for s in SERVICES}

# Founder photo in the homepage "Local, practical AI. Built in Benoni" section.
# Set to False to remove the photo block completely (the section then becomes a single column).
SHOW_FOUNDER_PHOTO = True

def founder_photo():
    if not SHOW_FOUNDER_PHOTO:
        return ""
    return """
      <figure class="sa-photo reveal">
        <img src="/assets/redesign/billy-faber-portrait.webp" alt="Billy Faber, founder of AI Auto Tech" width="620" height="691" loading="lazy" decoding="async" />
        <figcaption class="glass"><b>Billy Faber</b>Founder &amp; Managing Director, AI Auto Tech</figcaption>
      </figure>"""

MAP_EMBED = "https://www.google.com/maps?q=Benoni,+Gauteng,+South+Africa&z=11&output=embed"
MAP_LINK = "https://www.google.com/maps?q=Benoni,+Gauteng,+South+Africa"

def audit(p):
    return f"/audit/?utm_source=website&amp;utm_medium={p}&amp;utm_campaign=free_ai_audit"

def book(p):
    return f"/book/?utm_source=website&amp;utm_medium={p}&amp;utm_campaign=book_call"

def wa(text):
    return f"https://wa.me/{WA_NUM}?text={quote(text)}"

I = {
 "bot": '<rect x="4" y="8" width="16" height="12" rx="3"/><path d="M12 8V5M8.5 13.5h.01M15.5 13.5h.01M9 17h6"/><circle cx="12" cy="3.5" r="1.5"/>',
 "whatsapp": '<path d="M20.5 11.6a8.5 8.5 0 0 1-12.7 7.4L3 20.3l1.3-4.6a8.5 8.5 0 1 1 16.2-4.1z"/><path d="M9.2 8.3c-.4 2.9 2.6 6.4 6 6.3l.8-1.4-1.9-1-.9.8a4.6 4.6 0 0 1-2.3-2.3l.8-.9-1-1.9z"/>',
 "voice": '<path d="M4 15v-3a8 8 0 0 1 16 0v3"/><rect x="3" y="14" width="4" height="6" rx="1.5"/><rect x="17" y="14" width="4" height="6" rx="1.5"/><path d="M19 20c0 1.2-1.3 2-3 2h-3"/>',
 "crm": '<path d="M3 4h18l-7 8.5V19l-4 2v-8.5z"/>',
 "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20.5l1.3-4.8A8 8 0 1 1 21 12z"/><path d="M9 10.5v3M12 8.5v7M15 10.5v3"/>',
 "gear": '<circle cx="12" cy="12" r="3"/><path d="M12 2.5v3M12 18.5v3M4.2 5.6l2.1 2.1M17.7 16.3l2.1 2.1M2.5 12h3M18.5 12h3M4.2 18.4l2.1-2.1M17.7 7.7l2.1-2.1"/><circle cx="12" cy="12" r="7"/>',
 "monitor": '<rect x="2" y="4" width="20" height="13" rx="2"/><path d="M8 21h8M12 17v4M6 13l3-3 3 2 4-4"/>',
 "trend": '<path d="M3 17l6-6 4 4 8-8"/><path d="M14 7h7v7"/>',
 "research": '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3M8 11l2 2 4-4"/>',
 "hub": '<circle cx="12" cy="12" r="3"/><circle cx="12" cy="3" r="1.6"/><circle cx="12" cy="21" r="1.6"/><circle cx="3.8" cy="7.5" r="1.6"/><circle cx="20.2" cy="7.5" r="1.6"/><circle cx="3.8" cy="16.5" r="1.6"/><circle cx="20.2" cy="16.5" r="1.6"/><path d="M12 4.6V9M12 15v4.4M5.2 8.3l4.2 2.3M18.8 8.3l-4.2 2.3M5.2 15.7l4.2-2.3M18.8 15.7l-4.2-2.3"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "check": '<path d="M20 6L9 17l-5-5"/>',
 "leads": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M19 8v6M22 11h-6"/>',
 "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18M9 16l2 2 4-4"/>',
 "smile": '<circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2M9 9h.01M15 9h.01"/>',
 "growth": '<path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 5-6"/>',
 "bars": '<path d="M4 20h16M6 17v-6M10 17V7M14 17v-4M18 17V4"/>',
 "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
 "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 6l-10 7L2 6"/>',
 "pin": '<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
 "price": '<path d="M20.6 13.4l-7.2 7.2a2 2 0 0 1-2.8 0L2 12V2h10l8.6 8.6a2 2 0 0 1 0 2.8z"/><circle cx="7" cy="7" r="1.5"/>',
 "layers": '<path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>',
 "star": '<path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>',
 "clinic": '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M12 8v8M8 12h8"/>',
 "school": '<path d="M22 10L12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 2 9 2 12 0v-5"/>',
 "estate": '<path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
 "broker": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>',
 "service": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9z"/>',
 "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
 "close": '<path d="M6 6l12 12M18 6L6 18"/>',
 "meet": '<rect x="2" y="6" width="13" height="12" rx="2"/><path d="M15 10l6-4v12l-6-4z"/>',
 "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
 "mic": '<rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v4"/>',
}

def ic(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{I[name]}</svg>'

_fc = [0]
def flag(cls="flag"):
    _fc[0] += 1; fid = f"saT{_fc[0]}"
    return (f'<svg class="{cls}" viewBox="0 0 9 6" role="img" aria-label="South African flag"><clipPath id="{fid}"><path d="M0 0l4.5 3L0 6z"/></clipPath>'
            '<path fill="#001489" d="M0 0h9v6H0z"/><path fill="#E03C31" d="M0 0h9v3H0z"/>'
            '<path d="M0 0l4.5 3L0 6M4.5 3H9" stroke="#fff" stroke-width="2" fill="none"/>'
            '<path d="M0 0l4.5 3L0 6z" fill="#000"/>'
            f'<path d="M0 0l4.5 3L0 6" stroke="#FFB81C" stroke-width="2" fill="none" clip-path="url(#{fid})"/>'
            '<path d="M0 0l4.5 3L0 6M4.5 3H9" stroke="#007749" stroke-width="1.2" fill="none"/></svg>')

FONTS = ('<link rel="preload" href="/assets/fonts/inter-latin-wght.woff2" as="font" type="font/woff2" crossorigin />'
         '<link rel="preload" href="/assets/fonts/space-grotesk-latin-wght.woff2" as="font" type="font/woff2" crossorigin />')

OG_IMG = SITE + "/assets/og-share.jpg"
AREAS = [{"@type":"City","name":"Benoni"},{"@type":"AdministrativeArea","name":"Ekurhuleni"},{"@type":"City","name":"Johannesburg"},{"@type":"AdministrativeArea","name":"Gauteng"}]
ORG_ID = SITE + "/#organization"
ORG = {"@type":"ProfessionalService","@id":ORG_ID,"name":"AI AutoTech","legalName":"AI AutoTech (Pty) Ltd","url":SITE+"/",
       "logo":{"@type":"ImageObject","url":SITE+"/assets/logo.png","width":967,"height":746},"image":OG_IMG,
       "email":"billyfaber06@gmail.com","telephone":"+27646863803","areaServed":AREAS,"priceRange":"ZAR",
       "founder":{"@type":"Person","name":"Billy Faber","alternateName":"Willem Faber","jobTitle":"Founder and Managing Director"},
       "description":"AI AutoTech builds AI employees, WhatsApp automation, AI voice agents, CRM pipelines and websites for South African businesses.",
       "contactPoint":{"@type":"ContactPoint","contactType":"sales","telephone":"+27646863803","email":"billyfaber06@gmail.com","areaServed":"ZA","availableLanguage":["en"]}}
PROVIDER = {"@type":"ProfessionalService","@id":ORG_ID,"name":"AI AutoTech","url":SITE+"/","telephone":"+27646863803","email":"billyfaber06@gmail.com","areaServed":AREAS}

def crumbs_ld(items):
    return {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":k+1,"name":n,"item":SITE+u} for k,(n,u) in enumerate(items)]}

def graph(*nodes):
    return {"@context":"https://schema.org","@graph":list(nodes)}

def head(title, desc, path, og_title=None, jsonld=None, robots=None, canonical=True, extra=""):
    url = SITE + path
    rob = f'\n  <meta name="robots" content="{robots}" />' if robots else ""
    can = f'\n  <link rel="canonical" href="{url}" />' if canonical else ""
    ogt = escape(og_title or title)
    ld = f'\n  <script type="application/ld+json">\n{json.dumps(jsonld, indent=2, ensure_ascii=False)}\n  </script>' if jsonld else ""
    return f'''<!DOCTYPE html>
<html lang="en-ZA" class="no-js">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(desc)}" />
  <meta name="theme-color" content="#050814" />{rob}{can}
  <link rel="icon" href="/favicon.ico" sizes="any" />
  <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
  <link rel="icon" href="/assets/favicon-32.png" type="image/png" sizes="32x32" />
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png" />
  <link rel="manifest" href="/site.webmanifest" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="AI AutoTech" />
  <meta property="og:url" content="{url}" />
  <meta property="og:title" content="{ogt}" />
  <meta property="og:description" content="{escape(desc)}" />
  <meta property="og:image" content="{OG_IMG}" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="AI AutoTech: Your Business, Powered by AI Employees. aiautotech.co.za" />
  <meta property="og:locale" content="en_ZA" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{ogt}" />
  <meta name="twitter:description" content="{escape(desc)}" />
  <meta name="twitter:image" content="{OG_IMG}" />
  <meta name="twitter:image:alt" content="AI AutoTech: Your Business, Powered by AI Employees" />{ld}
  {FONTS}
  <link rel="stylesheet" href="/assets/redesign/site.css?v={V}" />{extra}
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
'''

NAV_LINKS = [("/#services", "Services"), ("/services/ai-employees/", "AI Employees"), ("/#pricing", "Pricing"), ("/#work", "Work"), ("/about.html", "About"), ("/#contact", "Contact")]

def nav(active_slug=None):
    links = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if (active_slug == "ai-employees" and h.endswith("ai-employees/")) or (active_slug == "about" and h == "/about.html") else ""}>{t}</a></li>' for h, t in NAV_LINKS)
    mm_main = "".join(f'<a href="{h}">{t}</a>' for h, t in NAV_LINKS)
    mm_svcs = "".join(f'<a href="/services/{s["slug"]}/"{" aria-current=\"page\"" if s["slug"] == active_slug else ""}>{escape(s["name"])}</a>' for s in SERVICES)
    mm_teams = "".join(f'<a href="/teams/{t["slug"]}/"{" aria-current=\"page\"" if t["slug"] == active_slug else ""}>{escape(t["name"])}</a>' for t in TEAMS)
    return f'''  <header class="nav">
    <div class="wrap">
      <a href="/" class="brand" aria-label="AI AutoTech home"><img src="/assets/redesign/nav-logo.webp" alt="" width="34" height="34" /><span>AI <b>AutoTech</b></span></a>
      <nav aria-label="Main"><ul class="nav-links">{links}</ul></nav>
      <div class="nav-right">
        <a href="{book("nav")}" class="btn-book-nav"{' aria-current="page"' if active_slug == "book" else ""}>{ic("calendar")}{BOOK["label"]}</a>
        <a href="{audit("nav")}" class="btn-audit-nav"><span class="pulse-dot" aria-hidden="true"></span>Free AI Audit</a>
        <button type="button" class="nav-toggle" id="nav-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu">{ic("menu","i-open")}{ic("close","i-close")}</button>
      </div>
    </div>
  </header>
  <div class="mobile-menu" id="mobile-menu">
    {mm_main}
    <p class="mm-label">Services</p>
    <div class="mm-services">{mm_svcs}</div>
    <p class="mm-label">AI teams</p>
    <div class="mm-services">{mm_teams}</div>
    <a href="{audit("mobile_menu")}" class="mm-audit"><span class="pulse-dot" aria-hidden="true"></span>Get my free AI audit</a>
    <a href="{book("mobile_menu")}" class="mm-book">{ic("calendar")}Book a 30-min call</a>
    <a href="{wa("Hi Billy, I saw the AI AutoTech website and would like to chat about AI for my business.")}" class="mm-wa" target="_blank" rel="noopener">Talk to us on WhatsApp</a>
  </div>
'''

def footer():
    li = lambda items: "".join(f'<li><a href="/services/{s["slug"]}/">{escape(s["name"])}</a></li>' for s in items)
    half = (len(SERVICES) + 1) // 2
    return f'''  <footer class="footer">
    <div class="wrap">
      <div>
        <a href="/" aria-label="AI AutoTech home"><img class="flogo" src="/assets/redesign/logo-footer.webp" alt="AI AutoTech" width="160" height="123" loading="lazy" decoding="async" /></a>
        <p style="margin-top:12px">AI employees, automation, websites and CRM for South African businesses. Benoni, Gauteng.</p>
        <p style="margin-top:8px"><a href="tel:0646863803" style="color:inherit">064 686 3803</a> · <a href="mailto:billyfaber06@gmail.com" style="color:inherit">billyfaber06@gmail.com</a></p>
      </div>
      <div><h2>Services</h2><ul>{li(SERVICES[:half])}</ul></div>
      <div><h2 class="blank" aria-hidden="true">&nbsp;</h2><ul>{li(SERVICES[half:])}</ul></div>
      <div><h2>Company</h2><ul>
        <li><a class="f-audit" href="{audit("footer")}">Free AI Audit</a></li>
        <li><a href="{book("footer")}">Book a call</a></li>
        <li><a href="/about.html">About</a></li>
        <li><a href="/#work">Work</a></li>
        <li><a href="/#contact">Contact</a></li>
        <li><a href="{wa("Hi Billy, I saw the AI AutoTech website and would like to chat about AI for my business.")}" target="_blank" rel="noopener">WhatsApp</a></li>
        <li><a href="/privacy.html">Privacy</a></li>
      </ul></div>
      <p class="legal">© <span id="year">2026</span> AI AutoTech (Pty) Ltd · Benoni, Gauteng, South Africa · All prices in ZAR, excl. VAT. Tool names (Grok, Perplexity, Hermes, Claude Code, Codex, Cursor, Supabase, Vercel) are trademarks of their owners and are shown to describe compatibility, not a partnership. Dashboards and chats shown on this site are illustrative examples.</p>
    </div>
  </footer>
'''

def sticky(placement, wa_text):
    return f'''  <div class="sticky-audit" id="sticky-audit">
    <a class="btn btn-primary" href="{audit(placement)}">Get my free AI audit {ic("arrow")}</a>
    <a class="btn btn-ghost" href="{wa(wa_text)}" target="_blank" rel="noopener" aria-label="Talk to us on WhatsApp"><span class="wa">{ic("whatsapp")}</span></a>
  </div>
'''

TAIL = f'''  <script src="/assets/redesign/site.js?v={V}" defer></script>
  <script src="/assets/redesign/contact-crm.js?v={V}" defer></script>
</body>
</html>
'''

def spark(d="M0 14 L10 11 L20 12 L30 7 L40 8 L50 4 L60 2", color="#2ee6d6"):
    return f'<svg viewBox="0 0 60 16" preserveAspectRatio="none" aria-hidden="true"><path d="{d}" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round"/></svg>'

def orch_svg(small=False):
    cx = cy = 300; R = 222; hr = 60
    defs = ('<defs><linearGradient id="lg" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="600" y2="600"><stop offset="0" stop-color="#2ee6d6"/><stop offset="1" stop-color="#b19cff"/></linearGradient>'
            '<radialGradient id="cg"><stop offset="0" stop-color="#e9fffd"/><stop offset=".25" stop-color="#2ee6d6"/><stop offset=".6" stop-color="rgba(139,92,246,.55)"/><stop offset="1" stop-color="rgba(139,92,246,0)"/></radialGradient></defs>')
    pts = []
    for k in range(8):
        a = math.radians(-90 + 45 * k)
        pts.append((cx + R * math.cos(a), cy + R * math.sin(a)))
    lines = "".join(f'<path class="ln" d="M{cx} {cy}L{x:.1f} {y:.1f}" style="animation-delay:-{k*0.3:.1f}s"/>' for k, (x, y) in enumerate(pts))
    ring = '<path class="ring" d="' + "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + 'z"/>'
    hexes = ""
    for (x, y), (name, tool, tone) in zip(pts, ORCH_NODES):
        hp = " ".join(f"{x + hr*math.cos(math.radians(60*j-90)):.1f},{y + hr*math.sin(math.radians(60*j-90)):.1f}" for j in range(6))
        fs = ' style="font-size:16px"' if len(name) > 8 else ""
        hexes += f'<g><polygon class="hex{" v" if tone=="v" else ""}" points="{hp}"/><text x="{x:.1f}" y="{y-2:.1f}"{fs}>{name}</text><text class="s" x="{x:.1f}" y="{y+18:.1f}">{tool}</text></g>'
    core = (f'<circle class="ring" cx="300" cy="300" r="118"/><circle class="ring" cx="300" cy="300" r="84" style="stroke:rgba(46,230,214,.35)"/>'
            f'<circle class="pulse" cx="300" cy="300" r="60"/><circle class="core" cx="300" cy="300" r="70"/>'
            f'<circle cx="300" cy="300" r="34" fill="rgba(5,8,20,.85)" stroke="#2ee6d6" stroke-width="2"/><text x="300" y="306" style="font-size:15px">HUB</text>')
    label = "Autonomous Orchestrator: a central hub coordinating eight AI agents: " + ", ".join(f"{n} ({t})" for n, t, _ in ORCH_NODES)
    return f'<svg class="orch-svg{" mini-hex" if small else ""}" viewBox="0 0 600 600" role="img" aria-label="{escape(label)}">{defs}{ring}{lines}{core}{hexes}</svg>'

# ---------------- Mockups for service pages ----------------
def mock(kind, s):
    lab = lambda t: f'<div class="mock-label"><b>{t}</b><span class="tag">Illustrative example</span></div>'
    if kind == "roster":
        rows = [("bot","Front-desk agent","Answering WhatsApp &amp; web enquiries","Online",""),("calendar","Booking agent","Offering Tue 10:00 or Wed 14:00","Online",""),
                ("leads","Follow-up agent","Checking in on quotes sent this week","Working",""),("layers","Admin agent","Filing new client documents","Queued","v"),("smile","Hand-over","Complaint flagged for a person","Needs you","v")]
        body = "".join(f'<div class="row"><span class="av">{ic(i)}</span><span><b>{a}</b><br>{b}</span><span class="st {v}">{st}</span></div>' for i,a,b,st,v in rows)
        return lab("Your AI team (sample)") + body + '<p class="note">Sample roles and tasks. Your AI team is designed around your business in the free audit.</p>'
    if kind == "chat":
        return lab("WhatsApp flow (sample chat)") + '''<div class="chatmock">
<div class="msg in">Hi! 👋 Thanks for messaging Sunrise Dental (example business). How can we help?<br>1️⃣ Book a visit 2️⃣ Prices 3️⃣ Speak to a person</div>
<div class="msg out">1</div>
<div class="msg in">Great. Which time suits you? <span class="slot">Tue 10:00</span><span class="slot">Wed 14:00</span><span class="slot">Thu 09:30</span></div>
<div class="msg out">Wed 14:00 please</div>
<div class="msg in">Booked ✅ We'll send you a reminder the day before.</div></div>
<div class="row" style="margin-top:12px"><span class="av">''' + ic("crm") + '''</span><span><b>Lead captured → CRM</b><br>Name, need and preferred time saved</span><span class="st">Saved</span></div>'''
    if kind == "voice":
        hs = [20,40,60,34,72,50,28,64,80,44,24,58,70,36,52,30,66,42,22,48]
        wave = "".join(f'<i style="--i:{k};--h:{h}"></i>' for k, h in enumerate(hs))
        return lab("Incoming call · after hours") + f'<div class="wave" aria-hidden="true">{wave}</div>' + ''.join([
          '<div class="row"><span class="av">' + ic("voice") + '</span><span><b>AI:</b> Good evening, you have reached Benoni Plumbing (example). How can I help?</span></div>',
          '<div class="row"><span class="av">' + ic("phone") + '</span><span><b>Caller:</b> My geyser is leaking. Can someone come tomorrow morning?</span></div>',
          '<div class="row"><span class="av">' + ic("check") + '</span><span><b>Qualified</b><br>Urgent · Benoni · tomorrow AM</span><span class="st">Booked 08:00</span></div>',
          '<div class="row"><span class="av">' + ic("mail") + '</span><span><b>Summary &amp; transcript</b><br>Sent to the on-call technician</span><span class="st v">Sent</span></div>'])
    if kind == "kanban":
        cols = [("New lead",[("Thandi M.","Clinic enquiry · WhatsApp"),("Sipho D.","Website form")]),("Contacted",[("Johan P.","School enrolment")]),
                ("Qualified",[("Nomsa K.","Viewing request"),("Ravi N.","Quote needed")]),("Won",[("Pieter V.","Quote accepted")])]
        k = "".join(f'<div class="col"><p class="kh">{t}</p>' + "".join(f'<div class="card"><b>{n}</b>{d}</div>' for n, d in cards) + '</div>' for t, cards in cols)
        return lab("Sales pipeline (sample)") + f'<div class="kanban">{k}</div>' + ''.join([
          '<div class="row" style="margin-top:10px"><span class="av">' + ic("whatsapp") + '</span><span><b>WhatsApp lead → CRM</b><br>Assigned to the sales team</span><span class="st">Auto</span></div>',
          '<div class="row"><span class="av">' + ic("calendar") + '</span><span><b>Follow-up reminder</b><br>Tomorrow 09:00 if no reply</span><span class="st v">Scheduled</span></div>'])
    if kind == "webchat":
        return lab("Website chat + voice notes (sample)") + '''<div class="chatmock">
<div class="msg in">Hi! I'm the virtual assistant for Glow Studio (example business). Ask me anything, or send a voice note.</div>
<div class="msg out">🎤 Voice note · 0:14<br><small style="opacity:.8">Transcribed: "Do you do teeth whitening and what does it cost?"</small></div>
<div class="msg in">Yes, we do. Whitening starts with a short consultation so we can recommend the right option and quote you properly. Shall I book a consultation?</div>
<div class="msg out">Yes please, Saturday morning</div></div>
<div class="row" style="margin-top:12px"><span class="av">''' + ic("chat") + '''</span><span><b>Same assistant on</b><br>Website · WhatsApp · Facebook · Instagram</span></div>'''
    if kind == "flow":
        steps = [("New client signs the quote","Trigger"),("Client created in the CRM","Done"),("Welcome WhatsApp + document checklist sent","Done"),("Invoice drafted in accounting","Done"),("Team notified with next steps","Running")]
        li = "".join(f'<li><span class="av" style="width:30px;height:30px;border-radius:10px;display:grid;place-items:center;background:var(--teal-soft);color:var(--teal);border:1px solid var(--teal-line)">{ic("check" if st=="Done" else "gear")}</span><span><b>{t}</b></span><span class="st{" v" if st!="Done" else ""}" style="margin-left:auto;font-size:.7rem;font-weight:700;padding:3px 8px;border-radius:999px;background:var(--teal-soft);color:var(--teal);border:1px solid var(--teal-line)">{st}</span></li>' for t, st in steps)
        return lab("Client onboarding workflow (sample)") + f'<ol class="flow">{li}</ol><p class="note">Each run is logged, with an alert if a step fails.</p>'
    if kind == "dashboard":
        hs = [30,42,38,55,48,62,58,70,66,78,74,86]
        bars = "".join(f'<i style="--h:{h}"></i>' for h in hs)
        rows = [("mail","Form enquiries"),("whatsapp","WhatsApp clicks"),("calendar","Bookings")]
        return lab("Website dashboard (sample)") + f'<div class="bars" aria-hidden="true">{bars}</div>' + "".join(f'<div class="row"><span class="av">{ic(i)}</span><span><b>{t}</b></span><span class="st">Tracked</span></div>' for i, t in rows) + '<p class="note">Illustrative chart with no real data. Your dashboard shows your own numbers.</p>'
    if kind == "phases":
        ph = [("Phase 1","Paper forms → digital forms","Done",""),("Phase 2","CRM &amp; shared WhatsApp inbox","In progress",""),("Phase 3","Quote, invoice &amp; reminder automations","Next","v"),("Phase 4","AI employees on top","Later","v")]
        return lab("Transformation roadmap (sample)") + "".join(f'<div class="row"><span class="av">{ic("layers")}</span><span><b>{a}</b><br>{b}</span><span class="st {v}">{st}</span></div>' for a, b, st, v in ph)
    if kind == "research":
        rows = [("Source 1 · government publication","Cited",""),("Source 2 · industry association report","Cited",""),("Source 3 · competitor websites","Cross-checked",""),("Two sources disagree on a figure","Flagged for you","v")]
        return lab("Research brief: private clinics in Ekurhuleni (example)") + "".join(f'<div class="row"><span class="av">{ic("research")}</span><span><b>{a}</b></span><span class="st {v}">{st}</span></div>' for a, st, v in rows) + '<div class="row"><span class="av">' + ic("mail") + '</span><span><b>Cited brief delivered</b><br>Email · Notion · dashboard</span><span class="st">Weekly</span></div>'
    if kind == "hex":
        return lab("Your AI team, coordinated (sample)") + orch_svg(small=True)
    return ""

# ---------------- Pages ----------------
def svc_button(s, placement_home=True):
    v = " v" if s["tone"] == "v" else ""
    pr = f'<span class="price">{escape(s["price"].replace(" (excl. VAT)",""))}</span>' if s.get("price") else ""
    return f'<a class="svc-btn{v}" href="/services/{s["slug"]}/"><span class="ico">{ic(s["icon"])}</span><span><b>{escape(s["name"])}</b><small>{escape(s["card"])}</small>{pr}</span>{ic("arrow","arr")}</a>'

def stack_block(compact=False):
    tiles = "".join(f'<li class="tool"><span class="g" aria-hidden="true">{g}</span><span><b>{n}</b><small>{d}</small></span></li>' for n, g, d in STACK)
    return f'''<div class="stack glass violet">
        <div class="stack-head">
          <h2>Built to work with your <span class="grad">AI stack</span></h2>
          <div class="works"><span>Works with <b>Claude Code</b></span><span>Works with <b>Codex</b></span><span>Works with <b>Cursor</b></span></div>
        </div>
        <ul class="stack-grid">{tiles}</ul>
        <p class="stack-foot">Use the tools you love. AI AutoTech builds with them and connects them to your business.</p>
      </div>'''

def home():
    org = dict(ORG); org["hasOfferCatalog"] = {"@type":"OfferCatalog","name":"AI AutoTech services","itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":s["name"],"url":f'{SITE}/services/{s["slug"]}/'}} for s in SERVICES]}
    ld = graph(org, {"@type":"WebSite","@id":SITE+"/#website","url":SITE+"/","name":"AI AutoTech","publisher":{"@id":ORG_ID},"inLanguage":"en-ZA"})
    wa_home = "Hi Billy, I saw the AI AutoTech website and would like to chat about AI for my business."
    kp = [("New leads","M0 14 L10 11 L20 12 L30 7 L40 8 L50 4 L60 2"),("Bookings","M0 12 L10 13 L20 9 L30 10 L40 6 L50 6 L60 3"),("Conversations","M0 10 L10 8 L20 11 L30 6 L40 7 L50 3 L60 4"),("Revenue","M0 15 L10 12 L20 12 L30 9 L40 6 L50 5 L60 2")]
    kpis = "".join(f'<div class="kpi"><span>{n}</span>{spark(d, "#2ee6d6" if i%2==0 else "#b19cff")}</div>' for i, (n, d) in enumerate(kp))
    outcomes = [("leads","More Leads","/services/whatsapp-automation/"),("calendar","More Bookings","/services/ai-voice-agents/"),("smile","Happier Customers","/services/ai-chat-voice/"),("growth","Greater Growth",audit("outcome_growth"))]
    oc = "".join(f'<a class="outcome float" style="--d:-{i*1.3:.1f}s" href="{h}">{ic(ico)}{t}</a>' for i, (ico, t, h) in enumerate(outcomes))
    svc_items = "".join(f'<li style="--d:-{(i*0.9)%7:.1f}s">{svc_button(s)}</li>' for i, s in enumerate(SERVICES))
    return head("AI AutoTech | Your Business, Powered by AI Employees (South Africa)",
                "AI employees, WhatsApp automation, AI voice agents, CRM and websites for South African businesses. Based in Benoni, Gauteng. Get your free AI audit.",
                "/", og_title="AI AutoTech: Your Business, Powered by AI Employees", jsonld=ld) + nav() + f'''  <main id="main">
  <section class="hero" aria-labelledby="hero-title">
    <div class="wrap">
      <div class="hero-text">
        <div class="hero-badge">{flag()}Benoni · Gauteng · South Africa</div>
        <h1 id="hero-title">Your business, powered by <span class="grad">AI employees</span></h1>
        <p class="tagline"><span>Automate.</span> <span>Streamline.</span> <span>Grow.</span></p>
        <p class="lead">We build AI employees that answer your WhatsApps and calls, follow up leads, book appointments and handle admin for South African businesses, so you can scale without hiring.</p>
        <div class="cta-row">
          <a class="btn btn-primary" href="{audit("hero")}">Get my free AI audit {ic("arrow")}</a>
          <a class="btn btn-ghost" href="{wa(wa_home)}" target="_blank" rel="noopener"><span class="wa">{ic("whatsapp")}</span>Talk to us on WhatsApp</a>
        </div>
        <p class="cta-note">Free AI Business Audit · about 5 minutes · no obligation</p>
        <a class="book-link" href="{book("hero")}">{ic("calendar")}<span>Prefer to talk first? <b>Book a 30-min call</b></span>{ic("arrow")}</a>
      </div>
      <nav class="outcomes" aria-label="Outcomes we deliver">{oc}</nav>
      <div class="hero-visual" role="img" aria-label="Illustrative example: an AI AutoTech dashboard on a laptop and a WhatsApp booking chat on a phone">
        <div class="laptop" aria-hidden="true">
          <div class="screen"><div class="dash">
            <div class="dash-side"><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
            <div>
              <div class="dash-top"><b>Good morning 👋 Your AI is working</b><span class="tag teal">Example dashboard</span></div>
              <div class="dash-kpis">{kpis}</div>
              <div class="dash-chart"><span>Lead growth (illustrative)</span>
                <svg viewBox="0 0 300 100" preserveAspectRatio="none"><defs><linearGradient id="ar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="rgba(46,230,214,.45)"/><stop offset="1" stop-color="rgba(139,92,246,0)"/></linearGradient></defs><path d="M0 88 L40 80 L80 72 L120 76 L160 52 L200 58 L240 34 L300 12 L300 100 L0 100z" fill="url(#ar)"/><path d="M0 88 L40 80 L80 72 L120 76 L160 52 L200 58 L240 34 L300 12" fill="none" stroke="#2ee6d6" stroke-width="2.5"/></svg>
              </div>
            </div>
          </div></div>
          <div class="base"></div>
        </div>
        <div class="phone" aria-hidden="true"><div class="phone-in">
          <div class="wa-head"><i></i><span><b>AI AutoTech</b><small>Example chat</small></span></div>
          <div class="wa-body">
            <div class="msg in">Hi! 👋 How can we help you today?</div>
            <div class="msg out">I'd like to book an appointment for next week.</div>
            <div class="msg in">Sure! Here are some times: <span class="slot">Tue 10:00</span><span class="slot">Wed 14:00</span></div>
            <div class="msg in">Shall I book this for you? ✅</div>
          </div>
        </div></div>
        <div class="stat glass s1 float" style="--d:-1s" aria-hidden="true">{ic("leads")}<span><b>Leads</b><span>Captured 24/7</span></span></div>
        <div class="stat glass violet s2 float" style="--d:-2.5s" aria-hidden="true">{ic("calendar")}<span><b>Bookings</b><span>Into your calendar</span></span></div>
        <div class="stat glass s3 float" style="--d:-4s" aria-hidden="true">{ic("bars")}<span><b>Revenue</b><span>Tracked in Rand</span></span></div>
        <div class="stat glass violet s4 float" style="--d:-5.2s" aria-hidden="true">{ic("smile")}<span><b>Happier customers</b><span>Instant replies</span></span></div>
        <p class="illus">Example dashboard &amp; chat, for illustration only</p>
      </div>
    </div>
  </section>

''' + teams_section() + f'''  <section class="section" id="services" aria-labelledby="svc-title">
    <div class="wrap">
      <div class="center reveal">
        <p class="eyebrow">What we build</p>
        <h2 class="section-title" id="svc-title">Pick a service. <span class="grad">See exactly how it works.</span></h2>
        <p class="section-sub">Ten ways we put AI to work in South African businesses. Tap any button for the full breakdown: how we implement it, what you gain and who it is for.</p>
      </div>
      <ul class="svc-grid">{svc_items}</ul>
    </div>
  </section>

  <section class="section" style="padding-top:20px" aria-label="AI stack">
    <div class="wrap reveal">{stack_block()}</div>
  </section>

  <section class="section" id="free-audit" aria-labelledby="audit-title">
    <div class="wrap">
      <div class="audit-band reveal">
        <div style="position:relative">
          <p class="eyebrow">Free · about 5 minutes</p>
          <h2 id="audit-title">Free AI Business <span class="grad">Audit</span></h2>
          <p>Answer a few quick questions about your business and get your personalised AI plan in about 5 minutes. No card, no obligation.</p>
          <a class="btn btn-primary" href="{audit("banner")}">Start my free AI audit {ic("arrow")}</a>
          <p class="cta-note">POPIA-aware · your answers are only used to prepare your plan</p>
          <a class="book-link" href="{book("banner")}">{ic("calendar")}<span>Done the audit? <b>Book your results call</b></span>{ic("arrow")}</a>
        </div>
        <ul class="audit-list" style="position:relative">
          <li><span class="num">01</span><div><b>Your top AI opportunities</b><span class="d">Where AI agents and automation fit your sales, marketing, service and operations.</span></div></li>
          <li><span class="num">02</span><div><b>Your recommended AI team</b><span class="d">Which AI agents we would deploy, grouped by department.</span></div></li>
          <li><span class="num">03</span><div><b>A Priority 1-2-3 plan</b><span class="d">What to automate first, with time-saving estimates based on your answers.</span></div></li>
        </ul>
      </div>
    </div>
  </section>

  <section class="section" id="orchestrator" aria-labelledby="orch-title">
    <div class="wrap orch">
      <div class="reveal">
        <p class="eyebrow">Autonomous Orchestrator</p>
        <h2 class="section-title" id="orch-title">One hub. <span class="grad">A whole AI team.</span></h2>
        <p class="section-sub" style="margin-bottom:0">As you add AI employees, the orchestrator coordinates them: it hands out tasks, shares context between agents, checks their work and asks a person before anything sensitive happens.</p>
        <ul>
          <li>{ic("check")}<span><b style="color:var(--text)">Hunter, Scout &amp; Keeper</b> find leads, research and remember every customer.</span></li>
          <li>{ic("check")}<span><b style="color:var(--text)">Architect, Builder &amp; Shipper</b> plan, build and ship your systems.</span></li>
          <li>{ic("check")}<span><b style="color:var(--text)">Vault &amp; Edge Runner</b> keep your data safe and your apps online.</span></li>
        </ul>
        <a class="btn btn-ghost" href="/services/autonomous-orchestrator/">How the orchestrator works {ic("arrow")}</a>
      </div>
      <div class="reveal">{orch_svg()}</div>
    </div>
  </section>

  <section class="section" id="pricing" aria-labelledby="price-title">
    <div class="wrap">
      <div class="center reveal">
        <p class="eyebrow">Pricing</p>
        <h2 class="section-title" id="price-title">Priced in Rand. <span class="grad">Scale without hiring.</span></h2>
        <p class="section-sub">Flat monthly pricing, excl. VAT. The free audit tells you exactly what you need, so you never pay for more than that.</p>
      </div>
      <div class="price-grid">
        <div class="price-card glass reveal"><span class="tag teal">AI Employees &amp; Agents</span><div class="amt">R8,999<small> /month</small></div><p>Starting price for an AI employee that answers, follows up, books and handles admin, 24/7.</p><a class="btn btn-ghost" href="/services/ai-employees/">See AI employees {ic("arrow")}</a></div>
        <div class="price-card glass violet reveal"><span class="tag">AI Voice Agents</span><div class="amt">R14,999<small> /month</small></div><p>Starting price for 24/7 call answering, lead qualification and booking by phone.</p><a class="btn btn-ghost" href="/services/ai-voice-agents/">See voice agents {ic("arrow")}</a></div>
        <div class="price-card glass other reveal"><span class="tag teal">Everything else</span><h3 style="margin-top:12px">Priced after your free audit</h3><p style="margin-top:8px">WhatsApp, CRM, automation, websites and research are scoped to your business, with a fixed quote.</p><a class="btn btn-primary" href="{audit("pricing")}">Get my free AI audit {ic("arrow")}</a></div>
      </div>
    </div>
  </section>

  <section class="section" id="why" aria-labelledby="why-title">
    <div class="wrap sa{"" if SHOW_FOUNDER_PHOTO else " no-photo"}">{founder_photo()}
      <div class="reveal">
        <div class="sa-badge glass">{flag()}<span>Built for South African businesses</span></div>
        <h2 class="section-title" id="why-title">Local, practical AI. <span class="grad">Built in Benoni.</span></h2>
        <p class="section-sub" style="margin-bottom:0">You deal directly with the people who build your system, not a call centre or an overseas agency.</p>
        <div class="why-grid">
          <div class="why glass"><h3>Local first</h3><p>We know South African realities: load shedding, data costs, cash-flow pressure and WhatsApp-first customers.</p></div>
          <div class="why glass"><h3>Rand pricing, no surprises</h3><p>All pricing in Rand. No dollar subscriptions quietly eating into your margins.</p></div>
          <div class="why glass"><h3>Done for you</h3><p>We build, deploy and manage the whole system so you can keep running your business.</p></div>
          <div class="why glass"><h3>Scale without hiring</h3><p>Add AI employees as you grow, with no recruitment, HR admin or long contracts.</p></div>
        </div>
      </div>
    </div>
  </section>

  <section class="section" id="work" aria-labelledby="work-title">
    <div class="wrap">
      <div class="reveal">
        <p class="eyebrow">Recent work</p>
        <h2 class="section-title" id="work-title">Live sites we shipped</h2>
        <p class="section-sub">Public .co.za properties for EASTC Holdings, live on HTTPS and built for the CEO to open and review.</p>
      </div>
      <div class="work-grid">
        <div class="work glass reveal"><h3>EASTC Holdings</h3><p>Hub plus Technical School, Artisanal College and Varsity (NATED N3–N6).</p><a href="https://eastech.co.za/" target="_blank" rel="noopener">eastech.co.za ↗</a></div>
        <div class="work glass reveal"><h3>EASTC Foundation NPC</h3><p>Scholarships, programmes and the campus story for the foundation.</p><a href="https://eastechfoundation.co.za/" target="_blank" rel="noopener">eastechfoundation.co.za ↗</a></div>
        <div class="work glass reveal"><h3>EASTECH Institute</h3><p>Higher-education site: programmes, admissions, quality and research.</p><a href="https://eastech-institute.co.za/" target="_blank" rel="noopener">eastech-institute.co.za ↗</a></div>
      </div>
    </div>
  </section>

  <section class="section" id="contact" aria-labelledby="contact-title">
    <div class="wrap contact">
      <div class="contact-card glass reveal">
        <p class="eyebrow">Contact</p>
        <h2 class="section-title" id="contact-title">Let's build your AI team</h2>
        <p style="color:var(--sub)">No hard sell and no jargon. Just a straight conversation about what AI can do for your business.</p>
        <ul class="contact-list">
          <li><a href="{book("contact")}">{ic("calendar")}Book a 30-min Google Meet</a></li>
          <li><a href="tel:0646863803">{ic("phone")}064 686 3803</a></li>
          <li><a href="mailto:billyfaber06@gmail.com">{ic("mail")}billyfaber06@gmail.com</a></li>
          <li><a href="{wa(wa_home)}" target="_blank" rel="noopener">{ic("whatsapp")}WhatsApp us</a></li>
          <li><a href="/about.html">{ic("pin")}Benoni, Gauteng · About us</a></li>
        </ul>
        <p class="audit-hint">Not sure what to automate first? <a href="{audit("contact")}">Take the free AI audit →</a></p>
      </div>
      <div class="contact-card glass violet reveal">
        <form class="contact-form" action="https://formsubmit.co/4b43618c4f12b0258208d17e157896bb" method="POST">
          <input type="hidden" name="_next" value="https://aiautotech.co.za/thanks.html" />
          <input type="hidden" name="_subject" value="New enquiry from aiautotech.co.za" />
          <input type="hidden" name="_template" value="table" />
          <input type="hidden" name="_captcha" value="false" />
          <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off" aria-hidden="true" />
          <label for="name">Name</label>
          <input id="name" name="name" type="text" required placeholder="Your name" autocomplete="name" />
          <label for="email">Email</label>
          <input id="email" name="email" type="email" required placeholder="you@company.co.za" autocomplete="email" />
          <label for="company">Business</label>
          <input id="company" name="company" type="text" placeholder="Business name (optional)" autocomplete="organization" />
          <label for="phone">Phone</label>
          <input id="phone" name="phone" type="tel" placeholder="0XX XXX XXXX" autocomplete="tel" />
          <label for="message">Message</label>
          <textarea id="message" name="message" required placeholder="What do you need automated?"></textarea>
          <button class="btn btn-primary" type="submit">Send us a message {ic("arrow")}</button>
          <p class="form-status" role="status" aria-live="polite" hidden></p>
        </form>
      </div>
      <div class="map-card glass reveal">
        <div class="map-head">
          <span class="map-pin">{ic("pin")}</span>
          <div>
            <h3>Based in Benoni, serving Ekurhuleni, Johannesburg &amp; Gauteng</h3>
            <p>Service-area business with no walk-in office. Talk to us on Google Meet, WhatsApp or phone.</p>
          </div>
        </div>
        <div class="map-frame">
          <iframe src="{MAP_EMBED}" title="Map of Benoni, Gauteng, South Africa: AI AutoTech's home base" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
        </div>
        <a class="map-link" href="{MAP_LINK}" target="_blank" rel="noopener">Open Benoni in Google Maps ↗</a>
      </div>
    </div>
  </section>
  </main>
''' + footer() + sticky("sticky_bar", wa_home) + TAIL

def service_page(s):
    slug = s["slug"]; pl = f"service_{slug}"
    wa_t = f"Hi Billy, I'm interested in {s['name']} for my business."
    price = s.get("price") or "Priced after your free audit"
    ld = {"@context":"https://schema.org","@type":"Service","name":s["name"],"serviceType":s["name"],"description":s["lead"],"url":f"{SITE}/services/{slug}/",
          "areaServed":AREAS,"provider":PROVIDER}
    if s.get("price_num"):
        ld["offers"] = {"@type":"Offer","priceCurrency":"ZAR","price":s["price_num"],"description":s["price"],"priceSpecification":{"@type":"UnitPriceSpecification","price":s["price_num"],"priceCurrency":"ZAR","unitText":"MONTH","valueAddedTaxIncluded":False}}
    steps = "".join(f'<li><span class="num">0{i+1}</span><div><b>{escape(t)}</b><p>{escape(d)}</p></div></li>' for i, (t, d) in enumerate(s["steps"]))
    gains = "".join(f'<li>{ic("check")}<span>{escape(g)}</span></li>' for g in s["gains"])
    who = "".join(f'<li class="who glass violet"><h3>{ic(k)}{label}</h3><p>{escape(s["who"][k])}</p></li>' for k, label in WHO_KEYS)
    tabs = "".join(f'<li><a class="svc-tab" href="/services/{o["slug"]}/"{" aria-current=\"page\"" if o["slug"]==slug else ""}>{ic(o["icon"])}{escape(o["short"])}</a></li>' for o in SERVICES)
    idx = [x["slug"] for x in SERVICES].index(slug)
    ld = graph(ld, crumbs_ld([("Home","/"),("Services","/#services"),(s["name"],f"/services/{slug}/")]))
    return head(s["title"], s["desc"], f"/services/{slug}/", jsonld=ld) + nav(slug) + f'''  <main id="main">
  <section class="svc-hero" aria-labelledby="svc-h1">
    <div class="wrap">
      <div>
        <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/#services">Services</a> / <span>{escape(s["name"])}</span></nav>
        <span class="tag teal" style="margin-bottom:14px">Service {idx+1:02d} / {len(SERVICES)}</span>
        <h1 id="svc-h1" style="margin-top:12px"><span class="grad">{escape(s["name"])}</span></h1>
        <p class="sub">{escape(s["sub"])}</p>
        <p class="lead">{escape(s["lead"])}</p>
        <div class="price-pill glass">{ic("price")}<span>{escape(price)}</span></div>
        <div class="cta-row">
          <a class="btn btn-primary" href="{audit(pl)}">Get my free AI audit {ic("arrow")}</a>
          <a class="btn btn-ghost" href="{wa(wa_t)}" target="_blank" rel="noopener"><span class="wa">{ic("whatsapp")}</span>Talk to us on WhatsApp</a>
        </div>
        <p class="cta-note">Free AI Business Audit · about 5 minutes · no obligation</p>
        <a class="book-link" href="{book(pl)}">{ic("calendar")}<span>Prefer to talk first? <b>Book a 30-min call</b></span>{ic("arrow")}</a>
      </div>
      <div class="mock glass reveal">{mock(s["mock"], s)}</div>
    </div>
  </section>

  <section class="section" style="padding-top:34px" aria-label="How it works">
    <div class="wrap two">
      <div class="box glass reveal"><h2>{ic("layers")}How we implement</h2><ol class="steps">{steps}</ol></div>
      <div class="box glass violet reveal"><h2>{ic("star")}How you gain</h2><ul class="gains">{gains}</ul></div>
    </div>
  </section>

  <section class="section" style="padding-top:10px" aria-labelledby="who-title">
    <div class="wrap">
      <h2 class="section-title reveal" id="who-title" style="font-size:clamp(1.5rem,4.6vw,2.2rem)">Who it's for</h2>
      <p class="section-sub reveal" style="margin-bottom:22px">Built for South African businesses that live on enquiries, bookings and follow-ups.</p>
      <ul class="who-grid">{who}</ul>
    </div>
  </section>

  <section class="section" style="padding-top:10px" aria-labelledby="cta-title">
    <div class="wrap">
      <div class="cta-band reveal">
        <p class="eyebrow">Start here</p>
        <h2 id="cta-title">See if {escape(s["name"])} fits your business</h2>
        <p>The free AI audit takes about 5 minutes. You get your top AI opportunities, a recommended AI team and a Priority 1-2-3 plan. <b style="color:var(--text)">{escape(price)}.</b></p>
        <div class="cta-row">
          <a class="btn btn-primary" href="{audit(pl)}">Get my free AI audit {ic("arrow")}</a>
          <a class="btn btn-ghost" href="{wa(wa_t)}" target="_blank" rel="noopener"><span class="wa">{ic("whatsapp")}</span>Talk to us on WhatsApp</a>
        </div>
        <a class="book-link" href="{book(pl)}" style="margin-top:16px">{ic("calendar")}<span>Or <b>book a 30-min Google Meet</b> with Billy</span>{ic("arrow")}</a>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:10px" aria-label="All services">
    <div class="wrap">
      <nav class="svc-nav glass" aria-label="Services"><h2>Explore our services</h2><ul class="svc-tabs">{tabs}</ul></nav>
    </div>
  </section>

  <section class="section" style="padding-top:10px" aria-label="AI stack">
    <div class="wrap">{stack_block()}</div>
  </section>
  </main>
''' + footer() + sticky(pl, wa_t) + TAIL


# ---------------- "Pick your AI team" ----------------
def team_buttons(t, placement):
    return (f'<a class="btn btn-team" href="{wa(t["wa"])}" target="_blank" rel="noopener"><span class="wa">{ic("whatsapp")}</span>Start with this team</a>'
            f'<a class="btn btn-ghost" href="{book(placement)}">{ic("calendar")}Book a call</a>')

def team_card(t):
    v = " violet" if t["tone"] == "v" else ""
    mem = "".join(f'<li>{ic(i)}<span><b>{escape(n)}</b>{escape(d)}</span></li>' for i, n, d in t["members"])
    when, what = t["day"][0]
    return f'''<article class="team-card glass{v} reveal" aria-labelledby="tm-{t["slug"]}">
          <div class="team-top"><span class="ico">{ic(t["icon"])}</span><div><span class="tag{" teal" if not v else ""}">{escape(t["short"])}</span><h3 id="tm-{t["slug"]}"><a href="/teams/{t["slug"]}/">{escape(t["name"])}</a></h3></div></div>
          <p class="team-pitch">{escape(t["pitch"])}</p>
          <p class="team-sub">{len(t["members"])} AI employees in this team</p>
          <ul class="team-members">{mem}</ul>
          <div class="team-day"><span class="tag">Illustrative example</span><p><b>{escape(when)}</b> {escape(what)}</p><a href="/teams/{t["slug"]}/">See the full day and team {ic("arrow")}</a></div>
          <p class="team-price">{ic("price")}<span><b>{TEAM_PRICE}</b> excl. VAT</span></p>
          <div class="team-cta">{team_buttons(t, "team_card_" + t["slug"].replace("-", "_"))}</div>
        </article>'''

def teams_section():
    cards = "".join(team_card(t) for t in TEAMS)
    return f'''
  <section class="section teams-sec" id="teams" aria-labelledby="teams-title">
    <div class="wrap">
      <div class="center reveal">
        <p class="eyebrow">Ready-made AI teams</p>
        <h2 class="section-title" id="teams-title">Pick your <span class="grad">AI team</span></h2>
        <p class="section-sub">Know your industry? Start with a ready-made team of AI employees, set up around your business. Not sure yet? The free AI audit tells you which team fits.</p>
      </div>
      <p class="swipe-hint" aria-hidden="true">Swipe to see all 4 teams {ic("arrow")}</p>
      <div class="teams-grid" role="region" aria-label="AI teams" tabindex="0">
        {cards}
        <article class="team-card team-choose glass reveal" aria-labelledby="tm-choose">
          <div>
            <p class="eyebrow">Option 3</p>
            <h3 id="tm-choose">Not sure? Get the free AI audit</h3>
            <p>Answer a few quick questions and get your recommended AI team and a Priority 1-2-3 plan. Or just talk to us.</p>
          </div>
          <div class="team-cta">
            <a class="btn btn-primary" href="{audit("teams_section")}">Get my free AI audit {ic("arrow")}</a>
            <a class="btn btn-ghost" href="{wa("Hi Billy, I saw the AI teams on your website. Can we chat about which one fits my business?")}" target="_blank" rel="noopener"><span class="wa">{ic("whatsapp")}</span>Just talk to us</a>
            <a class="btn btn-ghost" href="{book("teams_section")}">{ic("calendar")}Book a call</a>
          </div>
        </article>
      </div>
    </div>
  </section>
'''

def team_page(t):
    slug = t["slug"]; pl = "team_" + slug.replace("-", "_")
    ld = {"@context":"https://schema.org","@type":"Service","name":t["name"],"serviceType":"AI employees","description":t["desc"],"url":f"{SITE}/teams/{slug}/",
          "areaServed":AREAS,"provider":PROVIDER,
          "offers":{"@type":"Offer","priceCurrency":"ZAR","price":"8999","description":"From R8,999/month (excl. VAT)"}}
    mem = "".join(f'<li class="member glass{" violet" if k % 2 else ""} reveal"><span class="ico">{ic(i)}</span><div><h3>{escape(n)}</h3><p>{escape(d)}</p></div></li>' for k, (i, n, d) in enumerate(t["members"]))
    day = "".join(f'<li><span class="when">{escape(w)}</span><p>{escape(x)}</p></li>' for w, x in t["day"])
    fit = "".join(f'<li>{ic("check")}<span>{escape(f)}</span></li>' for f in t["fit"])
    others = "".join(f'<li><a class="svc-tab" href="/teams/{o["slug"]}/"{" aria-current=\"page\"" if o["slug"]==slug else ""}>{ic(o["icon"])}{escape(o["name"])}</a></li>' for o in TEAMS)
    note = f'<p class="team-note">{escape(t["note"])}</p>' if t.get("note") else ""
    ld = graph(ld, crumbs_ld([("Home","/"),("AI teams","/#teams"),(t["name"],f"/teams/{slug}/")]))
    return head(t["title"], t["desc"], f"/teams/{slug}/", jsonld=ld) + nav(slug) + f'''  <main id="main">
  <section class="svc-hero team-hero" aria-labelledby="team-h1">
    <div class="wrap">
      <div>
        <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/#teams">AI teams</a> / <span>{escape(t["name"])}</span></nav>
        <span class="tag teal" style="margin-bottom:14px">AI team · {escape(t["short"])}</span>
        <h1 id="team-h1" style="margin-top:12px"><span class="grad">{escape(t["name"])}</span></h1>
        <p class="sub">{escape(t["pitch"])}</p>
        <p class="lead">{escape(t["lead"])}</p>
        <div class="price-pill glass">{ic("price")}<span>{TEAM_PRICE} <small>({escape(TEAM_PRICE_NOTE)})</small></span></div>
        <div class="cta-row">{team_buttons(t, pl)}</div>
        <a class="book-link" href="{audit(pl)}">{ic("star")}<span>Not sure this is the right team? <b>Get the free AI audit</b></span>{ic("arrow")}</a>
      </div>
      <div class="mock glass reveal">
        <div class="mock-label"><b>Your {escape(t["name"])}</b><span class="tag">Illustrative example</span></div>
        {"".join(f'<div class="row"><span class="av">{ic(i)}</span><span><b>{escape(n)}</b><br>{escape(d.split(".")[0])}</span><span class="st{" v" if k % 2 else ""}">On duty</span></div>' for k, (i, n, d) in enumerate(t["members"]))}
        <p class="note">Sample team. Roles and tasks are set up around your business.</p>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:34px" aria-labelledby="mem-title">
    <div class="wrap">
      <h2 class="section-title reveal" id="mem-title" style="font-size:clamp(1.5rem,4.6vw,2.2rem)">Meet your AI employees</h2>
      <p class="section-sub reveal" style="margin-bottom:22px">Each AI employee has one clear job. Together they cover the whole front desk, and hand anything sensitive to your people.</p>
      <ul class="member-grid">{mem}</ul>
    </div>
  </section>

  <section class="section" style="padding-top:10px" aria-labelledby="day-title">
    <div class="wrap two">
      <div class="box glass reveal">
        <h2 id="day-title">{ic("clock")}A day with the team</h2>
        <span class="tag" style="margin:6px 0 14px;display:inline-flex">Illustrative example</span>
        <ol class="day-line">{day}</ol>
        <p class="note" style="margin-top:12px;color:var(--muted);font-size:.84rem">An example of how the team could work. Not a real client or real results.</p>
      </div>
      <div class="box glass violet reveal">
        <h2>{ic("star")}Who it's for</h2>
        <ul class="gains">{fit}</ul>
        {note}
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:10px" aria-labelledby="cta-title">
    <div class="wrap">
      <div class="cta-band reveal">
        <p class="eyebrow">Start here</p>
        <h2 id="cta-title">Start with the {escape(t["name"])}</h2>
        <p>Tell us about your business on WhatsApp or book a 30-min call. <b style="color:var(--text)">{TEAM_PRICE}</b> ({escape(TEAM_PRICE_NOTE)})</p>
        <div class="cta-row">{team_buttons(t, pl + "_band")}</div>
        <a class="book-link" href="{audit(pl + "_band")}" style="margin-top:16px">{ic("star")}<span>Or <b>get the free AI audit</b> first</span>{ic("arrow")}</a>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:10px" aria-label="All AI teams">
    <div class="wrap">
      <nav class="svc-nav glass" aria-label="AI teams"><h2>Other AI teams</h2><ul class="svc-tabs">{others}</ul></nav>
    </div>
  </section>
  </main>
''' + footer() + sticky(pl, t["wa"]) + TAIL

def book_page():
    wa_default = "Hi Billy, I'd like to book my AI Audit Results & Next Steps call."
    return head("Book your AI Audit Results & Next Steps call — AI AutoTech",
                "Book a free 30-minute Google Meet with Billy Faber to go through your AI business audit results, your recommended AI team and your Priority 1-2-3 plan.",
                "/book/", og_title="Book your AI Audit Results & Next Steps call — AI AutoTech") + nav("book") + f"""  <main id="main">
  <section class="book-hero" aria-labelledby="book-title">
    <div class="wrap">
      <div class="book-intro glass reveal">
        <p class="eyebrow">Free {BOOK["length"]} {BOOK["where"]}</p>
        <h1 id="book-title">Book your AI Audit Results &amp; <span class="grad">Next Steps</span> call</h1>
        <p class="lead">Free 30-minute Google Meet with Billy Faber. We'll go through your audit results, your recommended AI team and your Priority 1-2-3 plan, and agree next steps. Not done the audit yet? You can still book, or <a href="{audit("book")}">take the free AI audit first</a> (about 5 minutes).</p>
        <ul class="book-facts">
          <li>{ic("clock")}<span><b>30 minutes</b></span></li>
          <li>{ic("meet")}<span><b>Google Meet</b> link in your invite</span></li>
          <li>{ic("pin")}<span>Times in <b>{BOOK["tz"]}</b></span></li>
        </ul>
        <p class="ref-note" id="ref-note" hidden></p>
      </div>
    </div>
  </section>

  <section class="book-cal" aria-label="Choose a time">
    <div class="wrap">
      <p class="tz-line">{ic("clock")}<span>Times are shown in <b>SAST (Johannesburg, UTC+2)</b>. Every call is <b>30 minutes on Google Meet</b>; Google emails you the confirmation and Meet link. Outside South Africa? Check the time zone shown in the calendar.</span></p>
      <div class="cal-card">
        <div class="cal-inner">
          <div class="cal-loading" id="cal-loading">Loading available times…</div>
          <iframe id="cal-frame" title="Book your AI Audit Results &amp; Next Steps call with Billy Faber" data-src="{BOOK["embed"]}"></iframe>
          <noscript><iframe title="Book your AI Audit Results &amp; Next Steps call with Billy Faber" src="{BOOK["embed"]}" style="position:absolute;inset:0;width:100%;height:100%;border:0"></iframe></noscript>
        </div>
      </div>
      <div class="book-fallback glass violet">
        <p>Calendar not loading? <a href="{BOOK["google_page"]}" target="_blank" rel="noopener">Open the booking page &rarr;</a></p>
        <a id="wa" class="btn btn-ghost" href="https://wa.me/{WA_NUM}" target="_blank" rel="noopener"><span class="wa">{ic("whatsapp")}</span>Prefer WhatsApp? Message Billy</a>
      </div>
    </div>
  </section>
  </main>
""" + footer() + f"""  <script>
    (function () {{
      var frame = document.getElementById("cal-frame"), loading = document.getElementById("cal-loading");
      frame.addEventListener("load", function () {{ if (frame.src) loading.hidden = true; }});
      // Load the Google Calendar embed once the page itself has painted, so it doesn't hold up first render.
      function loadCal() {{ if (!frame.src) frame.src = frame.getAttribute("data-src"); }}
      if (document.readyState === "complete") setTimeout(loadCal, 50); else window.addEventListener("load", function () {{ setTimeout(loadCal, 50); }});
      setTimeout(loadCal, 3500);
      var raw = (new URLSearchParams(location.search).get("ref") || "").trim().toUpperCase();
      var ref = /^AAT-[A-Z0-9]{{4,10}}$/.test(raw) ? raw : "";
      var msg = "{wa_default}";
      if (ref) {{
        var note = document.getElementById("ref-note");
        note.appendChild(document.createTextNode("Your audit reference: "));
        var b = document.createElement("b"); b.textContent = ref; note.appendChild(b);
        note.appendChild(document.createTextNode(", please enter it in the booking form."));
        note.hidden = false;
        msg += " My audit reference is " + ref + ".";
      }}
      document.getElementById("wa").href = "https://wa.me/{WA_NUM}?text=" + encodeURIComponent(msg);
    }})();
  </script>
""" + TAIL

# ---------------- About / Privacy / Thanks / 404 ----------------
WA_GENERAL = "Hi Billy, I saw the AI AutoTech website and would like to chat about AI for my business."

def cta_band(pl, title, text):
    return f'''  <section class="section" style="padding-top:10px" aria-labelledby="cta-title">
    <div class="wrap">
      <div class="cta-band reveal">
        <p class="eyebrow">Start here</p>
        <h2 id="cta-title">{title}</h2>
        <p>{text}</p>
        <div class="cta-row">
          <a class="btn btn-primary" href="{audit(pl)}">Get my free AI audit {ic("arrow")}</a>
          <a class="btn btn-ghost" href="{wa(WA_GENERAL)}" target="_blank" rel="noopener"><span class="wa">{ic("whatsapp")}</span>Talk to us on WhatsApp</a>
        </div>
        <a class="book-link" href="{book(pl)}" style="margin-top:16px">{ic("calendar")}<span>Or <b>book a 30-min Google Meet</b> with Billy</span>{ic("arrow")}</a>
      </div>
    </div>
  </section>
'''

def about_page():
    ld = graph(dict(ORG), {"@type":"AboutPage","@id":SITE+"/about.html#page","url":SITE+"/about.html","name":"About AI AutoTech","about":{"@id":ORG_ID},"inLanguage":"en-ZA"},
               crumbs_ld([("Home","/"),("About","/about.html")]))
    svcs = "".join(f'<li><a class="svc-tab" href="/services/{o["slug"]}/">{ic(o["icon"])}{escape(o["name"])}</a></li>' for o in SERVICES)
    return head("About AI AutoTech | AI Employees & Automation, Benoni, Gauteng",
                "AI AutoTech (Pty) Ltd, Benoni: founded and led by Billy Faber. We build AI employees, WhatsApp automation, voice agents, CRM and websites for SA businesses.",
                "/about.html", og_title="About AI AutoTech: local, practical AI from Benoni", jsonld=ld) + nav("about") + f'''  <main id="main">
  <section class="svc-hero about-hero" aria-labelledby="about-h1">
    <div class="wrap">
      <div>
        <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <span>About</span></nav>
        <div class="hero-badge">{flag()}Benoni · Gauteng · South Africa</div>
        <h1 id="about-h1" style="margin-top:14px">About <span class="grad">AI AutoTech</span></h1>
        <p class="sub">Local, practical AI. Built in Benoni.</p>
        <p class="lead">AI AutoTech (Pty) Ltd is a South African company based in Benoni, Gauteng, founded and led by Billy Faber, our Managing Director. We build AI employees, WhatsApp automation, AI voice agents, CRM pipelines, websites and dashboards for South African businesses, priced in Rand and managed for you.</p>
        <div class="cta-row">
          <a class="btn btn-primary" href="{audit("about_hero")}">Get my free AI audit {ic("arrow")}</a>
          <a class="btn btn-ghost" href="{wa(WA_GENERAL)}" target="_blank" rel="noopener"><span class="wa">{ic("whatsapp")}</span>Talk to us on WhatsApp</a>
        </div>
        <a class="book-link" href="{book("about_hero")}">{ic("calendar")}<span>Prefer to talk first? <b>Book a 30-min call</b></span>{ic("arrow")}</a>
      </div>
      <figure class="sa-photo about-photo">
        <img src="/assets/redesign/billy-faber-office.webp" alt="Billy Faber, founder and Managing Director of AI AutoTech" width="560" height="732" fetchpriority="high" decoding="async" />
        <figcaption class="glass"><b>Billy Faber</b>Founder &amp; Managing Director</figcaption>
      </figure>
    </div>
  </section>

  <section class="section" style="padding-top:20px" aria-label="What we do and how we work">
    <div class="wrap two">
      <div class="box glass reveal">
        <h2>{ic("bot")}What we do</h2>
        <p class="prose-p">We put AI to work on the jobs that slow a business down: answering WhatsApps and calls, following up leads, booking appointments, keeping the CRM up to date and handling repetitive admin.</p>
        <p class="prose-p">Every system is set up around how your business already works, connected to the tools you use, and it hands anything sensitive to a person.</p>
      </div>
      <div class="box glass violet reveal">
        <h2>{ic("star")}How we work</h2>
        <ul class="gains">
          <li>{ic("check")}<span><b style="color:var(--text)">Local first.</b> We know South African realities: load shedding, data costs, cash-flow pressure and WhatsApp-first customers.</span></li>
          <li>{ic("check")}<span><b style="color:var(--text)">Rand pricing.</b> Flat monthly pricing in Rand, excl. VAT. No dollar subscriptions.</span></li>
          <li>{ic("check")}<span><b style="color:var(--text)">Done for you.</b> We build, deploy and manage the system so you can keep running your business.</span></li>
          <li>{ic("check")}<span><b style="color:var(--text)">Direct contact.</b> You deal directly with the people who build your system, not a call centre.</span></li>
        </ul>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:10px" aria-labelledby="facts-title">
    <div class="wrap">
      <div class="box glass reveal facts">
        <h2 id="facts-title">{ic("layers")}Company details</h2>
        <dl class="facts-list">
          <div><dt>Company</dt><dd>AI AutoTech (Pty) Ltd</dd></div>
          <div><dt>Founder &amp; Managing Director</dt><dd>Willem (Billy) Faber</dd></div>
          <div><dt>Based in</dt><dd>Benoni, Gauteng, South Africa. Service-area business with no walk-in office.</dd></div>
          <div><dt>Areas served</dt><dd>Benoni, Ekurhuleni, Johannesburg and Gauteng. Meetings on Google Meet, WhatsApp or phone.</dd></div>
          <div><dt>Phone / WhatsApp</dt><dd><a href="tel:+27646863803">064 686 3803</a></dd></div>
          <div><dt>Email</dt><dd><a href="mailto:billyfaber06@gmail.com">billyfaber06@gmail.com</a></dd></div>
        </dl>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:10px" aria-label="Our services">
    <div class="wrap">
      <nav class="svc-nav glass" aria-label="Services"><h2>What we build</h2><ul class="svc-tabs">{svcs}</ul></nav>
    </div>
  </section>

''' + cta_band("about", "See where AI fits your business", "The free AI audit takes about 5 minutes. You get your top AI opportunities, a recommended AI team and a Priority 1-2-3 plan.") + '''  </main>
''' + footer() + sticky("about_sticky", WA_GENERAL) + TAIL

PRIVACY_SECTIONS = [
 ("Who we are", '''<p>AI AutoTech (Pty) Ltd (“AI AutoTech”, “we”, “us”) is a South African company based in Benoni, Gauteng. This notice explains how we handle personal information when you use aiautotech.co.za or contact us, in line with the Protection of Personal Information Act (POPIA).</p>
<p><b>Responsible party:</b> AI AutoTech (Pty) Ltd, Benoni, Gauteng, South Africa. Contact: Willem (Billy) Faber, Founder and Managing Director, <a href="mailto:billyfaber06@gmail.com">billyfaber06@gmail.com</a>, <a href="tel:+27646863803">064 686 3803</a> (phone / WhatsApp).</p>'''),
 ("What we collect", '''<ul>
<li><b>Contact form:</b> your name, email address, and optionally your business name and phone number, plus your message. We also record the page you sent it from, the referring page and campaign tags (UTM) in the link you used.</li>
<li><b>Free AI Business Audit</b> (<a href="/audit/?utm_source=website&amp;utm_medium=privacy_text&amp;utm_campaign=free_ai_audit">/audit/</a>): your first name, surname, business name, email, mobile / WhatsApp number, your role, your answers to the audit questions, how you found us (for example an event QR code or campaign link) and your consent to be contacted.</li>
<li><b>Booking a call</b> (<a href="/book/?utm_source=website&amp;utm_medium=privacy_text&amp;utm_campaign=book_call">/book/</a>): bookings are made in a Google Calendar booking page embedded on our site. Google collects the name, email and any notes you enter and sends us the booking.</li>
<li><b>WhatsApp, email and phone:</b> whatever you choose to send us.</li>
<li><b>Technical data:</b> our hosting provider may log technical request data such as IP address and browser type.</li>
</ul>'''),
 ("Why we use it", '''<p>Only to reply to your enquiry, prepare your audit results, schedule and hold calls you book, quote for and deliver services you ask for, and keep records required by South African law. We do not sell personal information, and we do not use it for unrelated marketing.</p>'''),
 ("Where it is stored and who helps us", '''<p>We use a small number of service providers (operators) who process information for us:</p>
<ul>
<li><b>Supabase</b> hosts our customer database (CRM), where contact-form messages and audit submissions are stored.</li>
<li><b>Vercel</b> hosts the CRM application that receives form and audit submissions.</li>
<li><b>FormSubmit</b> delivers a copy of contact-form messages to our email inbox.</li>
<li><b>GitHub Pages</b> hosts this website.</li>
<li><b>Google</b> provides the booking calendar, Google Meet, email and the map on our home page.</li>
<li><b>WhatsApp (Meta)</b> handles messages you send us on WhatsApp.</li>
</ul>
<p>Some of these providers store data outside South Africa. We only use providers that protect information to a standard comparable to POPIA, and we only share what is needed to run the site, reply to you or deliver our services, or where the law requires it.</p>'''),
 ("Cookies, local storage and embedded content", '''<p>We do not set advertising or analytics cookies. Our fonts are hosted on our own site.</p>
<p>The audit saves your progress and your results in your browser's local storage, on your own device, so you can continue where you left off. Campaign tags from the link you used may also be kept there so we know how you found us. You can clear this at any time in your browser settings.</p>
<p>The Google Map on our home page and the Google Calendar booking page are loaded from Google. When they load, Google may set cookies or collect technical data under <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Google's privacy policy</a>.</p>'''),
 ("How long we keep it and how we protect it", '''<p>We keep enquiry and audit records for as long as needed to finish the conversation and any work that follows, and as required by law, then delete or anonymise them. We take reasonable technical and organisational steps to protect information in our control, but no internet transmission is completely secure.</p>'''),
 ("Your rights", '''<p>You may ask us whether we hold your personal information, ask for a copy, ask us to correct or delete it, or object to us using it. Email <a href="mailto:billyfaber06@gmail.com">billyfaber06@gmail.com</a>. You may also lodge a complaint with the Information Regulator (South Africa) at <a href="https://inforegulator.org.za/" target="_blank" rel="noopener">inforegulator.org.za</a>.</p>'''),
 ("Changes to this notice", '''<p>We may update this notice when our services or providers change. The date at the top shows the latest version.</p>'''),
]

def privacy_page():
    toc = "".join(f'<li><a href="#p{k+1}">{escape(h)}</a></li>' for k, (h, _) in enumerate(PRIVACY_SECTIONS))
    body = "".join(f'<section class="prose-sec" id="p{k+1}" aria-labelledby="p{k+1}-t"><h2 id="p{k+1}-t">{escape(h)}</h2>{html}</section>' for k, (h, html) in enumerate(PRIVACY_SECTIONS))
    ld = graph({"@type":"WebPage","@id":SITE+"/privacy.html#page","url":SITE+"/privacy.html","name":"Privacy Policy (POPIA notice)","publisher":{"@id":ORG_ID},"dateModified":LASTMOD,"inLanguage":"en-ZA"},
               crumbs_ld([("Home","/"),("Privacy","/privacy.html")]))
    return head("Privacy Policy (POPIA) | AI AutoTech",
                "How AI AutoTech (Pty) Ltd collects, uses and protects personal information from our website, contact form, free AI audit and bookings, and your rights under POPIA.",
                "/privacy.html", jsonld=ld) + nav("privacy") + f'''  <main id="main">
  <section class="svc-hero page-hero" aria-labelledby="priv-h1">
    <div class="wrap narrow">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <span>Privacy</span></nav>
      <h1 id="priv-h1">Privacy <span class="grad">Policy</span></h1>
      <p class="sub">POPIA notice · Updated 25 September 2026</p>
    </div>
  </section>
  <section class="section" style="padding-top:0">
    <div class="wrap narrow">
      <nav class="toc glass" aria-label="On this page"><h2>On this page</h2><ol>{toc}</ol></nav>
      <div class="prose glass">{body}</div>
      <p class="back-links"><a href="/">Back to home</a> · <a href="{audit("privacy")}">Free AI Audit</a> · <a href="/#contact">Contact us</a></p>
    </div>
  </section>
  </main>
''' + footer() + TAIL

def simple_page(title, desc, path, h1, sub, body_html, pl, robots=None, canonical=True, mark="thanks"):
    return head(title, desc, path, robots=robots, canonical=canonical) + nav(mark) + f'''  <main id="main">
  <section class="svc-hero page-hero status-hero" aria-labelledby="st-h1">
    <div class="wrap narrow center">
      <div class="status-card glass">
        {body_html[0]}
        <h1 id="st-h1">{h1}</h1>
        <p class="lead">{sub}</p>
        <div class="cta-row">
          <a class="btn btn-primary" href="{audit(pl)}">Get my free AI audit {ic("arrow")}</a>
          <a class="btn btn-ghost" href="{book(pl)}">{ic("calendar")}Book a 30-min call</a>
          <a class="btn btn-ghost" href="{wa(WA_GENERAL)}" target="_blank" rel="noopener"><span class="wa">{ic("whatsapp")}</span>WhatsApp us</a>
        </div>
        {body_html[1]}
      </div>
    </div>
  </section>
  </main>
''' + footer() + TAIL

def thanks_page():
    return simple_page("Message received | AI AutoTech",
        "Thanks for contacting AI AutoTech. Billy will get back to you shortly. Urgent? WhatsApp 064 686 3803, or take the free AI audit while you wait.",
        "/thanks.html", 'Message <span class="grad">received</span>',
        'Thanks for getting in touch. Billy will get back to you shortly. If it\'s urgent, WhatsApp <a href="https://wa.me/27646863803" target="_blank" rel="noopener">064 686 3803</a>. While you wait, you can take the free AI audit (about 5 minutes) or book a call.',
        (f'<span class="status-ico ok">{ic("check")}</span>', '<p class="back-links"><a href="/">Back to aiautotech.co.za</a></p>'),
        "thanks_page", robots="noindex, follow")

def notfound_page():
    links = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in [("/", "Home"), ("/#services", "Services"), ("/#teams", "AI teams"), ("/#pricing", "Pricing"), ("/about.html", "About"), ("/#contact", "Contact")])
    return simple_page("Page not found (404) | AI AutoTech",
        "This page could not be found on aiautotech.co.za. Take the free AI audit, book a call or WhatsApp AI AutoTech.",
        "/404.html", 'Page <span class="grad">not found</span>',
        "Sorry, we couldn't find that page. It may have moved, or the link may be mistyped. Here's where to go next:",
        (f'<span class="status-ico">404</span>', f'<ul class="nf-links">{links}</ul>'),
        "404_page", robots="noindex", canonical=False, mark="404")

def sitemap():
    urls = [("/", "weekly", "1.0"), ("/audit/", "monthly", "0.9"), ("/book/", "monthly", "0.7")]
    urls += [(f"/services/{s['slug']}/", "monthly", "0.8") for s in SERVICES]
    urls += [(f"/teams/{t['slug']}/", "monthly", "0.7") for t in TEAMS]
    urls += [("/about.html", "yearly", "0.6"), ("/privacy.html", "yearly", "0.3")]
    body = "".join(f"  <url>\n    <loc>{SITE}{u}</loc>\n    <lastmod>{LASTMOD}</lastmod>\n    <changefreq>{c}</changefreq>\n    <priority>{p}</priority>\n  </url>\n" for u, c, p in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}</urlset>\n'

MANIFEST = {"name":"AI AutoTech","short_name":"AI AutoTech","description":"AI employees, WhatsApp automation, voice agents, CRM and websites for South African businesses.",
            "start_url":"/?utm_source=pwa","scope":"/","display":"standalone","background_color":"#050814","theme_color":"#050814",
            "icons":[{"src":"/assets/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"/assets/icon-512.png","sizes":"512x512","type":"image/png"},
                     {"src":"/assets/icon-maskable-512.png","sizes":"512x512","type":"image/png","purpose":"maskable"}]}

def main():
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(home())
    for s in SERVICES:
        d = os.path.join(ROOT, "services", s["slug"]); os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(service_page(s))
    for t in TEAMS:
        d = os.path.join(ROOT, "teams", t["slug"]); os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(team_page(t))
    os.makedirs(os.path.join(ROOT, "book"), exist_ok=True)
    with open(os.path.join(ROOT, "book", "index.html"), "w", encoding="utf-8") as f:
        f.write(book_page())
    for name, fn in [("about.html", about_page), ("privacy.html", privacy_page), ("thanks.html", thanks_page), ("404.html", notfound_page)]:
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
            f.write(fn())
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap())
    with open(os.path.join(ROOT, "site.webmanifest"), "w", encoding="utf-8") as f:
        json.dump(MANIFEST, f, indent=2)
    print("built", 6 + len(SERVICES) + len(TEAMS), "pages + sitemap + manifest")

if __name__ == "__main__":
    main()
