"""Bygger Appelgrens Elektriskas statiska sidor.

Kör från repots rot:  python3 tools/appelgrens.py .

Allt innehåll står i listorna nedan. Avsnitt för referensprojekt, kundomdömen
och fler medarbetare visas först när respektive lista har riktigt innehåll –
se INNEHALL.md för vad som behövs.
"""
import html, json, os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
E = html.escape

def P(pexels_id, fallback):
    """Foto från Pexels (länkas direkt). Om det inte laddar visas img/foto-<fallback>.jpg."""
    return ("pexels", pexels_id, fallback)

# ---------------- företaget ----------------
FIRMA = "Appelgrens Elektriska"
TEL, TEL_HREF = "031-26 25 40", "tel:+4631262540"
MEJL = "info@appelgrensel.se"
ADRESS = ("Ögärdesvägen 19 B", "433 30 Partille")
VD = dict(namn="Clas Amandusson", roll="VD och ägare", tel="0707-95 25 31", href="tel:+46707952531", mejl="clas@appelgrensel.se")
KARTA = "https://www.google.com/maps/search/?api=1&query=%C3%96g%C3%A4rdesv%C3%A4gen+19B+Partille"
OMRADE = ["Alingsås", "Partille", "Göteborg", "Kungsbacka", "Varberg"]

IMG = dict(hero=P(27928762, 1), why=P(28196526, 14), om=P(901941, 4), sida_om=P(17842832, 4), kontakt=P(5691590, 2),
           referenser=P(8221720, 6), rot=P(7031594, 10), tjanster=P(33694019, 9), refband=P(30271883, 7),
           omrade=P(29470768, 23), ovriga=P(6349399, 22))

# ---------------- tjänster ----------------
# exempel = konkreta arbeten (från Appelgrens egen text), passar = vem tjänsten passar för.
TJANSTER = [
 dict(slug="nyinstallation", title="Nyinstallation och entreprenader", h1="Elinstallation och elentreprenader",
      seo="Elinstallation och elentreprenad i Partille och Göteborg", short="Skolor, bostäder, industri och kontor", img=P(34054464, 6),
      lead="Vi har lång erfarenhet av projektering och installation inom både privat och offentlig verksamhet.",
      body=["Våra uppdrag omfattar bland annat skolor, förskolor, gruppboenden, lägenheter, villor, industrier och kontorslokaler. Vi kan även projektera och ta fram ritningar i CAD."],
      exempel=["Elinstallation i skolor och förskolor", "Elinstallation i gruppboenden", "El i nybyggda lägenheter och villor", "Elinstallation i industrilokaler", "Elinstallation i kontorslokaler", "Projektering och ritningar i CAD"],
      passar="Byggföretag, fastighetsägare och offentliga beställare som bygger nytt – och privatpersoner som bygger villa."),
 dict(slug="service", title="Service och reparation", h1="Elservice och reparationer",
      seo="Elservice och elreparationer i Partille och Göteborg", short="Stora som små jobb – fullt utrustade servicebilar", img=P(442160, 10),
      lead="Vi utför alla typer av elservice och reparationer – oavsett om det gäller ett mindre jobb eller en större installation.",
      body=["Våra servicebilar är fullt utrustade och våra montörer är redo att hjälpa till."],
      exempel=["Byte och installation av dimmers och vägguttag", "Elinstallationer i kök och badrum", "Elinstallationer vid nybyggnation", "Felsökning och reparation", "Service och underhåll", "Installation av golvvärme"],
      passar="Privatpersoner, bostadsrättsföreningar, fastighetsägare och företag – från ett nytt vägguttag till felsökning av en hel anläggning.", rot=True),
 dict(slug="industri", title="Industri- och maskininstallationer", h1="Industri- och maskininstallationer",
      seo="Industrielektriker – maskininstallation och PLC i Göteborgsområdet", short="Maskiner, automatikskåp och PLC", img=P(14319099, 21),
      lead="Genom många års erfarenhet inom industrin har vi byggt upp gedigen kompetens inom service, utveckling och installation av industri- och verkstadsmaskiner.",
      body=[],
      exempel=["Felsökning och reparation av maskiner", "Ombyggnad och effektivisering av maskiner", "Installation och utveckling av maskinparker", "Konstruktion och byggnation av automatikskåp", "PLC-programmering", "Elinstallationer och styrsystem"],
      passar="Industri- och verkstadsföretag med maskiner, produktionslinjer och styrsystem som behöver service, ombyggnad eller nyinstallation."),
 dict(slug="data-tele", title="Data- och teleinstallationer", h1="Data- och teleinstallationer",
      seo="Datanät, passagesystem och porttelefoner i Partille och Göteborg", short="Certifierade för ELKO och Lexcom", img=P(5073493, 19),
      lead="Vi är certifierade datainstallatörer för ELKO och Lexcoms datanät.",
      body=["Vid större installationer och nät kan vi erbjuda systemgarantier på 15–20 år."],
      exempel=["Installation och service av datanät", "Teleinstallationer", "Passagesystem", "Porttelefoner", "Större nät med systemgaranti på 15–20 år"],
      passar="Företag, fastighetsägare och offentliga verksamheter som behöver datanät, passagesystem eller porttelefoner."),
 dict(slug="larm", title="Larm och säkerhet", h1="Installation av larm och säkerhetssystem",
      seo="Installation av inbrottslarm, brandlarm och utrymningslarm i Göteborgsområdet", short="Inbrotts-, brand- och utrymningslarm", img=5,
      lead="Tillsammans med certifierade larmföretag kan vi utföra installationer av både mindre och större säkerhetssystem.",
      body=[],
      exempel=["Inbrottslarm", "Brandlarm", "Utrymningslarm", "Larmanläggningar för skolor och förskolor", "Larmanläggningar för butiker och andra verksamheter"],
      passar="Skolor, förskolor, butiker, fastighetsägare och andra verksamheter som behöver larm och säkerhetssystem."),
 dict(slug="ombyggnation", title="Ombyggnationer och hyresgästanpassningar", h1="El vid ombyggnation och hyresgästanpassning",
      seo="El vid ombyggnad och hyresgästanpassning i Göteborgsområdet", short="El i fastigheter där livet pågår", img=P(15798784, 17),
      lead="Vi har lång erfarenhet av elinstallationer vid ombyggnationer och hyresgästanpassningar av bostäder, lägenheter, kontor, industrier, butiker och restauranger.",
      body=["Vi är vana vid att arbeta i fastigheter där verksamhet eller boende pågår samtidigt. Det ställer höga krav på planering, flexibilitet och hänsyn – något våra montörer arbetar aktivt med genom hela projektet."],
      exempel=["Ombyggnad av bostäder och lägenheter", "Hyresgästanpassning av kontor", "Ombyggnad av industrilokaler", "Elinstallation i butiker", "Elinstallation i restauranger"],
      passar="Fastighetsägare, hyresgäster och företag som bygger om – även när boende eller verksamhet pågår under tiden.", rot=True),
]
OVRIGA = ["Installation av värmekabel", "Styr- och reglerteknik", "Elbesiktningar", "EIO-eltest", "Elinstallationer för villor och andra fastigheter"]
STEG = [("Kontakta oss", f"Ring {TEL} eller skicka en offertförfrågan och berätta vad du behöver hjälp med."),
        ("Vi går igenom uppdraget", "Vi återkommer och går igenom vad som ska göras, så att vi förstår ditt behov."),
        ("Du får en offert", "Du får ett förslag på lösning och pris innan arbetet börjar."),
        ("Vi utför arbetet", "Våra elektriker utför jobbet. Gäller det ditt hem hjälper vi dig med ROT-avdraget.")]

