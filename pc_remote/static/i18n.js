"use strict";

// ---- Translations ----------------------------------------------------------
// Strings live in /static/locales/<code>.json; en.json is the reference and the
// fallback for any missing key. Static text is marked in index.html with
// data-i18n (text), data-i18n-aria (aria-label) and data-i18n-placeholder.
const LANGUAGES = {
  en: "English",
  ar: "العربية",
  zh: "中文",
  ja: "日本語",
  ru: "Русский",
  de: "Deutsch",
  gsw: "Schwiizerdütsch",
};
const RTL_LANGUAGES = new Set(["ar"]);
const LANG_STORAGE = "pc-remote-lang";

const i18n = {
  lang: "en",
  strings: {},
  fallback: {},
  listeners: [],

  t(key) {
    return this.strings[key] ?? this.fallback[key] ?? key;
  },

  onChange(fn) {
    this.listeners.push(fn);
  },

  async use(lang) {
    if (!(lang in LANGUAGES)) lang = "en";
    const [fallback, strings] = await Promise.all([loadLocale("en"), loadLocale(lang)]);
    this.lang = lang;
    this.fallback = fallback;
    this.strings = strings;
    applyToPage();
    this.listeners.forEach((fn) => fn());
  },
};

const localeCache = {};
async function loadLocale(lang) {
  if (!localeCache[lang]) {
    localeCache[lang] = fetch(`/static/locales/${lang}.json`)
      .then((res) => (res.ok ? res.json() : {}))
      .catch(() => ({}));
  }
  return localeCache[lang];
}

function detectLanguage() {
  try {
    const saved = localStorage.getItem(LANG_STORAGE);
    if (saved in LANGUAGES) return saved;
  } catch (_) {}
  for (const tag of navigator.languages || [navigator.language || ""]) {
    const code = tag.toLowerCase();
    // Swiss German has its own code (gsw); Swiss phones usually report de-CH.
    if (code.startsWith("gsw") || code === "de-ch") return "gsw";
    const base = code.split("-")[0];
    if (base in LANGUAGES) return base;
  }
  return "en";
}

function applyToPage() {
  const root = document.documentElement;
  root.lang = i18n.lang;
  root.dir = RTL_LANGUAGES.has(i18n.lang) ? "rtl" : "ltr";
  document.querySelectorAll("[data-i18n]").forEach((el) => { el.textContent = i18n.t(el.dataset.i18n); });
  document.querySelectorAll("[data-i18n-aria]").forEach((el) => { el.setAttribute("aria-label", i18n.t(el.dataset.i18nAria)); });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => { el.placeholder = i18n.t(el.dataset.i18nPlaceholder); });
  root.classList.remove("i18n-loading");
}

// ---- Language picker ---------------------------------------------------------
const langSelect = document.getElementById("lang");
for (const [code, name] of Object.entries(LANGUAGES)) {
  const option = new Option(name, code);
  option.lang = code;
  langSelect.add(option);
}
langSelect.addEventListener("change", () => {
  try { localStorage.setItem(LANG_STORAGE, langSelect.value); } catch (_) {}
  i18n.use(langSelect.value);
});

i18n.ready = i18n.use(detectLanguage()).then(() => { langSelect.value = i18n.lang; });
// Never leave the page hidden if the locale files are slow or missing.
setTimeout(() => document.documentElement.classList.remove("i18n-loading"), 1500);
