"""Skrapar text och bilder från nuvarande hemsida (www.appelgrensel.se).

Kör från repots rot:  python3 tools/skrapa.py
Sparar texten per sida i skrapat/text/*.md och bilderna i img/skrapat/.
Följer bara länkar inom samma domän. Kräver bara Pythons standardbibliotek.
"""
import os, re, sys, urllib.parse, urllib.request
from html.parser import HTMLParser

START = sys.argv[1] if len(sys.argv) > 1 else "https://www.appelgrensel.se/"
HOST = urllib.parse.urlparse(START).netloc
TXT_DIR, IMG_DIR, MAX = "skrapat/text", "img/skrapat", 60
UA = {"User-Agent": "Mozilla/5.0 (Appelgrens hemsida – innehållsflytt)"}

class Page(HTMLParser):
    BLOCK = {"p", "h1", "h2", "h3", "h4", "li", "div", "section", "br", "tr", "td", "address"}
    def __init__(self, url):
        super().__init__(); self.url, self.out, self.links, self.imgs, self.skip, self.title = url, [], set(), set(), 0, ""
        self._in_title = False
    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag in ("script", "style", "noscript", "svg"): self.skip += 1
        if tag == "title": self._in_title = True
        if tag in ("h1", "h2", "h3", "h4"): self.out.append("\n\n" + "#" * int(tag[1]) + " ")
        elif tag == "li": self.out.append("\n* ")
        elif tag in self.BLOCK: self.out.append("\n")
        if tag == "a" and a.get("href"): self.links.add(urllib.parse.urljoin(self.url, a["href"]).split("#")[0])
        if tag in ("img", "source"):
            for k in ("src", "data-src", "data-lazy-src"):
                if a.get(k): self.imgs.add(urllib.parse.urljoin(self.url, a[k]))
            for k in ("srcset", "data-srcset"):
                if a.get(k):
                    best = a[k].split(",")[-1].strip().split(" ")[0]
                    if best: self.imgs.add(urllib.parse.urljoin(self.url, best))
        for u in re.findall(r"url\(['\"]?([^'\")]+)", a.get("style", "")): self.imgs.add(urllib.parse.urljoin(self.url, u))
    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "svg") and self.skip: self.skip -= 1
        if tag == "title": self._in_title = False
    def handle_data(self, d):
        if self._in_title: self.title += d
        if not self.skip: self.out.append(re.sub(r"\s+", " ", d))
    def text(self):
        t = re.sub(r"[ \t]+\n", "\n", "".join(self.out))
        return re.sub(r"\n{3,}", "\n\n", t).strip()

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return r.headers.get_content_type(), r.read()

def slug(url):
    p = urllib.parse.urlparse(url).path.strip("/") or "start"
    return re.sub(r"[^a-z0-9åäö_-]+", "-", p.lower()).strip("-")

os.makedirs(TXT_DIR, exist_ok=True); os.makedirs(IMG_DIR, exist_ok=True)
todo, seen, images = [START], set(), {}
while todo and len(seen) < MAX:
    url = todo.pop(0)
    if url in seen: continue
    seen.add(url)
    try: ctype, body = get(url)
    except Exception as e: print("FEL", url, e); continue
    if ctype != "text/html": continue
    pg = Page(url); pg.feed(body.decode("utf-8", "replace"))
    with open(f"{TXT_DIR}/{slug(url)}.md", "w") as f: f.write(f"<!-- {url} -->\n# {pg.title.strip()}\n\n{pg.text()}\n")
    print("sida", url)
    for l in pg.links:
        u = urllib.parse.urlparse(l)
        if u.netloc == HOST and u.scheme in ("http", "https") and not re.search(r"\.(jpe?g|png|gif|webp|svg|pdf|zip)$", u.path, re.I) and l not in seen: todo.append(l)
    for i in pg.imgs: images.setdefault(i, url)

with open(f"{TXT_DIR}/_bilder.txt", "w") as idx:
    for src, page in sorted(images.items()):
        name = re.sub(r"[^A-Za-z0-9._-]+", "-", urllib.parse.unquote(os.path.basename(urllib.parse.urlparse(src).path))) or "bild"
        try:
            ctype, data = get(src)
            if not ctype.startswith("image/"): continue
            with open(f"{IMG_DIR}/{name}", "wb") as f: f.write(data)
            idx.write(f"{IMG_DIR}/{name}\t{src}\t(från {page})\n"); print("bild", name)
        except Exception as e: print("FEL", src, e)
print(f"Klart: {len(seen)} sidor, {len(images)} bilder hittade.")
