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

MARKER_START = "/* PRIME_DROP_FEATURED_UNIFORM_SEARCH_FINAL_START */"
MARKER_END = "/* PRIME_DROP_FEATURED_UNIFORM_SEARCH_FINAL_END */"

BLOCK = r"""
/* PRIME_DROP_FEATURED_UNIFORM_SEARCH_FINAL_START */
add_action('wp_head', function() {
    ?>
    <style id="prime-drop-featured-uniform-search-final-css">
    /* Buscador uniforme en /bolsos y todas las categorias */
    body.page-id-547 .woo-listing-top,
    body.tax-product_cat .woo-listing-top,
    body.woocommerce-shop .woo-listing-top,
    body.post-type-archive-product .woo-listing-top {
      width: min(1180px, calc(100% - 56px)) !important;
      max-width: 1180px !important;
      margin: 0 auto 32px !important;
      padding: 18px 0 !important;
      display: grid !important;
      grid-template-columns: minmax(240px, 1fr) 360px minmax(240px, 1fr) !important;
      grid-template-areas: "count search order" !important;
      column-gap: 28px !important;
      row-gap: 14px !important;
      align-items: center !important;
      justify-items: stretch !important;
      border-top: 1px solid #eeeeee !important;
      border-bottom: 1px solid #eeeeee !important;
      box-sizing: border-box !important;
    }

    body.page-id-547 .woo-listing-top .woocommerce-result-count,
    body.tax-product_cat .woo-listing-top .woocommerce-result-count,
    body.woocommerce-shop .woo-listing-top .woocommerce-result-count,
    body.post-type-archive-product .woo-listing-top .woocommerce-result-count {
      grid-area: count !important;
      justify-self: start !important;
      align-self: center !important;
      margin: 0 !important;
      padding: 0 !important;
      width: auto !important;
      min-width: 0 !important;
      min-height: 0 !important;
      display: flex !important;
      align-items: center !important;
      justify-content: flex-start !important;
      float: none !important;
      white-space: nowrap !important;
    }

    body.page-id-547 .pd-shop-search,
    body.tax-product_cat .pd-shop-search,
    body.woocommerce-shop .pd-shop-search,
    body.post-type-archive-product .pd-shop-search {
      grid-area: search !important;
      justify-self: center !important;
      align-self: center !important;
      width: 360px !important;
      min-width: 360px !important;
      max-width: 360px !important;
      margin: 0 !important;
      padding: 0 !important;
      display: block !important;
      float: none !important;
      visibility: visible !important;
      opacity: 1 !important;
    }

    body.page-id-547 .pd-shop-search form,
    body.tax-product_cat .pd-shop-search form,
    body.woocommerce-shop .pd-shop-search form,
    body.post-type-archive-product .pd-shop-search form {
      width: 360px !important;
      height: 46px !important;
      display: flex !important;
      align-items: center !important;
      padding: 4px !important;
      background: #ffffff !important;
      border: 0 !important;
      border-radius: 999px !important;
      overflow: hidden !important;
      box-shadow: 0 12px 28px rgba(0,0,0,.08), inset 0 0 0 1px rgba(0,0,0,.08) !important;
      box-sizing: border-box !important;
    }

    body.page-id-547 .pd-shop-search input[type="search"],
    body.tax-product_cat .pd-shop-search input[type="search"],
    body.woocommerce-shop .pd-shop-search input[type="search"],
    body.post-type-archive-product .pd-shop-search input[type="search"] {
      flex: 1 1 auto !important;
      min-width: 0 !important;
      height: 38px !important;
      margin: 0 !important;
      padding: 0 14px 0 18px !important;
      border: 0 !important;
      outline: 0 !important;
      box-shadow: none !important;
      background: transparent !important;
      color: #111111 !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 13.5px !important;
      line-height: 38px !important;
    }

    body.page-id-547 .pd-shop-search button[type="submit"],
    body.tax-product_cat .pd-shop-search button[type="submit"],
    body.woocommerce-shop .pd-shop-search button[type="submit"],
    body.post-type-archive-product .pd-shop-search button[type="submit"] {
      flex: 0 0 38px !important;
      width: 38px !important;
      min-width: 38px !important;
      height: 38px !important;
      min-height: 38px !important;
      margin: 0 !important;
      padding: 0 !important;
      border: 0 !important;
      border-radius: 50% !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      background: #000000 !important;
      color: #ffffff !important;
      box-shadow: none !important;
    }

    body.page-id-547 .woo-listing-top .woocommerce-ordering,
    body.tax-product_cat .woo-listing-top .woocommerce-ordering,
    body.woocommerce-shop .woo-listing-top .woocommerce-ordering,
    body.post-type-archive-product .woo-listing-top .woocommerce-ordering {
      grid-area: order !important;
      justify-self: end !important;
      align-self: center !important;
      width: 240px !important;
      margin: 0 !important;
      padding: 0 !important;
      display: flex !important;
      align-items: center !important;
      float: none !important;
    }

    /* Destacadas: todas las imagenes con el mismo fondo blanco y caja */
    body.page-id-14 .woocommerce ul.products {
      align-items: stretch !important;
    }

    body.page-id-14 .woocommerce ul.products li.product {
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      justify-content: flex-start !important;
      text-align: center !important;
      background: transparent !important;
      box-shadow: none !important;
      border: 0 !important;
    }

    body.page-id-14 .woocommerce ul.products li.product figure,
    body.page-id-14 .woocommerce ul.products li.product figure > a.ct-media-container,
    body.page-id-14 .woocommerce ul.products li.product .ct-media-container {
      width: 100% !important;
      aspect-ratio: 4 / 5 !important;
      height: auto !important;
      min-height: 0 !important;
      max-height: none !important;
      margin: 0 0 16px !important;
      padding: 0 !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      background: #ffffff !important;
      background-color: #ffffff !important;
      border: 0 !important;
      border-radius: 0 !important;
      box-shadow: none !important;
      overflow: hidden !important;
      box-sizing: border-box !important;
    }

    body.page-id-14 .woocommerce ul.products li.product figure img,
    body.page-id-14 .woocommerce ul.products li.product a img,
    body.page-id-14 .woocommerce ul.products li.product img {
      width: 100% !important;
      height: 100% !important;
      min-height: 0 !important;
      max-height: none !important;
      aspect-ratio: auto !important;
      object-fit: contain !important;
      object-position: center center !important;
      margin: 0 !important;
      padding: 22px 16px 16px !important;
      background: transparent !important;
      background-color: transparent !important;
      border: 0 !important;
      box-shadow: none !important;
      display: block !important;
      box-sizing: border-box !important;
      transform: none !important;
      filter: none !important;
      mix-blend-mode: normal !important;
    }

    body.page-id-14 .woocommerce ul.products li.product .woocommerce-loop-product__title {
      min-height: 54px !important;
      display: flex !important;
      align-items: flex-start !important;
      justify-content: center !important;
      text-align: center !important;
    }

    body.page-id-14 .woocommerce ul.products li.product .price {
      min-height: 24px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      text-align: center !important;
      white-space: nowrap !important;
    }

    @media (max-width: 900px) {
      body.page-id-547 .woo-listing-top,
      body.tax-product_cat .woo-listing-top,
      body.woocommerce-shop .woo-listing-top,
      body.post-type-archive-product .woo-listing-top {
        width: min(100% - 28px, 560px) !important;
        grid-template-columns: 1fr !important;
        grid-template-areas:
          "search"
          "count"
          "order" !important;
        justify-items: center !important;
      }

      body.page-id-547 .pd-shop-search,
      body.tax-product_cat .pd-shop-search,
      body.woocommerce-shop .pd-shop-search,
      body.post-type-archive-product .pd-shop-search,
      body.page-id-547 .pd-shop-search form,
      body.tax-product_cat .pd-shop-search form,
      body.woocommerce-shop .pd-shop-search form,
      body.post-type-archive-product .pd-shop-search form {
        width: min(100%, 360px) !important;
        min-width: 0 !important;
        max-width: 360px !important;
      }

      body.page-id-547 .woo-listing-top .woocommerce-result-count,
      body.tax-product_cat .woo-listing-top .woocommerce-result-count,
      body.woocommerce-shop .woo-listing-top .woocommerce-result-count,
      body.post-type-archive-product .woo-listing-top .woocommerce-result-count,
      body.page-id-547 .woo-listing-top .woocommerce-ordering,
      body.tax-product_cat .woo-listing-top .woocommerce-ordering,
      body.woocommerce-shop .woo-listing-top .woocommerce-ordering,
      body.post-type-archive-product .woo-listing-top .woocommerce-ordering {
        justify-self: center !important;
      }
    }
    </style>
    <?php
}, 999);
/* PRIME_DROP_FEATURED_UNIFORM_SEARCH_FINAL_END */
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
    session.headers.update({"User-Agent": "PrimeDropFeaturedUniformSearchFinal/1.0"})
    login(session)

    editor_url = urljoin(BASE, "/wp-admin/theme-editor.php?file=functions.php&theme=blocksy")
    page = session.get(editor_url, timeout=30)
    page.raise_for_status()

    textarea = re.search(r'<textarea[^>]+name=["\']newcontent["\'][^>]*>(.*?)</textarea>', page.text, re.S)
    if not textarea:
        raise RuntimeError("Could not find functions.php editor textarea")

    current = html.unescape(textarea.group(1))
    Path("wp-backups").mkdir(exist_ok=True)
    backup = Path("wp-backups") / f"functions_before_featured_uniform_search_{datetime.now():%Y%m%d_%H%M%S}.php"
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
    if resp.status_code >= 400:
        raise RuntimeError(f"Update failed: {resp.status_code}")

    print(f"updated=true backup={backup} purged={purge_cache(session)}")


if __name__ == "__main__":
    main()
