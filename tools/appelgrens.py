"""Bygger Appelgrens Elektriskas statiska sidor.

Kör från repots rot:  python3 tools/appelgrens.py .
Allt innehåll står i listorna nedan. Bilderna väljs i IMG och TJANSTER; byt
numren (eller sätt sökvägar, t.ex. "img/skrapat/bild.jpg") när riktiga bilder
från appelgrensel.se finns i img/.
"""
import html, os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
E = html.escape

FIRMA = "Appelgrens Elektriska"
TEL, TEL_HREF = "031-26 25 40", "tel:+4631262540"
MEJL = "info@appelgrensel.se"
ADRESS = ("Ögärdesvägen 19 B", "433 30 Partille")
VD = dict(namn="Clas Amandusson", roll="VD och ägare", tel="0707-95 25 31", href="tel:+46707952531", mejl="clas@appelgrensel.se")
KARTA = "https://www.google.com/maps/search/?api=1&query=%C3%96g%C3%A4rdesv%C3%A4gen+19B+Partille"
FORM_OK = f"Tack! Formuläret är inte kopplat ännu – ring {TEL} eller mejla {MEJL} så hjälper vi dig."

# Tillfälliga bilder (img/foto-NN.jpg). Byt mot bilder från nuvarande hemsida.
IMG = dict(hero=(4, "50% 30%"), om=(14, "50% 25%"), kontakt=14, referenser=6, rot=10)

# Ikoner (24×24, linjer) till tjänsterna
ICON = {
 "nyinstallation": '<path d="M3 21h18M5 21V8l7-4 7 4v13"/><path d="M9 21v-5h6v5M9 11h.01M15 11h.01"/>',
 "service": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>',
 "industri": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/>',
 "data-tele": '<rect x="9" y="2" width="6" height="5" rx="1"/><rect x="2" y="17" width="6" height="5" rx="1"/><rect x="16" y="17" width="6" height="5" rx="1"/><path d="M12 7v5M5 17v-5h14v5"/>',
 "larm": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>',
 "ombyggnation": '<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9v12h14V9"/><path d="M10 21v-6h4v6"/>',
}
def icon(slug, cls="ico"): return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[slug]}</svg>'
CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>'
MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/></svg>'
PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>'

