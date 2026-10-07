import re, os, sys, html
BASE, OUT, TOOLS = sys.argv[1], sys.argv[2], sys.argv[3]
base = open(BASE).read()
E = html.escape
css = re.search(r"<style>(.*?)</style>", base, re.S).group(1)
os.makedirs(f"{OUT}/assets", exist_ok=True)
open(f"{OUT}/assets/site.css", "w").write(css.strip() + "\n" + open(f"{TOOLS}/extra.css").read())
open(f"{OUT}/assets/site.js", "w").write(open(f"{TOOLS}/site.js").read())

def img(n, alt="", pos="50% 50%"):
    return f'<img class="photo" src="img/foto-{n:02d}.jpg" alt="{E(alt)}" loading="lazy" style="object-position:{pos}">'
def ph(n, alt="", pos="50% 50%", extra=""):
    return f'<div class="ph"{extra}>{img(n, alt, pos)}</div>'
ARROW = '<svg class="arr" viewBox="0 0 52 52" fill="none" stroke-width="2.2" aria-hidden="true"><path d="M10 42 42 10M16 10h26v26"/></svg>'

# ---------------- innehåll ----------------
SERVICES = [
 dict(slug="bostader", title="Bostäder", short="Villor, radhus och flerbostadshus", img=6, lead="Vi bygger hem där människor vill bo länge – från småhusområden till kvarter med hundratals lägenheter.",
      body=["Varje år lämnar vi över omkring 300 nya bostäder i Sjuhärad och Göteborgsregionen. Vi bygger både åt bostadsbolag och åt egna Lindvik Bostad.",
            "Många av husen har stomme i trä från vår egen fabrik. Det ger kortare byggtid på plats, tystare byggarbetsplatser och lägre klimatavtryck."],
      bullets=["Flerbostadshus i 3–8 våningar","Radhus och parhus","Hyresrätter, bostadsrätter och äganderätter","Trygghetsboenden och LSS-boenden"],
      stats=[("312","bostäder klara 2025"),("212","lägenheter byggs nu"),("14 mån","byggtid för 40 lgh")], person=("Anna Berg","Affärschef bostäder","033-20 40 71"), projects=["sjoglimten","ekbacken"]),
 dict(slug="skolor", title="Skolor och förskolor", short="Lugna, ljusa miljöer i trä", img=5, lead="Barn lär sig bäst där det är lugnt, ljust och tryggt. Därför bygger vi skolor med mycket dagsljus, bra ljud och friska material.",
      body=["Sedan 2018 har vi byggt elva förskolor och fyra skolor. Vi arbetar nära pedagoger och elever redan i skissen, så att rummen passar hur man faktiskt använder dem.",
            "Vi bygger ofta medan skolan är i drift. Då planerar vi transporter och bullriga moment till lov och kvällar."],
      bullets=["Förskolor och skolor i trä","Idrottshallar och matsalar","Om- och tillbyggnad av befintliga skolor","Utemiljöer och skolgårdar"],
      stats=[("15","skolor sedan 2018"),("0","olyckor i fjol"),("98 %","nöjda beställare")], person=("Johan Ek","Affärschef samhällsbyggnad","033-20 40 72"), projects=["ekbacken","viskahallen"]),
 dict(slug="mark", title="Mark och anläggning", short="Grund, vatten, avlopp och vägar", img=20, lead="Allt som händer under och kring husen: schakt, grundläggning, ledningar, gator och vägar.",
      body=["Lindvik Mark har egna maskiner och egna förare. Det gör att vi kan starta snabbt och ha full koll på tidplanen från första spadtaget.",
            "Vi tar hand om massorna på plats så långt det går. Det minskar transporterna och sparar både pengar och koldioxid."],
      bullets=["Schakt och grundläggning","Vatten, avlopp och dagvatten","Gator, vägar och rondeller","Parker och lekplatser"],
      stats=[("64","egna maskiner"),("38 km","ledningar 2025"),("71 %","massor återanvända")], person=("Erik Sand","Platschef mark","033-20 40 73"), projects=["rondell"]),
 dict(slug="trabyggnation", title="Träbyggnation", short="KL-trä och limträ från egen fabrik", img=9, lead="Vi ritar, tillverkar och monterar trästommar själva. Det ger 40 % lägre klimatavtryck än betong och halverad byggtid på plats.",
      body=["Stommarna tillverkas inomhus i vår fabrik i Viskafors, i rätt mått och med färdiga hål för installationer. På byggplatsen lyfts de på plats med kran.",
            "Massivt trä förkolnar på ytan vid brand och skyddar då kärnan. Alla våra trähus klarar Boverkets brandkrav."],
      bullets=["Stommar i KL-trä och limträ","Färdiga vägg- och bjälklagselement","Hus upp till 8 våningar","Klimatberäkning för varje projekt"],
      stats=[("−40 %","klimatavtryck mot betong"),("6 veckor","stomme för 40 lgh"),("12 000 m³","trä per år")], person=("Maria Lind","Chef Lindvik Trä","033-20 40 74"), projects=["sjoglimten","ekbacken"]),
 dict(slug="byggservice", title="Byggservice", short="Snabb hjälp med det lilla – även för privatpersoner", img=22, lead="Ett läckande tak, ett nytt badrum eller en dörr som kärvar. Lindvik Service hjälper företag, föreningar och privatpersoner.",
      body=["Vi har elva servicebilar som utgår från Borås, Ulricehamn och Kinna. De flesta ärenden hinner vi titta på inom två arbetsdagar.",
            "För fastighetsägare erbjuder vi serviceavtal med fast pris per år."],
      bullets=["Badrum och kök","Mindre tillbyggnader och altaner","Reparationer och skadeservice","Serviceavtal för fastighetsägare"],
      stats=[("11","servicebilar"),("2 dagar","till första besök"),("1 900","uppdrag 2025")], person=("Sara Holm","Serviceansvarig","033-20 40 75"), projects=[]),
 dict(slug="projektutveckling", title="Projektutveckling", short="Från tomt till färdigt kvarter", img=18, lead="Vi tar idéer från tomt till färdigt kvarter, tillsammans med kommunen och de som ska bo där.",
      body=["Vi köper eller arrenderar mark, tar fram detaljplaner tillsammans med kommunen och bygger sedan själva. Det ger korta beslutsvägar och ett helhetsansvar.",
            "Just nu utvecklar vi fyra nya områden i Sjuhärad med totalt 650 bostäder."],
      bullets=["Markförvärv och detaljplan","Samråd med grannar och kommun","Bostäder, lokaler och service","Försäljning via Lindvik Bostad"],
      stats=[("4","områden under utveckling"),("650","planerade bostäder"),("1987","sedan vi började")], person=("Peter Ljung","Projektutvecklare","033-20 40 76"), projects=["sjoglimten"]),
]
COS = [
 dict(slug="bostad", name="Lindvik Bostad", tag="Bostäder", img=18, short="Säljer och hyr ut bostäderna vi bygger.", lead="Lindvik Bostad säljer bostadsrätter och hyr ut lägenheter i våra egna projekt.",
      body=["Just nu säljer vi 18 nyproducerade radhus i Fristad med inflyttning hösten 2027, och hyr ut 64 lägenheter i Kv. Sjöglimten i Ulricehamn.","Alla bostäder har solceller, laddplatser och trädgård eller balkong i söderläge."], stats=[("820","egna hyresrätter"),("18","radhus till salu"),("2027","nästa inflyttning")]),
 dict(slug="fastighet", name="Lindvik Fastighet", tag="Lokaler", img=19, short="Äger och förvaltar 40 000 kvadratmeter lokaler.", lead="Lindvik Fastighet äger och förvaltar kontor, butiker och lager i Borås och Ulricehamn.",
      body=["Vi har egen förvaltning och egna fastighetstekniker, så hyresgästerna har alltid någon att ringa.","Vi anpassar lokalerna efter verksamheten och bygger om när behoven ändras."], stats=[("40 000","kvadratmeter"),("120","hyresgäster"),("96 %","uthyrt")]),
 dict(slug="mark", name="Lindvik Mark", tag="Mark och anläggning", img=20, short="Mark, väg och ledningar i hela Västsverige.", lead="Lindvik Mark gör markarbeten, vägar och ledningar åt kommuner, företag och våra egna projekt.",
      body=["Bolaget har 64 egna maskiner och 85 medarbetare.","Vi är certifierade för arbete vid väg och har egen mätning och projektering."], stats=[("85","medarbetare"),("64","maskiner"),("38 km","ledningar 2025")]),
 dict(slug="tra", name="Lindvik Trä", tag="Husfabrik", img=21, short="Husfabriken i Viskafors som tillverkar våra stommar.", lead="Lindvik Trä tillverkar stommar och väggelement i trä i vår fabrik i Viskafors.",
      body=["Fabriken byggdes 2019 och har 45 medarbetare. Vi använder trä från skogar i Västra Götaland som är certifierade enligt FSC eller PEFC.","Varje element tillverkas inomhus, i rätt mått och klart för montage."], stats=[("45","medarbetare"),("12 000 m³","trä per år"),("2019","fabriken byggdes")]),
 dict(slug="service", name="Lindvik Service", tag="Byggservice", img=22, short="Byggservice och underhåll, även för privatpersoner.", lead="Lindvik Service hjälper till med reparationer, renoveringar och underhåll.",
      body=["Vi har elva servicebilar och tar uppdrag från både företag och privatpersoner.","Du kan få ROT-avdrag på arbetskostnaden när vi gör jobb i ditt hem."], stats=[("11","servicebilar"),("1 900","uppdrag 2025"),("4,8/5","i snittbetyg")]),
]
PROJ = [
 dict(slug="ekbacken", title="Förskolan Ekbacken", place="Borås", year="2026", img=5, cat="Skola", lead="En förskola i trä för 120 barn, med stora fönster mot skogen och en gård som sluttar ner mot bäcken.",
      body=["Förskolan har åtta avdelningar, en egen matsal och ett tillagningskök. Stommen är KL-trä från Lindvik Trä.","Ekbacken vann Borås byggnadspris 2026. Juryn lyfte fram dagsljuset och hur lugnt det är i rummen."], stats=[("1 450 m²","yta"),("120","barn"),("11 mån","byggtid")]),
 dict(slug="sjoglimten", title="Kv. Sjöglimten", place="Ulricehamn", year="2025", img=6, cat="Bostäder", lead="64 hyresrätter i två huskroppar med utsikt över Åsunden.",
      body=["Husen är byggda i trä på en betonggrund och har solceller på taken. Alla lägenheter har balkong eller uteplats.","Projektet gjordes i samverkan med Ulricehamns Bostäder, med öppna kostnader från start."], stats=[("64","lägenheter"),("5 200 m²","yta"),("14 mån","byggtid")]),
 dict(slug="viskahallen", title="Viskahallen", place="Viskafors", year="2025", img=7, cat="Idrott", lead="En idrottshall för skola, föreningar och kvällsträning.",
      body=["Hallen har plats för 400 åskådare och kan delas i tre mindre salar.","Taket bärs av limträbalkar som är 32 meter långa, tillverkade i vår fabrik några kilometer bort."], stats=[("2 300 m²","yta"),("400","åskådare"),("32 m","limträbalkar")]),
 dict(slug="rondell", title="Rondell Hultafors", place="Bollebygd", year="2024", img=8, cat="Mark och väg", lead="En ny rondell och 1,2 kilometer gång- och cykelväg som gör korsningen säkrare.",
      body=["Vi byggde om korsningen medan trafiken rullade, i fyra etapper.","Massorna från schaktet användes i vägbanken, så vi slapp 900 lastbilstransporter."], stats=[("1,2 km","gång- och cykelväg"),("900","transporter sparade"),("7 mån","byggtid")]),
]
NEWS = [
 dict(slug="ekbacken-pris", title="Förskolan Ekbacken vinner Borås byggnadspris", date="2026-10-02", dtext="2 oktober 2026", img=13, short="Juryn lyfte fram hur trä och dagsljus gör förskolan lugn och varm.",
      body=["Borås byggnadspris 2026 går till Förskolan Ekbacken, som vi byggde åt Borås Stad.","– Det är ett pris till alla som har varit med: pedagogerna som berättade hur de jobbar, arkitekterna och våra snickare, säger platschefen Johan Ek.","Förskolan har stomme i trä från vår egen fabrik i Viskafors."]),
 dict(slug="ny-vd", title="Sara Lindqvist blir ny vd", date="2026-09-24", dtext="24 september 2026", img=14, short="Sara har arbetat på Lindvik sedan 2009, senast som platschef.", pos="50% 25%",
      body=["Styrelsen har utsett Sara Lindqvist till ny vd för Lindvik Bygg. Hon tillträder den 1 januari 2027.","Sara började som arbetsledare 2009 och har sedan dess varit projektchef och platschef för flera av våra största bostadsprojekt.","– Jag vill fortsätta det vi är bäst på: att bygga ihop med våra kunder, säger Sara Lindqvist."]),
 dict(slug="goda-rad", title="Fem saker att tänka på innan du bygger hus", date="2026-09-10", dtext="10 september 2026", img=15, short="Budget, tomt och tidplan – så undviker du de vanligaste misstagen.",
      body=["1. Börja med budgeten. Räkna med 10–15 % extra för oväntade kostnader.","2. Kolla detaljplanen för tomten innan du köper den. Den styr hur stort och högt du får bygga.","3. Bestäm tidigt vad som är viktigast för dig. Det är billigare att ändra på papperet än på bygget.","4. Fråga efter referenser och besök ett hus som byggaren har gjort.","5. Gör en tidplan med marginal, särskilt över vintern."]),
]
exec(open(TOOLS + "/more.py").read())
JOBS = [("Platschef bostäder","Borås","Heltid"),("Snickare","Ulricehamn","Heltid"),("Maskinförare","Kinna","Heltid"),("Montör trästommar","Viskafors","Heltid"),("Kalkylator","Borås","Heltid"),("Sommarjobb 2027","Alla orter","Sommar")]

