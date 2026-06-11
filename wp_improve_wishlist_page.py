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

MARKER_START = "/* PRIME_DROP_WISHLIST_PAGE_START */"
MARKER_END = "/* PRIME_DROP_WISHLIST_PAGE_END */"

BLOCK = r"""
/* PRIME_DROP_WISHLIST_PAGE_START */
add_action('wp_footer', function() {
    if (!is_page('wishlist') && !is_page(591)) {
        return;
    }
    ?>
    <style id="prime-drop-wishlist-page">
    body.woocommerce-wishlist .entry-header {
      max-width: 1180px !important;
      margin: 0 auto !important;
      padding: 44px 24px 28px !important;
      text-align: center !important;
      background: #ffffff !important;
    }

    body.woocommerce-wishlist .entry-title,
    body.woocommerce-wishlist .page-title {
      margin: 0 !important;
      color: #000000 !important;
      font-size: clamp(34px, 4vw, 54px) !important;
      line-height: 1.05 !important;
      letter-spacing: 0 !important;
    }

    body.woocommerce-wishlist .entry-content {
      max-width: 1180px !important;
      margin: 0 auto 90px !important;
      padding: 0 24px !important;
      box-sizing: border-box !important;
    }

    body.woocommerce-wishlist .yith-wcwl-form {
      width: 100% !important;
      max-width: 100% !important;
      margin: 0 auto !important;
      padding: 0 !important;
    }

    body.woocommerce-wishlist .wishlist-title-container,
    body.woocommerce-wishlist .wishlist-title {
      text-align: center !important;
      margin: 0 0 28px !important;
    }

    body.woocommerce-wishlist .wishlist-title h2,
    body.woocommerce-wishlist .yith-wcwl-form h2 {
      margin: 0 !important;
      font-size: clamp(28px, 3vw, 42px) !important;
      line-height: 1.1 !important;
      color: #000000 !important;
      text-align: center !important;
    }

    body.woocommerce-wishlist .wishlist_table {
      width: 100% !important;
      border: 1px solid #eeeeee !important;
      border-radius: 14px !important;
      overflow: hidden !important;
      background: #ffffff !important;
      box-shadow: 0 18px 50px rgba(0, 0, 0, 0.05) !important;
      border-collapse: separate !important;
      border-spacing: 0 !important;
      margin: 0 !important;
    }

    body.woocommerce-wishlist .wishlist_table th {
      padding: 18px 16px !important;
      background: #f7f7f7 !important;
      color: #000000 !important;
      font-size: 11px !important;
      font-weight: 700 !important;
      letter-spacing: 1.4px !important;
      text-transform: uppercase !important;
      text-align: center !important;
      border: 0 !important;
    }

    body.woocommerce-wishlist .wishlist_table td {
      padding: 18px 16px !important;
      vertical-align: middle !important;
      text-align: center !important;
      border-top: 1px solid #f0f0f0 !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
    }

    body.woocommerce-wishlist .wishlist_table .product-thumbnail img {
      width: 92px !important;
      height: 92px !important;
      object-fit: contain !important;
      background: #f7f7f7 !important;
      border-radius: 10px !important;
      padding: 8px !important;
    }

    body.woocommerce-wishlist .wishlist_table .product-name a {
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      font-size: 15px !important;
      font-weight: 700 !important;
      line-height: 1.35 !important;
      text-decoration: none !important;
    }

    body.woocommerce-wishlist .wishlist_table .product-price,
    body.woocommerce-wishlist .wishlist_table .product-price * {
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      font-weight: 600 !important;
    }

    body.woocommerce-wishlist .wishlist_table .product-stock-status span {
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      min-height: 30px !important;
      padding: 6px 13px !important;
      border-radius: 20px !important;
      background: #f3f3f3 !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      font-size: 11px !important;
      font-weight: 700 !important;
      letter-spacing: 1px !important;
      text-transform: uppercase !important;
    }

    body.woocommerce-wishlist .wishlist_table .product-add-to-cart a,
    body.woocommerce-wishlist .wishlist_table .product-add-to-cart .button {
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      min-height: 42px !important;
      padding: 11px 24px !important;
      border-radius: 25px !important;
      background: #000000 !important;
      color: #ffffff !important;
      -webkit-text-fill-color: #ffffff !important;
      border: 0 !important;
      font-size: 11px !important;
      font-weight: 700 !important;
      letter-spacing: 1.5px !important;
      text-transform: uppercase !important;
      text-decoration: none !important;
      white-space: nowrap !important;
    }

    body.woocommerce-wishlist .wishlist_table .product-remove a {
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      width: 34px !important;
      height: 34px !important;
      border-radius: 50% !important;
      border: 1px solid #eeeeee !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      background: #ffffff !important;
      text-decoration: none !important;
    }

    body.woocommerce-wishlist.pd-wishlist-empty .wishlist_table thead {
      display: none !important;
    }

    body.woocommerce-wishlist .wishlist-empty {
      padding: 58px 24px !important;
      text-align: center !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      font-size: 0 !important;
      border: 0 !important;
    }

    body.woocommerce-wishlist .wishlist-empty::before {
      content: "♡" !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      width: 58px !important;
      height: 58px !important;
      margin: 0 auto 18px !important;
      border-radius: 50% !important;
      border: 1px solid #e4e4e4 !important;
      color: #000000 !important;
      font-size: 30px !important;
      line-height: 1 !important;
    }

    body.woocommerce-wishlist .wishlist-empty::after {
      content: "Tu lista de deseos está vacía" !important;
      display: block !important;
      max-width: 360px !important;
      margin: 0 auto !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      font-size: 22px !important;
      font-weight: 700 !important;
      line-height: 1.25 !important;
      text-align: center !important;
    }

    body.woocommerce-wishlist .pd-wishlist-empty-copy {
      max-width: 430px !important;
      margin: 12px auto 0 !important;
      color: #555555 !important;
      -webkit-text-fill-color: #555555 !important;
      font-size: 14px !important;
      line-height: 1.55 !important;
      text-align: center !important;
    }

    body.woocommerce-wishlist .pd-wishlist-empty-cta {
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      min-height: 44px !important;
      margin: 22px auto 0 !important;
      padding: 12px 28px !important;
      border-radius: 25px !important;
      background: #000000 !important;
      color: #ffffff !important;
      -webkit-text-fill-color: #ffffff !important;
      font-size: 12px !important;
      font-weight: 700 !important;
      letter-spacing: 1.8px !important;
      text-transform: uppercase !important;
      text-decoration: none !important;
    }

    @media (max-width: 768px) {
      body.woocommerce-wishlist .entry-header {
        padding: 34px 18px 18px !important;
      }

      body.woocommerce-wishlist .entry-content {
        padding-left: 16px !important;
        padding-right: 16px !important;
        margin-bottom: 64px !important;
      }

      body.woocommerce-wishlist .wishlist_table,
      body.woocommerce-wishlist .wishlist_table thead,
      body.woocommerce-wishlist .wishlist_table tbody,
      body.woocommerce-wishlist .wishlist_table tr,
      body.woocommerce-wishlist .wishlist_table td {
        display: block !important;
        width: 100% !important;
        box-sizing: border-box !important;
      }

      body.woocommerce-wishlist .wishlist_table thead {
        display: none !important;
      }

      body.woocommerce-wishlist .wishlist_table tr {
        padding: 18px !important;
        border-top: 1px solid #f0f0f0 !important;
      }

      body.woocommerce-wishlist .wishlist_table td {
        padding: 8px 0 !important;
        border: 0 !important;
      }

      body.woocommerce-wishlist .wishlist_table .product-thumbnail img {
        width: 140px !important;
        height: 140px !important;
      }

      body.woocommerce-wishlist .wishlist-empty {
        padding: 48px 20px !important;
      }
    }
    </style>
    <script id="prime-drop-wishlist-page-js">
    (function() {
      function polishWishlist() {
        var emptyCell = document.querySelector('body.woocommerce-wishlist .wishlist-empty');
        if (!emptyCell) return;
        document.body.classList.add('pd-wishlist-empty');

        if (!emptyCell.querySelector('.pd-wishlist-empty-copy')) {
          var copy = document.createElement('p');
          copy.className = 'pd-wishlist-empty-copy';
          copy.textContent = 'Guarda aquí tus bolsos favoritos para encontrarlos rápido cuando quieras comprarlos.';
          emptyCell.appendChild(copy);
        }

        if (!emptyCell.querySelector('.pd-wishlist-empty-cta')) {
          var cta = document.createElement('a');
          cta.className = 'pd-wishlist-empty-cta';
          cta.href = '/bolsos/';
          cta.textContent = 'VER BOLSOS';
          emptyCell.appendChild(cta);
        }
      }

      document.addEventListener('DOMContentLoaded', polishWishlist);
      window.addEventListener('load', polishWishlist);
      setTimeout(polishWishlist, 600);
    })();
    </script>
    <?php
}, 10002);
/* PRIME_DROP_WISHLIST_PAGE_END */
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
    s.headers.update({"User-Agent": "PrimeDropWishlistPage/1.0"})
    login(s)

    editor_url = urljoin(BASE, "/wp-admin/theme-editor.php?file=functions.php&theme=blocksy")
    page = s.get(editor_url, timeout=30)
    page.raise_for_status()

    textarea = re.search(r'<textarea[^>]+name=["\']newcontent["\'][^>]*>(.*?)</textarea>', page.text, re.S)
    if not textarea:
        raise RuntimeError("Could not find functions.php editor textarea")

    current = html.unescape(textarea.group(1))
    Path("wp-backups").mkdir(exist_ok=True)
    backup = Path("wp-backups") / f"functions_before_wishlist_page_{datetime.now():%Y%m%d_%H%M%S}.php"
    backup.write_text(current, encoding="utf-8")

    pattern = re.compile(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), re.S)
    if pattern.search(current):
        updated = pattern.sub(BLOCK.strip(), current)
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