# ---------------- innehåll ----------------
TJANSTER = [
 dict(slug="nyinstallation", title="Nyinstallation och entreprenader", short="Projektering och installation åt skolor, boenden, bostäder, industrier och kontor.", img=1,
      lead="Vi har lång erfarenhet av projektering och installation inom både privat och offentlig verksamhet.",
      body=["Våra uppdrag omfattar bland annat skolor, förskolor, gruppboenden, lägenheter, villor, industrier och kontorslokaler.",
            "Vi kan även projektera och ta fram ritningar i CAD."],
      rubrik="Exempel på uppdrag", bullets=["Skolor och förskolor", "Gruppboenden", "Lägenheter och villor", "Industrier", "Kontorslokaler", "Projektering och ritningar i CAD"]),
 dict(slug="service", title="Service och reparation", short="Allt från ett nytt vägguttag till felsökning – med fullt utrustade servicebilar.", img=10,
      lead="Vi utför alla typer av elservice och reparationer – oavsett om det gäller ett mindre jobb eller en större installation.",
      body=["Våra servicebilar är fullt utrustade och våra montörer är redo att hjälpa till."],
      rubrik="Vi hjälper bland annat till med", bullets=["Byte och installation av dimmers och vägguttag", "Elinstallationer i kök och badrum", "Elinstallationer vid nybyggnation", "Felsökning och reparation", "Service och underhåll", "Installation av golvvärme"]),
 dict(slug="industri", title="Industri- och maskininstallationer", short="Service, ombyggnad och automatikskåp för industri- och verkstadsmaskiner. PLC-programmering.", img=21,
      lead="Genom många års erfarenhet inom industrin har vi byggt upp gedigen kompetens inom service, utveckling och installation av industri- och verkstadsmaskiner.",
      body=[],
      rubrik="Vi hjälper våra kunder med bland annat", bullets=["Felsökning och reparation", "Ombyggnad och effektivisering av maskiner", "Installation och utveckling av maskinparker", "Konstruktion och byggnation av automatikskåp", "PLC-programmering", "Elinstallationer och styrsystem"]),
 dict(slug="data-tele", title="Data- och teleinstallationer", short="Certifierade för ELKO och Lexcom. Systemgaranti på 15–20 år för större nät.", img=19,
      lead="Vi är certifierade datainstallatörer för ELKO och Lexcoms datanät.",
      body=["Vid större installationer och nät kan vi erbjuda systemgarantier på 15–20 år."],
      rubrik="Vi installerar och servar även", bullets=["Datanät", "Teleinstallationer", "Passagesystem", "Porttelefoner"]),
 dict(slug="larm", title="Larm och säkerhet", short="Inbrotts-, brand- och utrymningslarm tillsammans med certifierade larmföretag.", img=5,
      lead="Tillsammans med certifierade larmföretag kan vi utföra installationer av både mindre och större säkerhetssystem.",
      body=[],
      rubrik="Vi arbetar bland annat med", bullets=["Inbrottslarm", "Brandlarm", "Utrymningslarm", "Larmanläggningar för skolor, förskolor, butiker och andra verksamheter"]),
 dict(slug="ombyggnation", title="Ombyggnationer och hyresgästanpassningar", short="El i bostäder, kontor, butiker och restauranger – även där verksamheten pågår.", img=17,
      lead="Vi har lång erfarenhet av elinstallationer vid ombyggnationer och hyresgästanpassningar av bostäder, lägenheter, kontor, industrier, butiker och restauranger.",
      body=["Vi är vana vid att arbeta i fastigheter där verksamhet eller boende pågår samtidigt. Det ställer höga krav på planering, flexibilitet och hänsyn – något våra montörer arbetar aktivt med genom hela projektet."],
      rubrik="Typer av lokaler", bullets=["Bostäder och lägenheter", "Kontor", "Industrier", "Butiker", "Restauranger"]),
]
OVRIGA = ["Installation av värmekabel", "Styr- och reglerteknik", "Elbesiktningar", "EIO-eltest", "Elinstallationer för villor och andra fastigheter"]
REFERENSER = ["Partillebo AB", "Robnor AB", "Smålandsvillan", "Electroheat AB", "SweMaint AB", "Olivergren & Sundberg Fastighets AB", "NCC", "Skanska", "Erlandsson Bygg AB", "Triumf Glass"]
SIFFROR = [("1960", "startade vi i Partille"), ("12", "kompetenta elektriker"), ("15–20 år", "systemgaranti på större datanät"), ("30 %", "ROT-avdrag på arbetskostnaden")]
ORTER = [("Alingsås", "nordost"), ("Partille", "här finns vi"), ("Göteborg", ""), ("Kungsbacka", ""), ("Varberg", "sydväst")]
STEG = [("Hör av dig", f"Ring {TEL} eller skicka ett meddelande och berätta vad du behöver hjälp med."),
        ("Vi planerar", "Vi går igenom uppdraget och föreslår en lösning som passar ditt behov."),
        ("Vi utför jobbet", "Våra montörer kommer med fullt utrustade servicebilar och gör jobbet med hänsyn till dig och din vardag."),
        ("Klart – med ROT", "Gäller arbetet ditt hem hjälper vi dig med ROT-avdraget.")]
FAQ = [("Vilka områden arbetar ni i?", "Vi är verksamma i Partille och Stor-Göteborg, med ett arbetsområde som sträcker sig från Alingsås i nordost till Kungsbacka och Varberg i sydväst."),
       ("Tar ni även mindre jobb?", "Ja. Vi hjälper till med allt från mindre servicearbeten, som att byta ett vägguttag eller en dimmer, till större entreprenader och industriella installationer."),
       ("Kan jag få ROT-avdrag?", "Elinstallationer i ditt hem kan omfattas av ROT-avdrag enligt Skatteverkets regler. Avdraget är 30 % av arbetskostnaden för den som uppfyller villkoren."),
       ("Arbetar ni åt företag och kommuner?", "Ja. Vi arbetar åt privatpersoner, företag, fastighetsägare, byggföretag och kommunal verksamhet."),
       ("Kan ni ta fram ritningar?", "Ja, vi kan projektera och ta fram ritningar i CAD.")]