# ---------------- gemensamma delar ----------------
LOGO_SVG = '<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#1f4d3a"/><path d="M7 23V12l9-5 9 5v11" fill="none" stroke="#a9c3a0" stroke-width="2.6" stroke-linejoin="round"/><path d="M13 23v-6h6v6" fill="none" stroke="#fff" stroke-width="2.6"/></svg>'
LOGO_SVG_L = '<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#a9c3a0"/><path d="M7 23V12l9-5 9 5v11" fill="none" stroke="#1f4d3a" stroke-width="2.6" stroke-linejoin="round"/><path d="M13 23v-6h6v6" fill="none" stroke="#fff" stroke-width="2.6"/></svg>'
def head(title, desc):
    return f'''<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Source+Sans+3:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<div class="demo">Testlayout med påhittat företag och påhittade fakta. Foton från Pexels.</div>
<header>
  <div class="in nav">
    <a class="logo" href="index.html" aria-label="Lindvik Bygg, till startsidan"><span class="cube">{LOGO_SVG}</span>Lindvik Bygg</a>
    <button class="burger" id="burger" aria-expanded="false" aria-controls="overlay" aria-label="Öppna menyn"><span></span><span></span><span></span></button>
    <a class="btn btn-g" href="kontakt.html">Kontakta oss</a>
  </div>
</header>
<div class="overlay" id="overlay" aria-hidden="true" inert>
  <div class="ov-top"><a class="logo" href="index.html"><span class="cube">{LOGO_SVG_L}</span>Lindvik Bygg</a><button class="ov-close" id="menuClose" type="button" aria-label="Stäng menyn">Stäng <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M4 4l12 12M16 4 4 16"/></svg></button></div>
  <nav aria-label="Huvudmeny"><ul>
    <li><a href="tjanster.html">Vårt erbjudande</a></li>
    <li><a href="projekt.html">Projekt</a></li>
    <li><a href="om-oss.html">Om oss</a></li>
    <li><a href="hallbarhet.html">Hållbarhet</a></li>
    <li><a href="nyheter.html">Nyheter</a></li>
    <li><a href="jobb.html">Jobba hos oss</a></li>
    <li><a href="kontakt.html">Kontakt</a></li>
  </ul>
  <div class="ov-sub">{"".join(f'<a href="tjanst-{s["slug"]}.html">{E(s["title"])}</a>' for s in SERVICES)}</div>
  <div class="ov-foot"><span>033-20 40 60</span><span>info@lindvikbygg.se</span><span>Allégatan 12, Borås</span></div></nav>
</div>
'''
SOC = {"LinkedIn":'<path d="M4 3a2 2 0 1 1 0 4 2 2 0 0 1 0-4zm-2 6h4v12H2zm7 0h4v1.7c.6-1 2-2 4-2 4 0 5 2.5 5 6V21h-4v-5.5c0-1.6-.3-3-2-3s-2.3 1.3-2.3 3V21H9z"/>',
       "Instagram":'<path d="M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10zm0 8a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm5.3-9.5a1.2 1.2 0 1 0 0 2.4 1.2 1.2 0 0 0 0-2.4zM12 2c-2.7 0-3 0-4.1.1C4.4 2.2 2.2 4.4 2.1 7.9 2 9 2 9.3 2 12s0 3 .1 4.1c.1 3.5 2.3 5.7 5.8 5.8 1.1.1 1.4.1 4.1.1s3 0 4.1-.1c3.5-.1 5.7-2.3 5.8-5.8.1-1.1.1-1.4.1-4.1s0-3-.1-4.1c-.1-3.5-2.3-5.7-5.8-5.8C15 2 14.7 2 12 2z"/>',
       "Facebook":'<path d="M14 8V6.5c0-.7.5-1.2 1.2-1.2H17V2h-2.8C11.6 2 10 3.7 10 6.3V8H7.5v3.3H10V22h4V11.3h2.8l.5-3.3z"/>'}
