(function () {
  var doc = document;

  doc.querySelectorAll(".sidebar-title").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var group = btn.closest(".sidebar-group");
      if (group) group.classList.toggle("open");
    });
  });

  var hamburger = doc.querySelector(".hamburger");
  var mask = doc.querySelector(".sidebar-mask");
  function closeNav() { doc.body.classList.remove("nav-open"); }
  function openNav() { doc.body.classList.add("nav-open"); }
  if (hamburger) hamburger.addEventListener("click", function () {
    doc.body.classList.toggle("nav-open");
  });
  if (mask) mask.addEventListener("click", closeNav);
  doc.querySelectorAll(".sidebar a").forEach(function (a) {
    a.addEventListener("click", closeNav);
  });

  var tocLinks = [].slice.call(doc.querySelectorAll(".toc a"));
  var heads = tocLinks.map(function (a) {
    var id = decodeURIComponent((a.getAttribute("href") || "").replace(/^#/, ""));
    return doc.getElementById(id);
  });
  function syncToc() {
    var y = window.scrollY + 90;
    var current = 0;
    heads.forEach(function (el, i) {
      if (el && el.offsetTop <= y) current = i;
    });
    tocLinks.forEach(function (a, i) {
      a.classList.toggle("active", i === current);
    });
  }
  if (tocLinks.length) {
    window.addEventListener("scroll", syncToc, { passive: true });
    syncToc();
  }

  var maskSearch = doc.querySelector(".search-mask");
  var input = doc.querySelector(".search-input");
  var results = doc.querySelector(".search-results");
  var openers = doc.querySelectorAll("[data-open-search]");

  function openSearch() {
    if (!maskSearch) return;
    maskSearch.classList.add("open");
    if (input) {
      input.value = "";
      renderSearch("");
      setTimeout(function () { input.focus(); }, 20);
    }
  }
  function closeSearch() {
    if (maskSearch) maskSearch.classList.remove("open");
  }
  openers.forEach(function (el) { el.addEventListener("click", openSearch); });
  if (maskSearch) {
    maskSearch.addEventListener("click", function (e) {
      if (e.target === maskSearch) closeSearch();
    });
  }
  doc.addEventListener("keydown", function (e) {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      if (maskSearch && maskSearch.classList.contains("open")) closeSearch();
      else openSearch();
    }
    if (e.key === "Escape") {
      closeSearch();
      closeNav();
    }
  });

  function relAsset(name) {
    var script = doc.querySelector('script[src*="assets/js/app.js"]');
    var src = script ? script.getAttribute("src") : "../assets/js/app.js";
    return src.replace(/app\.js$/, name);
  }

  function snippet(text, q) {
    var i = text.toLowerCase().indexOf(q.toLowerCase());
    if (i < 0) return text.slice(0, 80);
    var s = Math.max(0, i - 24);
    var e = Math.min(text.length, i + q.length + 36);
    var cut = (s > 0 ? "…" : "") + text.slice(s, e) + (e < text.length ? "…" : "");
    var re = new RegExp(q.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "ig");
    return cut.replace(re, function (m) { return "<mark>" + m + "</mark>"; });
  }

  function renderSearch(q) {
    if (!results) return;
    q = (q || "").trim();
    var index = window.SEARCH_INDEX || [];
    if (!q) {
      results.innerHTML = '<div class="search-hint">输入关键词，例如「派工」「电表」「演示账号」。</div>';
      return;
    }
    var hits = [];
    for (var i = 0; i < index.length; i++) {
      var item = index[i];
      var hay = (item.title + " " + item.text).toLowerCase();
      if (hay.indexOf(q.toLowerCase()) !== -1) hits.push(item);
      if (hits.length >= 20) break;
    }
    if (!hits.length) {
      results.innerHTML = '<div class="search-empty">没有找到结果</div>';
      return;
    }
    var root = doc.documentElement.getAttribute("data-root") || "";
    results.innerHTML = hits.map(function (item) {
      return '<a href="' + root + item.url + '"><div class="s-title">' + item.title +
        '</div><div class="s-snippet">' + snippet(item.text, q) + "</div></a>";
    }).join("");
  }

  if (input) {
    input.addEventListener("input", function () { renderSearch(input.value); });
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        var first = results && results.querySelector("a");
        if (first) location.href = first.getAttribute("href");
      }
    });
  }

  var indexScript = doc.createElement("script");
  indexScript.src = relAsset("search-index.js");
  indexScript.onload = function () { if (input && maskSearch && maskSearch.classList.contains("open")) renderSearch(input.value); };
  doc.body.appendChild(indexScript);
})();