# ---------------- byggstenar ----------------
def img(n, alt="", pos="50% 50%", lazy=True):
    src = n if isinstance(n, str) else f"img/foto-{n:02d}.jpg"
    return f'<img src="{src}" alt="{E(alt)}"{" loading=\"lazy\"" if lazy else ""} style="object-position:{pos}">'
def logo_svg(bg, bolt): return f'<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="6" fill="{bg}"/><path d="M18.5 5 9 18h6l-1.5 9L23 14h-6z" fill="{bolt}"/></svg>'
LOGO, LOGO_L = logo_svg("#14325c", "#f5c400"), logo_svg("#f5c400", "#0d1a2b")
def checks(lst, cls="checks"): return f'<ul class="{cls}">' + "".join(f"<li>{CHECK}<span>{E(x)}</span></li>" for x in lst) + "</ul>"
def svc_cards(lst, num=True):
    return '<div class="svc-grid">' + "".join(
        f'<a class="svc" href="tjanst-{t["slug"]}.html">{f"<span class=\"svc-n\">{i:02d}</span>" if num else ""}{icon(t["slug"])}<h3>{E(t["title"])}</h3><p>{E(t["short"])}</p><span class="more">Läs mer</span></a>'
        for i, t in enumerate(lst, 1)) + "</div>"
def crumbs(lst): return '<nav class="crumbs" aria-label="Brödsmulor">' + ' <span aria-hidden="true">/</span> '.join(f'<a href="{u}">{E(t)}</a>' if u else f'<span aria-current="page">{E(t)}</span>' for t, u in lst) + "</nav>"
def pghead(h1, lead, cr, media=""):
    return f'<section class="pg-head{" has-media" if media else ""}"><div class="in"><div class="pg-txt">{crumbs(cr)}<h1>{E(h1)}</h1><p>{E(lead)}</p></div>{media}</div></section>'
def pgimg(n, pos="50% 50%"): return f'<div class="pg-media">{img(n, "", pos, lazy=False)}</div>'
def kontaktkort(rubrik="Prata med oss"):
    return f'''<aside class="aside card-dark"><h3>{E(rubrik)}</h3><div class="who"><span class="av" aria-hidden="true">CA</span><div><b>{VD["namn"]}</b><br><span class="sub">{VD["roll"]}</span></div></div><dl><div><dt>Växel</dt><dd><a href="{TEL_HREF}">{TEL}</a></dd></div><div><dt>Direkt</dt><dd><a href="{VD["href"]}">{VD["tel"]}</a></dd></div><div><dt>E-post</dt><dd><a href="mailto:{VD["mejl"]}">{VD["mejl"]}</a></dd></div></dl><a class="btn btn-y" href="kontakt.html">Skicka en förfrågan</a></aside>'''
def section_head(kicker, h2, lead="", center=False):
    return f'<div class="sec-head{" center" if center else ""}"><span class="kicker">{E(kicker)}</span><h2>{E(h2)}</h2>{f"<p>{E(lead)}</p>" if lead else ""}</div>'