def foot():
    soc = "".join(f'<a href="https://www.{n.lower()}.com" target="_blank" rel="noopener" aria-label="{n} (öppnas i ny flik)"><svg viewBox="0 0 24 24" aria-hidden="true">{p}</svg></a>' for n, p in SOC.items())
    return f'''<section class="fcta" aria-label="Kontakta oss">
  <div class="in"><div><h2>Har du ett projekt på gång?</h2><p>Berätta om det, så hör vi av oss inom två arbetsdagar.</p></div><a class="btn btn-w" href="kontakt.html">Kontakta oss</a></div>
</section>
<footer>
  <div class="in">
    <div class="fgrid">
      <div><a class="logo" href="index.html"><span class="cube">{LOGO_SVG_L}</span>Lindvik Bygg</a>
        <p style="margin-top:14px;max-width:36ch">Ett familjeägt bygg- och anläggningsföretag i Västsverige. 240 medarbetare och fyra kontor sedan 1987.</p>
        <p style="margin-top:12px">Allégatan 12, 503 32 Borås<br>033-20 40 60 · info@lindvikbygg.se</p>
        <div class="social">{soc}</div>
        <form class="news-f" data-demo><label for="nf">Få våra nyheter</label><div class="row"><input id="nf" type="email" required placeholder="din@mejl.se" autocomplete="email"><button type="submit">Prenumerera</button></div><p class="form-ok" hidden tabindex="-1">Tack! Det här är en testsida, så inget skickades.</p></form>
      </div>
      <div><h4>Vårt erbjudande</h4><ul>{"".join(f'<li><a href="tjanst-{s["slug"]}.html">{E(s["title"])}</a></li>' for s in SERVICES)}</ul></div>
      <div><h4>Våra bolag</h4><ul>{"".join(f'<li><a href="bolag-{c["slug"]}.html">{E(c["name"])}</a></li>' for c in COS)}</ul></div>
      <div><h4>Om Lindvik</h4><ul><li><a href="om-oss.html">Om oss</a></li><li><a href="om-oss.html#historia">Vår historia</a></li><li><a href="projekt.html">Projekt</a></li><li><a href="hallbarhet.html">Hållbarhet</a></li><li><a href="nyheter.html">Nyheter och press</a></li><li><a href="jobb.html">Jobba hos oss</a></li><li><a href="kontakt.html">Kontakt</a></li></ul></div>
    </div>
    <div class="certs" aria-label="Certifieringar"><span>ISO 9001</span><span>ISO 14001</span><span>ISO 45001</span><span>Svanen-licens</span></div>
    <div class="fbottom"><span>© 2026 Lindvik Bygg AB · Påhittat testföretag · Foton: Pexels</span><a class="totop" href="#" data-top>Till toppen ↑</a></div>
  </div>
</footer>
<script src="assets/site.js"></script>
</body>
</html>
'''
def page(fn, title, desc, main):
    open(f"{OUT}/{fn}", "w").write(head(title + " – Lindvik Bygg", desc) + "<main>\n" + main + EXTRA_PAGE.get(fn, "") + "\n</main>\n" + foot())