# ---------------- förtroende ----------------
# Bara verifierade uppgifter. Lägg till behörigheter (t.ex. auktorisation hos Elsäkerhetsverket) när de är bekräftade.
CERTS = [("Certifierad datainstallatör – ELKO", "Installation av datanät enligt ELKO:s system."),
         ("Certifierad datainstallatör – Lexcom", "Installation av datanät enligt Lexcoms system."),
         ("Systemgaranti 15–20 år", "Vid större installationer och nät i ELKO- och Lexcom-system.")]
REFERENSER = ["Partillebo AB", "Robnor AB", "Smålandsvillan", "Electroheat AB", "SweMaint AB", "Olivergren & Sundberg Fastighets AB", "NCC", "Skanska", "Erlandsson Bygg AB", "Triumf Glass"]

# Referensprojekt – fyll i med riktiga uppdrag. Avsnitten visas när listan inte är tom.
# dict(titel="", kund="", plats="", ar="", tjanst="service", bild=P(pexels_id, reserv) eller "img/projekt/fil.jpg",
#      uppdrag="Kort om uppdraget", utfort=["Vad vi gjorde", "..."])
PROJEKT = []
# Kundomdömen – bara riktiga, med kundens tillstånd. dict(citat="", namn="", roll="")
OMDOMEN = []
# Medarbetare. dict(namn="", roll="", bild="img/team/fil.jpg" eller None)
TEAM = [dict(namn=VD["namn"], roll=VD["roll"], bild=None, tel=VD["tel"], href=VD["href"], mejl=VD["mejl"])]
# Historik – bara bekräftade årtal.
HISTORIA = [("1960", "Appelgrens Elektriska startar i Partille."),
            ("Idag", "Tolv elektriker hjälper privatpersoner, företag och organisationer i Partille och Stor-Göteborg.")]

WHY = [("Över 60 års erfarenhet", "Sedan 1960 har vi gjort elinstallationer i Partille med omnejd – för privatpersoner, företag, industri och kommunal verksamhet."),
       ("Tolv elektriker, bred kompetens", "Från service och nyinstallation till industrimaskiner, styrsystem och PLC-programmering. Vi projekterar och ritar i CAD."),
       ("Hänsyn där livet pågår", "Vi är vana vid att arbeta i fastigheter där boende eller verksamhet pågår, och planerar arbetet därefter."),
       ("Installationer som håller", "Certifierade datainstallatörer för ELKO och Lexcom, med systemgaranti på 15–20 år vid större nät.")]
FAQ = [("Vilka områden arbetar ni i?", "Vi utgår från Partille och arbetar i hela Stor-Göteborg – från Alingsås i nordost till Kungsbacka och Varberg i sydväst."),
       ("Tar ni även mindre jobb?", "Ja. Vi hjälper till med allt från att byta ett vägguttag eller en dimmer till större entreprenader och industriella installationer."),
       ("Kan jag få ROT-avdrag för elarbete?", "Elinstallationer i ditt hem kan omfattas av ROT-avdrag enligt Skatteverkets regler. Avdraget är 30 % av arbetskostnaden för den som uppfyller villkoren, och vi hjälper dig med ansökan."),
       ("Arbetar ni åt företag och kommuner?", "Ja. Vi arbetar åt privatpersoner, företag, fastighetsägare, byggföretag och kommunal verksamhet."),
       ("Hur begär jag en offert?", f"Ring {TEL} eller fyll i offertformuläret på kontaktsidan och beskriv vad du behöver hjälp med.")]

# ---------------- byggstenar ----------------
def img(n, alt="", pos="50% 50%", lazy=True, sizes="(max-width: 760px) 100vw, 50vw"):
    extra = ' fetchpriority="high"' if not lazy else ' loading="lazy"'
    if isinstance(n, tuple):
        _, pid, back = n
        base = f"https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg?auto=compress&amp;cs=tinysrgb"
        srcset = ", ".join(f"{base}&amp;w={w} {w}w" for w in (640, 1024, 1600, 2200))
        return (f'<img class="photo" src="{base}&amp;w=1600" srcset="{srcset}" sizes="{sizes}" alt="{E(alt)}" decoding="async"{extra}'
                f' onerror="this.onerror=null;this.removeAttribute(\'srcset\');this.src=\'img/foto-{back:02d}.jpg\'" style="object-position:{pos}">')
    src = n if isinstance(n, str) else f"img/foto-{n:02d}.jpg"
    return f'<img class="photo" src="{src}" alt="{E(alt)}" decoding="async"{extra} style="object-position:{pos}">'
