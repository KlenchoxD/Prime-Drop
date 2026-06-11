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

MARKER_START = "/* PRIME_DROP_MATCH_BUILDER_PRODUCTS_START */"
MARKER_END = "/* PRIME_DROP_MATCH_BUILDER_PRODUCTS_END */"

BLOCK = r"""
/* PRIME_DROP_MATCH_BUILDER_PRODUCTS_START */
add_action('wp_footer', function() {
    ?>
    <style id="prime-drop-match-builder-products-css">
    /* Solo cards: /bolsos, hombre, mujer y destacadas */
    body.page-id-547 .woocommerce ul.products li.product,
    body.tax-product_cat .woocommerce ul.products li.product,
    body.post-type-archive-product .woocommerce ul.products li.product,
    body.page-id-14 .woocommerce ul.products li.product {
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      justify-content: flex-start !important;
      background: transparent !important;
      border: none !important;
      box-shadow: none !important;
      overflow: visible !important;
      text-align: center !important;
      height: auto !important;
      min-height: 0 !important;
      padding: 0 !important;
    }

    body.page-id-547 .woocommerce ul.products li.product a.woocommerce-loop-product__link,
    body.tax-product_cat .woocommerce ul.products li.product a.woocommerce-loop-product__link,
    body.post-type-archive-product .woocommerce ul.products li.product a.woocommerce-loop-product__link,
    body.page-id-14 .woocommerce ul.products li.product a.woocommerce-loop-product__link {
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      width: 100% !important;
      flex: 1 1 auto !important;
      background: transparent !important;
      text-align: center !important;
      color: #000000 !important;
      text-decoration: none !important;
    }

    body.page-id-547 .woocommerce ul.products li.product a img,
    body.page-id-547 .woocommerce ul.products li.product img,
    body.tax-product_cat .woocommerce ul.products li.product a img,
    body.tax-product_cat .woocommerce ul.products li.product img,
    body.post-type-archive-product .woocommerce ul.products li.product a img,
    body.post-type-archive-product .woocommerce ul.products li.product img,
    body.page-id-14 .woocommerce ul.products li.product a img,
    body.page-id-14 .woocommerce ul.products li.product img {
      width: 100% !important;
      aspect-ratio: 4 / 5 !important;
      height: auto !important;
      min-height: 0 !important;
      max-height: none !important;
      object-fit: contain !important;
      object-position: center center !important;
      margin: 0 0 14px !important;
      padding: 24px 18px 18px !important;
      background: #f5f5f5 !important;
      border: none !important;
      border-radius: 0 !important;
      box-sizing: border-box !important;
      display: block !important;
      transform: none !important;
      filter: none !important;
    }

    body.page-id-547 .woocommerce ul.products li.product .woocommerce-loop-product__title,
    body.tax-product_cat .woocommerce ul.products li.product .woocommerce-loop-product__title,
    body.post-type-archive-product .woocommerce ul.products li.product .woocommerce-loop-product__title,
    body.page-id-14 .woocommerce ul.products li.product .woocommerce-loop-product__title {
      width: 100% !important;
      min-height: 44px !important;
      height: auto !important;
      margin: 0 0 8px !important;
      padding: 0 8px !important;
      display: flex !important;
      align-items: flex-start !important;
      justify-content: center !important;
      overflow: visible !important;
      -webkit-line-clamp: unset !important;
      -webkit-box-orient: initial !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 18px !important;
      font-weight: 800 !important;
      line-height: 1.08 !important;
      letter-spacing: 0 !important;
      text-align: center !important;
      text-transform: none !important;
      color: #000000 !important;
    }

    @media (min-width: 768px) {
      body.page-id-547 .woocommerce ul.products li.product .woocommerce-loop-product__title,
      body.tax-product_cat .woocommerce ul.products li.product .woocommerce-loop-product__title,
      body.post-type-archive-product .woocommerce ul.products li.product .woocommerce-loop-product__title,
      body.page-id-14 .woocommerce ul.products li.product .woocommerce-loop-product__title {
        min-height: 66px !important;
      }
    }

    body.page-id-547 .woocommerce ul.products li.product .price,
    body.tax-product_cat .woocommerce ul.products li.product .price,
    body.post-type-archive-product .woocommerce ul.products li.product .price,
    body.page-id-14 .woocommerce ul.products li.product .price {
      width: 100% !important;
      min-height: 18px !important;
      height: auto !important;
      margin: 0 0 16px !important;
      padding: 0 !important;
      display: block !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 12px !important;
      font-weight: 400 !important;
      line-height: 1.2 !important;
      text-align: center !important;
      color: #000000 !important;
    }

    body.page-id-547 .woocommerce ul.products li.product .button,
    body.tax-product_cat .woocommerce ul.products li.product .button,
    body.post-type-archive-product .woocommerce ul.products li.product .button,
    body.page-id-14 .woocommerce ul.products li.product .button {
      margin-top: auto !important;
      align-self: center !important;
    }

    @media (max-width: 520px) {
      body.page-id-547 .woocommerce ul.products li.product a img,
      body.tax-product_cat .woocommerce ul.products li.product a img,
      body.post-type-archive-product .woocommerce ul.products li.product a img,
      body.page-id-14 .woocommerce ul.products li.product a img {
        padding: 18px 10px 12px !important;
      }

      body.page-id-547 .woocommerce ul.products li.product .woocommerce-loop-product__title,
      body.tax-product_cat .woocommerce ul.products li.product .woocommerce-loop-product__title,
      body.post-type-archive-product .woocommerce ul.products li.product .woocommerce-loop-product__title,
      body.page-id-14 .woocommerce ul.products li.product .woocommerce-loop-product__title {
        min-height: 50px !important;
        font-size: 15px !important;
      }
    }
    </style>
    <?php
}, 10100);
/* PRIME_DROP_MATCH_BUILDER_PRODUCTS_END */
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
    session.headers.update({"User-Agent": "PrimeDropMatchBuilderProducts/1.0"})
    login(session)

    editor_url = urljoin(BASE, "/wp-admin/theme-editor.php?file=functions.php&theme=blocksy")
    page = session.get(editor_url, timeout=30)
    page.raise_for_status()

    textarea = re.search(r'<textarea[^>]+name=["\']newcontent["\'][^>]*>(.*?)</textarea>', page.text, re.S)
    if not textarea:
        raise RuntimeError("Could not find functions.php editor textarea")

    current = html.unescape(textarea.group(1))
    Path("wp-backups").mkdir(exist_ok=True)
    backup = Path("wp-backups") / f"functions_before_match_builder_products_{datetime.now():%Y%m%d_%H%M%S}.php"
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
