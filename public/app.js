// Movix Live TV — frontend SPA.
// Talks to the backend API (manifest/catalog/stream) and plays the proxied
// HLS streams with hls.js.

const els = {
  catalogs: document.getElementById("catalogs"),
  grid: document.getElementById("grid"),
  gridEmpty: document.getElementById("grid-empty"),
  gridLoading: document.getElementById("grid-loading"),
  title: document.getElementById("catalog-title"),
  search: document.getElementById("search"),
  playerSection: document.getElementById("player-section"),
  video: document.getElementById("video"),
  overlay: document.getElementById("player-overlay"),
  playerMessage: document.getElementById("player-message"),
  nowPlaying: document.getElementById("now-playing"),
  nowPlayingSub: document.getElementById("now-playing-sub"),
  sourceSwitch: document.getElementById("source-switch"),
  closePlayer: document.getElementById("close-player"),
  statusDot: document.getElementById("status-dot"),
  statusText: document.getElementById("status-text"),
  toast: document.getElementById("toast"),
  sidebar: document.getElementById("sidebar"),
  menuToggle: document.getElementById("menu-toggle"),
};

const state = {
  catalogs: [],
  activeCatalog: null,
  channels: [],
  hls: null,
  toastTimer: null,
};

// Friendly grouping of the flat catalog list for the sidebar.
const GROUP_RULES = [
  { label: "Chaînes TV", test: (id) => id.startsWith("vavoo_") },
  { label: "Wiflix", test: (id) => id.startsWith("wiflix_") },
  { label: "Bolaloca", test: (id) => id.startsWith("sosplay_") },
  { label: "Sport en direct", test: (id) => id.startsWith("livetv_") },
];

function toast(msg) {
  els.toast.textContent = msg;
  els.toast.classList.remove("hidden");
  clearTimeout(state.toastTimer);
  state.toastTimer = setTimeout(() => els.toast.classList.add("hidden"), 4200);
}