def ph(n, alt="", pos="50% 50%", lazy=True, sizes="100vw"): return f'<div class="ph">{img(n, alt, pos, lazy, sizes)}</div>'
FAVICON = "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%2314325c'/><text x='16' y='23' font-family='Arial' font-weight='700' font-size='20' fill='%23ffffff' text-anchor='middle'>A</text></svg>"
LOGO_TXT = '<img src="img/logo.png" alt="Appelgrens Elektriska – Service Partille AB" width="240" height="48">'
CARD_SIZES = "(max-width: 560px) 100vw, (max-width: 960px) 50vw, 400px"

def pcards(lst, extra=None):
    extra = len(lst) % 3 == 2 if extra is None else extra
    cards = "".join(f'<a class="pcard3" href="tjanst-{t["slug"]}.html"><div class="pc-img">{img(t["img"], "", sizes=CARD_SIZES)}</div><h3>{E(t["title"])}</h3><p>{E(t["short"])}</p></a>' for t in lst)
    if extra: cards += f'<a class="pcard3" href="tjanster.html#ovriga"><div class="pc-img">{img(IMG["ovriga"], "", sizes=CARD_SIZES)}</div><h3>Övriga tjänster</h3><p>Värmekabel, styr- och reglerteknik, elbesiktningar och EIO-eltest</p></a>'
    return f'<div class="pcards">{cards}</div>'
def pband(n, inner, pos="50% 50%", cls="", label=""):
    return f'<section class="pband {cls}" aria-label="{E(label)}">{ph(n, "", pos)}<div class="in">{inner}</div></section>'
def crumbs(lst): return '<nav class="crumbs" aria-label="Brödsmulor">' + ' <span aria-hidden="true">/</span> '.join(f'<a href="{u}">{E(t)}</a>' if u else f"<span>{E(t)}</span>" for t, u in lst) + "</nav>"
def phero(n, h1, lead, cr, pos="50% 50%", cta=True):
    btns = f'<div class="row"><a class="btn btn-w" href="kontakt.html#offert">Begär offert</a><a class="btn btn-o" href="{TEL_HREF}" style="color:#fff">Ring {TEL}</a></div>' if cta else ""
    return f'<section class="phero" aria-label="{E(h1)}">{ph(n, "", pos, lazy=False)}<div class="in">{crumbs(cr)}<h1>{E(h1)}</h1><p>{E(lead)}</p>{btns}</div></section>'
def eyebrow(t, light=False): return f'<p class="eyebrow"{" style=\"color:rgb(255 255 255/.8)\"" if light else ""}>{E(t)}</p>'
def steps(): return '<ol class="steps2">' + "".join(f"<li><b>{E(a)}</b><p>{E(b)}</p></li>" for a, b in STEG) + "</ol>"
def offer_card(rubrik="Begär offert", tjanst=""):
    q = f"?tjanst={tjanst}" if tjanst else ""
    return f'''<aside class="aside offer"><h3>{E(rubrik)}</h3><p>Berätta vad du behöver hjälp med, så återkommer vi med ett förslag.</p>
<a class="btn btn-y" href="kontakt.html{q}#offert">Begär offert</a><a class="btn btn-ow" href="{TEL_HREF}">Ring {TEL}</a>
<dl><div><dt>{VD["roll"]}</dt><dd>{VD["namn"]}, <a href="{VD["href"]}">{VD["tel"]}</a></dd></div><div><dt>E-post</dt><dd><a href="mailto:{MEJL}">{MEJL}</a></dd></div></dl></aside>'''
def ref_cols(): return '<ul class="ref-cols">' + "".join(f"<li>{E(r)}</li>" for r in REFERENSER) + "</ul>"
def proj_cards(lst):
    return '<div class="projs">' + "".join(
        f'''<article class="proj"><div class="pc-img">{img(p["bild"], p["titel"], sizes=CARD_SIZES)}</div><p class="proj-meta">{E(" · ".join(x for x in (p.get("kund"), p.get("plats"), p.get("ar")) if x))}</p>
<h3>{E(p["titel"])}</h3><p>{E(p["uppdrag"])}</p>{('<h4>Vi utförde</h4><ul>' + "".join(f"<li>{E(u)}</li>" for u in p["utfort"]) + "</ul>") if p.get("utfort") else ""}</article>''' for p in lst) + "</div>"
def quotes(lst):
    return '<div class="quotes">' + "".join(f'<figure class="quote"><blockquote>{E(q["citat"])}</blockquote><figcaption><b>{E(q["namn"])}</b>{(", " + E(q["roll"])) if q.get("roll") else ""}</figcaption></figure>' for q in lst) + "</div>"
def initials(n): return "".join(w[0] for w in n.split()[:2])

NAV = [("tjanster.html", "Tjänster"), ("om-oss.html", "Om oss"), ("referenser.html", "Referenser"), ("rot-avdrag.html", "ROT-avdrag"), ("kontakt.html", "Kontakt")]
SCHEMA = {"@context": "https://schema.org", "@type": "Electrician", "name": f"{FIRMA} AB", "telephone": "+46-31-26 25 40", "email": MEJL,
          "foundingDate": "1960", "address": {"@type": "PostalAddress", "streetAddress": ADRESS[0], "postalCode": "433 30", "addressLocality": "Partille", "addressCountry": "SE"},
          "areaServed": ["Partille", "Göteborg", "Alingsås", "Kungsbacka", "Varberg"]}

