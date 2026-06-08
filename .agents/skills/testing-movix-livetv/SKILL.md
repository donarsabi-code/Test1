---
name: testing-movix-livetv
description: Run and end-to-end test the Movix Live TV web app (Express proxy backend + hls.js player). Use when verifying proxy, extractor, catalog, or player changes.
---

# Testing Movix Live TV

## Run locally
```bash
npm install
npm start        # serves http://localhost:3000
```
Health check: `curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/health` should print `200`.

Lint: `npm run lint` (ported files `server/extractors.js` / `server/providers.js` are intentionally ignored in `eslint.config.js`).

## No auth required
The app is self-hosted and aggregates public third-party sources. No login, API keys, or secrets are needed to test it.

## Primary end-to-end flow (browser)
1. Open `http://localhost:3000`. The first catalog (TvVoo • France) auto-loads; wait for the grid to populate (~800 channels).
2. Type into the search box (top-right) to filter the grid live by channel name.
3. Click a channel card — the player section opens and shows N source buttons ("N source(s) disponible(s)").
4. Wait for playback. The loading overlay ("Chargement du flux…") clears when the `playing` event fires.

## Decisive playback assertion
A spinner or a single screenshot is NOT proof. Confirm the `<video>` is actually advancing:
```js
var v=document.querySelector('video');
console.log(JSON.stringify({t:v.currentTime, paused:v.paused, readyState:v.readyState, w:v.videoWidth, src:v.src.slice(0,40)}));
```
Sample twice ~3-6s apart: `currentTime` must increase, `paused` must be `false`, `readyState` should be 4, and `src` is a `blob:` URL (hls.js MSE). A blob src + advancing time proves the proxy fetched the m3u8, rewrote it, and segments downloaded same-origin.

Note: `browser_console` only returns values via `console.log(...)` — a bare expression returns `undefined`. Always wrap output in `console.log`.

## Known flakiness / workarounds
- Upstream sources can be down at any time. If the first source shows "Lecture impossible (flux indisponible)" or the overlay sticks, click the next source button and retry. The test passes if ANY source plays.
- EUROSPORT 1 (Vavoo) has historically been a reliable channel to test with, but pick any LIVE channel — sport channels tend to have active streams.
- If the whole catalog fails to load (status shows "Hors ligne"), the backend likely can't reach the upstream Vavoo config (`https://tvvoo.hayd.uk/cfg-fr`); check server logs.

## Devin Secrets Needed
None.
