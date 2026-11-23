# amalficoastboatguide.com

Sito pubblicato: cartella `site/`, servita da Cloudflare Workers (static assets).
Generatore: `cd src && python3 build.py`. Dettagli in LEGGIMI.md.

## Hosting (dal 23 novembre 2026)
- Cloudflare Workers, progetto `amalficoastboatguide`, collegato a GitHub: ogni push su `main` fa un nuovo deploy (`npx wrangler deploy`, nessun build command).
- `wrangler.jsonc`: assets da `./site`, `auto-trailing-slash`, `404-page` (usa il `404.html` più vicino, quindi `/it/...` mostra `/it/404.html`).
- `worker/index.js`: 301 da `www.amalficoastboatguide.com` al dominio senza www, il resto lo servono gli asset.
- Header HTTP in `site/_headers` (sorgente: `src/root/_headers`).
- DNS su Cloudflare (nameserver cambiati su Namecheap). Il TXT `google-site-verification` serve a Search Console: non cancellarlo.
- `netlify.toml` resta solo come storico: Netlify non pubblica più il sito.