def head(title, desc, fn=""):
    sub = "".join(f'<a href="tjanst-{t["slug"]}.html">{E(t["title"])}</a>' for t in TJANSTER) + '<a href="tjanster.html#ovriga">Övriga tjänster</a>'
    nav = "".join((f'<li class="has-sub"><div class="sub-row"><a href="{u}">{t}</a><button class="sub-toggle" type="button" aria-expanded="false" aria-controls="ov-tjanster" aria-label="Visa alla tjänster"><span class="chev" aria-hidden="true"></span></button></div><div class="ov-sub" id="ov-tjanster"><div class="ov-sub-in">{sub}</div></div></li>' if u == "tjanster.html" else f'<li><a href="{u}">{t}</a></li>') for u, t in NAV)
    cur = lambda u: " aria-current=\"page\"" if u == fn or (u == "tjanster.html" and fn.startswith("tjanst-")) else ""
    mega = '<div class="mega"><div class="mega-in"><div><p class="eyebrow">Tjänster</p><p class="mega-lead">Elinstallationer, service och entreprenader för privatpersoner, företag och industri.</p></div><ul>' + "".join(f'<li><a href="tjanst-{t["slug"]}.html">{E(t["title"])}</a></li>' for t in TJANSTER) + '<li><a href="tjanster.html#ovriga">Övriga tjänster</a></li></ul></div></div>'
    topnav = "".join((f'<div class="has-mega"><a href="{u}"{cur(u)} aria-haspopup="true">{t}<span class="chev" aria-hidden="true"></span></a>{mega}</div>' if u == "tjanster.html" else f'<a href="{u}"{cur(u)}>{t}</a>') for u, t in NAV)
    return f'''<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta property="og:type" content="website"><meta property="og:locale" content="sv_SE"><meta property="og:site_name" content="{FIRMA}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta name="theme-color" content="#14325c">
<link rel="icon" href="data:image/svg+xml,{FAVICON}">
<link rel="preconnect" href="https://images.pexels.com">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;700&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="assets/site.css">
<link rel="stylesheet" href="assets/appelgrens.css">
<script type="application/ld+json">{json.dumps(SCHEMA, ensure_ascii=False)}</script>
</head>
<body{' class="home"' if fn == "index.html" else ""}>
<a class="skip" href="#innehall">Hoppa till innehållet</a>
<header>
  <div class="in nav">
    <a class="logo" href="index.html" aria-label="{FIRMA}, till startsidan">{LOGO_TXT}</a>
    <nav class="topnav" aria-label="Huvudmeny">{topnav}</nav>
    <a class="btn btn-g hd-offer" href="kontakt.html">Kontakta oss</a>
    <button class="burger" id="burger" aria-expanded="false" aria-controls="overlay" aria-label="Öppna menyn"><span></span><span></span><span></span></button>
  </div>
</header>
<div class="overlay" id="overlay" aria-hidden="true" inert>
  <div class="ov-top"><a class="logo" href="index.html">{LOGO_TXT}</a><button class="ov-close" id="menuClose" type="button" aria-label="Stäng menyn">Stäng</button></div>
  <nav aria-label="Mobilmeny"><ul>{nav}</ul>
  <div class="ov-foot"><a href="{TEL_HREF}">Ring {TEL}</a><a href="kontakt.html#offert">Begär offert</a></div></nav>
</div>
'''

def foot():
    return f'''<section class="fcta" aria-label="Kontakta oss">
  <div class="in"><div><h2>Behöver du en elektriker?</h2><p>Ring {TEL} eller skicka en förfrågan, så återkommer vi.</p></div><a class="btn btn-w" href="kontakt.html#offert">Begär offert</a></div>
</section>
<footer>
  <div class="in">
    <div class="fgrid">
      <div><a class="logo" href="index.html">{LOGO_TXT}</a>
        <p style="margin-top:14px;max-width:36ch">Trygga och professionella elinstallationer i Partille och Göteborgsområdet sedan 1960.</p>
        <p style="margin-top:12px">{ADRESS[0]}, {ADRESS[1]}<br><a href="{TEL_HREF}">{TEL}</a> · <a href="mailto:{MEJL}">{MEJL}</a></p>
      </div>
      <div><h4>Våra tjänster</h4><ul>{"".join(f'<li><a href="tjanst-{t["slug"]}.html">{E(t["title"])}</a></li>' for t in TJANSTER)}<li><a href="tjanster.html#ovriga">Övriga tjänster</a></li></ul></div>
      <div><h4>Om Appelgrens</h4><ul><li><a href="om-oss.html">Om oss</a></li><li><a href="om-oss.html#behorigheter">Behörigheter</a></li><li><a href="miljo-kvalitet.html">Miljö och kvalitet</a></li><li><a href="referenser.html">Referenser</a></li><li><a href="rot-avdrag.html">ROT-avdrag</a></li><li><a href="kontakt.html">Kontakt</a></li></ul></div>
      <div><h4>Direktkontakt</h4><ul><li>{VD["namn"]}</li><li>{VD["roll"]}</li><li><a href="{VD["href"]}">{VD["tel"]}</a></li><li><a href="mailto:{VD["mejl"]}">{VD["mejl"]}</a></li></ul></div>
    </div>
    <div class="certs" aria-label="Certifieringar"><span>Certifierad datainstallatör ELKO</span><span>Certifierad datainstallatör Lexcom</span><span>Sedan 1960</span></div>
    <div class="fbottom"><span>© 2026 {FIRMA} AB · Förhandsversion, bilderna är tillfälliga</span><a class="totop" href="#" data-top>Till toppen</a></div>
  </div>
</footer>
<script src="assets/site.js" defer></script>
<script src="assets/appelgrens.js" defer></script>
</body>
</html>
'''

def page(fn, title, desc, main):
    full = title if fn == "index.html" else f"{title} – {FIRMA}"
    with open(os.path.join(OUT, fn), "w") as f:
        f.write(head(full, desc, fn) + '<main id="innehall">\n' + main + "\n</main>\n" + foot())

faq_html = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in FAQ)
why_html = "".join(f"<div><h3>{E(a)}</h3><p>{E(b)}</p></div>" for a, b in WHY)
towns = '<ul class="area-towns">' + "".join(f"<li>{o}</li>" for o in OMRADE) + "</ul>"
STRIP = [("Sedan 1960", "elfirma i Partille"), ("12 elektriker", "service, installation och industri"), ("ELKO och Lexcom", "certifierade datainstallatörer"), ("30 % ROT-avdrag", "på arbetskostnaden i hemmet")]

# ---------------- startsidan ----------------
refs_home = (f'<section id="referenser"><div class="in"><div class="headrow"><div>{eyebrow("Referensprojekt")}<h2 style="margin-top:10px">Uppdrag vi har utfört</h2></div><a class="arrow" href="referenser.html">Alla referenser</a></div>{proj_cards(PROJEKT[:3])}</div></section>'
             if PROJEKT else
             pband(IMG["refband"], f'<div class="refs-split"><div>{eyebrow("Referenser", True)}<h2 style="margin-top:10px">Uppdragsgivare i urval</h2><p style="margin-top:12px">Vi har arbetat med ett stort antal kunder inom privat och offentlig verksamhet samt olika delar av näringslivet.</p><a class="arrow" style="margin-top:18px" href="referenser.html">Alla referenser</a></div>{ref_cols()}</div>', "50% 50%", "refs-band", "Referenser"))