def phero(n, h1, lead, crumbs, pos="50% 50%"):
    cr = " <span aria-hidden=\"true\">›</span> ".join([f'<a href="{u}">{E(t)}</a>' if u else f"<span>{E(t)}</span>" for t, u in crumbs])
    return f'''<section class="phero" aria-label="{E(h1)}">{ph(n, "", pos)}<div class="in"><nav class="crumbs" aria-label="Brödsmulor">{cr}</nav><h1>{E(h1)}</h1><p>{E(lead)}</p></div></section>'''
def stats(lst): return '<div class="stats">' + "".join(f'<div><b>{E(a)}</b><span>{E(b)}</span></div>' for a, b in lst) + "</div>"
def pcards(lst): return '<div class="cards3">' + "".join(f'<a class="pcard2" href="projekt-{p["slug"]}.html">{ph(p["img"], p["title"])}<h3>{E(p["title"])}</h3><small>{E(p["cat"])} · {E(p["place"])} · {p["year"]}</small></a>' for p in lst) + "</div>"
BYID = {p["slug"]: p for p in PROJ}
def secs(lst): return "".join(f"<h2>{E(h)}</h2>" + "".join(f"<p>{x}</p>" for x in ps) for h, ps in lst)
def steps(lst): return '<ol class="timeline">' + "".join(f"<li><b>{E(a)}</b><p>{E(b)}</p></li>" for a, b in lst) + "</ol>"
def ncard3(lst): return "".join(f'<a class="pcard2" href="nyhet-{o["slug"]}.html">{ph(o["img"], o["title"], o.get("pos", "50% 50%"))}<small>{o["dtext"]}</small><h3>{E(o["title"])}</h3></a>' for o in lst)
def links(lst): return "".join(f'<a href="{u}">{E(t)}</a>' for u, t in lst)

