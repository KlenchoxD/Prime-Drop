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

MARKER_START = "/* PRIME_DROP_BRAND_ARCHIVE_PRICE_STYLE_START */"
MARKER_END = "/* PRIME_DROP_BRAND_ARCHIVE_PRICE_STYLE_END */"

BLOCK = r"""
/* PRIME_DROP_BRAND_ARCHIVE_PRICE_STYLE_START */
add_action('wp_footer', function() {
    ?>
    <style id="prime-drop-brand-archive-price-style-css">
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Serif:wght@400;500;600;700;800&display=swap');

    /* Marcas: misma base visual de productos que /bolsos/ */
    body.tax-product_cat .woocommerce-products-header,
    body.tax-product_cat .woocommerce-notices-wrapper,
    body.tax-product_cat .woocommerce-result-count,
    body.tax-product_cat .woocommerce-ordering,
    body.tax-product_cat .woocommerce ul.products,
    body.tax-product_cat .woocommerce ul.products li.product,
    body.tax-product_cat .woocommerce ul.products li.product a,
    body.tax-product_cat .woocommerce ul.products li.product .woocommerce-loop-product__title,
    body.tax-product_cat .woocommerce ul.products li.product .price,
    body.tax-product_cat .woocommerce ul.products li.product .button {
      font-family: "Roboto Serif", Georgia, serif !important;
    }

    body.tax-product_cat .woocommerce-products-header {
      max-width: 1200px !important;
      margin: 0 auto 22px !important;
      padding: 26px 20px 0 !important;
      text-align: center !important;
    }

    body.tax-product_cat .woocommerce-products-header .page-title {
      margin: 0 !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 30px !important;
      font-weight: 800 !important;
      line-height: 1.15 !important;
      color: #000000 !important;
      text-align: center !important;
    }

    body.tax-product_cat .woocommerce-result-count,
    body.tax-product_cat .woocommerce-ordering {
      font-size: 12px !important;
      font-weight: 700 !important;
      letter-spacing: 1.2px !important;
      text-transform: uppercase !important;
      color: #000000 !important;
    }

    /* Precio estilo Parchita: visible, centrado y con COP solo en listados */
    body.page-id-547 .woocommerce ul.products li.product .price,
    body.tax-product_cat .woocommerce ul.products li.product .price,
    body.post-type-archive-product .woocommerce ul.products li.product .price,
    body.page-id-14 .woocommerce ul.products li.product .price,
    body.single-product .related.products ul.products li.product .price {
      display: block !important;
      width: 100% !important;
      min-height: 22px !important;
      margin: 0 0 16px !important;
      padding: 0 !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 14px !important;
      font-weight: 700 !important;
      line-height: 1.25 !important;
      letter-spacing: 0 !important;
      text-align: center !important;
      color: #000000 !important;
      opacity: 1 !important;
      visibility: visible !important;
    }

    body.page-id-547 .woocommerce ul.products li.product .price .woocommerce-Price-amount,
    body.tax-product_cat .woocommerce ul.products li.product .price .woocommerce-Price-amount,
    body.post-type-archive-product .woocommerce ul.products li.product .price .woocommerce-Price-amount,
    body.page-id-14 .woocommerce ul.products li.product .price .woocommerce-Price-amount,
    body.single-product .related.products ul.products li.product .price .woocommerce-Price-amount {
      color: #000000 !important;
      font: inherit !important;
      white-space: nowrap !important;
    }

    body.page-id-547 .woocommerce ul.products li.product .price .woocommerce-Price-amount::after,
    body.tax-product_cat .woocommerce ul.products li.product .price .woocommerce-Price-amount::after,
    body.post-type-archive-product .woocommerce ul.products li.product .price .woocommerce-Price-amount::after,
    body.page-id-14 .woocommerce ul.products li.product .price .woocommerce-Price-amount::after,
    body.single-product .related.products ul.products li.product .price .woocommerce-Price-amount::after {
      content: " COP";
      font: inherit;
    }

    body.page-id-547 .woocommerce ul.products li.product .woocommerce-loop-product__title,
    body.tax-product_cat .woocommerce ul.products li.product .woocommerce-loop-product__title,
    body.post-type-archive-product .woocommerce ul.products li.product .woocommerce-loop-product__title,
    body.page-id-14 .woocommerce ul.products li.product .woocommerce-loop-product__title,
    body.single-product .related.products ul.products li.product .woocommerce-loop-product__title {
      font-family: "Roboto Serif", Georgia, serif !important;
    }

    body.tax-product_cat select.orderby,
    body.page-id-547 select.orderby,
    body.woocommerce-shop select.orderby {
      color: #ffffff !important;
      background-color: #000000 !important;
      border-color: #000000 !important;
      font-family: "Roboto Serif", Georgia, serif !important;
    }

    body.tax-product_cat select.orderby option,
    body.page-id-547 select.orderby option,
    body.woocommerce-shop select.orderby option {
      color: #000000 !important;
      background-color: #ffffff !important;
    }

    @media (max-width: 768px) {
      body.tax-product_cat .woocommerce-products-header {
        padding-top: 18px !important;
        margin-bottom: 18px !important;
      }

      body.tax-product_cat .woocommerce-products-header .page-title {
        font-size: 24px !important;
      }

      body.page-id-547 .woocommerce ul.products li.product .price,
      body.tax-product_cat .woocommerce ul.products li.product .price,
      body.post-type-archive-product .woocommerce ul.products li.product .price,
      body.page-id-14 .woocommerce ul.products li.product .price,
      body.single-product .related.products ul.products li.product .price {
        font-size: 13px !important;
      }
    }
    </style>
    <?php
}, 10220);
/* PRIME_DROP_BRAND_ARCHIVE_PRICE_STYLE_END */
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


def purge_cache(session):
    dashboard = session.get(urljoin(BASE, "/wp-admin/"), timeout=30)
    for href in re.findall(r'href=["\']([^"\']+)["\']', dashboard.text):
        raw = html.unescape(href)
        if "litespeed" in raw.lower() and "purge" in raw.lower():
            session.get(urljoin(BASE, raw), timeout=25)
            return True
    return False


def main():
    session = requests.Session()
    session.headers.update({"User-Agent": "PrimeDropBrandArchivePriceStyle/1.0"})
    login(session)

    editor_url = urljoin(BASE, "/wp-admin/theme-editor.php?file=functions.php&theme=blocksy")
    page = session.get(editor_url, timeout=30)
    page.raise_for_status()

    textarea = re.search(r'<textarea[^>]+name=["\']newcontent["\'][^>]*>(.*?)</textarea>', page.text, re.S)
    if not textarea:
        raise RuntimeError("Could not find functions.php editor textarea")

    current = html.unescape(textarea.group(1))
    Path("wp-backups").mkdir(exist_ok=True)
    backup = Path("wp-backups") / f"functions_before_brand_archive_price_style_{datetime.now():%Y%m%d_%H%M%S}.php"
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

    print(f"updated=true backup={backup} purged={purge_cache(session)}")


if __name__ == "__main__":
    main()