omdomen_html = f'<section class="tint"><div class="in">{eyebrow("Kundomdömen")}<h2 style="margin-top:10px">Det här säger våra kunder</h2>{quotes(OMDOMEN)}</div></section>' if OMDOMEN else ""

ENTRY_IMG = [P(6301168, 18), P(9301037, 15), P(34718930, 20)]
ENTRIES = [("Privatpersoner", "Elinstallationer i villor och lägenheter, kök och badrum. ROT-avdrag på 30 % av arbetskostnaden.", "rot-avdrag.html", "Om ROT-avdrag"),
           ("Företag och fastighetsägare", "Entreprenader, ombyggnationer och hyresgästanpassningar – även där verksamhet eller boende pågår.", "tjanst-ombyggnation.html", "Ombyggnationer"),
           ("Industri och offentlig verksamhet", "Maskininstallationer, automatikskåp och PLC samt installationer i skolor, förskolor och gruppboenden.", "tjanst-industri.html", "Industriinstallationer")]
entries = "".join(f'<a class="entry" href="{c}"><div class="en-img">{img(ENTRY_IMG[i], "", sizes=CARD_SIZES)}</div><div class="en-txt"><span class="eyebrow">För</span><h3>{E(a)}</h3><p>{E(b)}</p><span class="arrow">{E(d)}</span></div></a>' for i, (a, b, c, d) in enumerate(ENTRIES))
PRINCIPER = [("Planering", "Vi är vana vid att arbeta i fastigheter där verksamhet eller boende pågår samtidigt. Det ställer höga krav på planering, flexibilitet och hänsyn genom hela projektet."),
             ("Kompetens", "Tolv elektriker med erfarenhet av allt från service och nyinstallation till industrimaskiner, styrsystem och PLC-programmering."),
             ("Långsiktighet", "Certifierade datainstallatörer för ELKO och Lexcom, med systemgarantier på 15–20 år vid större installationer och nät.")]
principles = "".join(f"<div><h3>{E(a)}</h3><p>{E(b)}</p></div>" for a, b in PRINCIPER)
BOLAG_HEM = [("Grundat", "1960"), ("Säte", "Partille"), ("Medarbetare", "12 elektriker"), ("VD och ägare", VD["namn"]), ("Certifiering", "Datainstallatör för ELKO och Lexcom"), ("Arbetsområde", "Alingsås till Varberg")]
bolagsfakta = '<dl class="bolag">' + "".join(f"<div><dt>{E(a)}</dt><dd>{E(b)}</dd></div>" for a, b in BOLAG_HEM) + "</dl>"

page("index.html", f"Elektriker i Partille och Göteborg – {FIRMA}",
     "Elektriker i Partille och Stor-Göteborg sedan 1960. Elservice, elinstallation, industri, datanät och larm. ROT-avdrag för privatpersoner. Ring 031-26 25 40.", f'''
  <section class="hero2 corp" aria-label="Välkommen">
    {ph(IMG["hero"], "Elektriker som arbetar i en elcentral", "50% 40%", lazy=False)}
    <div class="in">
      <p class="over">Elfirma i Partille sedan 1960</p>
      <h1>Elektriker i Partille och Göteborgsområdet</h1>
      <p>Installationer, service och entreprenader åt privatpersoner, företag och offentlig verksamhet – utförda av tolv erfarna elektriker.</p>
      <div class="row"><a class="btn btn-w" href="kontakt.html#offert">Begär offert</a><a class="btn btn-o" href="{TEL_HREF}" style="color:#fff">Ring {TEL}</a></div>
    </div>
  </section>
  <div class="in entries">{entries}</div>

  <section id="tjanster" style="background:var(--beige)">
    <div class="in">
      <div class="headrow"><div>{eyebrow("Verksamhetsområden")}<h2 style="margin-top:10px">Våra tjänster</h2><p class="lead" style="margin-top:12px">Kompletta elinstallationer och eltjänster för privatpersoner, företag och industriverksamheter.</p></div><a class="arrow" href="tjanster.html">Alla tjänster</a></div>
      {pcards(TJANSTER)}
    </div>
  </section>

  <section class="about" id="om" style="background:var(--white)">
    <div class="in about2 flip">
      <div class="media">{ph(IMG["om"], "", "50% 30%", sizes="(max-width: 860px) 100vw, 50vw")}</div>
      <div class="txt">
        {eyebrow("Om företaget")}
        <h2 style="margin-top:10px">Vår kunskap och service gör dig nöjd</h2>
        <p class="lead" style="margin-top:14px">Med över 60 års erfarenhet, bred kompetens och ett engagerat team hjälper vi våra kunder med trygga elinstallationer, service och entreprenader i Partille och Stor-Göteborg.</p>
        {bolagsfakta}
      </div>
    </div>
  </section>

  <section id="arbetssatt" style="background:var(--beige)">
    <div class="in work">
      <div class="work-img">{img(IMG["why"], "", "50% 20%", sizes="(max-width: 860px) 100vw, 45vw")}</div>
      <div>
        {eyebrow("Arbetssätt")}
        <h2 style="margin-top:10px">Så arbetar vi</h2>
        <div class="principles">{principles}</div>
      </div>
    </div>
  </section>

  {refs_home}
  {omdomen_html}

  {pband(IMG["omrade"], f'<div class="area2"><div>{eyebrow("Arbetsområde", True)}<h2 style="margin-top:10px">Från Alingsås i nordost till Kungsbacka och Varberg i sydväst</h2></div><div><p>Vi utgår från Partille och arbetar i hela Stor-Göteborg. Våra servicebilar är fullt utrustade och våra montörer är redo att hjälpa till.</p>{towns}<a class="btn btn-w" href="{KARTA}" target="_blank" rel="noopener">Hitta till oss</a></div></div>', "50% 60%", "area-band", "Arbetsområde")}

  <section id="faq">
    <div class="in faq">
      <div>{eyebrow("Frågor och svar")}<h2 style="margin-top:10px">Frågor och svar</h2><p class="lead" style="margin-top:14px">Hittar du inte svaret? Ring oss på <a href="{TEL_HREF}">{TEL}</a>.</p><a class="arrow" style="margin-top:18px" href="kontakt.html">Fråga oss något annat</a></div>
      <div>{faq_html}</div>
    </div>
  </section>''')

