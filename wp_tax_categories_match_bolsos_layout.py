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

MARKER_START = "/* PRIME_DROP_TAX_CATEGORIES_MATCH_BOLSOS_START */"
MARKER_END = "/* PRIME_DROP_TAX_CATEGORIES_MATCH_BOLSOS_END */"

BLOCK = r"""
/* PRIME_DROP_TAX_CATEGORIES_MATCH_BOLSOS_START */
add_action('wp_footer', function() {
    ?>
    <style id="prime-drop-tax-categories-match-bolsos-css">
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Serif:wght@400;500;600;700;800&display=swap');

    /* Categorias/marcas: misma estructura visual que /bolsos/ */
    body.tax-product_cat .woocommerce-products-header,
    body.tax-product_cat .pd-shop-search {
      display: none !important;
    }

    body.tax-product_cat .site-main .woocommerce {
      max-width: 900px !important;
      margin: 0 auto !important;
      padding: 0 0 78px !important;
      border-top: 1px solid #eeeeee !important;
      font-family: "Roboto Serif", Georgia, serif !important;
    }

    body.tax-product_cat .woocommerce-result-count {
      float: left !important;
      display: flex !important;
      align-items: center !important;
      min-height: 58px !important;
      margin: 0 !important;
      padding: 0 !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 12px !important;
      font-weight: 800 !important;
      letter-spacing: 1.3px !important;
      text-transform: uppercase !important;
      color: #000000 !important;
    }

    body.tax-product_cat .woocommerce-ordering {
      float: right !important;
      display: flex !important;
      align-items: center !important;
      min-height: 58px !important;
      margin: 0 !important;
      padding: 0 !important;
      font-family: "Roboto Serif", Georgia, serif !important;
    }

    body.tax-product_cat select.orderby {
      min-width: 180px !important;
      height: 34px !important;
      border-radius: 999px !important;
      border: 1px solid #000000 !important;
      background-color: #000000 !important;
      color: #ffffff !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 11px !important;
      font-weight: 800 !important;
      letter-spacing: 1px !important;
      text-transform: uppercase !important;
      padding: 0 34px 0 18px !important;
      box-shadow: none !important;
    }

    body.tax-product_cat select.orderby option {
      background: #ffffff !important;
      color: #000000 !important;
      font-family: "Roboto Serif", Georgia, serif !important;
    }

    body.tax-product_cat .woocommerce ul.products {
      clear: both !important;
      display: grid !important;
      grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
      gap: 46px 28px !important;
      align-items: stretch !important;
      width: 100% !important;
      max-width: 900px !important;
      margin: 0 auto !important;
      padding: 24px 0 0 !important;
      border-top: 1px solid #eeeeee !important;
      list-style: none !important;
    }

    body.tax-product_cat .woocommerce ul.products::before,
    body.tax-product_cat .woocommerce ul.products::after {
      display: none !important;
      content: none !important;
    }

    body.tax-product_cat .woocommerce ul.products li.product {
      float: none !important;
      width: auto !important;
      max-width: none !important;
      min-width: 0 !important;
      margin: 0 !important;
      padding: 0 !important;
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      justify-content: flex-start !important;
      text-align: center !important;
      background: transparent !important;
      border: none !important;
      box-shadow: none !important;
      overflow: visible !important;
      box-sizing: border-box !important;
    }

    body.tax-product_cat .woocommerce ul.products li.product figure {
      width: 100% !important;
      margin: 0 0 0 !important;
      padding: 0 !important;
      background: #f5f5f5 !important;
      overflow: hidden !important;
      border: none !important;
      border-radius: 0 !important;
      box-sizing: border-box !important;
    }

    body.tax-product_cat .woocommerce ul.products li.product figure a.ct-media-container,
    body.tax-product_cat .woocommerce ul.products li.product a.woocommerce-loop-product__link {
      width: 100% !important;
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      justify-content: flex-start !important;
      text-align: center !important;
      color: #000000 !important;
      text-decoration: none !important;
      background: transparent !important;
    }

    body.tax-product_cat .woocommerce ul.products li.product figure a.ct-media-container {
      height: 278px !important;
      min-height: 278px !important;
      max-height: 278px !important;
      justify-content: center !important;
      background: #f5f5f5 !important;
    }

    body.tax-product_cat .woocommerce ul.products li.product a img,
    body.tax-product_cat .woocommerce ul.products li.product img {
      width: 100% !important;
      height: 100% !important;
      min-height: 0 !important;
      max-height: none !important;
      aspect-ratio: auto !important;
      object-fit: contain !important;
      object-position: center center !important;
      margin: 0 !important;
      padding: 18px !important;
      background: #f5f5f5 !important;
      border: none !important;
      border-radius: 0 !important;
      box-shadow: none !important;
      display: block !important;
      box-sizing: border-box !important;
      transform: none !important;
      filter: none !important;
    }

    body.tax-product_cat .woocommerce ul.products li.product .woocommerce-loop-product__title {
      width: 100% !important;
      min-height: 42px !important;
      margin: 0 0 10px !important;
      padding: 0 8px !important;
      display: flex !important;
      align-items: flex-start !important;
      justify-content: center !important;
      overflow: visible !important;
      -webkit-line-clamp: unset !important;
      -webkit-box-orient: initial !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 16px !important;
      font-weight: 800 !important;
      line-height: 1.12 !important;
      letter-spacing: 0 !important;
      text-align: center !important;
      text-transform: none !important;
      color: #000000 !important;
    }

    body.tax-product_cat .woocommerce ul.products li.product .woocommerce-loop-product__title a {
      color: #000000 !important;
      text-decoration: none !important;
      font: inherit !important;
      text-align: center !important;
    }

    body.tax-product_cat .woocommerce ul.products li.product .price {
      width: 100% !important;
      min-height: 22px !important;
      margin: 0 0 16px !important;
      padding: 0 !important;
      display: block !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 14px !important;
      font-weight: 700 !important;
      line-height: 1.25 !important;
      letter-spacing: 0 !important;
      text-align: center !important;
      color: #000000 !important;
    }

    body.tax-product_cat .woocommerce ul.products li.product .entry-meta,
    body.tax-product_cat .woocommerce ul.products li.product .meta-categories {
      display: none !important;
    }

    body.tax-product_cat .woocommerce ul.products li.product .button,
    body.tax-product_cat .woocommerce ul.products li.product:hover .button {
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      width: auto !important;
      min-width: 120px !important;
      max-width: 100% !important;
      min-height: 30px !important;
      margin: auto auto 0 !important;
      padding: 7px 14px !important;
      background: #ffffff !important;
      color: #000000 !important;
      border: 1.4px solid #000000 !important;
      border-radius: 999px !important;
      box-shadow: none !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 10.5px !important;
      font-weight: 700 !important;
      letter-spacing: 0 !important;
      line-height: 1.15 !important;
      text-align: center !important;
      text-transform: uppercase !important;
      white-space: nowrap !important;
      opacity: 1 !important;
      transform: none !important;
      pointer-events: auto !important;
      box-sizing: border-box !important;
    }

    body.tax-product_cat .woocommerce ul.products li.product .button:hover {
      background: #000000 !important;
      color: #ffffff !important;
    }

    @media (max-width: 999px) {
      body.tax-product_cat .site-main .woocommerce {
        max-width: calc(100% - 36px) !important;
      }

      body.tax-product_cat .woocommerce ul.products {
        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        gap: 34px 18px !important;
      }

      body.tax-product_cat .woocommerce ul.products li.product figure a.ct-media-container {
        height: 245px !important;
        min-height: 245px !important;
        max-height: 245px !important;
      }
    }

    @media (max-width: 767px) {
      body.tax-product_cat .site-main .woocommerce {
        max-width: 100% !important;
        padding-left: 10px !important;
        padding-right: 10px !important;
      }

      body.tax-product_cat .woocommerce-result-count,
      body.tax-product_cat .woocommerce-ordering {
        float: none !important;
        width: 100% !important;
        min-height: 0 !important;
        justify-content: center !important;
        margin: 0 0 12px !important;
      }

      body.tax-product_cat .woocommerce-result-count {
        padding-top: 14px !important;
      }

      body.tax-product_cat .woocommerce ul.products {
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        gap: 24px 12px !important;
        padding-top: 18px !important;
      }

      body.tax-product_cat .woocommerce ul.products li.product figure a.ct-media-container {
        height: 235px !important;
        min-height: 235px !important;
        max-height: 235px !important;
      }

      body.tax-product_cat .woocommerce ul.products li.product a img,
      body.tax-product_cat .woocommerce ul.products li.product img {
        padding: 10px !important;
      }

      body.tax-product_cat .woocommerce ul.products li.product .woocommerce-loop-product__title {
        min-height: 48px !important;
        font-size: 15px !important;
      }
    }
    </style>
    <?php
}, 10240);
/* PRIME_DROP_TAX_CATEGORIES_MATCH_BOLSOS_END */
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
    session.headers.update({"User-Agent": "PrimeDropTaxCategoriesMatchBolsos/1.0"})
    login(session)

    editor_url = urljoin(BASE, "/wp-admin/theme-editor.php?file=functions.php&theme=blocksy")
    page = session.get(editor_url, timeout=30)
    page.raise_for_status()

    textarea = re.search(r'<textarea[^>]+name=["\']newcontent["\'][^>]*>(.*?)</textarea>', page.text, re.S)
    if not textarea:
        raise RuntimeError("Could not find functions.php editor textarea")

    current = html.unescape(textarea.group(1))
    Path("wp-backups").mkdir(exist_ok=True)
    backup = Path("wp-backups") / f"functions_before_tax_categories_match_bolsos_{datetime.now():%Y%m%d_%H%M%S}.php"
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