# ---------------- startsidan ----------------
s = base
s = s[s.index("<main"):s.index("</main>") + len("</main>")]
def sect(marker, new):
    global s
    i = s.index(marker); j = s.index("</section>", i) + len("</section>"); s = s[:i] + new + s[j:]
tiles = "".join(f'<a class="tile" href="tjanst-{x["slug"]}.html">{img(x["img"])}{ARROW}<span><b>{E(x["title"])}</b><small>{E(x["short"])}</small></span></a>' for x in SERVICES)
sect("  <!-- Tjänster", f'''  <!-- Tjänster: som Brixly -->
  <section id="tjanster">
    <div class="in">
      <div class="headrow"><div><h2>Det här bygger vi</h2></div><a class="arrow" href="tjanster.html">Alla tjänster</a></div>
      <div class="tiles">{tiles}</div>
    </div>
  </section>''')
sect("  <!-- Om oss", f'''  <!-- Om oss -->
  <section class="about" id="om">
    <div class="in about2">
      <div class="media">{ph(4, "Byggteam som tittar på en ritning", "50% 30%")}</div>
      <div class="txt">
        <h2 style="margin-top:8px">Ett lokalt byggföretag med 240 egna medarbetare</h2>
        <p class="lead" style="margin-top:14px">Vi är ett familjeägt bygg- och anläggningsföretag från Borås. När beställare, arkitekt och hantverkare sitter vid samma bord från början blir husen bättre, billigare och klara i tid.</p>
        <div class="facts"><div><b>240</b><span>medarbetare</span></div><div><b>1 100</b><span>byggda projekt</span></div><div><b>4</b><span>kontor i Sjuhärad</span></div></div>
        <div class="minis">
          <a class="mini" href="tjanster.html"><b>Tjänster och projekt</b><span>Bostäder, skolor och mark i Sjuhärad och Göteborgsregionen.</span></a>
          <a class="mini" href="om-oss.html#historia"><b>Vår historia</b><span>Från ett garage i Viskafors till fyra kontor.</span></a>
          <a class="mini" href="jobb.html"><b>Jobba med oss</b><span>Ansvar tidigt och kollegor som hjälper till.</span></a>
        </div>
      </div>
    </div>
  </section>''')
cos = "".join(f'<a class="co2" href="bolag-{c["slug"]}.html">{ph(c["img"], c["name"])}<div class="body"><small>{E(c["tag"])}</small><h3>{E(c["name"])}</h3><p>{E(c["short"])}</p><span class="arrow">Till {E(c["name"])}</span></div></a>' for c in COS)
i = s.index('<div class="cos">'); j = s.index('<div class="shortcuts"')
s = s[:i] + f'<div class="cos2">{cos}</div>\n      ' + s[j:]
s = re.sub(r'\s*<!-- Kundtjänst.*?</section>', '', s, flags=re.S)
s = s.replace('<!-- Våra bolag: Granitor  +  Genvägar: ByggPartner -->\n  <section style="background:var(--beige)">', '<!-- Våra bolag -->\n  <section id="bolag" style="background:var(--beige)">', 1)  # ersatt av footerns kontaktband
# länkar till riktiga sidor
L = {'href="#tjanster" >': 'x'}
reps = [('<a class="btn btn-w" href="#tjanster">Se vårt erbjudande</a>', '<a class="btn btn-w" href="tjanster.html">Se vårt erbjudande</a>'),
        ('<a class="btn btn-o" href="#projekt"', '<a class="btn btn-o" href="projekt.html"'),
        ('<a class="btn btn-g" style="margin-top:22px" href="#projekt">Alla projekt</a>', '<a class="btn btn-g" style="margin-top:22px" href="projekt.html">Alla projekt</a>'),
        ('<a class="btn btn-w" href="#kontakt">Läs om vårt träbyggande</a>', '<a class="btn btn-w" href="tjanst-trabyggnation.html">Läs om vårt träbyggande</a>'),
        ('<a class="arrow" href="#kontakt">Se lediga bostäder</a>', '<a class="arrow" href="bolag-bostad.html">Se lediga bostäder</a>'),
        ('<a class="btn btn-w" href="#hallbarhet">Läs redovisningen</a>', '<a class="btn btn-w" href="hallbarhet.html">Läs redovisningen</a>'),
        ('<a class="arrow" href="#nyheter">Alla nyheter</a>', '<a class="arrow" href="nyheter.html">Alla nyheter</a>'),
        ('<a class="btn btn-w" href="#jobb">Lediga jobb (14)</a>', '<a class="btn btn-w" href="jobb.html">Lediga jobb (6)</a>'),
        ('<a class="arrow" href="#jobb">Så är det att jobba här</a>', '<a class="arrow" href="jobb.html">Så är det att jobba här</a>'),
        ('<a class="sc" href="#om">', '<a class="sc" href="om-oss.html">'), ('<a class="sc" href="#kontakt">', '<a class="sc" href="kontakt.html#kontor">'),
        ('<a class="sc" href="#hallbarhet">', '<a class="sc" href="hallbarhet.html">'), ('<a class="sc" href="#projekt">', '<a class="sc" href="projekt.html">'),
        ('<a class="arrow" style="margin-top:18px" href="#kontakt">Fler frågor och svar</a>', '<a class="arrow" style="margin-top:18px" href="kontakt.html">Fråga oss något annat</a>')]