# ---------------- tjänster ----------------
page("tjanster.html", "Eltjänster i Partille och Göteborg", "Elservice, elinstallation, industri- och maskininstallationer, datanät, larm och ombyggnationer i Partille och Stor-Göteborg.",
     phero(IMG["tjanster"], "Våra eltjänster", "Kompletta elinstallationer och eltjänster för privatpersoner, företag och industriverksamheter.", [("Start", "index.html"), ("Tjänster", None)])
     + f'''<section><div class="in">{pcards(TJANSTER)}</div></section>
<section class="related" id="ovriga"><div class="in content"><div class="prose">{eyebrow("Övriga tjänster")}<h2 style="margin-top:0">Det här gör vi också</h2><ul class="ex-list">{"".join(f"<li>{E(x)}</li>" for x in OVRIGA)}</ul>
<h2>Så går det till</h2>{steps()}</div>{offer_card()}</div></section>''')

for t in TJANSTER:
    rel = [p for p in PROJEKT if p.get("tjanst") == t["slug"]]
    rot = '<p class="note-rot">Gäller arbetet ditt hem kan du få <a href="rot-avdrag.html">ROT-avdrag</a> på 30 % av arbetskostnaden. Vi hjälper dig med ansökan.</p>' if t.get("rot") else ""
    page(f"tjanst-{t['slug']}.html", t["seo"], f'{t["lead"]} {FIRMA} i Partille – ring {TEL} eller begär offert.',
         phero(t["img"], t["h1"], t["lead"], [("Start", "index.html"), ("Tjänster", "tjanster.html"), (t["title"], None)])
         + f'''<section><div class="in content"><div class="prose">
{"".join(f"<p>{E(p)}</p>" for p in t["body"])}
<h2{' style="margin-top:0"' if not t["body"] else ""}>Exempel på arbeten</h2><ul class="ex-list">{"".join(f"<li>{E(x)}</li>" for x in t["exempel"])}</ul>
<div class="fits"><h3>Passar för</h3><p>{E(t["passar"])}</p></div>
{rot}
<h2>Så går du vidare</h2>{steps()}
</div>{offer_card("Begär offert", t["slug"])}</div></section>
{f'<section class="tint"><div class="in">{eyebrow("Referensprojekt")}<h2 style="margin-top:10px">Uppdrag inom {E(t["title"].lower())}</h2>{proj_cards(rel)}</div></section>' if rel else ""}
<section class="related"><div class="in">{eyebrow("Fler tjänster")}<h2 style="margin-top:10px">Det här hjälper vi också till med</h2>{pcards([o for o in TJANSTER if o is not t])}</div></section>''')

# ---------------- om oss ----------------
team_html = '<div class="team">' + "".join(
    f'''<div class="member">{f'<div class="m-img">{img(m["bild"], m["namn"], sizes="300px")}</div>' if m.get("bild") else f'<span class="m-av" aria-hidden="true">{initials(m["namn"])}</span>'}
<b>{E(m["namn"])}</b><span>{E(m["roll"])}</span>{f'<a href="{m["href"]}">{m["tel"]}</a>' if m.get("tel") else ""}{f'<a href="mailto:{m["mejl"]}">{m["mejl"]}</a>' if m.get("mejl") else ""}</div>''' for m in TEAM) + "</div>"
hist_html = '<ol class="hist">' + "".join(f"<li><b>{E(a)}</b><p>{E(b)}</p></li>" for a, b in HISTORIA) + "</ol>"
certs_html = '<div class="certs2">' + "".join(f"<div><h3>{E(a)}</h3><p>{E(b)}</p></div>" for a, b in CERTS) + "</div>"
ARBETSSATT = [("Planering", "I fastigheter där boende eller verksamhet pågår planerar vi arbetet noga och tar hänsyn genom hela projektet."),
              ("Kompetens", "Tolv elektriker med erfarenhet av allt från service och nyinstallation till industrimaskiner, styrsystem och PLC-programmering."),
              ("Långsiktighet", "Vi bygger installationer som håller, med systemgarantier på 15–20 år vid större datanät.")]
BOLAG = [("Grundat", "1960"), ("Säte", "Partille"), ("Medarbetare", "12 elektriker"), ("VD och ägare", VD["namn"]), ("Arbetsområde", "Alingsås till Varberg")]
page("om-oss.html", "Om oss – elfirma i Partille sedan 1960", "Appelgrens Elektriska har gjort elinstallationer i Partille med omnejd sedan 1960. Möt teamet och läs om vår historia och vårt arbetssätt.",
     phero(IMG["sida_om"], "Om Appelgrens Elektriska", "En lokal elfirma i Partille sedan 1960 – idag tolv elektriker.", [("Start", "index.html"), ("Om oss", None)], "50% 30%", cta=False)
     + f'''<section><div class="in about2 flip"><div class="media">{ph(IMG["om"], "Elektriker från Appelgrens Elektriska", "50% 30%", sizes="(max-width: 860px) 100vw, 50vw")}</div><div class="txt">
{eyebrow("Vår historia")}<h2 style="margin-top:10px">Elektriker i Partille i över 60 år</h2>
<p class="lead" style="margin-top:14px">Appelgrens Elektriska har levererat trygga och professionella elinstallationer i Partille med omnejd sedan 1960. Under årens lopp har företaget byggt upp en stark position på den lokala marknaden.</p>
<p style="margin-top:12px">Idag hjälper tolv elektriker privatpersoner, företag och organisationer – med allt från mindre servicearbeten till större projekt inom industri, byggnation, kommunal verksamhet och privatmarknaden.</p>
{hist_html}</div></div></section>
<section class="tint"><div class="in">{eyebrow("Teamet")}<h2 style="margin-top:10px">Människorna bakom</h2><p class="lead" style="margin-top:12px">Appelgrens leds av {VD["roll"].lower()} {VD["namn"]}. Ring direkt om du vill prata om ett större uppdrag.</p>{team_html}</div></section>
<section><div class="in">{eyebrow("Arbetssätt")}<h2 style="margin-top:10px">Så arbetar vi</h2><div class="principles three">{"".join(f"<div><h3>{E(a)}</h3><p>{E(b)}</p></div>" for a, b in ARBETSSATT)}</div></div></section>
<section class="tint" id="behorigheter"><div class="in content"><div>{eyebrow("Behörigheter och certifieringar")}<h2 style="margin-top:10px">Certifierade installationer</h2>{certs_html}<p class="small-note">Larm och säkerhetssystem installerar vi tillsammans med certifierade larmföretag.</p><p style="margin-top:18px"><a class="arrow" href="miljo-kvalitet.html">Läs vår miljöpolicy och kvalitetspolicy</a></p></div>
<aside class="aside"><h3>Fakta</h3><dl>{"".join(f"<div><dt>{E(a)}</dt><dd>{E(b)}</dd></div>" for a, b in BOLAG)}</dl></aside></div></section>
{omdomen_html}''')

