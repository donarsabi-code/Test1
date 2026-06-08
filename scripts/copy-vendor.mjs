// Copies the bundled hls.js build into public/vendor so the frontend can load
// it locally without relying on a CDN.
import { copyFile, mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(__dirname, "..");

async function main() {
  const src = path.join(root, "node_modules", "hls.js", "dist", "hls.min.js");
  const destDir = path.join(root, "public", "vendor");
  const dest = path.join(destDir, "hls.min.js");
  try {
    await mkdir(destDir, { recursive: true });
    await copyFile(src, dest);
    console.log("[vendor] copied hls.min.js -> public/vendor/");
  } catch (err) {
    console.warn("[vendor] could not copy hls.js:", err?.message || err);
  }
}

main();
