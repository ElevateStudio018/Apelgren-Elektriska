"""Bygger Appelgrens Elektriskas statiska sidor.

Kör från repots rot:  python3 tools/appelgrens.py .
Allt innehåll står i listorna nedan. Bilderna väljs i IMG; byt numren (eller
sökvägarna) när riktiga bilder från appelgrensel.se finns i img/.
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
IMG = dict(hero=[(1, "50% 50%"), (19, "50% 50%"), (6, "50% 50%")], om=4, kontakt=14, referenser=6, rot=10, tjanster=1)

# ---------------- innehåll ----------------
TJANSTER = [
 dict(slug="nyinstallation", title="Nyinstallation och entreprenader", short="Skolor, bostäder, industri och kontor", img=1,
      lead="Vi har lång erfarenhet av projektering och installation inom både privat och offentlig verksamhet.",
      body=["Våra uppdrag omfattar bland annat skolor, förskolor, gruppboenden, lägenheter, villor, industrier och kontorslokaler.",
            "Vi kan även projektera och ta fram ritningar i CAD."],
      rubrik="Exempel på uppdrag", bullets=["Skolor och förskolor", "Gruppboenden", "Lägenheter och villor", "Industrier", "Kontorslokaler", "Projektering och ritningar i CAD"]),
 dict(slug="service", title="Service och reparation", short="Stora som små jobb – fullt utrustade servicebilar", img=10,
      lead="Vi utför alla typer av elservice och reparationer – oavsett om det gäller ett mindre jobb eller en större installation.",
      body=["Våra servicebilar är fullt utrustade och våra montörer är redo att hjälpa till."],
      rubrik="Vi hjälper bland annat till med", bullets=["Byte och installation av dimmers och vägguttag", "Elinstallationer i kök och badrum", "Elinstallationer vid nybyggnation", "Felsökning och reparation", "Service och underhåll", "Installation av golvvärme"]),
 dict(slug="industri", title="Industri- och maskininstallationer", short="Maskiner, automatikskåp och PLC", img=21,
      lead="Genom många års erfarenhet inom industrin har vi byggt upp gedigen kompetens inom service, utveckling och installation av industri- och verkstadsmaskiner.",
      body=[],
      rubrik="Vi hjälper våra kunder med bland annat", bullets=["Felsökning och reparation", "Ombyggnad och effektivisering av maskiner", "Installation och utveckling av maskinparker", "Konstruktion och byggnation av automatikskåp", "PLC-programmering", "Elinstallationer och styrsystem"]),
 dict(slug="data-tele", title="Data- och teleinstallationer", short="Certifierade för ELKO och Lexcom", img=19,
      lead="Vi är certifierade datainstallatörer för ELKO och Lexcoms datanät.",
      body=["Vid större installationer och nät kan vi erbjuda systemgarantier på 15–20 år."],
      rubrik="Vi installerar och servar även", bullets=["Datanät", "Teleinstallationer", "Passagesystem", "Porttelefoner"]),
 dict(slug="larm", title="Larm och säkerhet", short="Inbrotts-, brand- och utrymningslarm", img=5,
      lead="Tillsammans med certifierade larmföretag kan vi utföra installationer av både mindre och större säkerhetssystem.",
      body=[],
      rubrik="Vi arbetar bland annat med", bullets=["Inbrottslarm", "Brandlarm", "Utrymningslarm", "Larmanläggningar för skolor, förskolor, butiker och andra verksamheter"]),
 dict(slug="ombyggnation", title="Ombyggnationer och hyresgästanpassningar", short="El i fastigheter där livet pågår", img=17,
      lead="Vi har lång erfarenhet av elinstallationer vid ombyggnationer och hyresgästanpassningar av bostäder, lägenheter, kontor, industrier, butiker och restauranger.",
      body=["Vi är vana vid att arbeta i fastigheter där verksamhet eller boende pågår samtidigt. Det ställer höga krav på planering, flexibilitet och hänsyn – något våra montörer arbetar aktivt med genom hela projektet."],
      rubrik="Typer av lokaler", bullets=["Bostäder och lägenheter", "Kontor", "Industrier", "Butiker", "Restauranger"]),
]
OVRIGA = ["Installation av värmekabel", "Styr- och reglerteknik", "Elbesiktningar", "EIO-eltest", "Elinstallationer för villor och andra fastigheter"]
REFERENSER = ["Partillebo AB", "Robnor AB", "Smålandsvillan", "Electroheat AB", "SweMaint AB", "Olivergren & Sundberg Fastighets AB", "NCC", "Skanska", "Erlandsson Bygg AB", "Triumf Glass"]
FAKTA = [("1960", "grundat i Partille"), ("12", "kompetenta elektriker"), ("60+", "års erfarenhet")]

# ---------------- byggstenar ----------------
def img(n, alt="", pos="50% 50%", lazy=True):
    src = n if isinstance(n, str) else f"img/foto-{n:02d}.jpg"
    return f'<img class="photo" src="{src}" alt="{E(alt)}"{" loading=\"lazy\"" if lazy else ""} style="object-position:{pos}">'
def ph(n, alt="", pos="50% 50%"): return f'<div class="ph">{img(n, alt, pos)}</div>'
FAVICON = "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%2314325c'/><text x='16' y='23' font-family='Arial' font-weight='700' font-size='20' fill='%23ffffff' text-anchor='middle'>A</text></svg>"
def ul(lst): return "<ul>" + "".join(f"<li>{E(x)}</li>" for x in lst) + "</ul>"
def tiles(lst): return '<div class="tiles">' + "".join(f'<a class="tile" href="tjanst-{t["slug"]}.html">{img(t["img"])}<span><b>{E(t["title"])}</b><small>{E(t["short"])}</small></span></a>' for t in lst) + "</div>"
def crumbs(lst): return '<nav class="crumbs" aria-label="Brödsmulor">' + ' <span aria-hidden="true">/</span> '.join(f'<a href="{u}">{E(t)}</a>' if u else f"<span>{E(t)}</span>" for t, u in lst) + "</nav>"
def phero(n, h1, lead, cr, pos="50% 50%"): return f'<section class="phero" aria-label="{E(h1)}">{ph(n, "", pos)}<div class="in">{crumbs(cr)}<h1>{E(h1)}</h1><p>{E(lead)}</p></div></section>'
def kontaktkort(rubrik="Prata med oss"):
    return f'''<aside class="aside"><h3>{E(rubrik)}</h3><div class="who"><span class="av" aria-hidden="true">CA</span><div><b>{VD["namn"]}</b><br><span style="color:var(--muted);font-size:14px">{VD["roll"]}</span></div></div><dl><div><dt>Växel</dt><dd><a href="{TEL_HREF}">{TEL}</a></dd></div><div><dt>Direkt</dt><dd><a href="{VD["href"]}">{VD["tel"]}</a></dd></div><div><dt>E-post</dt><dd><a href="mailto:{VD["mejl"]}">{VD["mejl"]}</a></dd></div></dl><a class="btn btn-g" href="kontakt.html">Skicka en förfrågan</a></aside>'''
LOGO_TXT = '<span class="wm">Appelgrens</span> Elektriska'

def head(title, desc):
    nav = "".join(f'<li><a href="{u}">{t}</a></li>' for u, t in [("tjanster.html", "Våra tjänster"), ("om-oss.html", "Om oss"), ("referenser.html", "Referenser"), ("rot-avdrag.html", "ROT-avdrag"), ("kontakt.html", "Kontakt")])
    return f'''<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="theme-color" content="#14325c">
<link rel="icon" href="data:image/svg+xml,{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Source+Sans+3:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="assets/site.css">
<link rel="stylesheet" href="assets/appelgrens.css">
</head>
<body>
<div class="demo">Förhandsversion av nya hemsidan. Bilderna är tillfälliga.</div>
<header>
  <div class="in nav">
    <a class="logo" href="index.html" aria-label="{FIRMA}, till startsidan">{LOGO_TXT}</a>
    <a class="hdr-tel" href="{TEL_HREF}">{TEL}</a>
    <button class="burger" id="burger" aria-expanded="false" aria-controls="overlay" aria-label="Öppna menyn"><span></span><span></span><span></span></button>
    <a class="btn btn-g" href="kontakt.html">Kontakta oss</a>
  </div>
</header>
<div class="overlay" id="overlay" aria-hidden="true" inert>
  <div class="ov-top"><a class="logo" href="index.html">{LOGO_TXT}</a><button class="ov-close" id="menuClose" type="button" aria-label="Stäng menyn">Stäng</button></div>
  <nav aria-label="Huvudmeny"><ul>{nav}</ul>
  <div class="ov-sub">{"".join(f'<a href="tjanst-{t["slug"]}.html">{E(t["title"])}</a>' for t in TJANSTER)}</div>
  <div class="ov-foot"><span>{TEL}</span><span>{MEJL}</span><span>{ADRESS[0]}, Partille</span></div></nav>
</div>
'''

def foot():
    return f'''<section class="fcta" aria-label="Kontakta oss">
  <div class="in"><div><h2>Behöver du en erfaren elektriker?</h2><p>Ring {TEL} eller skicka ett meddelande, så hjälper vi dig att hitta en lösning som passar ditt behov.</p></div><a class="btn btn-w" href="kontakt.html">Kontakta oss</a></div>
</section>
<footer>
  <div class="in">
    <div class="fgrid">
      <div><a class="logo" href="index.html">{LOGO_TXT}</a>
        <p style="margin-top:14px;max-width:36ch">Trygga och professionella elinstallationer i Partille och Stor-Göteborg sedan 1960.</p>
        <p style="margin-top:12px">{FIRMA} AB<br>{ADRESS[0]}, {ADRESS[1]}<br><a href="{TEL_HREF}">{TEL}</a> · <a href="mailto:{MEJL}">{MEJL}</a></p>
      </div>
      <div><h4>Våra tjänster</h4><ul>{"".join(f'<li><a href="tjanst-{t["slug"]}.html">{E(t["title"])}</a></li>' for t in TJANSTER)}<li><a href="tjanster.html#ovriga">Övriga tjänster</a></li></ul></div>
      <div><h4>Om Appelgrens</h4><ul><li><a href="om-oss.html">Om oss</a></li><li><a href="referenser.html">Referenser</a></li><li><a href="rot-avdrag.html">ROT-avdrag</a></li><li><a href="kontakt.html">Kontakt</a></li></ul></div>
      <div><h4>Direktkontakt</h4><ul><li>{VD["namn"]}, {VD["roll"].lower()}</li><li><a href="{VD["href"]}">{VD["tel"]}</a></li><li><a href="mailto:{VD["mejl"]}">{VD["mejl"]}</a></li></ul></div>
    </div>
    <div class="fbottom"><span>© 2026 {FIRMA} AB</span><a class="totop" href="#" data-top>Till toppen</a></div>
  </div>
</footer>
<script src="assets/site.js"></script>
</body>
</html>
'''

def page(fn, title, desc, main):
    full = title if fn == "index.html" else f"{title} – {FIRMA}"
    with open(os.path.join(OUT, fn), "w") as f:
        f.write(head(full, desc) + "<main" + (' id="top"' if fn == "index.html" else "") + ">\n" + main + "\n</main>\n" + foot())

# ---------------- startsidan ----------------
slides = "".join(f'<div class="ph slide{" on" if i == 0 else ""}">{img(n, "", pos, lazy=False)}</div>' for i, (n, pos) in enumerate(IMG["hero"]))
dots = "".join(f'<button aria-label="Bild {i + 1}"{" aria-current=\"true\"" if i == 0 else ""}></button>' for i in range(len(IMG["hero"])))
facts = '<div class="facts">' + "".join(f"<div><b>{a}</b><span>{E(b)}</span></div>" for a, b in FAKTA) + "</div>"
refchips = '<ul class="refs">' + "".join(f"<li>{E(r)}</li>" for r in REFERENSER) + "</ul>"
FAQ = [("Vilka områden arbetar ni i?", "Vi är verksamma i Partille och Stor-Göteborg, med ett arbetsområde som sträcker sig från Alingsås i nordost till Kungsbacka och Varberg i sydväst."),
       ("Tar ni även mindre jobb?", "Ja. Vi hjälper till med allt från mindre servicearbeten, som att byta ett vägguttag eller en dimmer, till större entreprenader och industriella installationer."),
       ("Kan jag få ROT-avdrag?", "Elinstallationer i ditt hem kan omfattas av ROT-avdrag enligt Skatteverkets regler. Avdraget är 30 % av arbetskostnaden för den som uppfyller villkoren."),
       ("Arbetar ni åt företag och kommuner?", "Ja. Vi arbetar åt privatpersoner, företag, fastighetsägare, byggföretag och kommunal verksamhet."),
       ("Kan ni ta fram ritningar?", "Ja, vi kan projektera och ta fram ritningar i CAD.")]
faq = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in FAQ)
page("index.html", f"{FIRMA} – Elektriker i Partille och Stor-Göteborg",
     "Appelgrens Elektriska har levererat trygga elinstallationer i Partille med omnejd sedan 1960. Service, entreprenader, industri, data, larm och ROT-avdrag.", f'''
  <section class="hero" aria-label="Välkommen">
    {slides}
    <div class="in">
      <h1>Trygg el i Partille sedan 1960</h1>
      <p>Elinstallationer, service och entreprenader för privatpersoner, företag och industri i Partille och Stor-Göteborg.</p>
      <div class="row"><a class="btn btn-w" href="tjanster.html">Våra tjänster</a><a class="btn btn-o" href="{TEL_HREF}" style="color:#fff">Ring {TEL}</a>
        <div class="dots" role="group" aria-label="Byt bild">{dots}</div></div>
    </div>
  </section>

  <section id="tjanster">
    <div class="in">
      <div class="headrow"><div><h2>Våra tjänster</h2><p class="lead" style="margin-top:12px">Från mindre servicearbeten till större entreprenader och industriella installationer.</p></div><a class="arrow" href="tjanster.html">Alla tjänster</a></div>
      {tiles(TJANSTER)}
    </div>
  </section>

  <section class="about" id="om">
    <div class="in about2">
      <div class="media">{ph(IMG["om"], "", "50% 30%")}</div>
      <div class="txt">
        <h2 style="margin-top:8px">Vår kunskap och service gör dig nöjd</h2>
        <p class="lead" style="margin-top:14px">Med över 60 års erfarenhet, bred kompetens och ett engagerat team hjälper vi våra kunder med trygga elinstallationer, service och entreprenader i Partille och Stor-Göteborg.</p>
        {facts}
        <div class="minis">
          <a class="mini" href="om-oss.html"><b>Om oss</b><span>Ett lokalt elföretag med en stark position i Partille.</span></a>
          <a class="mini" href="referenser.html"><b>Referenser</b><span>NCC, Skanska, Partillebo och många fler.</span></a>
          <a class="mini" href="rot-avdrag.html"><b>ROT-avdrag</b><span>30 % avdrag på arbetskostnaden för privatpersoner.</span></a>
        </div>
      </div>
    </div>
  </section>

  <section class="band" aria-label="ROT-avdrag">
    {ph(IMG["rot"], "", "50% 40%")}
    <div class="in">
      <h2>ROT-avdrag på elarbeten i hemmet</h2>
      <p>För privatpersoner som uppfyller Skatteverkets villkor kan ROT-avdraget innebära ett avdrag på 30 % av arbetskostnaden. Vi hjälper dig med ansökan.</p>
      <div><a class="btn btn-w" href="rot-avdrag.html">Så fungerar ROT-avdraget</a></div>
    </div>
  </section>

  <section id="referenser" style="background:var(--beige)">
    <div class="in">
      <div class="headrow"><div><h2>Några av våra referenser</h2><p class="lead" style="margin-top:12px">Vi har arbetat med ett stort antal kunder inom privat och offentlig verksamhet och olika delar av näringslivet.</p></div><a class="arrow" href="referenser.html">Alla referenser</a></div>
      {refchips}
    </div>
  </section>

  <section id="omrade">
    <div class="in sust">
      <div class="box">
        <h2>Från Alingsås till Varberg</h2>
        <p>Vi utgår från Partille och arbetar i hela Stor-Göteborg – från Alingsås i nordost till Kungsbacka och Varberg i sydväst.</p>
        <div><a class="btn btn-w" href="{KARTA}" target="_blank" rel="noopener">Hitta till oss</a></div>
      </div>
      <div class="mosaic">
        <div class="t sand"><b>12</b><span>elektriker</span></div>
        <div class="t sage"><b>1960</b><span>startade vi i Partille</span></div>
        <div class="t sage"><b>15–20 år</b><span>systemgaranti på större datanät</span></div>
        <div class="t sand"><b>30 %</b><span>ROT-avdrag på arbetskostnaden</span></div>
      </div>
    </div>
  </section>

  <section id="faq" style="background:var(--beige)">
    <div class="in faq">
      <div><h2 style="margin-top:8px">Vanliga frågor</h2><p class="lead" style="margin-top:14px">Hittar du inte svaret? Ring oss på {TEL}.</p><a class="arrow" style="margin-top:18px" href="kontakt.html">Fråga oss något annat</a></div>
      <div>{faq}</div>
    </div>
  </section>''')

# ---------------- tjänster ----------------
page("tjanster.html", "Våra tjänster", "Elinstallationer och eltjänster för privatpersoner, företag och industri i Partille och Stor-Göteborg.",
     phero(IMG["tjanster"], "Våra tjänster", "Kompletta elinstallationer och eltjänster för privatpersoner, företag och industriverksamheter.", [("Start", "index.html"), ("Våra tjänster", None)])
     + f'''<section><div class="in">{tiles(TJANSTER)}</div></section>
<section class="related" id="ovriga"><div class="in content"><div class="prose"><h2 style="margin-top:0">Lång erfarenhet och bred kompetens</h2><p>{FIRMA} erbjuder kompletta elinstallationer och eltjänster för privatpersoner, företag och industriverksamheter. Med lång erfarenhet och bred kompetens hjälper vi våra kunder med allt från mindre servicearbeten till större entreprenader och industriella installationer.</p><h2>Övriga tjänster</h2><p>Vi erbjuder även:</p>{ul(OVRIGA)}</div>{kontaktkort()}</div></section>''')

for t in TJANSTER:
    others = "".join(f'<a href="tjanst-{o["slug"]}.html">{E(o["title"])}</a>' for o in TJANSTER if o is not t)
    page(f"tjanst-{t['slug']}.html", t["title"], t["lead"],
         phero(t["img"], t["title"], t["lead"], [("Start", "index.html"), ("Våra tjänster", "tjanster.html"), (t["title"], None)])
         + f'''<section><div class="in content"><div class="prose">{"".join(f"<p>{E(p)}</p>" for p in t["body"])}<h2{' style="margin-top:0"' if not t["body"] else ""}>{E(t["rubrik"])}</h2>{ul(t["bullets"])}<h2>Kontakta oss</h2><p>Berätta vad du behöver hjälp med, så återkommer vi. Du når oss på <a href="{TEL_HREF}">{TEL}</a> eller <a href="mailto:{MEJL}">{MEJL}</a>.</p></div>{kontaktkort()}</div></section>
<section class="related"><div class="in"><h2>Fler tjänster</h2><div class="links-row">{others}<a href="tjanster.html#ovriga">Övriga tjänster</a></div></div></section>''')

# ---------------- om oss ----------------
page("om-oss.html", "Om oss", "Appelgrens Elektriska har levererat elinstallationer i Partille med omnejd sedan 1960. Idag är vi 12 elektriker.",
     phero(IMG["om"], "Om Appelgrens Elektriska", "Trygga och professionella elinstallationer i Partille med omnejd sedan 1960.", [("Start", "index.html"), ("Om oss", None)], "50% 30%")
     + f'''<section><div class="in content"><div class="prose">{facts.replace('class="facts"', 'class="stats"')}
<p>{FIRMA} har levererat trygga och professionella elinstallationer i Partille med omnejd sedan <b>1960</b>.</p>
<p>Under årens lopp har företaget byggt upp en stark position på den lokala marknaden. Idag består verksamheten av <b>12 kompetenta elektriker</b> som hjälper både privatpersoner, företag och organisationer med elinstallationer, service och reparationer.</p>
<p>Våra uppdrag omfattar allt från mindre servicearbeten till större projekt inom bland annat industri, byggnation, kommunal verksamhet och privatmarknaden.</p>
<h2>Var vi arbetar</h2><p>Vi är verksamma i <b>Partille och Stor-Göteborg</b>, med ett arbetsområde som sträcker sig från <b>Alingsås i nordost till Kungsbacka och Varberg i sydväst</b>.</p>
<h2>Behöver du en erfaren elektriker?</h2><p>Kontakta {FIRMA} så hjälper vi dig att hitta en lösning som passar ditt behov. Ring <a href="{TEL_HREF}">{TEL}</a>.</p></div>{kontaktkort("Ledning")}</div></section>
<section class="related"><div class="in"><h2>Det här gör vi</h2><div style="margin-top:24px">{tiles(TJANSTER)}</div></div></section>''')

# ---------------- referenser ----------------
page("referenser.html", "Referenser", "Några av Appelgrens Elektriskas tidigare och nuvarande kunder: Partillebo, NCC, Skanska, Robnor med flera.",
     phero(IMG["referenser"], "Våra referenser", "Under våra många år i branschen har vi arbetat med ett stort antal kunder inom privat och offentlig verksamhet samt olika delar av näringslivet.", [("Start", "index.html"), ("Referenser", None)])
     + f'''<section><div class="in content"><div class="prose"><h2 style="margin-top:0">Några av våra tidigare och nuvarande referenser</h2>{refchips}<p style="margin-top:24px">Vill du veta mer om något av uppdragen? Kontakta oss så berättar vi gärna.</p></div>{kontaktkort()}</div></section>''')

# ---------------- ROT ----------------
def fld(i, label, typ="text", req=True, auto=""):
    return f'<label for="{i}">{label}<input id="{i}" name="{i}" type="{typ}"{" required" if req else ""}{f" autocomplete=\"{auto}\"" if auto else ""}></label>'
page("rot-avdrag.html", "ROT-avdrag", "Elinstallationer kan omfattas av ROT-avdrag – 30 % av arbetskostnaden. Så lämnar du uppgifterna till oss.",
     phero(IMG["rot"], "ROT-avdrag", "Elinstallationer i hemmet kan ge 30 % avdrag på arbetskostnaden.", [("Start", "index.html"), ("ROT-avdrag", None)], "50% 40%")
     + f'''<section><div class="in content"><div class="prose"><h2 style="margin-top:0">Så fungerar det</h2>
<p>Vi utför elinstallationer som kan omfattas av ROT-avdrag enligt Skatteverkets regler.</p>
<p>För privatpersoner som uppfyller villkoren kan ROT-avdraget innebära ett avdrag på <b>30 % av arbetskostnaden</b>.</p>
<h2>Uppgifter vi behöver</h2><p>För att vi ska kunna hantera ROT-avdraget behöver vi vissa uppgifter från dig, bland annat:</p>
{ul(["Namn", "Personnummer", "Fastighets- eller lägenhetsbeteckning", "BRF:s organisationsnummer, om du bor i bostadsrätt", "E-postadress", "Telefonnummer"])}
<h3 style="margin-top:20px">Medsökande</h3><p>Om det finns en medsökande behöver även följande uppgifter lämnas:</p>
{ul(["Medsökandes namn", "Medsökandes personnummer", "Fastighets- eller lägenhetsbeteckning", "BRF:s organisationsnummer, om tillämpligt"])}
<p>När alla uppgifter är ifyllda skickar du in formuläret så hjälper vi dig vidare.</p></div>{kontaktkort("Frågor om ROT?")}</div></section>
<section class="related" id="formular"><div class="in"><form class="cform" data-demo>
  <h2>Uppgifter för ROT-avdrag</h2>
  {fld("rn", "Namn", auto="name")}{fld("rp", "Personnummer", auto="off")}{fld("rf", "Fastighets- eller lägenhetsbeteckning")}{fld("rb", "BRF:s organisationsnummer (om bostadsrätt)", req=False)}{fld("re", "E-post", "email", auto="email")}{fld("rt", "Telefon", "tel", auto="tel")}
  <fieldset class="med"><legend>Medsökande (om det finns)</legend>{fld("mn", "Medsökandes namn", req=False)}{fld("mp", "Medsökandes personnummer", req=False)}{fld("mf", "Fastighets- eller lägenhetsbeteckning", req=False)}{fld("mb", "BRF:s organisationsnummer (om tillämpligt)", req=False)}</fieldset>
  <button class="btn btn-g" type="submit" style="justify-self:start">Skicka uppgifterna</button>
  <p class="form-ok" hidden tabindex="-1">{E(FORM_OK)}</p>
</form></div></section>''')

# ---------------- kontakt ----------------
page("kontakt.html", "Kontakt", f"Kontakta Appelgrens Elektriska i Partille: {TEL}, {MEJL}, {ADRESS[0]}.",
     f'''<section class="phero plain"><div class="in">{crumbs([("Start", "index.html"), ("Kontakt", None)])}<h1>Kontakta oss</h1><p>Har du frågor, behöver hjälp med en elinstallation eller vill du komma i kontakt med oss? Fyll i formuläret så återkommer vi.</p></div></section>
<section><div class="in content"><form class="cform" data-demo>
    <h2>Skicka ett meddelande</h2>
    {fld("cn", "Namn", auto="name")}{fld("ce", "E-post", "email", auto="email")}{fld("cs", "Ämne")}
    <label for="cm">Meddelande<textarea id="cm" name="cm" required></textarea></label>
    <button class="btn btn-g" type="submit" style="justify-self:start">Skicka</button>
    <p class="form-ok" hidden tabindex="-1">{E(FORM_OK)}</p>
  </form>
  <aside class="aside"><h3>Hitta till oss</h3><p><b>{FIRMA} AB</b><br>{ADRESS[0]}<br>{ADRESS[1]}</p><dl><div><dt>Telefon</dt><dd><a href="{TEL_HREF}">{TEL}</a></dd></div><div><dt>E-post</dt><dd><a href="mailto:{MEJL}">{MEJL}</a></dd></div></dl><a class="arrow" href="{KARTA}" target="_blank" rel="noopener">Visa på karta</a>
  <h3 style="margin-top:28px">Direktkontakt</h3><div class="who"><span class="av" aria-hidden="true">CA</span><div><b>{VD["namn"]}</b><br><span style="color:var(--muted);font-size:14px">{VD["roll"]}</span></div></div><dl><div><dt>Telefon</dt><dd><a href="{VD["href"]}">{VD["tel"]}</a></dd></div><div><dt>E-post</dt><dd><a href="mailto:{VD["mejl"]}">{VD["mejl"]}</a></dd></div></dl></aside></div></section>''')

# ---------------- 404 ----------------
with open(os.path.join(OUT, "404.html"), "w") as f:
    f.write(f'''<!doctype html>
<html lang="sv"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sidan finns inte – {FIRMA}</title>
<style>body{{margin:0;min-height:100vh;display:grid;place-items:center;background:#eef2f7;color:#14202e;font:17px/1.6 system-ui,sans-serif;text-align:center;padding:20px}}h1{{color:#14325c;margin:0 0 8px}}a{{color:#14325c;font-weight:700}}</style></head>
<body><div><h1>Sidan finns inte</h1><p>Den här sidan hittades inte. <a href="./">Till startsidan</a> eller ring <a href="{TEL_HREF}">{TEL}</a>.</p></div></body></html>
''')
print("Klart:", OUT)
