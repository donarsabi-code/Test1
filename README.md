# Movix · Live TV

Application web **clé en main** pour regarder le Live TV / sport en direct.
Elle reprend la logique de l'extension userscript Movix mais côté serveur :

- **Backend proxy (Node/Express)** — contourne le CORS, injecte les bons headers
  (`Referer` / `Origin` / `User-Agent`) par host, et **réécrit les playlists
  HLS (`.m3u8`)** pour que chaque segment passe aussi par le proxy.
- **Extracteurs de sources** — portés depuis le userscript : `voe`, `fsvid`,
  `vidzy`, `vidmoly`, `sibnet`, `uqload`, `doodstream`, `seekstreaming`
  (décodage Dean Edwards packer, déchiffrement VOE/AES, etc.).
- **Agrégateur de chaînes** — Vavoo, Wiflix (WITV), Bolaloca (SosPlay) et LiveTV
  (sports en direct), exposés via une API REST de style Stremio
  (`manifest` / `catalog` / `stream`).
- **Frontend SPA** — liste des catégories, grille de chaînes, recherche et
  lecteur intégré (`hls.js`) avec sélecteur de source.

> ⚠️ L'app agrège des sources tierces publiques. Leur disponibilité dépend des
> serveurs en amont ; assure-toi de respecter les lois et conditions
> d'utilisation applicables dans ta juridiction.

## Démarrage

```bash
npm install      # installe les deps + copie hls.js dans public/vendor
npm start        # démarre sur http://localhost:3000
```

Puis ouvre <http://localhost:3000>.

Variables d'environnement :

- `PORT` — port d'écoute (défaut `3000`).

## API

| Méthode | Route | Description |
| --- | --- | --- |
| `GET` | `/api/manifest` | Liste des catalogues (catégories). |
| `GET` | `/api/catalog/:type/:id` | Chaînes d'un catalogue (`{ metas: [...] }`). |
| `GET` | `/api/stream/:type/:id` | Flux d'une chaîne (`{ streams: [{ url, playUrl }] }`). |
| `GET` | `/api/extract?url=&type=` | Extrait une source m3u8 d'un embed. |
| `GET` | `/proxy?url=&h=` | Proxy média + réécriture des playlists HLS. |
| `POST` | `/api/action` | Passe une action brute au handler porté du userscript. |

## Architecture

```
server/
  index.js       # Express : API REST + fichiers statiques
  providers.js   # Catalogues + résolution des flux (porté de background.js)
  extractors.js  # Extracteurs de sources (porté de extractors.js)
  proxy.js       # Proxy CORS + réécriture m3u8 + injection de headers
  shims.js       # Remplace chrome.* / GM_* par des équivalents serveur
public/          # Frontend SPA (index.html, app.js, styles.css)
```

Le proxy est la pièce maîtresse : `hls.js` charge un `.m3u8` via `/proxy`, le
serveur récupère la playlist avec les headers injectés, réécrit chaque URI de
segment vers `/proxy`, et relaie les segments `.ts` en streaming.