NAV = [("tjanster.html", "Tjänster"), ("om-oss.html", "Om oss"), ("referenser.html", "Referenser"), ("rot-avdrag.html", "ROT-avdrag"), ("kontakt.html", "Kontakt")]
def head(title, desc, fn):
    nav = "".join(f'<a href="{u}"{" aria-current=\"page\"" if u == fn or (u == "tjanster.html" and fn.startswith("tjanst-")) else ""}>{t}</a>' for u, t in NAV)
    ovnav = "".join(f'<li><a href="{u}">{t}</a></li>' for u, t in NAV)
    return f'''<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="theme-color" content="#14325c">
<link rel="icon" href="data:image/svg+xml,{LOGO.replace('"', "'").replace("#", "%23")}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="assets/site.css">
<link rel="stylesheet" href="assets/appelgrens.css">
</head>
<body>
<a class="skip" href="#innehall">Hoppa till innehållet</a>
<div class="topbar"><div class="in"><span class="tb-l">Elinstallationer i Partille och Stor-Göteborg sedan 1960</span><span class="tb-r"><a href="{TEL_HREF}">{PHONE}{TEL}</a><a href="mailto:{MEJL}">{MAIL}{MEJL}</a></span></div></div>
<header class="hd">
  <div class="in nav">
    <a class="logo" href="index.html" aria-label="{FIRMA}, till startsidan"><span class="cube">{LOGO}</span><span class="lt">Appelgrens<small>Elektriska AB</small></span></a>
    <nav class="mainnav" aria-label="Huvudmeny">{nav}</nav>
    <a class="btn btn-y hd-cta" href="kontakt.html">Få hjälp</a>
    <button class="burger" id="burger" aria-expanded="false" aria-controls="overlay" aria-label="Öppna menyn"><span></span><span></span><span></span></button>
  </div>
</header>
<div class="overlay" id="overlay" aria-hidden="true" inert>
  <div class="ov-top"><a class="logo" href="index.html"><span class="cube">{LOGO_L}</span>{FIRMA}</a><button class="ov-close" id="menuClose" type="button" aria-label="Stäng menyn">Stäng <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M4 4l12 12M16 4 4 16"/></svg></button></div>
  <nav aria-label="Mobilmeny"><ul>{ovnav}</ul>
  <div class="ov-sub">{"".join(f'<a href="tjanst-{t["slug"]}.html">{E(t["title"])}</a>' for t in TJANSTER)}</div>
  <div class="ov-foot"><a href="{TEL_HREF}">{TEL}</a><a href="mailto:{MEJL}">{MEJL}</a></div></nav>
</div>
'''

def foot():
    return f'''<section class="cta-y" aria-label="Kontakta oss">
  <div class="in"><div><h2>Behöver du en erfaren elektriker?</h2><p>Kontakta oss så hjälper vi dig att hitta en lösning som passar ditt behov.</p></div><div class="cta-btns"><a class="btn btn-dark" href="{TEL_HREF}">{PHONE}Ring {TEL}</a><a class="btn btn-line" href="kontakt.html">Skicka meddelande</a></div></div>
</section>
<footer class="ft">
  <div class="in">
    <div class="ft-grid">
      <div class="ft-brand"><a class="logo" href="index.html"><span class="cube">{LOGO_L}</span>{FIRMA}</a>
        <p>Trygga och professionella elinstallationer i Partille och Stor-Göteborg sedan 1960.</p></div>
      <div><h4>Tjänster</h4><ul>{"".join(f'<li><a href="tjanst-{t["slug"]}.html">{E(t["title"])}</a></li>' for t in TJANSTER)}<li><a href="tjanster.html#ovriga">Övriga tjänster</a></li></ul></div>
      <div><h4>Företaget</h4><ul><li><a href="om-oss.html">Om oss</a></li><li><a href="referenser.html">Referenser</a></li><li><a href="rot-avdrag.html">ROT-avdrag</a></li><li><a href="kontakt.html">Kontakt</a></li></ul></div>
      <div><h4>Kontakt</h4><ul class="ft-contact"><li>{PIN}<span>{ADRESS[0]}<br>{ADRESS[1]}</span></li><li>{PHONE}<a href="{TEL_HREF}">{TEL}</a></li><li>{MAIL}<a href="mailto:{MEJL}">{MEJL}</a></li></ul></div>
    </div>
    <div class="ft-bottom"><span>© 2026 {FIRMA} AB</span><span>Förhandsversion – bilderna är tillfälliga</span><a href="#" data-top>Till toppen ↑</a></div>
  </div>
</footer>
<script src="assets/site.js"></script>
</body>
</html>
'''

