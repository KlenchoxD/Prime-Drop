import html
import os
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import requests

BASE = "https://primedropelite.com"
USER = os.environ["PD_WP_USER"]
PASS = os.environ["PD_WP_PASS"]

MARKER_START = "/* PRIME_DROP_MOBILE_BOLSOS_AND_BAG_TITLE_START */"
MARKER_END = "/* PRIME_DROP_MOBILE_BOLSOS_AND_BAG_TITLE_END */"

BLOCK = r"""
/* PRIME_DROP_MOBILE_BOLSOS_AND_BAG_TITLE_START */
add_action('wp_footer', function() {
    ?>
    <style id="prime-drop-mobile-bolsos-and-bag-title-css">
    @media (max-width: 1024px) {
      .pd-bolsos-menu-parent.pd-submenu-open > .pd-bolsos-submenu {
        opacity: 1 !important;
        visibility: visible !important;
        pointer-events: auto !important;
      }

      .pd-bolsos-submenu a[data-pd-all-bags="1"] {
        font-weight: 900 !important;
      }
    }
    </style>

    <script id="prime-drop-mobile-bolsos-and-bag-title-js">
    (function() {
      function isTouchMenuMode() {
        return window.matchMedia('(max-width: 1024px)').matches || window.matchMedia('(hover: none)').matches;
      }

      function getDirectBolsosLink(li) {
        if (!li) return null;
        return Array.prototype.slice.call(li.children).find(function(child) {
          return child.tagName === 'A' && /^BOLSOS$/i.test((child.textContent || '').trim());
        });
      }

      function ensureAllBagsItem(li) {
        var submenu = li && li.querySelector(':scope > .pd-bolsos-submenu');
        if (!submenu || submenu.querySelector('a[data-pd-all-bags="1"]')) return;
        var item = document.createElement('li');
        item.innerHTML = '<a data-pd-all-bags="1" href="/bolsos/">TODOS LOS BOLSOS</a>';
        submenu.insertBefore(item, submenu.firstChild);
      }

      function fixMobileBolsosMenu() {
        var selectors = [
          'nav[data-id="mobile-menu"] li.pd-bolsos-menu-parent',
          '#offcanvas li.pd-bolsos-menu-parent',
          '.ct-panel li.pd-bolsos-menu-parent',
          '.ct-drawer-canvas li.pd-bolsos-menu-parent',
          'header li.pd-bolsos-menu-parent'
        ].join(',');

        document.querySelectorAll(selectors).forEach(function(li) {
          var link = getDirectBolsosLink(li);
          if (!link) return;

          ensureAllBagsItem(li);

          if (link.dataset.pdTouchBolsosReady === '1') return;

          var cleanLink = link.cloneNode(true);
          cleanLink.dataset.pdBolsosFixed = '1';
          cleanLink.dataset.pdTouchBolsosReady = '1';
          cleanLink.setAttribute('href', '/bolsos/');
          link.replaceWith(cleanLink);

          cleanLink.addEventListener('click', function(event) {
            if (!isTouchMenuMode()) return;
            event.preventDefault();
            event.stopPropagation();
            event.stopImmediatePropagation();
            var open = li.classList.toggle('pd-submenu-open');
            cleanLink.setAttribute('aria-expanded', open ? 'true' : 'false');

            var toggle = li.querySelector(':scope > .pd-submenu-toggle');
            if (toggle) toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
          }, true);
        });
      }

      function renameCartDrawerTitle() {
        var selectors = [
          '.pd-cart-drawer-header h3',
          '.cart-drawer-header h3',
          '#cart-drawer h3',
          '.pd-cart-drawer h3',
          '.cart-drawer h3'
        ].join(',');

        document.querySelectorAll(selectors).forEach(function(title) {
          var text = (title.textContent || '').trim();
          if (/carrito\s+de\s+compra/i.test(text) || /carrito\s+de\s+compras/i.test(text)) {
            title.textContent = 'Bolsa de compra';
          }
        });
      }

      function runPrimeDropMobileBagFixes() {
        fixMobileBolsosMenu();
        renameCartDrawerTitle();
      }

      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', runPrimeDropMobileBagFixes);
      } else {
        runPrimeDropMobileBagFixes();
      }

      window.addEventListener('load', runPrimeDropMobileBagFixes);
      window.addEventListener('resize', runPrimeDropMobileBagFixes);
      document.addEventListener('click', function() {
        setTimeout(runPrimeDropMobileBagFixes, 80);
      }, true);

      var attempts = 0;
      var timer = setInterval(function() {
        runPrimeDropMobileBagFixes();
        attempts += 1;
        if (attempts >= 20) clearInterval(timer);
      }, 250);

      new MutationObserver(runPrimeDropMobileBagFixes).observe(document.documentElement, {
        childList: true,
        subtree: true
      });
    })();
    </script>
    <?php
}, 10040);
/* PRIME_DROP_MOBILE_BOLSOS_AND_BAG_TITLE_END */
"""