# ---------------- referenser ----------------
page("referenser.html", "Referenser och elprojekt", "Referensprojekt och uppdragsgivare: Partillebo, NCC, Skanska, Robnor med flera. Se vad Appelgrens Elektriska har utfört.",
     phero(IMG["referenser"], "Referenser", "Under våra många år i branschen har vi arbetat med ett stort antal kunder inom privat och offentlig verksamhet samt olika delar av näringslivet.", [("Start", "index.html"), ("Referenser", None)])
     + (f'<section><div class="in">{eyebrow("Referensprojekt")}<h2 style="margin-top:10px">Uppdrag vi har utfört</h2>{proj_cards(PROJEKT)}</div></section>' if PROJEKT else "")
     + f'''<section{' class="tint"' if PROJEKT else ""}><div class="in content"><div class="prose">{eyebrow("Uppdragsgivare")}<h2 style="margin-top:0">Några av våra tidigare och nuvarande kunder</h2>{ref_cols()}<p style="margin-top:24px">Vill du veta mer om något av uppdragen? Kontakta oss så berättar vi gärna.</p></div>{offer_card()}</div></section>
{omdomen_html}''')

# ---------------- formulär ----------------
def fld(i, label, typ="text", req=True, auto=""):
    return f'<label for="{i}">{label}{"" if req else " <small>(valfritt)</small>"}<input id="{i}" name="{i}" type="{typ}" data-label="{label}"{" required" if req else ""}{f" autocomplete=\"{auto}\"" if auto else ""}></label>'
def mail_ok():
    return f'<p class="form-ok" hidden tabindex="-1">Ditt e-postprogram öppnas med meddelandet ifyllt – skicka det därifrån. Fungerar det inte? Ring <a href="{TEL_HREF}">{TEL}</a> eller mejla <a href="mailto:{MEJL}">{MEJL}</a>.</p>'

page("rot-avdrag.html", "ROT-avdrag för elarbete", "Elinstallationer i hemmet kan ge ROT-avdrag på 30 % av arbetskostnaden. Så lämnar du uppgifterna till Appelgrens Elektriska.",
     phero(IMG["rot"], "ROT-avdrag för elarbete", "Elinstallationer i hemmet kan ge 30 % avdrag på arbetskostnaden.", [("Start", "index.html"), ("ROT-avdrag", None)], "50% 40%", cta=False)
     + f'''<section><div class="in content"><div class="prose"><h2 style="margin-top:0">Så fungerar det</h2>
<p>Vi utför elinstallationer som kan omfattas av ROT-avdrag enligt Skatteverkets regler. För privatpersoner som uppfyller villkoren kan ROT-avdraget innebära ett avdrag på <b>30 % av arbetskostnaden</b>.</p>
<h2>Uppgifter vi behöver</h2><ul class="ex-list"><li>Namn</li><li>Personnummer</li><li>Fastighets- eller lägenhetsbeteckning</li><li>BRF:s organisationsnummer, om du bor i bostadsrätt</li><li>E-postadress</li><li>Telefonnummer</li></ul>
<p>Om det finns en medsökande behöver vi samma uppgifter för hen. När uppgifterna är ifyllda skickar du formuläret, så hjälper vi dig vidare.</p></div>{offer_card("Frågor om ROT?")}</div></section>
<section class="related" id="formular"><div class="in"><form class="cform form-card" data-mailto="{MEJL}" data-subject="Uppgifter för ROT-avdrag" novalidate>
  <h2>Uppgifter för ROT-avdrag</h2>
  <div class="f2">{fld("rn", "Namn", auto="name")}{fld("rp", "Personnummer", auto="off")}{fld("rf", "Fastighets- eller lägenhetsbeteckning")}{fld("rb", "BRF:s organisationsnummer", req=False)}{fld("re", "E-post", "email", auto="email")}{fld("rt", "Telefon", "tel", auto="tel")}</div>
  <fieldset class="med"><legend>Medsökande (om det finns)</legend><div class="f2">{fld("mn", "Medsökandes namn", req=False)}{fld("mp", "Medsökandes personnummer", req=False)}{fld("mf", "Medsökandes fastighetsbeteckning", req=False)}{fld("mb", "Medsökandes BRF-organisationsnummer", req=False)}</div></fieldset>
  <p class="small-note">Uppgifterna skickas som e-post från ditt eget e-postprogram till {MEJL}. Inget sparas på webbplatsen.</p>
  <button class="btn btn-g" type="submit" style="justify-self:start">Skicka uppgifterna</button>
  {mail_ok()}
</form></div></section>''')

