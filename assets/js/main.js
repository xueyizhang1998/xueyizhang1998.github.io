/* =========================================================
   交互：语言切换 / 邮箱反爬 / 论文展开
   ========================================================= */
(function () {
  var root = document.documentElement;
  var nav = document.querySelector('.topnav');
  if (nav && typeof ResizeObserver !== 'undefined') {
    new ResizeObserver(function () {
      root.style.setProperty('--nav-clearance', (nav.offsetHeight + 16) + 'px');
    }).observe(nav);
  }

  var navLinks = nav ? Array.prototype.slice.call(nav.querySelectorAll('a[href^="#"]')) : [];
  var navSections = navLinks.map(function (link) {
    return document.getElementById(link.getAttribute('href').slice(1));
  });
  function syncActiveSection() {
    if (!navLinks.length) return;
    var current = 0;
    var threshold = nav.getBoundingClientRect().bottom + 64;
    navSections.forEach(function (section, index) {
      if (section && section.getBoundingClientRect().top <= threshold) current = index;
    });
    if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 4) {
      current = navLinks.length - 1;
    }
    navLinks.forEach(function (link, index) {
      if (index === current) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }
  var navUpdatePending = false;
  window.addEventListener('scroll', function () {
    if (navUpdatePending) return;
    navUpdatePending = true;
    window.requestAnimationFrame(function () {
      syncActiveSection();
      navUpdatePending = false;
    });
  }, { passive: true });
  window.addEventListener('resize', syncActiveSection);
  syncActiveSection();

  /* ---------- 语言切换 ---------- */
  function currentLang() {
    return root.classList.contains('lang-zh') ? 'zh' : 'en';
  }
  function setLang(l) {
    root.classList.remove('lang-en', 'lang-zh');
    root.classList.add('lang-' + l);
    root.setAttribute('lang', l);
    try { localStorage.setItem('lang', l); } catch (e) {}
    syncToggleLabel();
    window.requestAnimationFrame(syncActiveSection);
  }
  var langBtn = document.getElementById('langBtn');
  if (langBtn) {
    langBtn.addEventListener('click', function () {
      setLang(currentLang() === 'zh' ? 'en' : 'zh');
    });
  }

  /* ---------- 邮箱反爬（把 user + domain 拼起来）---------- */
  document.querySelectorAll('.email-link').forEach(function (a) {
    var user = a.getAttribute('data-user');
    var dom = a.getAttribute('data-dom');
    if (user && dom) {
      var addr = user + '@' + dom;
      a.textContent = addr;
      a.href = 'mailto:' + addr;
    }
  });

  /* ---------- 展开 / 收起（按 data-toggle-for 分组，互不干扰） ---------- */
  function itemsOf(group) {
    var box = document.querySelector('[data-collapse-group="' + group + '"]');
    return box ? box.querySelectorAll('.collapsible') : [];
  }
  function syncLabel(btn) {
    var items = itemsOf(btn.getAttribute('data-toggle-for'));
    var anyHidden = Array.prototype.some.call(items, function (el) {
      return el.classList.contains('hidden');
    });
    var en = btn.querySelector('.i18n-en'), zh = btn.querySelector('.i18n-zh');
    if (!en || !zh) return;
    en.textContent = btn.getAttribute(anyHidden ? 'data-more-en' : 'data-less-en');
    zh.textContent = btn.getAttribute(anyHidden ? 'data-more-zh' : 'data-less-zh');
  }
  document.querySelectorAll('[data-toggle-for]').forEach(function (btn) {
    var expanded = false;
    btn.addEventListener('click', function () {
      expanded = !expanded;
      itemsOf(btn.getAttribute('data-toggle-for')).forEach(function (el) {
        el.classList.toggle('hidden', !expanded);
      });
      syncLabel(btn);
    });
    syncLabel(btn);
  });
  function syncToggleLabel() {
    document.querySelectorAll('[data-toggle-for]').forEach(syncLabel);
  }

  /* ---------- 论文主图点击放大 ---------- */
  var lb = document.getElementById('lightbox');
  if (lb) {
    var lbImg = document.getElementById('lbImg');
    var lbCap = document.getElementById('lbCap');
    var lbClose = document.getElementById('lbClose');
    var lastFocus = null;

    function openLb(src, cap) {
      lbImg.src = src;
      lbImg.alt = cap || '';
      lbCap.textContent = cap || '';
      lb.hidden = false;
      document.body.classList.add('lb-open');
      lbClose.focus();
    }
    function closeLb() {
      lb.hidden = true;
      lbImg.src = '';
      document.body.classList.remove('lb-open');
      if (lastFocus) { lastFocus.focus(); lastFocus = null; }
    }

    document.querySelectorAll('.pub .thumb .zoom').forEach(function (btn) {
      btn.addEventListener('click', function () {
        lastFocus = btn;
        openLb(btn.getAttribute('data-full'), btn.getAttribute('data-cap'));
      });
    });

    lbClose.addEventListener('click', closeLb);
    /* 点图片以外的区域关闭 */
    lb.addEventListener('click', function (e) {
      if (e.target === lb || e.target.classList.contains('lb-fig')) closeLb();
    });
    document.addEventListener('keydown', function (e) {
      if (lb.hidden) return;
      if (e.key === 'Escape') { closeLb(); return; }
      /* 弹层打开时把 Tab 焦点锁在关闭按钮上 */
      if (e.key === 'Tab') { e.preventDefault(); lbClose.focus(); }
    });
  }
})();