def page(fn, title, desc, main):
    full = title if fn == "index.html" else f"{title} – {FIRMA}"
    with open(os.path.join(OUT, fn), "w") as f:
        f.write(head(full, desc, fn) + '<main id="innehall">\n' + main + "\n</main>\n" + foot())

# ---------------- startsidan ----------------
hero_img, hero_pos = IMG["hero"]
stats_band = '<section class="numbers" aria-label="Appelgrens i siffror"><div class="in">' + "".join(f"<div><b>{E(a)}</b><span>{E(b)}</span></div>" for a, b in SIFFROR) + "</div></section>"
logo_wall = '<ul class="logo-wall">' + "".join(f"<li>{E(r)}</li>" for r in REFERENSER) + "</ul>"
steps = '<ol class="steps">' + "".join(f"<li><b>{E(a)}</b><p>{E(b)}</p></li>" for a, b in STEG) + "</ol>"
wire = '<ol class="wire">' + "".join(f'<li{" class=\"home\"" if o == "Partille" else ""}><b>{o}</b>{f"<span>{E(s)}</span>" if s else ""}</li>' for o, s in ORTER) + "</ol>"
faq = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in FAQ)
rot_calc = '''<div class="calc" aria-label="Räkneexempel"><h3>Räkneexempel</h3><dl>
<div><dt>Arbetskostnad</dt><dd>10 000 kr</dd></div><div><dt>ROT-avdrag 30 %</dt><dd>−3 000 kr</dd></div><div class="sum"><dt>Du betalar för arbetet</dt><dd>7 000 kr</dd></div></dl>
<p>Exempel. Avdraget gäller arbetskostnaden och förutsätter att du uppfyller Skatteverkets villkor.</p></div>'''

page("index.html", f"{FIRMA} – Elektriker i Partille och Stor-Göteborg",
     "Appelgrens Elektriska har levererat trygga elinstallationer i Partille med omnejd sedan 1960. Service, entreprenader, industri, data, larm och ROT-avdrag.", f'''
  <section class="hx">
    <div class="in hx-grid">
      <div class="hx-txt">
        <span class="kicker">Elfirma i Partille sedan 1960</span>
        <h1>Trygg el – från vägguttag till <em>maskinpark</em></h1>
        <p>Elinstallationer, service och entreprenader för privatpersoner, företag och industri i Partille och Stor-Göteborg.</p>
        <div class="row"><a class="btn btn-y" href="tjanster.html">Se våra tjänster</a><a class="btn btn-line-w" href="{TEL_HREF}">{PHONE}{TEL}</a></div>
        {checks(["12 kompetenta elektriker", "ROT-avdrag på 30 %", "Från Alingsås till Varberg"], "hx-checks")}
      </div>
      <div class="hx-media">{img(hero_img, "Elektriker från Appelgrens Elektriska", hero_pos, lazy=False)}<div class="hx-badge"><b>60+</b><span>års erfarenhet</span></div></div>
    </div>
  </section>

  <section class="svc-sec">
    <div class="in">
      <div class="sec-row">{section_head("Våra tjänster", "Allt inom el – under samma tak", "Kompletta elinstallationer och eltjänster för privatpersoner, företag och industriverksamheter.")}<a class="arrow" href="tjanster.html">Alla tjänster</a></div>
      {svc_cards(TJANSTER)}
    </div>
  </section>

  {stats_band}

  <section class="about-x">
    <div class="in ax-grid">
      <div class="ax-txt">
        {section_head("Om oss", "Vår kunskap och service gör dig nöjd")}
        <p class="lead">Med över 60 års erfarenhet, bred kompetens och ett engagerat team hjälper vi våra kunder med trygga elinstallationer, service och entreprenader i Partille och Stor-Göteborg.</p>
        {checks(["Uppdrag inom industri, byggnation, kommunal verksamhet och privatmarknaden", "Certifierade datainstallatörer för ELKO och Lexcom", "Projektering och ritningar i CAD"])}
        <div class="ax-card"><span class="av" aria-hidden="true">CA</span><div><b>{VD["namn"]}</b><span>{VD["roll"]}</span><a href="{VD["href"]}">{VD["tel"]}</a></div></div>
        <a class="arrow" href="om-oss.html">Mer om oss</a>
      </div>
      <div class="ax-media">{img(IMG["om"][0], "", IMG["om"][1])}</div>
    </div>
  </section>

  <section class="how">
    <div class="in">
      {section_head("Så går det till", "Enkelt från första samtalet", center=True)}
      {steps}
    </div>
  </section>

  <section class="rot-x">
    <div class="in rx-grid">
      <div>{section_head("ROT-avdrag", "Sänk kostnaden för elarbetet hemma", "För privatpersoner som uppfyller Skatteverkets villkor kan ROT-avdraget innebära ett avdrag på 30 % av arbetskostnaden. Vi hjälper dig med ansökan.")}
        <a class="btn btn-dark" href="rot-avdrag.html">Så fungerar ROT-avdraget</a></div>
      {rot_calc}
    </div>
  </section>

  <section class="refs-sec">
    <div class="in">
      <div class="sec-row">{section_head("Referenser", "De har anlitat oss")}<a class="arrow" href="referenser.html">Alla referenser</a></div>
      {logo_wall}
    </div>
  </section>

  <section class="area">
    <div class="in">
      {section_head("Arbetsområde", "Partille och Stor-Göteborg", "Vårt arbetsområde sträcker sig från Alingsås i nordost till Kungsbacka och Varberg i sydväst.", center=True)}
      {wire}
    </div>
  </section>

  <section class="faq-x">
    <div class="in fx-grid">
      <div>{section_head("Vanliga frågor", "Undrar du något?", f"Hittar du inte svaret? Ring oss på {TEL}.")}</div>
      <div class="acc">{faq}</div>
    </div>
  </section>''')

