import express from "express";
import path from "node:path";
import { fileURLToPath } from "node:url";

import {
  getManifest,
  getCatalog,
  getStream,
  handleMessage,
} from "./providers.js";
import { registerProxyRoutes, proxyUrlFor } from "./proxy.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PORT = process.env.PORT || 3000;

const app = express();
app.use(express.json({ limit: "1mb" }));

// Permissive CORS for the API (the app is meant to be self-hosted).
app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Headers", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET,POST,OPTIONS");
  if (req.method === "OPTIONS") {
    res.sendStatus(204);
    return;
  }
  next();
});

const asyncHandler = (fn) => (req, res) =>
  Promise.resolve(fn(req, res)).catch((err) => {
    if (!res.headersSent) {
      res.status(500).json({ error: err?.message || String(err) });
    }
  });

app.get("/api/health", (_req, res) => res.json({ ok: true }));

app.get(
  "/api/manifest",
  asyncHandler(async (_req, res) => {
    res.json(await getManifest());
  }),
);

app.get(
  "/api/catalog/:type/:id",
  asyncHandler(async (req, res) => {
    const { type, id } = req.params;
    res.json(await getCatalog(type, id, req.query.accessKey || null));
  }),
);

// Annotate every returned stream with a ready-to-play proxied URL.
function withPlayUrls(result) {
  if (result && Array.isArray(result.streams)) {
    result.streams = result.streams.map((s) => ({
      ...s,
      playUrl: s.url ? proxyUrlFor(s.url, {}) : undefined,
    }));
  }
  return result;
}

app.get(
  "/api/stream/:type/:id",
  asyncHandler(async (req, res) => {
    const { type, id } = req.params;
    const result = await getStream(type, id, req.query.accessKey || null, {
      ...req.query,
    });
    res.json(withPlayUrls(result));
  }),
);

// Generic source extraction (voe/fsvid/vidzy/sibnet/uqload/...).
app.get(
  "/api/extract",
  asyncHandler(async (req, res) => {
    const { url, type } = req.query;
    if (!url) {
      res.status(400).json({ error: "Missing url" });
      return;
    }
    const result = await handleMessage({
      action: "EXTRACT_M3U8",
      payload: { url, type: type || null },
    });
    if (result && result.success) {
      const videoUrl = result.hlsUrl || result.m3u8Url;
      if (videoUrl) result.playUrl = proxyUrlFor(videoUrl, {});
    }
    res.json(result);
  }),
);

// Escape hatch: forward any extension-style action to the ported handler.
app.post(
  "/api/action",
  asyncHandler(async (req, res) => {
    res.json(await handleMessage(req.body || {}));
  }),
);

registerProxyRoutes(app);

// Static frontend.
app.use(express.static(path.join(__dirname, "..", "public")));
app.get("/", (_req, res) => {
  res.sendFile(path.join(__dirname, "..", "public", "index.html"));
});

app.listen(PORT, () => {
  console.log(`Movix Live TV running on http://localhost:${PORT}`);
});

export { app };