async function api(pathname) {
  const res = await fetch(pathname);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

async function loadManifest() {
  try {
    const manifest = await api("/api/manifest");
    state.catalogs = manifest.catalogs || [];
    renderCatalogs();
    els.statusDot.classList.add("ok");
    els.statusText.textContent = `${state.catalogs.length} catégories`;
    // Auto-open the first catalog.
    if (state.catalogs.length) selectCatalog(state.catalogs[0]);
  } catch (err) {
    els.statusDot.classList.add("err");
    els.statusText.textContent = "Hors ligne";
    toast("Impossible de charger le catalogue : " + err.message);
  }
}

function renderCatalogs() {
  els.catalogs.innerHTML = "";
  const used = new Set();
  for (const rule of GROUP_RULES) {
    const items = state.catalogs.filter(
      (c) => rule.test(c.id) && !used.has(c.id),
    );
    if (!items.length) continue;
    const label = document.createElement("div");
    label.className = "cat-group-label";
    label.textContent = rule.label;
    els.catalogs.appendChild(label);
    for (const c of items) {
      used.add(c.id);
      els.catalogs.appendChild(makeCatalogButton(c));
    }
  }
  // Anything not matched by a rule.
  const rest = state.catalogs.filter((c) => !used.has(c.id));
  if (rest.length) {
    const label = document.createElement("div");
    label.className = "cat-group-label";
    label.textContent = "Autres";
    els.catalogs.appendChild(label);
    rest.forEach((c) => els.catalogs.appendChild(makeCatalogButton(c)));
  }
}

function makeCatalogButton(catalog) {
  const btn = document.createElement("button");
  btn.className = "cat-item";
  btn.dataset.id = catalog.id;
  btn.textContent = catalog.name || catalog.id;
  btn.addEventListener("click", () => {
    selectCatalog(catalog);
    els.sidebar.classList.remove("open");
  });
  return btn;
}

async function selectCatalog(catalog) {
  state.activeCatalog = catalog;
  els.title.textContent = catalog.name || catalog.id;
  els.search.value = "";
  document
    .querySelectorAll(".cat-item")
    .forEach((b) => b.classList.toggle("active", b.dataset.id === catalog.id));

  els.grid.innerHTML = "";
  els.gridEmpty.classList.add("hidden");
  els.gridLoading.classList.remove("hidden");

  try {
    const data = await api(
      `/api/catalog/${catalog.type || "tv"}/${encodeURIComponent(catalog.id)}`,
    );
    state.channels = data.metas || [];
    renderChannels(state.channels);
    if (!state.channels.length) {
      els.gridEmpty.querySelector("p").textContent =
        data.disabled_by_user
          ? "Cette catégorie est désactivée."
          : "Aucune chaîne disponible pour le moment.";
      els.gridEmpty.classList.remove("hidden");
    }
  } catch (err) {
    toast("Erreur de chargement des chaînes : " + err.message);
    els.gridEmpty.querySelector("p").textContent =
      "Erreur de chargement. Réessaie plus tard.";
    els.gridEmpty.classList.remove("hidden");
  } finally {
    els.gridLoading.classList.add("hidden");
  }
}

function renderChannels(channels) {
  els.grid.innerHTML = "";
  const frag = document.createDocumentFragment();
  for (const ch of channels) {
    frag.appendChild(makeCard(ch));
  }
  els.grid.appendChild(frag);
}

function makeCard(channel) {
  const card = document.createElement("div");
  card.className = "card";

  const thumb = document.createElement("div");
  thumb.className = "card-thumb";
  const img = channel.poster || channel.logo || channel.background;
  if (img) {
    const im = document.createElement("img");
    im.loading = "lazy";
    im.src = img;
    im.alt = channel.name || "";
    im.addEventListener("error", () => {
      im.remove();
      const fb = document.createElement("span");
      fb.className = "fallback";
      fb.textContent = "📺";
      thumb.appendChild(fb);
    });
    thumb.appendChild(im);
  } else {
    const fb = document.createElement("span");
    fb.className = "fallback";
    fb.textContent = "📺";
    thumb.appendChild(fb);
  }
  const live = document.createElement("span");
  live.className = "live-badge";
  live.textContent = "LIVE";
  thumb.appendChild(live);

  const name = document.createElement("div");
  name.className = "card-name";
  name.textContent = (channel.name || channel.id || "").replace(/\s+/g, " ");

  card.append(thumb, name);
  card.addEventListener("click", () => playChannel(channel));
  return card;
}

function applySearch() {
  const q = els.search.value.trim().toLowerCase();
  if (!q) {
    renderChannels(state.channels);
    return;
  }
  renderChannels(
    state.channels.filter((c) =>
      (c.name || "").toLowerCase().includes(q),
    ),
  );
}

async function playChannel(channel) {
  els.playerSection.classList.remove("hidden");
  els.playerSection.scrollIntoView({ behavior: "smooth", block: "start" });
  els.nowPlaying.textContent = channel.name || channel.id;
  els.nowPlayingSub.textContent = "Résolution de la source…";
  els.sourceSwitch.innerHTML = "";
  showOverlay("Résolution de la source…");

  try {
    const data = await api(
      `/api/stream/tv/${encodeURIComponent(channel.id)}`,
    );
    const streams = (data.streams || []).filter((s) => s.url || s.playUrl);
    if (!streams.length) {
      const reason = data.error ? `(${data.error})` : "";
      throw new Error("Aucun flux jouable trouvé " + reason);
    }
    els.nowPlayingSub.textContent = `${streams.length} source(s) disponible(s)`;
    renderSourceButtons(streams);
    loadStream(streams[0], 0);
  } catch (err) {
    showOverlay("Échec : " + err.message);
    toast(err.message);
  }
}

function renderSourceButtons(streams) {
  els.sourceSwitch.innerHTML = "";
  streams.forEach((s, i) => {
    const btn = document.createElement("button");
    btn.className = "src-btn" + (i === 0 ? " active" : "");
    btn.textContent = cleanSourceLabel(s, i);
    btn.addEventListener("click", () => {
      document
        .querySelectorAll(".src-btn")
        .forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      loadStream(s, i);
    });
    els.sourceSwitch.appendChild(btn);
  });
}

function cleanSourceLabel(stream, i) {
  const raw = (stream.name || stream.title || "").split("\n")[0].trim();
  const cleaned = raw.replace(/[^\w\sÀ-ÿ()\-]/g, "").trim();
  return cleaned || `Source ${i + 1}`;
}

function loadStream(stream, index) {
  const url = stream.playUrl || `/proxy?url=${encodeURIComponent(stream.url)}`;
  showOverlay("Chargement du flux…");
  startPlayback(url);
}

function destroyHls() {
  if (state.hls) {
    state.hls.destroy();
    state.hls = null;
  }
}

function startPlayback(url) {
  destroyHls();
  const video = els.video;
  const Hls = window.Hls;

  const onPlaying = () => hideOverlay();
  video.removeEventListener("playing", onPlaying);
  video.addEventListener("playing", onPlaying, { once: true });

  if (Hls && Hls.isSupported()) {
    const hls = new Hls({
      lowLatencyMode: true,
      maxBufferLength: 30,
      manifestLoadingTimeOut: 20000,
      fragLoadingTimeOut: 30000,
    });
    state.hls = hls;
    hls.loadSource(url);
    hls.attachMedia(video);
    hls.on(Hls.Events.MANIFEST_PARSED, () => {
      video.play().catch(() => {});
    });
    hls.on(Hls.Events.ERROR, (_evt, data) => {
      if (!data.fatal) return;
      switch (data.type) {
        case Hls.ErrorTypes.NETWORK_ERROR:
          hls.startLoad();
          break;
        case Hls.ErrorTypes.MEDIA_ERROR:
          hls.recoverMediaError();
          break;
        default:
          showOverlay("Lecture impossible (flux indisponible).");
          toast("Flux indisponible — essaie une autre source.");
          destroyHls();
      }
    });
  } else if (video.canPlayType("application/vnd.apple.mpegurl")) {
    // Native HLS (Safari / iOS).
    video.src = url;
    video.addEventListener("loadedmetadata", () => video.play().catch(() => {}), {
      once: true,
    });
    video.addEventListener(
      "error",
      () => showOverlay("Lecture impossible (flux indisponible)."),
      { once: true },
    );
  } else {
    showOverlay("Ton navigateur ne supporte pas la lecture HLS.");
  }
}

function showOverlay(msg) {
  els.playerMessage.textContent = msg;
  els.overlay.classList.remove("hidden");
}
function hideOverlay() {
  els.overlay.classList.add("hidden");
}

function closePlayer() {
  destroyHls();
  els.video.removeAttribute("src");
  els.video.load();
  els.playerSection.classList.add("hidden");
}

// ---- wiring ----
els.search.addEventListener("input", applySearch);
els.closePlayer.addEventListener("click", closePlayer);
els.menuToggle.addEventListener("click", () =>
  els.sidebar.classList.toggle("open"),
);

loadManifest();