# ---------------- tjänster ----------------
page("tjanster.html", "Våra tjänster", "Elinstallationer och eltjänster för privatpersoner, företag och industri i Partille och Stor-Göteborg.",
     pghead("Våra tjänster", "Kompletta elinstallationer och eltjänster för privatpersoner, företag och industriverksamheter.", [("Start", "index.html"), ("Tjänster", None)])
     + f'''<section><div class="in">{svc_cards(TJANSTER)}</div></section>
<section class="tint" id="ovriga"><div class="in content"><div class="prose"><h2 style="margin-top:0">Lång erfarenhet och bred kompetens</h2><p>{FIRMA} erbjuder kompletta elinstallationer och eltjänster för privatpersoner, företag och industriverksamheter. Med lång erfarenhet och bred kompetens hjälper vi våra kunder med allt från mindre servicearbeten till större entreprenader och industriella installationer.</p><h2>Övriga tjänster</h2><p>Vi erbjuder även:</p>{checks(OVRIGA)}</div>{kontaktkort()}</div></section>''')

for t in TJANSTER:
    others = [o for o in TJANSTER if o is not t]
    page(f"tjanst-{t['slug']}.html", t["title"], t["lead"],
         pghead(t["title"], t["lead"], [("Start", "index.html"), ("Tjänster", "tjanster.html"), (t["title"], None)], pgimg(t["img"]))
         + f'''<section><div class="in content"><div class="prose">{"".join(f"<p>{E(p)}</p>" for p in t["body"])}<h2{' style="margin-top:0"' if not t["body"] else ""}>{E(t["rubrik"])}</h2>{checks(t["bullets"], "checks two")}<div class="note">{PHONE}<p>Berätta vad du behöver hjälp med, så återkommer vi. Ring <a href="{TEL_HREF}">{TEL}</a> eller mejla <a href="mailto:{MEJL}">{MEJL}</a>.</p></div></div>{kontaktkort()}</div></section>
<section class="tint"><div class="in"><div class="sec-row">{section_head("Fler tjänster", "Det här gör vi också")}<a class="arrow" href="tjanster.html#ovriga">Övriga tjänster</a></div>{svc_cards(others, num=False)}</div></section>''')

