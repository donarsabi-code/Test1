// HLS / media proxy. Bypasses CORS and injects the per-host Referer/Origin/
// User-Agent headers registered during source extraction, then rewrites m3u8
// playlists so every segment and sub-playlist is also fetched through here.
import { getInjectedHeaders } from "./shims.js";

const DEFAULT_UA =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36";

const M3U8_CONTENT_TYPES = [
  "application/vnd.apple.mpegurl",
  "application/x-mpegurl",
  "audio/mpegurl",
  "audio/x-mpegurl",
];

function proxyUrlFor(targetUrl, headers) {
  const params = new URLSearchParams({ url: targetUrl });
  if (headers && Object.keys(headers).length > 0) {
    params.set("h", Buffer.from(JSON.stringify(headers)).toString("base64"));
  }
  return `/proxy?${params.toString()}`;
}

function isM3u8(url, contentType) {
  if (contentType) {
    const ct = contentType.toLowerCase();
    if (M3U8_CONTENT_TYPES.some((t) => ct.includes(t))) return true;
  }
  return /\.m3u8(\?|$)/i.test(url);
}

/**
 * Rewrite every URI in an HLS playlist to flow back through the proxy,
 * carrying the same injected headers so segments authenticate correctly.
 */
function rewriteM3u8(playlist, baseUrl, headers) {
  const resolve = (uri) => {
    try {
      return new URL(uri, baseUrl).href;
    } catch {
      return uri;
    }
  };
  const lines = playlist.split(/\r?\n/);
  const out = lines.map((line) => {
    const trimmed = line.trim();
    if (!trimmed) return line;

    if (trimmed.startsWith("#")) {
      // Rewrite URI="..." attributes (EXT-X-KEY, EXT-X-MEDIA, EXT-X-MAP, ...).
      return line.replace(/URI="([^"]+)"/g, (_m, uri) => {
        return `URI="${proxyUrlFor(resolve(uri), headers)}"`;
      });
    }
    // A non-comment, non-empty line is a segment or sub-playlist URI.
    return proxyUrlFor(resolve(trimmed), headers);
  });
  return out.join("\n");
}

export function registerProxyRoutes(app) {
  app.get("/proxy", async (req, res) => {
    const target = req.query.url;
    if (!target || typeof target !== "string") {
      res.status(400).json({ error: "Missing url parameter" });
      return;
    }

    let parsed;
    try {
      parsed = new URL(target);
    } catch {
      res.status(400).json({ error: "Invalid url parameter" });
      return;
    }
    if (parsed.protocol !== "http:" && parsed.protocol !== "https:") {
      res.status(400).json({ error: "Unsupported protocol" });
      return;
    }

    // Headers come from (1) explicit base64 hint carried in rewritten playlists
    // and (2) the dynamic rules registered during extraction.
    let explicitHeaders = {};
    if (typeof req.query.h === "string") {
      try {
        explicitHeaders = JSON.parse(
          Buffer.from(req.query.h, "base64").toString("utf-8"),
        );
      } catch {
        explicitHeaders = {};
      }
    }
    const injected = getInjectedHeaders(target, "media");
    const headers = {
      "User-Agent": DEFAULT_UA,
      Accept: "*/*",
      ...injected,
      ...explicitHeaders,
    };

    // Forward Range requests so seeking and partial segment fetches work.
    if (req.headers.range) headers.Range = req.headers.range;

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 25000);
    res.on("close", () => controller.abort());

    try {
      const upstream = await fetch(target, {
        headers,
        redirect: "follow",
        signal: controller.signal,
      });

      const contentType = upstream.headers.get("content-type") || "";
      res.setHeader("Access-Control-Allow-Origin", "*");
      res.setHeader("Access-Control-Allow-Headers", "*");
      res.setHeader("Cache-Control", "no-cache");

      const finalUrl = upstream.url || target;

      if (isM3u8(finalUrl, contentType)) {
        const text = await upstream.text();
        // The headers needed for the segments are those injected for this host.
        const segmentHeaders = { ...injected, ...explicitHeaders };
        const rewritten = rewriteM3u8(text, finalUrl, segmentHeaders);
        res.status(upstream.status);
        res.setHeader("Content-Type", "application/vnd.apple.mpegurl");
        res.send(rewritten);
        return;
      }

      // Binary/segment passthrough.
      res.status(upstream.status);
      if (contentType) res.setHeader("Content-Type", contentType);
      for (const h of ["content-length", "content-range", "accept-ranges"]) {
        const v = upstream.headers.get(h);
        if (v) res.setHeader(h, v);
      }
      if (!upstream.body) {
        res.end();
        return;
      }
      const reader = upstream.body.getReader();
      const pump = async () => {
        for (;;) {
          const { done, value } = await reader.read();
          if (done) break;
          if (!res.write(Buffer.from(value))) {
            await new Promise((r) => res.once("drain", r));
          }
        }
        res.end();
      };
      await pump();
    } catch (err) {
      if (!res.headersSent) {
        res.status(502).json({
          error: "Proxy fetch failed",
          detail: err?.message || String(err),
        });
      } else {
        res.end();
      }
    } finally {
      clearTimeout(timer);
    }
  });

  // Helper used by the frontend to build a playable proxied URL for any stream.
  app.get("/api/play-url", (req, res) => {
    const target = req.query.url;
    if (!target || typeof target !== "string") {
      res.status(400).json({ error: "Missing url" });
      return;
    }
    res.json({ url: proxyUrlFor(target, {}) });
  });
}

export { proxyUrlFor };