def login(session):
    session.get(urljoin(BASE, "/wp-login.php"), timeout=25)
    resp = session.post(
        urljoin(BASE, "/wp-login.php"),
        data={
            "log": USER,
            "pwd": PASS,
            "wp-submit": "Log In",
            "redirect_to": urljoin(BASE, "/wp-admin/"),
            "testcookie": "1",
        },
        timeout=30,
        allow_redirects=True,
    )
    if "wp-admin" not in resp.url and "Escritorio" not in resp.text and "Dashboard" not in resp.text:
        raise RuntimeError("Login failed")


def hidden_value(text, name):
    for tag in re.findall(r"<input[^>]+>", text, re.I):
        if not re.search(rf'name=["\']{re.escape(name)}["\']', tag, re.I):
            continue
        match = re.search(r'value=["\']([^"\']*)', tag, re.I)
        return html.unescape(match.group(1)) if match else ""
    return ""


def main():
    s = requests.Session()
    s.headers.update({"User-Agent": "PrimeDropMobileBolsosAndBagTitle/1.0"})
    login(s)

    editor_url = urljoin(BASE, "/wp-admin/theme-editor.php?file=functions.php&theme=blocksy")
    page = s.get(editor_url, timeout=30)
    page.raise_for_status()

    textarea = re.search(r'<textarea[^>]+name=["\']newcontent["\'][^>]*>(.*?)</textarea>', page.text, re.S)
    if not textarea:
        raise RuntimeError("Could not find functions.php editor textarea")

    current = html.unescape(textarea.group(1))
    Path("wp-backups").mkdir(exist_ok=True)
    backup = Path("wp-backups") / f"functions_before_mobile_bolsos_and_bag_title_{datetime.now():%Y%m%d_%H%M%S}.php"
    backup.write_text(current, encoding="utf-8")

    pattern = re.compile(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), re.S)
    if pattern.search(current):
        updated = pattern.sub(lambda _: BLOCK.strip(), current)
    else:
        updated = current.rstrip() + "\n\n" + BLOCK.strip() + "\n"

    nonce = hidden_value(page.text, "_wpnonce") or hidden_value(page.text, "nonce")
    if not nonce:
        raise RuntimeError("Could not find theme editor nonce")

    resp = s.post(
        urljoin(BASE, "/wp-admin/theme-editor.php"),
        data={
            "nonce": nonce,
            "_wp_http_referer": "/wp-admin/theme-editor.php?file=functions.php&theme=blocksy",
            "newcontent": updated,
            "action": "update",
            "file": "functions.php",
            "theme": "blocksy",
            "docs-list": "",
            "scrollto": "0",
            "submit": "Actualizar archivo",
        },
        timeout=45,
        allow_redirects=True,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"Update failed: {resp.status_code}")

    dashboard = s.get(urljoin(BASE, "/wp-admin/"), timeout=30)
    purged = False
    for href in re.findall(r'href=["\']([^"\']+)["\']', dashboard.text):
        raw = html.unescape(href)
        if "litespeed" in raw.lower() and "purge" in raw.lower():
            s.get(urljoin(BASE, raw), timeout=25)
            purged = True
            break

    print(f"updated=true backup={backup} purged={purged}")


if __name__ == "__main__":
    main()