# ---------------- om oss ----------------
page("om-oss.html", "Om oss", "Appelgrens Elektriska har levererat elinstallationer i Partille med omnejd sedan 1960. Idag är vi 12 elektriker.",
     pghead("Om Appelgrens Elektriska", "Trygga och professionella elinstallationer i Partille med omnejd sedan 1960.", [("Start", "index.html"), ("Om oss", None)], pgimg(IMG["om"][0], IMG["om"][1]))
     + stats_band
     + f'''<section><div class="in content"><div class="prose">
<p class="lead">{FIRMA} har levererat trygga och professionella elinstallationer i Partille med omnejd sedan <b>1960</b>.</p>
<p>Under årens lopp har företaget byggt upp en stark position på den lokala marknaden. Idag består verksamheten av <b>12 kompetenta elektriker</b> som hjälper både privatpersoner, företag och organisationer med elinstallationer, service och reparationer.</p>
<p>Våra uppdrag omfattar allt från mindre servicearbeten till större projekt inom bland annat industri, byggnation, kommunal verksamhet och privatmarknaden.</p>
<h2>Var vi arbetar</h2><p>Vi är verksamma i <b>Partille och Stor-Göteborg</b>, med ett arbetsområde som sträcker sig från <b>Alingsås i nordost till Kungsbacka och Varberg i sydväst</b>.</p>
{wire}
<h2>Behöver du en erfaren elektriker?</h2><p>Kontakta {FIRMA} så hjälper vi dig att hitta en lösning som passar ditt behov. Ring <a href="{TEL_HREF}">{TEL}</a>.</p></div>{kontaktkort("Ledning")}</div></section>
<section class="tint"><div class="in">{section_head("Det här gör vi", "Våra tjänster")}{svc_cards(TJANSTER)}</div></section>''')

# ---------------- referenser ----------------
page("referenser.html", "Referenser", "Några av Appelgrens Elektriskas tidigare och nuvarande kunder: Partillebo, NCC, Skanska, Robnor med flera.",
     pghead("Våra referenser", "Under våra många år i branschen har vi arbetat med ett stort antal kunder inom privat och offentlig verksamhet samt olika delar av näringslivet.", [("Start", "index.html"), ("Referenser", None)])
     + f'''<section><div class="in">{section_head("Kunder", "Några av våra tidigare och nuvarande referenser")}{logo_wall}<p class="lead" style="margin-top:28px">Vill du veta mer om något av uppdragen? <a class="arrow" href="kontakt.html">Kontakta oss</a></p></div></section>''')

# ---------------- ROT ----------------
def fld(i, label, typ="text", req=True, auto=""):
    return f'<label for="{i}">{label}{"" if req else " <small>(valfritt)</small>"}<input id="{i}" name="{i}" type="{typ}"{" required" if req else ""}{f" autocomplete=\"{auto}\"" if auto else ""}></label>'