for a, b in reps:
    assert a in s, a
    s = s.replace(a, b)
# projektkort och nyhetskort blir länkar
pslugs = ["ekbacken", "sjoglimten", "viskahallen", "rondell"]
k = iter(pslugs)
s = re.sub(r'<div class="pcard">(.*?)</div></div>', lambda m: f'<a class="pcard" href="projekt-{next(k)}.html">{m.group(1)}</div></a>', s, flags=re.S)
k2 = iter([n["slug"] for n in NEWS])
s = re.sub(r'<div class="news" data-tilt>(.*?)</p></div>', lambda m: f'<a class="news" data-tilt href="nyhet-{next(k2)}.html">{m.group(1)}</p></a>', s, flags=re.S)
s = s.replace("Lediga jobb</span></div></a>", "Lediga jobb</span></div></a>")
s = s.replace('<a class="door"', '<a class="door"')
idx = head("Lindvik Bygg – vi bygger det Västsverige växer i", "Lindvik Bygg är ett familjeägt bygg- och anläggningsföretag i Västsverige. Testsida med påhittat innehåll.").replace('<a class="logo" href="index.html" aria-label="Lindvik Bygg, till startsidan">', '<a class="logo" href="index.html" aria-label="Lindvik Bygg, till toppen">')
idx = idx.replace("<title>Lindvik Bygg – vi bygger det Västsverige växer i</title>", "<title>Lindvik Bygg</title>")
open(f"{OUT}/index.html", "w").write(idx + s + "\n" + foot())

for n in NEWS: n["body"] = n["body"] + NEWS_MORE.get(n["slug"], [])
NEWS = NEWS + NEWS_EXTRA
# ---------------- tjänster ----------------
page("tjanster.html", "Vårt erbjudande", "Allt Lindvik Bygg gör, från bostäder till byggservice.",
     phero(9, "Vårt erbjudande", "Från första skissen till nyckelöverlämning och servicen efteråt. Sex områden, en kontakt.", [("Start", "index.html"), ("Vårt erbjudande", None)]) +
     f'<section><div class="in"><div class="tiles">{tiles}</div></div></section>')
for x in SERVICES:
    pr = [BYID[p] for p in x["projects"]]
    name, role, tel = x["person"]; ini = "".join(w[0] for w in name.split())
    page(f'tjanst-{x["slug"]}.html', x["title"], x["lead"],
      phero(x["img"], x["title"], x["lead"], [("Start", "index.html"), ("Vårt erbjudande", "tjanster.html"), (x["title"], None)]) +
      f'''<section><div class="in content"><div class="prose">{stats(x["stats"])}{"".join(f"<p>{E(b)}</p>" for b in x["body"])}<h2>Det här ingår</h2><ul>{"".join(f"<li>{E(b)}</li>" for b in x["bullets"])}</ul>{secs(SVC_MORE[x["slug"]])}<h2>Så går ett uppdrag till</h2>{steps(SVC_STEPS)}</div>
      <aside class="aside"><h3>Prata med oss</h3><div class="who"><span class="av" aria-hidden="true">{ini}</span><div><b>{E(name)}</b><br><span style="color:var(--muted);font-size:14px">{E(role)}</span></div></div><dl><div><dt>Telefon</dt><dd>{tel}</dd></div><div><dt>Mejl</dt><dd>{name.split()[0].lower()}@lindvikbygg.se</dd></div></dl><a class="btn btn-g" href="kontakt.html">Skicka en förfrågan</a></aside></div></section>''' +
      (f'<section class="related"><div class="in"><h2>Projekt vi har gjort</h2><div style="margin-top:24px">{pcards(pr)}</div></div></section>' if pr else "") +
      f'<section><div class="in"><h2>Fler tjänster</h2><div class="links-row">{links([("tjanst-" + o["slug"] + ".html", o["title"]) for o in SERVICES if o is not x])}</div></div></section>')

# ---------------- bolag ----------------
for c in COS:
    page(f'bolag-{c["slug"]}.html', c["name"], c["lead"],
      phero(c["img"], c["name"], c["lead"], [("Start", "index.html"), ("Våra bolag", "index.html#bolag"), (c["name"], None)]) +
      f'''<section><div class="in content"><div class="prose">{stats(c["stats"])}{"".join(f"<p>{E(b)}</p>" for b in c["body"])}{secs(CO_MORE[c["slug"]])}</div>
      <aside class="aside"><h3>{E(c["name"])}</h3><dl><div><dt>Telefon</dt><dd>033-20 40 60</dd></div><div><dt>Mejl</dt><dd>{c["slug"]}@lindvikbygg.se</dd></div><div><dt>Adress</dt><dd>Allégatan 12, Borås</dd></div></dl><a class="btn btn-g" href="kontakt.html">Kontakta bolaget</a></aside></div></section>''' +
      f'<section class="related"><div class="in"><h2>Fler bolag i koncernen</h2><div class="links-row">{links([("bolag-" + o["slug"] + ".html", o["name"]) for o in COS if o is not c])}</div></div></section>')

# ---------------- projekt ----------------
page("projekt.html", "Projekt", "Projekt som Lindvik Bygg har byggt.",
     phero(1, "Byggt av oss", "Över 1 100 projekt sedan 1987. Här är några av de senaste.", [("Start", "index.html"), ("Projekt", None)]) +
     f'<section><div class="in">{pcards(PROJ)}</div></section>')
