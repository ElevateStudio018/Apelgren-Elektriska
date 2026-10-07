# Appelgrens Elektriska AB

Statisk hemsida för Appelgrens Elektriska AB, Partille (031-26 25 40).

## Innehåll
- `index.html` – startsidan
- `tjanster.html` + sex tjänstesidor (`tjanst-*.html`)
- `om-oss.html`, `referenser.html`, `rot-avdrag.html`, `kontakt.html`, `404.html`
- `assets/site.css` – grundlayout, `assets/appelgrens.css` – färgtema, `assets/site.js` – meny m.m.
- `img/` – **tillfälliga** bilder (Pexels) tills bilderna från nuvarande hemsida är på plats
- `tools/appelgrens.py` – generatorn; all text står i den filen
- `tools/skrapa.py` – hämtar text och bilder från www.appelgrensel.se

## Bygga om sidorna
```
python3 tools/appelgrens.py .
```

## Hämta text och bilder från nuvarande hemsida
```
python3 tools/skrapa.py
```
Texten hamnar i `skrapat/text/`, bilderna i `img/skrapat/` (med en lista över varifrån
varje bild kommer i `skrapat/text/_bilder.txt`). Byt sedan bildnumren i `IMG` och
`TJANSTER` i `tools/appelgrens.py` mot sökvägar som `"img/skrapat/logga.png"` och bygg om.

## Att göra
- Kontaktformuläret och ROT-formuläret skickar inget ännu (statisk sida). Koppla till
  t.ex. Formspree eller en egen e-posttjänst – ROT-formuläret innehåller personnummer,
  så det måste skickas krypterat till en betrodd mottagare.

## Publicera med GitHub Pages
Settings → Pages → Branch: `main`, mapp: `/ (root)` → Save.