page("rot-avdrag.html", "ROT-avdrag", "Elinstallationer kan omfattas av ROT-avdrag – 30 % av arbetskostnaden. Så lämnar du uppgifterna till oss.",
     pghead("ROT-avdrag", "Elinstallationer i hemmet kan ge 30 % avdrag på arbetskostnaden.", [("Start", "index.html"), ("ROT-avdrag", None)], pgimg(IMG["rot"], "50% 40%"))
     + f'''<section><div class="in content"><div class="prose"><h2 style="margin-top:0">Så fungerar det</h2>
<p>Vi utför elinstallationer som kan omfattas av ROT-avdrag enligt Skatteverkets regler.</p>
<p>För privatpersoner som uppfyller villkoren kan ROT-avdraget innebära ett avdrag på <b>30 % av arbetskostnaden</b>.</p>
{rot_calc}
<h2>Uppgifter vi behöver</h2><p>För att vi ska kunna hantera ROT-avdraget behöver vi vissa uppgifter från dig, bland annat:</p>
{checks(["Namn", "Personnummer", "Fastighets- eller lägenhetsbeteckning", "BRF:s organisationsnummer, om du bor i bostadsrätt", "E-postadress", "Telefonnummer"], "checks two")}
<h3 style="margin-top:10px">Medsökande</h3><p>Om det finns en medsökande behöver även följande uppgifter lämnas:</p>
{checks(["Medsökandes namn", "Medsökandes personnummer", "Fastighets- eller lägenhetsbeteckning", "BRF:s organisationsnummer, om tillämpligt"], "checks two")}
<p>När alla uppgifter är ifyllda skickar du in formuläret så hjälper vi dig vidare.</p><a class="btn btn-dark" href="#formular" style="align-self:start">Till formuläret</a></div>{kontaktkort("Frågor om ROT?")}</div></section>
<section class="tint" id="formular"><div class="in"><form class="cform form-card" data-demo>
  <h2>Uppgifter för ROT-avdrag</h2>
  <div class="f2">{fld("rn", "Namn", auto="name")}{fld("rp", "Personnummer", auto="off")}{fld("rf", "Fastighets- eller lägenhetsbeteckning")}{fld("rb", "BRF:s organisationsnummer", req=False)}{fld("re", "E-post", "email", auto="email")}{fld("rt", "Telefon", "tel", auto="tel")}</div>
  <fieldset class="med"><legend>Medsökande (om det finns)</legend><div class="f2">{fld("mn", "Medsökandes namn", req=False)}{fld("mp", "Medsökandes personnummer", req=False)}{fld("mf", "Fastighets- eller lägenhetsbeteckning", req=False)}{fld("mb", "BRF:s organisationsnummer", req=False)}</div></fieldset>
  <button class="btn btn-y" type="submit" style="justify-self:start">Skicka uppgifterna</button>
  <p class="form-ok" hidden tabindex="-1">{E(FORM_OK)}</p>
</form></div></section>''')

# ---------------- kontakt ----------------
page("kontakt.html", "Kontakt", f"Kontakta Appelgrens Elektriska i Partille: {TEL}, {MEJL}, {ADRESS[0]}.",
     pghead("Kontakta oss", "Har du frågor, behöver hjälp med en elinstallation eller vill du komma i kontakt med oss? Fyll i formuläret så återkommer vi.", [("Start", "index.html"), ("Kontakt", None)])
     + f'''<section><div class="in">
  <div class="cards-c">
    <a class="cc" href="{TEL_HREF}">{PHONE}<span>Telefon</span><b>{TEL}</b></a>
    <a class="cc" href="mailto:{MEJL}">{MAIL}<span>E-post</span><b>{MEJL}</b></a>
    <a class="cc" href="{KARTA}" target="_blank" rel="noopener">{PIN}<span>Besöksadress</span><b>{ADRESS[0]}, {ADRESS[1]}</b></a>
  </div>
  <div class="content" style="margin-top:48px"><form class="cform form-card" data-demo>
    <h2>Skicka ett meddelande</h2>
    <div class="f2">{fld("cn", "Namn", auto="name")}{fld("ce", "E-post", "email", auto="email")}</div>{fld("cs", "Ämne")}
    <label for="cm">Meddelande<textarea id="cm" name="cm" required></textarea></label>
    <button class="btn btn-y" type="submit" style="justify-self:start">Skicka</button>
    <p class="form-ok" hidden tabindex="-1">{E(FORM_OK)}</p>
  </form>
  {kontaktkort("Direktkontakt")}</div></div></section>''')

# ---------------- 404 ----------------
with open(os.path.join(OUT, "404.html"), "w") as f:
    f.write(f'''<!doctype html>
<html lang="sv"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sidan finns inte – {FIRMA}</title>
<style>body{{margin:0;min-height:100vh;display:grid;place-items:center;background:#0d1a2b;color:#fff;font:17px/1.6 system-ui,sans-serif;text-align:center;padding:20px}}h1{{color:#f5c400;margin:0 0 8px;font-size:2.4rem}}a{{color:#f5c400;font-weight:700}}</style></head>
<body><div><h1>Sidan finns inte</h1><p>Den här sidan hittades inte. <a href="./">Till startsidan</a> eller ring <a href="{TEL_HREF}">{TEL}</a>.</p></div></body></html>
''')
print("Klart:", OUT)