for p in PROJ:
    others = [o for o in PROJ if o is not p][:3]
    page(f'projekt-{p["slug"]}.html', p["title"], p["lead"],
      phero(p["img"], p["title"], p["lead"], [("Start", "index.html"), ("Projekt", "projekt.html"), (p["title"], None)]) +
      f'''<section><div class="in content"><div class="prose">{stats(p["stats"])}{"".join(f"<p>{E(b)}</p>" for b in p["body"])}{secs(PROJ_MORE[p["slug"]])}<div class="gallery" style="margin-top:12px">{ph(p["img"], p["title"])}{ph(4, "Byggmöte på plats", "50% 30%")}{ph(9, "Trästomme under montage")}</div></div>
      <aside class="aside"><h3>Fakta</h3><dl><div><dt>Ort</dt><dd>{E(p["place"])}</dd></div><div><dt>Klart</dt><dd>{p["year"]}</dd></div><div><dt>Typ</dt><dd>{E(p["cat"])}</dd></div></dl><a class="btn btn-g" href="kontakt.html">Bygga något liknande?</a></aside></div></section>''' +
      f'<section class="related"><div class="in"><h2>Fler projekt</h2><div style="margin-top:24px">{pcards(others)}</div></div></section>')

# ---------------- nyheter ----------------
ncards = '<div class="cards3">' + "".join(f'<a class="pcard2" href="nyhet-{n["slug"]}.html">{ph(n["img"], n["title"], n.get("pos", "50% 50%"))}<small><time datetime="{n["date"]}">{n["dtext"]}</time></small><h3>{E(n["title"])}</h3><p style="color:var(--muted);font-size:15px">{E(n["short"])}</p></a>' for n in NEWS) + "</div>"
page("nyheter.html", "Nyheter och press", "Nyheter och pressmeddelanden från Lindvik Bygg.",
     '<section class="phero plain"><div class="in"><nav class="crumbs"><a href="index.html">Start</a> <span aria-hidden="true">›</span> <span>Nyheter</span></nav><h1>Nyheter och press</h1><p>Det senaste från oss. Presskontakt: press@lindvikbygg.se, 033-20 40 79.</p></div></section>' +
     f'<section><div class="in">{ncards}</div></section>')
for n in NEWS:
    page(f'nyhet-{n["slug"]}.html', n["title"], n["short"],
      phero(n["img"], n["title"], n["short"], [("Start", "index.html"), ("Nyheter", "nyheter.html"), (n["title"], None)], n.get("pos", "50% 50%")) +
      f'<section><div class="in article"><time datetime="{n["date"]}">{n["dtext"]}</time>{"".join(f"<p>{b}</p>" for b in n["body"])}<p style="color:var(--muted);font-size:15px">Frågor om nyheten? Kontakta vår presstjänst på press@lindvikbygg.se eller 033-20 40 79.</p><a class="arrow" href="nyheter.html">Alla nyheter</a></div></section>' +
      f'<section class="related"><div class="in"><h2>Fler nyheter</h2><div style="margin-top:24px" class="cards3">{ncard3([q for q in NEWS if q is not n][:3])}</div></div></section>')

# ---------------- om oss ----------------
TL = [("1987","Karl Lindvik startar firman i ett garage i Viskafors."),("1995","Första flerbostadshuset, 24 lägenheter i Borås."),("2004","Lindvik Mark startas med egna maskiner."),("2012","Andra generationen tar över. 150 medarbetare."),("2019","Husfabriken i Viskafors öppnar."),("2026","240 medarbetare och fyra kontor.")]
page("om-oss.html", "Om oss", "Lindvik Bygg är ett familjeägt bygg- och anläggningsföretag från Borås.",
  phero(17, "Om Lindvik Bygg", "Ett familjeägt byggföretag från Borås med 240 egna medarbetare.", [("Start", "index.html"), ("Om oss", None)]) +
  f'''<section><div class="in content"><div class="prose"><h2 id="kultur" style="margin-top:0">Vi tror på samverkan</h2><p>När beställare, arkitekt och hantverkare sitter vid samma bord från början, med öppna kostnader, blir husen bättre, billigare och klara i tid. Ett hus med 40 lägenheter tar oss ungefär 14 månader.</p>
  <p>Vi har egna snickare, maskinförare och en egen husfabrik. Det gör att vi kan hålla vad vi lovar.</p>
  <h2>Våra värderingar</h2><ul><li><b>Ärliga.</b> Vi säger som det är, även när det är obekvämt.</li><li><b>Nära.</b> Vi är lokala och finns kvar efter att huset är klart.</li><li><b>Omtanke.</b> Om människorna, platsen och klimatet.</li></ul>
  <h2 id="historia">Vår historia</h2><ol class="timeline">{"".join(f"<li><b>{y}</b><p>{E(t)}</p></li>" for y, t in TL)}</ol>
  <h2>Ledning</h2><div class="people">{"".join(f'<div class="person"><span class="av" aria-hidden="true">{"".join(w[0] for w in n.split())}</span><b>{E(n)}</b><span>{E(r)}</span></div>' for n, r in [("Lars Lindvik","Vd till och med 2026"),("Sara Lindqvist","Tillträdande vd"),("Omar Haddad","Ekonomichef")])}</div></div>
  <aside class="aside"><h3>Lindvik i siffror</h3><dl><div><dt>Medarbetare</dt><dd>240</dd></div><div><dt>Omsättning 2025</dt><dd>1,1 miljarder kronor</dd></div><div><dt>Kontor</dt><dd>Borås, Ulricehamn, Kinna, Göteborg</dd></div></dl><a class="btn btn-g" href="jobb.html">Jobba hos oss</a></aside></div></section>''')

