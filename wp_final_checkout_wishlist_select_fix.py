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

MARKER_START = "/* PRIME_DROP_FINAL_CHECKOUT_WISHLIST_SELECT_FIX_START */"
MARKER_END = "/* PRIME_DROP_FINAL_CHECKOUT_WISHLIST_SELECT_FIX_END */"

BLOCK = r"""
/* PRIME_DROP_FINAL_CHECKOUT_WISHLIST_SELECT_FIX_START */
add_action('wp_footer', function() {
    ?>
    <style id="prime-drop-final-checkout-wishlist-select-fix">
    /* Checkout: no permitir que el drawer/parpadeo aparezca dentro del checkout */
    body.woocommerce-checkout #cart-drawer,
    body.woocommerce-checkout .cart-drawer,
    body.woocommerce-checkout .pd-cart-drawer,
    body.woocommerce-checkout [id*="cart-drawer"],
    body.woocommerce-checkout [class*="cart-drawer"],
    body.woocommerce-checkout #cart-drawer-overlay,
    body.woocommerce-checkout .cart-drawer-overlay,
    body.woocommerce-checkout .pd-cart-overlay,
    body.woocommerce-checkout .pd-cart-drawer-overlay {
      display: none !important;
      visibility: hidden !important;
      opacity: 0 !important;
      pointer-events: none !important;
    }

    /* Checkout: "Ya eres cliente" limpio, sin icono peleando con texto */
    body.woocommerce-checkout .woocommerce-form-login-toggle .woocommerce-info {
      display: flex !important;
      align-items: center !important;
      justify-content: space-between !important;
      gap: 18px !important;
      min-height: 48px !important;
      padding: 14px 22px !important;
      border: 1px solid #eeeeee !important;
      border-radius: 14px !important;
      background: #fafafa !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      line-height: 1.35 !important;
      overflow: hidden !important;
    }

    body.woocommerce-checkout .woocommerce-form-login-toggle .woocommerce-info::before,
    body.woocommerce-checkout .woocommerce-form-login-toggle .woocommerce-info svg,
    body.woocommerce-checkout .woocommerce-form-login-toggle .woocommerce-info .ct-icon,
    body.woocommerce-checkout .woocommerce-form-login-toggle .woocommerce-info i,
    body.woocommerce-checkout .woocommerce-form-login-toggle .woocommerce-info [class*="icon"] {
      display: none !important;
      content: none !important;
      width: 0 !important;
      height: 0 !important;
      margin: 0 !important;
      padding: 0 !important;
      opacity: 0 !important;
    }

    body.woocommerce-checkout .woocommerce-form-login-toggle .woocommerce-info a {
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      text-decoration: underline !important;
      text-underline-offset: 3px !important;
      white-space: nowrap !important;
    }

    @media (max-width: 600px) {
      body.woocommerce-checkout .woocommerce-form-login-toggle .woocommerce-info {
        align-items: flex-start !important;
        flex-direction: column !important;
        gap: 8px !important;
      }
    }

    /* Checkout: select/dropdown sin hover transparente */
    body.woocommerce-checkout select,
    body.woocommerce-checkout select option,
    body.woocommerce-checkout .select2-container,
    body.woocommerce-checkout .select2-selection,
    body.woocommerce-checkout .select2-dropdown,
    body.woocommerce-checkout .select2-results__option {
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      background: #ffffff !important;
    }

    body.woocommerce-checkout select:focus,
    body.woocommerce-checkout select:hover,
    body.woocommerce-checkout select option:hover,
    body.woocommerce-checkout select option:focus,
    body.woocommerce-checkout select option:checked,
    body.woocommerce-checkout .select2-results__option--highlighted,
    body.woocommerce-checkout .select2-results__option--highlighted[aria-selected],
    body.woocommerce-checkout .select2-results__option--highlighted[data-selected],
    body.woocommerce-checkout .select2-results__option[aria-selected="true"],
    body.woocommerce-checkout .select2-results__option[data-selected="true"] {
      color: #ffffff !important;
      -webkit-text-fill-color: #ffffff !important;
      background: #000000 !important;
    }

    body.woocommerce-checkout .select2-dropdown {
      border: 1px solid #000000 !important;
      border-radius: 12px !important;
      overflow: hidden !important;
      box-shadow: 0 12px 28px rgba(0,0,0,0.12) !important;
    }

    body.woocommerce-checkout .select2-results__option {
      padding: 11px 16px !important;
      font-size: 14px !important;
      line-height: 1.35 !important;
    }

    /* Wishlist: no reemplazar contenido real, solo maquillar estados del plugin */
    body.woocommerce-wishlist .pd-wishlist-empty-clean {
      display: none !important;
    }

    body.woocommerce-wishlist .entry-header,
    body.woocommerce-wishlist .entry-title,
    body.woocommerce-wishlist h1.entry-title {
      display: none !important;
    }

    body.woocommerce-wishlist .entry-content {
      padding-top: 54px !important;
    }

    body.woocommerce-wishlist .wishlist-title h2,
    body.woocommerce-wishlist .yith-wcwl-form h2 {
      font-size: clamp(34px, 4vw, 52px) !important;
      line-height: 1.08 !important;
      text-align: center !important;
      margin-bottom: 34px !important;
    }

    body.woocommerce-wishlist .wishlist_table,
    body.woocommerce-wishlist .yith-wcwl-form,
    body.woocommerce-wishlist .entry-content,
    body.woocommerce-wishlist .woocommerce {
      visibility: visible !important;
      opacity: 1 !important;
    }

    body.woocommerce-wishlist .wishlist_table {
      max-width: 980px !important;
      margin-left: auto !important;
      margin-right: auto !important;
      border-radius: 18px !important;
      box-shadow: 0 18px 60px rgba(0,0,0,0.06) !important;
    }

    body.woocommerce-wishlist .wishlist-empty {
      padding-top: 64px !important;
      padding-bottom: 64px !important;
    }

    body.woocommerce-wishlist .wishlist-empty::after {
      display: none !important;
      content: none !important;
    }

    body.woocommerce-wishlist .pd-wishlist-empty-title {
      display: block !important;
      margin: 18px auto 10px !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      font-family: 'Roboto Serif', Georgia, serif !important;
      font-size: clamp(24px, 3vw, 34px) !important;
      line-height: 1.15 !important;
      font-weight: 800 !important;
      text-align: center !important;
    }
    </style>
    <script id="prime-drop-final-checkout-wishlist-select-fix-js">
    (function() {
      function decodeProductTitles() {
        document.querySelectorAll('.woocommerce-loop-product__title, h1.product_title, .product-title, .product-name a').forEach(function(el) {
          if (!el || !el.textContent) return;
          el.textContent = el.textContent
            .replace(/&amp;#8211;|&#8211;|&amp;ndash;|&ndash;/g, '–')
            .replace(/\s+–\s+/g, ' – ');
        });
      }

      function stabilizeCheckout() {
        if (!document.body.classList.contains('woocommerce-checkout')) return;
        document.querySelectorAll('#cart-drawer, .cart-drawer, .pd-cart-drawer, [id*="cart-drawer"], [class*="cart-drawer"], #cart-drawer-overlay, .cart-drawer-overlay, .pd-cart-overlay, .pd-cart-drawer-overlay').forEach(function(el) {
          el.classList.remove('active', 'open', 'show', 'is-open', 'ct-open');
          el.setAttribute('aria-hidden', 'true');
        });
        document.documentElement.style.overflow = '';
        document.body.style.overflow = '';
        document.body.style.position = '';
        document.body.style.top = '';
        document.body.style.left = '';
        document.body.style.right = '';
        document.body.style.width = '';
      }

      function recoverWishlist() {
        if (!/\/wishlist\/?/.test(window.location.pathname)) return;
        document.body.classList.remove('pd-wishlist-empty');
        document.querySelectorAll('.pd-wishlist-empty-clean').forEach(function(el) {
          el.remove();
        });

        var emptyCell = document.querySelector('.wishlist-empty');
        if (!emptyCell) return;

        var hasProductRows = Array.from(document.querySelectorAll('.wishlist_table tbody tr')).some(function(row) {
          return !row.querySelector('.wishlist-empty') && (row.querySelector('.product-name a') || row.querySelector('.product-thumbnail img'));
        });

        if (hasProductRows) return;

        if (!emptyCell.querySelector('.pd-wishlist-empty-title')) {
          var title = document.createElement('h2');
          title.className = 'pd-wishlist-empty-title';
          title.textContent = 'Tu lista de deseos esta vacia';
          var copy = emptyCell.querySelector('.pd-wishlist-empty-copy');
          emptyCell.insertBefore(title, copy || emptyCell.firstChild);
        }
      }

      function run() {
        decodeProductTitles();
        stabilizeCheckout();
        recoverWishlist();
      }

      document.addEventListener('DOMContentLoaded', run);
      window.addEventListener('pageshow', run);
      window.addEventListener('load', run);
      document.body && document.body.addEventListener('updated_checkout', run);
      [100, 500, 1200, 2400].forEach(function(delay) {
        setTimeout(run, delay);
      });
    })();
    </script>
    <?php
}, 10009);
/* PRIME_DROP_FINAL_CHECKOUT_WISHLIST_SELECT_FIX_END */
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
    s.headers.update({"User-Agent": "PrimeDropFinalCheckoutWishlistSelectFix/1.0"})
    login(s)

    editor_url = urljoin(BASE, "/wp-admin/theme-editor.php?file=functions.php&theme=blocksy")
    page = s.get(editor_url, timeout=30)
    page.raise_for_status()
    textarea = re.search(r'<textarea[^>]+name=["\']newcontent["\'][^>]*>(.*?)</textarea>', page.text, re.S)
    if not textarea:
        raise RuntimeError("Could not find functions.php editor textarea")

    current = html.unescape(textarea.group(1))
    Path("wp-backups").mkdir(exist_ok=True)
    backup = Path("wp-backups") / f"functions_before_final_checkout_wishlist_select_fix_{datetime.now():%Y%m%d_%H%M%S}.php"
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
