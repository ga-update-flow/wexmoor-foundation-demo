/* Site behaviour: announcement bar, mobile menu, dropdowns (touch), accordions,
   homepage popup, site search, and honest handling of demonstration forms. */
(function () {
  function store(kind, key, val) {
    try {
      var s = window[kind];
      if (val === undefined) return s.getItem(key);
      s.setItem(key, val);
    } catch (e) { return null; }
  }

  // Announcement bar
  var bar = document.querySelector('[data-announce]');
  if (bar) {
    if (store('sessionStorage', 'wf-announce-closed') === '1') bar.classList.add('is-hidden');
    var close = bar.querySelector('[data-announce-close]');
    close && close.addEventListener('click', function () {
      bar.classList.add('is-hidden');
      store('sessionStorage', 'wf-announce-closed', '1');
    });
  }

  // Mobile menu
  var toggle = document.querySelector('[data-menu-toggle]');
  var mobile = document.getElementById('mobile-menu');
  if (toggle && mobile) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      mobile.hidden = open;
    });
  }

  // Dropdowns: first tap on a parent item opens its sub-menu on touch devices
  document.querySelectorAll('.main-navigation .has-children > a').forEach(function (a) {
    a.addEventListener('touchend', function (e) {
      var li = a.parentElement;
      if (!li.classList.contains('open')) {
        e.preventDefault();
        document.querySelectorAll('.main-navigation .has-children.open').forEach(function (o) { o.classList.remove('open'); });
        li.classList.add('open');
      }
    });
  });

  // Accordions
  document.querySelectorAll('[data-accordion]').forEach(function (acc) {
    acc.querySelectorAll('.accordion_title button').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var item = btn.closest('.accordion-item');
        var willOpen = !item.classList.contains('open');
        acc.querySelectorAll('.accordion-item.open').forEach(function (o) {
          o.classList.remove('open');
          o.querySelector('button').setAttribute('aria-expanded', 'false');
        });
        if (willOpen) {
          item.classList.add('open');
          btn.setAttribute('aria-expanded', 'true');
        }
      });
    });
  });

  // Homepage annual report popup (auto-opens once per browser session)
  var popup = document.getElementById('report-popup');
  if (popup && typeof popup.showModal === 'function') {
    if (store('sessionStorage', 'wf-popup-seen') !== '1') {
      setTimeout(function () { popup.showModal(); store('sessionStorage', 'wf-popup-seen', '1'); }, 600);
    }
    popup.querySelector('.pum-close').addEventListener('click', function () { popup.close(); });
    popup.addEventListener('click', function (e) { if (e.target === popup) popup.close(); });
  }

  // Site search (results page)
  var results = document.getElementById('search-results');
  if (results) {
    var q = new URLSearchParams(location.search).get('s') || '';
    var input = document.getElementById('search-again');
    if (input) input.value = q;
    var heading = document.getElementById('search-heading');
    if (!q.trim()) { heading.textContent = 'Search this site'; }
    else {
      heading.textContent = 'Search Results for: ' + q;
      fetch('/wexmoor-foundation-demo/search-index.json').then(function (r) { return r.json(); }).then(function (idx) {
        var terms = q.toLowerCase().split(/\s+/).filter(Boolean);
        var hits = idx.filter(function (p) {
          var hay = (p.title + ' ' + p.text).toLowerCase();
          return terms.every(function (t) { return hay.indexOf(t) !== -1; });
        });
        if (!hits.length) { results.innerHTML = '<p>Sorry, but nothing matched your search terms. Please try again with some different keywords.</p>'; return; }
        results.innerHTML = '';
        hits.forEach(function (h) {
          var art = document.createElement('article');
          var t = h.text, i = t.toLowerCase().indexOf(terms[0]);
          var snip = t.slice(Math.max(0, i - 80), i + 180);
          art.innerHTML = '<h3><a></a></h3><p></p>';
          art.querySelector('a').href = h.url;
          art.querySelector('a').textContent = h.title;
          art.querySelector('p').textContent = (i > 80 ? '…' : '') + snip + '…';
          results.appendChild(art);
        });
      }).catch(function () { results.innerHTML = '<p>Search is temporarily unavailable.</p>'; });
    }
  }

  // Demonstration forms: never transmit anything; say so plainly.
  document.querySelectorAll('form[data-demo-form]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var status = form.querySelector('.form-status') || document.getElementById(form.getAttribute('data-status'));
      if (status) { status.hidden = false; status.focus && status.focus(); }
      form.querySelectorAll('input, select, textarea, button').forEach(function (el) { if (el.type !== 'hidden') el.disabled = true; });
    });
  });

  // Portal sign-in: continue to eligibility quiz without collecting anything
  var signin = document.querySelector('form[data-portal-signin]');
  if (signin) {
    signin.addEventListener('submit', function (e) {
      e.preventDefault();
      location.href = '/wexmoor-foundation-demo/portal/eligibility-quiz/';
    });
  }

  // Eligibility quiz scoring
  var quiz = document.querySelector('form[data-eligibility-quiz]');
  if (quiz) {
    quiz.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!quiz.reportValidity()) return;
      var data = new FormData(quiz);
      var ok = true;
      quiz.querySelectorAll('fieldset[data-pass]').forEach(function (fs) {
        var name = fs.getAttribute('data-name');
        if (data.get(name) !== fs.getAttribute('data-pass')) ok = false;
      });
      document.getElementById('quiz-pass').hidden = !ok;
      document.getElementById('quiz-fail').hidden = ok;
      (ok ? document.getElementById('quiz-pass') : document.getElementById('quiz-fail')).scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  }
})();
