# amalficoastboatguide.com: come pubblicare

## 1. Pubblicazione (Cloudflare)
Il sito è su Cloudflare Workers, collegato al repo GitHub `shayzanz/amalficoastboatguide`. Basta fare push (o merge) su `main` con la cartella `site/` aggiornata: Cloudflare pubblica da solo in un paio di minuti. Dettagli tecnici nel README.

## 2. Indicizzazione (appena il sito è online)
- **Google Search Console**: aggiungi la proprietà di dominio, invia `https://amalficoastboatguide.com/sitemap.xml`.
- **Bing Webmaster Tools**: importa da Search Console e invia la stessa sitemap (Bing alimenta anche ChatGPT search e Copilot).
- **IndexNow** (Bing, Yandex, Seznam, Naver), dalla cartella `amalficoastboatguide/`:
  ```
  curl -X POST "https://api.indexnow.org/indexnow" -H "Content-Type: application/json; charset=utf-8" --data @indexnow-payload.json
  ```
  La chiave è già pubblicata in `/dfd8f96f3ff4b6bc65b66af6b3e8a2e7.txt`. Rilancia il comando dopo ogni aggiornamento.

## 3. Cosa c'è dentro
- 5 lingue complete (EN alla radice, /it/, /es/, /de/, /fr/) con slug tradotti, hreflang reciproci + x-default, sitemap con alternates.
- Per lingua: home con comparatore e filtri, classifica "best boat tours" con voti per criterio, 8 guide, 8 pagine tour con mappa del percorso, chi siamo/metodo, contatti, privacy, 404.
- Schema.org: Organization, WebSite, BreadcrumbList, Article, FAQPage, ItemList, TouristTrip con itinerario geolocalizzato. Nessun AggregateRating (niente recensioni inventate).
- `robots.txt` che autorizza esplicitamente i bot AI (GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, Google-Extended, Applebot-Extended...), `llms.txt` e `llms-full.txt`.
- GetYourGuide: link con partner_id EQTZMZ9 e widget ufficiale (si carica dopo il consenso cookie, come richiesto dal GDPR). Viator: pid P00328677, mcid 42383. Tutti i link affiliati hanno rel="sponsored nofollow".
- WhatsApp +39 393 855 2086: pulsante fisso, box su ogni guida, messaggio precompilato nella lingua della pagina.
- Leaflet ospitato in locale (nessuna dipendenza da CDN), mappa SVG di riserva se JavaScript non si carica.

## 4. Da completare da parte tua
- **Titolare**: la privacy indica amalficoastboatguide.com come responsabile, contatto WhatsApp. Se vuoi aggiungere un'email, compila `OWNER_EMAIL` in `src/data.py` e ricostruisci.
- **Foto**: non ho inserito foto (non posso scaricare da Unsplash da qui). Le immagini dei tour arrivano dal widget GetYourGuide. Se vuoi foto Unsplash nella hero, mandami i link e le integro con alt e attribuzione.
- **Prezzi**: sono fasce indicative ("typical ranges"), da ricontrollare a inizio stagione.

## 5. Modificare e ricostruire
I testi sono in `src/content/<lingua>.py`, i dati comuni (prezzi, voti, coordinate) in `src/data.py`.
```
cd src && python3 build.py
```
Rigenera `site/` e `indexnow-payload.json`.

## 6. Partner, foto e recensioni (in `src/data.py`)
- `PARTNER_ORDER = ['gyg', 'viator']`: il primo prende il bottone principale "Prenota ora", il secondo "Confronta i prezzi". Inverti se Viator ti rende di più (guarda l'EPC nei due pannelli).
- `GYG_TOUR_IDS`: per mostrare tour GetYourGuide precisi (con le loro foto e valutazioni) in una pagina, metti gli ID delle attività (il numero dopo `-t` nell'URL GYG).
- `VIATOR_WIDGETS`: incolla qui il codice del widget creato nel pannello Viator Partner (sezione widget). Compare accanto al widget GYG, sempre dopo il consenso cookie.
- Recensioni testuali con nome dell'autore: solo tramite API ufficiali (GetYourGuide Partner API su richiesta, Viator Partner API con la tua API key). Niente copia/scraping.
Dopo ogni modifica: `cd src && python3 build.py`.