# ---------------- hållbarhet ----------------
page("hallbarhet.html", "Hållbarhet", "Hur Lindvik Bygg arbetar med klimat, människor och ekonomi.",
  phero(11, "Vi mäter det vi bygger", "Hur vi arbetar med klimat, människor och ekonomi.", [("Start", "index.html"), ("Hållbarhet", None)]) +
  f'''<section><div class="in content"><div class="prose">{stats([("−38 %","koldioxid per m² sedan 2020"),("92 %","av byggavfallet sorteras"),("0","allvarliga olyckor 2025")])}
  <p>Varje år redovisar vi hur vi påverkar miljön, människorna och ekonomin omkring oss. I år nådde vi målet för återvunnet material ett år tidigare än planerat.</p>
  <h2>Våra mål till 2030</h2><ul><li>Halvera klimatavtrycket per kvadratmeter jämfört med 2020.</li><li>Alla arbetsmaskiner ska gå på el eller förnybart bränsle.</li><li>Minst 20 lärlingar varje år.</li><li>Inga allvarliga olyckor på våra byggen.</li></ul>
  <h2>Så gör vi</h2><p>Vi bygger mer i trä, återanvänder massor på plats och klimatberäknar varje projekt innan vi börjar. Vår fabrik drivs med solel från taket.</p></div>
  <aside class="aside"><h3>Hela redovisningen</h3><p>Redovisningen 2026 är på 48 sidor och följer GRI-standarden.</p><a class="btn btn-g" href="kontakt.html">Beställ redovisningen</a></aside></div></section>''')

# ---------------- jobb ----------------
page("jobb.html", "Jobba hos oss", "Lediga jobb och hur det är att jobba på Lindvik Bygg.",
  phero(16, "Vi bygger människor också", "Hos oss får du ansvar tidigt och kollegor som hjälper till.", [("Start", "index.html"), ("Jobba hos oss", None)], "50% 30%") +
  f'''<section><div class="in content"><div class="prose"><h2 style="margin-top:0">Lediga jobb</h2><ul class="jobs-list">{"".join(f'<li><div><b>{E(t)}</b><br><span>{E(o)} · {E(h)}</span></div><a class="arrow" href="kontakt.html">Sök</a></li>' for t, o, h in JOBS)}</ul>
  <h2>Lärling eller student?</h2><p>Varje år tar vi in 20 lärlingar och 10 sommarjobbare. Du får en egen handledare och lön från första dagen.</p>
  <h2>Därför trivs folk här</h2><ul><li>Egen personal, inga långa kedjor av underentreprenörer.</li><li>Friskvårdsbidrag på 5 000 kronor per år.</li><li>Kollektivavtal och tjänstepension.</li></ul></div>
  <aside class="aside"><h3>Hittar du inget?</h3><p>Skicka en spontanansökan till jobb@lindvikbygg.se. Vi läser alla.</p><a class="btn btn-g" href="kontakt.html">Kontakta HR</a></aside></div></section>''')

# ---------------- kontakt ----------------
OFF = [("Borås (huvudkontor)","Allégatan 12, 503 32 Borås","033-20 40 60"),("Ulricehamn","Storgatan 4, 523 30 Ulricehamn","0321-55 10 20"),("Kinna","Kinnavägen 18, 511 54 Kinna","0320-20 30 40"),("Göteborg","Lilla Bommen 3, 411 04 Göteborg","031-70 80 90")]
page("kontakt.html", "Kontakt", "Kontakta Lindvik Bygg.",
  '<section class="phero plain"><div class="in"><nav class="crumbs"><a href="index.html">Start</a> <span aria-hidden="true">›</span> <span>Kontakt</span></nav><h1>Kontakta oss</h1><p>Kundtjänst vardagar 07–16: 033-20 40 60 · info@lindvikbygg.se</p></div></section>' +
  f'''<section><div class="in content"><form class="cform" data-demo>
    <h2>Skicka ett meddelande</h2>
    <label for="cn">Namn<input id="cn" required autocomplete="name"></label>
    <label for="ce">Mejl<input id="ce" type="email" required autocomplete="email"></label>
    <label for="ct">Vad gäller det?<select id="ct"><option>Nytt projekt</option><option>Byggservice</option><option>Bostad eller lokal</option><option>Jobb</option><option>Faktura</option><option>Annat</option></select></label>
    <label for="cm">Meddelande<textarea id="cm" required></textarea></label>
    <button class="btn btn-g" type="submit" style="justify-self:start">Skicka</button>
    <p class="form-ok" hidden tabindex="-1">Tack! Det här är en testsida, så inget skickades.</p>
  </form>
  <aside class="aside" id="faktura"><h3>Fakturering</h3><dl><div><dt>Fakturaadress</dt><dd>Lindvik Bygg AB, FE 123, 105 69 Stockholm</dd></div><div><dt>Organisationsnummer</dt><dd>556000-0000 (påhittat)</dd></div></dl><h3>Press</h3><p>press@lindvikbygg.se<br>033-20 40 79</p></aside></div></section>
  <section class="related" id="kontor"><div class="in"><h2>Våra kontor</h2><div class="offices" style="margin-top:24px">{"".join(f'<div class="office"><b>{E(n)}</b><span>{E(a)}</span><span>{E(t)}</span></div>' for n, a, t in OFF)}</div></div></section>''')
print("pages:", len([f for f in os.listdir(OUT) if f.endswith(".html")]))
