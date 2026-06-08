// Server-side shims that replace the browser-extension APIs used by the
// original Movix userscript (chrome.declarativeNetRequest, chrome.storage,
// GM_* storage). Header injection that the extension performed via
// declarativeNetRequest is instead applied by the HLS proxy (proxy.js),
// which consults the in-memory `dynamicRules` registry maintained here.

// ---- URL / rule matching (ported from the userscript top section) ----

function escapeRegExp(value) {
  return value.replace(/[|\\{}()[\]^$+?.]/g, "\\$&");
}

function wildcardToRegExp(pattern) {
  return new RegExp(
    "^" +
      String(pattern || "*")
        .split("*")
        .map((part) => escapeRegExp(part))
        .join(".*") +
      "$",
    "i",
  );
}

function matchesRule(rule, url, resourceType = "xmlhttprequest") {
  if (!rule || !rule.condition) return false;
  const resourceTypes = rule.condition.resourceTypes;
  if (Array.isArray(resourceTypes) && resourceTypes.length > 0) {
    if (!resourceTypes.includes(resourceType)) return false;
  }
  const urlFilter = rule.condition.urlFilter || "*";
  if (!wildcardToRegExp(urlFilter).test(url)) return false;
  return true;
}

// ---- declarativeNetRequest replacement ----

// dynamicRules holds the modifyHeaders rules registered during extraction so
// the proxy can re-apply the right Referer/Origin/User-Agent per upstream host.
const dynamicRules = [];

/**
 * Resolve the request headers that should be injected when fetching `url`
 * through the proxy, based on all registered modifyHeaders rules.
 */
function getInjectedHeaders(url, resourceType = "xmlhttprequest") {
  const headers = {};
  for (const rule of dynamicRules) {
    if (
      rule?.action?.type !== "modifyHeaders" ||
      !Array.isArray(rule?.action?.requestHeaders)
    ) {
      continue;
    }
    if (!matchesRule(rule, url, resourceType)) continue;
    for (const headerRule of rule.action.requestHeaders) {
      if (!headerRule?.header) continue;
      if (headerRule.operation === "set") {
        headers[headerRule.header] = headerRule.value;
      } else if (headerRule.operation === "remove") {
        delete headers[headerRule.header];
      }
    }
  }
  return headers;
}

const chrome = {
  declarativeNetRequest: {
    async getDynamicRules() {
      return dynamicRules.map((r) => ({ ...r }));
    },
    async updateDynamicRules({ addRules = [], removeRuleIds = [] } = {}) {
      if (removeRuleIds.length > 0) {
        const remove = new Set(removeRuleIds);
        for (let i = dynamicRules.length - 1; i >= 0; i--) {
          if (remove.has(dynamicRules[i].id)) dynamicRules.splice(i, 1);
        }
      }
      for (const rule of addRules) {
        const idx = dynamicRules.findIndex((r) => r.id === rule.id);
        if (idx >= 0) dynamicRules[idx] = rule;
        else dynamicRules.push(rule);
      }
    },
  },
  storage: {
    local: (() => {
      const store = new Map();
      return {
        async get(key) {
          if (typeof key === "string") {
            return store.has(key) ? { [key]: store.get(key) } : {};
          }
          const out = {};
          for (const k of [].concat(key || [])) {
            if (store.has(k)) out[k] = store.get(k);
          }
          return out;
        },
        async set(obj) {
          for (const [k, v] of Object.entries(obj)) store.set(k, v);
        },
        async remove(key) {
          for (const k of [].concat(key)) store.delete(k);
        },
      };
    })(),
  },
  runtime: {
    onInstalled: { addListener() {} },
    onStartup: { addListener() {} },
    onMessage: { addListener() {} },
  },
};

// ---- GM_* value storage replacement ----

const gmStore = new Map();
async function gmGetValueCompat(key, fallbackValue) {
  return gmStore.has(key) ? gmStore.get(key) : fallbackValue;
}
async function gmSetValueCompat(key, value) {
  gmStore.set(key, value);
}
async function gmDeleteValueCompat(key) {
  gmStore.delete(key);
}

export {
  chrome,
  dynamicRules,
  getInjectedHeaders,
  matchesRule,
  wildcardToRegExp,
  gmGetValueCompat,
  gmSetValueCompat,
  gmDeleteValueCompat,
};