options = "".join(f'<option data-slug="{t["slug"]}">{E(t["title"])}</option>' for t in TJANSTER) + '<option data-slug="ovriga">Övriga tjänster</option><option data-slug="rot">ROT-avdrag</option><option>Annat</option>'
page("kontakt.html", "Kontakt och offert – elektriker i Partille", f"Begär offert eller kontakta Appelgrens Elektriska i Partille. Ring {TEL} eller mejla {MEJL}. {ADRESS[0]}, {ADRESS[1]}.",
     phero(IMG["kontakt"], "Begär offert eller kontakta oss", "Beskriv vad du behöver hjälp med, så återkommer vi med ett förslag. Vill du prata direkt? Ring oss.", [("Start", "index.html"), ("Kontakt", None)], "50% 30%", cta=False)
     + f'''<section id="offert"><div class="in content"><form class="cform form-card" data-mailto="{MEJL}" data-subject="Offertförfrågan" novalidate>
    <h2>Offertförfrågan</h2>
    <div class="f2">{fld("cn", "Namn", auto="name")}{fld("ct", "Telefon", "tel", auto="tel")}{fld("ce", "E-post", "email", auto="email")}{fld("co", "Adress eller ort", req=False, auto="street-address")}</div>
    <label for="cj">Vad gäller det?<select id="cj" name="tjanst" data-label="Gäller">{options}</select></label>
    <label for="cm">Beskriv uppdraget<textarea id="cm" name="cm" data-label="Beskrivning" required placeholder="Till exempel: nya uttag i kök, felsökning av maskin, datanät till kontor"></textarea></label>
    <label for="ck">Hur vill du bli kontaktad?<select id="ck" name="ck" data-label="Kontakt via"><option>Telefon</option><option>E-post</option></select></label>
    <button class="btn btn-g" type="submit" style="justify-self:start">Skicka förfrågan</button>
    {mail_ok()}
  </form>
  <aside class="aside"><h3>Ring eller mejla</h3><dl><div><dt>Växel</dt><dd><a href="{TEL_HREF}">{TEL}</a></dd></div><div><dt>E-post</dt><dd><a href="mailto:{MEJL}">{MEJL}</a></dd></div>
  <div><dt>{VD["roll"]}</dt><dd>{VD["namn"]}<br><a href="{VD["href"]}">{VD["tel"]}</a><br><a href="mailto:{VD["mejl"]}">{VD["mejl"]}</a></dd></div>
  <div><dt>Besöksadress</dt><dd>{FIRMA} AB<br>{ADRESS[0]}<br>{ADRESS[1]}</dd></div></dl><a class="arrow" href="{KARTA}" target="_blank" rel="noopener">Visa på karta</a></aside></div></section>
<section class="related"><div class="in">{eyebrow("Så går det till")}<h2 style="margin-top:10px">Från förfrågan till färdigt jobb</h2>{steps()}</div></section>''')

# ---------------- miljö och kvalitet ----------------
MILJO_INTRO = "Vi skapar konkurrenskraft hos våra kunder genom att erbjuda hög leveranssäkerhet, kvalité och god kompetens. Verksamheten skall bedrivas på ett sådant sätt att miljön och människan skyddas och energi- och naturresurser sparas så att Appelgrens bidrar till ett långsiktigt uthålligt samhälle."
MILJO = ["Vi skall påverka, ställa krav på och samarbeta med kunder, leverantörer och myndigheter och andra intressenter för att uppnå minsta möjliga miljöpåverkan.",
         "Vi skall genom uppföljning och ständiga förbättringar säkerställa att fastställda miljömål nås.",
         "Vi skall uppfylla aktuell miljölagstiftning och andra miljöförordningar som berör verksamheten.",
         "Vi skall visa öppenhet och informera om företagets miljöpåverkan och miljöarbete samt vara lyhörda för nya rön och erfarenheter på miljöområdet.",
         "Vi skall genom utbildning främja och uppmuntra miljömedvetandet hos samtliga medarbetare samt göra dem medvetna om sitt och företagets miljöansvar.",
         "Vi skall ha en effektiv avfallshantering och en optimal källsortering."]
KVAL_GENOM = ["Affärsmässighet", "Flexibilitet", "Långsiktighet", "Erforderlig och kvalificerad teknik", "Lyhördhet"]
KVAL_TRYGG = ["Uppfyller behov och förväntningar.", "Uppfyller lagar och förordningar.", "Levererar tjänster och produkter i rätt tid och av högsta kvalitet.",
              "Utför erforderliga kontroller av installationer såväl under som efter utfört arbete enligt utarbetade rutiner."]
SIGN = '<p class="sign">Partille 2016-11-01<br><b>Clas Amandusson</b>, ägare och VD, Appelgrens Elektriska AB</p>'
def pol_list(lst): return '<ul class="ex-list one">' + "".join(f"<li>{E(x)}</li>" for x in lst) + "</ul>"
page("miljo-kvalitet.html", "Miljöpolicy och kvalitetspolicy", "Appelgrens Elektriskas miljöpolicy och kvalitetspolicy – så arbetar vi med miljö, kvalitet och kontroll av installationer.",
     phero(IMG["om"], "Miljö och kvalitet", "Vår miljöpolicy och kvalitetspolicy.", [("Start", "index.html"), ("Om oss", "om-oss.html"), ("Miljö och kvalitet", None)], "50% 30%", cta=False)
     + f'''<section id="miljopolicy"><div class="in content"><div class="prose">{eyebrow("Miljöpolicy")}<h2 style="margin-top:0">Miljöpolicy</h2>
<p>{E(MILJO_INTRO)}</p><p>Detta innebär att:</p>{pol_list(MILJO)}{SIGN}</div>{offer_card()}</div></section>
<section class="tint" id="kvalitetspolicy"><div class="in content"><div class="prose">{eyebrow("Kvalitetspolicy")}<h2 style="margin-top:0">Kvalitetspolicy</h2>
<p>Appelgrens Elektriska skall genom:</p>{pol_list(KVAL_GENOM)}
<p>säkerställa att verksamheten uppfyller våra kunders, leverantörers, samarbetspartners och andra intressenters krav.</p>
<p>Kunderna skall alltid känna sig trygga i vårt samarbete genom att veta att vi efter bästa förmåga:</p>{pol_list(KVAL_TRYGG)}{SIGN}</div></div></section>''')

# ---------------- 404 ----------------
with open(os.path.join(OUT, "404.html"), "w") as f:
    f.write(f'''<!doctype html>
<html lang="sv"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sidan finns inte – {FIRMA}</title><meta name="robots" content="noindex">
<style>body{{margin:0;min-height:100vh;display:grid;place-items:center;background:#eef2f7;color:#14202e;font:17px/1.6 system-ui,sans-serif;text-align:center;padding:20px}}h1{{color:#14325c;margin:0 0 8px}}a{{color:#14325c;font-weight:700}}</style></head>
<body><div><h1>Sidan finns inte</h1><p>Den här sidan hittades inte. <a href="./">Till startsidan</a> eller ring <a href="{TEL_HREF}">{TEL}</a>.</p></div></body></html>
''')
print("Klart:", OUT)
