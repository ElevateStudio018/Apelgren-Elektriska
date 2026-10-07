# Lindvik Bygg

En statisk hemsida för det påhittade byggföretaget Lindvik Bygg. Allt innehåll är testfakta.

## Innehåll
- `index.html` – startsidan
- 29 undersidor (tjänster, bolag, projekt, nyheter, om oss, hållbarhet, jobb, kontakt, 404)
- `assets/` – gemensam CSS och JavaScript
- `img/` – bilder från Pexels
- `screenshots/` – skärmdumpar
- `tools/` – Python-generatorn som bygger sidorna

## Bygga om sidorna
```
python3 tools/sitegen.py tools/base.html . tools
```

## Publicera med GitHub Pages
Settings → Pages → Branch: `main`, mapp: `/ (root)` → Save.
