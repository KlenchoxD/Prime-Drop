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

MARKER_START = "/* PRIME_DROP_BOLSOS_OLD_CARD_STYLE_START */"
MARKER_END = "/* PRIME_DROP_BOLSOS_OLD_CARD_STYLE_END */"

BLOCK = r"""
/* PRIME_DROP_BOLSOS_OLD_CARD_STYLE_START */
add_action('wp_footer', function() {
    ?>
    <style id="prime-drop-bolsos-old-card-style-css">
    /* /bolsos/: tarjetas estilo pagina anterior */
    body.page-id-547 .woocommerce ul.products {
      align-items: stretch !important;
      gap: 28px 22px !important;
    }

    body.page-id-547 .woocommerce ul.products li.product {
      display: flex !important;
      flex-direction: column !important;
      align-items: stretch !important;
      justify-content: flex-start !important;
      background: #ffffff !important;
      border: 1px solid #d8d8d8 !important;
      border-radius: 0 !important;
      padding: 0 6px 8px !important;
      overflow: hidden !important;
      text-align: left !important;
      box-sizing: border-box !important;
      box-shadow: none !important;
    }

    body.page-id-547 .woocommerce ul.products li.product a.woocommerce-loop-product__link {
      display: flex !important;
      flex-direction: column !important;
      align-items: stretch !important;
      justify-content: flex-start !important;
      width: 100% !important;
      background: #ffffff !important;
      text-align: left !important;
      color: #000000 !important;
      text-decoration: none !important;
    }

    body.page-id-547 .woocommerce ul.products li.product a img,
    body.page-id-547 .woocommerce ul.products li.product img,
    body.page-id-547 .woocommerce-page ul.products li.product a img,
    body.page-id-547 .woocommerce-page ul.products li.product img {
      width: calc(100% + 12px) !important;
      margin: 0 0 12px -6px !important;
      height: 300px !important;
      min-height: 300px !important;
      max-height: 300px !important;
      object-fit: contain !important;
      object-position: center center !important;
      background: #f4f4f4 !important;
      border-radius: 0 !important;
      padding: 14px !important;
      box-sizing: border-box !important;
      display: block !important;
      flex-shrink: 0 !important;
    }

    body.page-id-547 .woocommerce ul.products li.product figure {
      margin: 0 !important;
      background: #f4f4f4 !important;
      border-radius: 0 !important;
      overflow: hidden !important;
    }

    body.page-id-547 .woocommerce ul.products li.product .woocommerce-loop-product__title {
      min-height: 0 !important;
      height: auto !important;
      margin: 0 0 6px !important;
      padding: 0 !important;
      overflow: visible !important;
      display: block !important;
      -webkit-line-clamp: unset !important;
      -webkit-box-orient: initial !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 18px !important;
      font-weight: 800 !important;
      line-height: 1.12 !important;
      letter-spacing: 0 !important;
      text-transform: none !important;
      text-align: left !important;
      color: #000000 !important;
    }

    body.page-id-547 .woocommerce ul.products li.product .price {
      display: block !important;
      height: auto !important;
      min-height: 0 !important;
      margin: 0 0 10px !important;
      padding: 0 !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 12px !important;
      font-weight: 400 !important;
      line-height: 1.3 !important;
      text-align: left !important;
      color: #000000 !important;
    }

    body.page-id-547 .woocommerce ul.products li.product .button,
    body.page-id-547 .woocommerce ul.products li.product:hover .button {
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      width: 100% !important;
      min-width: 0 !important;
      max-width: none !important;
      min-height: 36px !important;
      margin: auto 0 0 !important;
      padding: 9px 14px !important;
      background: #ffffff !important;
      color: #000000 !important;
      border: 1.5px solid #000000 !important;
      border-radius: 999px !important;
      box-shadow: none !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 12px !important;
      font-weight: 500 !important;
      letter-spacing: 0 !important;
      line-height: 1.15 !important;
      text-align: center !important;
      text-transform: none !important;
      white-space: normal !important;
      opacity: 1 !important;
      transform: none !important;
      pointer-events: auto !important;
    }

    body.page-id-547 .woocommerce ul.products li.product .button:hover {
      background: #000000 !important;
      color: #ffffff !important;
    }

    @media (min-width: 1000px) {
      body.page-id-547 .woocommerce ul.products li.product a img,
      body.page-id-547 .woocommerce ul.products li.product img,
      body.page-id-547 .woocommerce-page ul.products li.product a img,
      body.page-id-547 .woocommerce-page ul.products li.product img {
        height: 330px !important;
        min-height: 330px !important;
        max-height: 330px !important;
      }
    }

    @media (min-width: 768px) and (max-width: 999px) {
      body.page-id-547 .woocommerce ul.products {
        gap: 24px 18px !important;
      }

      body.page-id-547 .woocommerce ul.products li.product a img,
      body.page-id-547 .woocommerce ul.products li.product img,
      body.page-id-547 .woocommerce-page ul.products li.product a img,
      body.page-id-547 .woocommerce-page ul.products li.product img {
        height: 285px !important;
        min-height: 285px !important;
        max-height: 285px !important;
      }
    }

    @media (max-width: 767px) {
      body.page-id-547 .woocommerce ul.products {
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        gap: 18px 12px !important;
        padding-left: 10px !important;
        padding-right: 10px !important;
      }

      body.page-id-547 .woocommerce ul.products li.product {
        padding: 0 5px 7px !important;
      }

      body.page-id-547 .woocommerce ul.products li.product a img,
      body.page-id-547 .woocommerce ul.products li.product img,
      body.page-id-547 .woocommerce-page ul.products li.product a img,
      body.page-id-547 .woocommerce-page ul.products li.product img {
        width: calc(100% + 10px) !important;
        margin-left: -5px !important;
        height: 235px !important;
        min-height: 235px !important;
        max-height: 235px !important;
        padding: 10px !important;
      }

      body.page-id-547 .woocommerce ul.products li.product .woocommerce-loop-product__title {
        font-size: 15px !important;
        line-height: 1.12 !important;
      }

      body.page-id-547 .woocommerce ul.products li.product .button,
      body.page-id-547 .woocommerce ul.products li.product:hover .button {
        min-height: 35px !important;
        font-size: 11px !important;
        padding: 8px 10px !important;
      }
    }
    </style>
    <?php
}, 10080);
/* PRIME_DROP_BOLSOS_OLD_CARD_STYLE_END */
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
    session = requests.Session()
    session.headers.update({"User-Agent": "PrimeDropOldBolsosCardStyle/1.0"})
    login(session)

    editor_url = urljoin(BASE, "/wp-admin/theme-editor.php?file=functions.php&theme=blocksy")
    page = session.get(editor_url, timeout=30)
    page.raise_for_status()

    textarea = re.search(r'<textarea[^>]+name=["\']newcontent["\'][^>]*>(.*?)</textarea>', page.text, re.S)
    if not textarea:
        raise RuntimeError("Could not find functions.php editor textarea")

    current = html.unescape(textarea.group(1))
    Path("wp-backups").mkdir(exist_ok=True)
    backup = Path("wp-backups") / f"functions_before_bolsos_old_card_style_{datetime.now():%Y%m%d_%H%M%S}.php"
    backup.write_text(current, encoding="utf-8")

    pattern = re.compile(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), re.S)
    if pattern.search(current):
        updated = pattern.sub(lambda _: BLOCK.strip(), current)
    else:
        updated = current.rstrip() + "\n\n" + BLOCK.strip() + "\n"

    nonce = hidden_value(page.text, "_wpnonce") or hidden_value(page.text, "nonce")
    if not nonce:
        raise RuntimeError("Could not find theme editor nonce")

    resp = session.post(
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

    dashboard = session.get(urljoin(BASE, "/wp-admin/"), timeout=30)
    purged = False
    for href in re.findall(r'href=["\']([^"\']+)["\']', dashboard.text):
        raw = html.unescape(href)
        if "litespeed" in raw.lower() and "purge" in raw.lower():
            session.get(urljoin(BASE, raw), timeout=25)
            purged = True
            break

    print(f"updated=true backup={backup} purged={purged}")


if __name__ == "__main__":
    main()
