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

MARKER_START = "/* PRIME_DROP_CENTER_ORDERBY_OPTIONS_START */"
MARKER_END = "/* PRIME_DROP_CENTER_ORDERBY_OPTIONS_END */"

BLOCK = r"""
/* PRIME_DROP_CENTER_ORDERBY_OPTIONS_START */
add_filter('woocommerce_catalog_orderby', function($options) {
    $labels = array(
        'menu_order' => 'ORDEN POR DEFECTO',
        'popularity' => 'POPULARIDAD',
        'rating' => 'CALIFICACIÓN',
        'date' => 'ÚLTIMAS',
        'price' => 'MENOR PRECIO',
        'price-desc' => 'MAYOR PRECIO',
    );

    foreach ($labels as $key => $label) {
        if (isset($options[$key])) {
            $options[$key] = $label;
        }
    }

    return $options;
}, 99);

add_filter('woocommerce_default_catalog_orderby_options', function($options) {
    $labels = array(
        'menu_order' => 'ORDEN POR DEFECTO',
        'popularity' => 'POPULARIDAD',
        'rating' => 'CALIFICACIÓN',
        'date' => 'ÚLTIMAS',
        'price' => 'MENOR PRECIO',
        'price-desc' => 'MAYOR PRECIO',
    );

    foreach ($labels as $key => $label) {
        if (isset($options[$key])) {
            $options[$key] = $label;
        }
    }

    return $options;
}, 99);

add_action('wp_footer', function() {
    ?>
    <style id="prime-drop-center-orderby-options-css">
    body.page-id-547 select.orderby,
    body.tax-product_cat select.orderby,
    body.woocommerce-shop select.orderby,
    body.post-type-archive-product select.orderby {
      appearance: none !important;
      -webkit-appearance: none !important;
      -moz-appearance: none !important;
      text-align: center !important;
      text-align-last: center !important;
      -moz-text-align-last: center !important;
      text-indent: 0 !important;
      padding-left: 44px !important;
      padding-right: 44px !important;
      background-image: none !important;
    }

    body.page-id-547 select.orderby::-ms-expand,
    body.tax-product_cat select.orderby::-ms-expand,
    body.woocommerce-shop select.orderby::-ms-expand,
    body.post-type-archive-product select.orderby::-ms-expand {
      display: none !important;
    }

    body.page-id-547 .woocommerce-ordering,
    body.tax-product_cat .woocommerce-ordering,
    body.woocommerce-shop .woocommerce-ordering,
    body.post-type-archive-product .woocommerce-ordering {
      position: relative !important;
    }

    body.page-id-547 .woocommerce-ordering::after,
    body.tax-product_cat .woocommerce-ordering::after,
    body.woocommerce-shop .woocommerce-ordering::after,
    body.post-type-archive-product .woocommerce-ordering::after {
      content: "" !important;
      position: absolute !important;
      top: 50% !important;
      right: 22px !important;
      width: 6px !important;
      height: 6px !important;
      border-right: 1.5px solid #ffffff !important;
      border-bottom: 1.5px solid #ffffff !important;
      transform: translateY(-65%) rotate(45deg) !important;
      pointer-events: none !important;
      z-index: 2 !important;
    }

    body.page-id-547 select.orderby option,
    body.tax-product_cat select.orderby option,
    body.woocommerce-shop select.orderby option,
    body.post-type-archive-product select.orderby option {
      text-align: center !important;
      text-align-last: center !important;
      -moz-text-align-last: center !important;
      padding-left: 0 !important;
      padding-right: 0 !important;
      text-indent: 0 !important;
      direction: ltr !important;
    }

    body.page-id-547 .woof_products_top_panel,
    body.page-id-547 .woof_products_top_panel_content,
    body.tax-product_cat .woof_products_top_panel,
    body.tax-product_cat .woof_products_top_panel_content,
    body.woocommerce-shop .woof_products_top_panel,
    body.woocommerce-shop .woof_products_top_panel_content,
    body.post-type-archive-product .woof_products_top_panel,
    body.post-type-archive-product .woof_products_top_panel_content {
      display: none !important;
      height: 0 !important;
      min-height: 0 !important;
      margin: 0 !important;
      padding: 0 !important;
      overflow: hidden !important;
    }
    </style>
    <script id="prime-drop-center-orderby-options-js">
    (function() {
      function centerOrderOptions() {
        document.querySelectorAll('select.orderby option').forEach(function(option) {
          option.style.textAlign = 'center';
          option.style.textAlignLast = 'center';
          option.style.paddingLeft = '0';
          option.style.paddingRight = '0';
          option.style.textIndent = '0';
          option.style.direction = 'ltr';
        });
      }

      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', centerOrderOptions);
      } else {
        centerOrderOptions();
      }

      window.addEventListener('pageshow', centerOrderOptions);
      window.addEventListener('load', centerOrderOptions);
    })();
    </script>
    <?php
}, 10300);
/* PRIME_DROP_CENTER_ORDERBY_OPTIONS_END */
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
    session.headers.update({"User-Agent": "PrimeDropCenterOrderbyOptions/1.0"})
    login(session)

    editor_url = urljoin(BASE, "/wp-admin/theme-editor.php?file=functions.php&theme=blocksy")
    page = session.get(editor_url, timeout=30)
    page.raise_for_status()

    textarea = re.search(r'<textarea[^>]+name=["\']newcontent["\'][^>]*>(.*?)</textarea>', page.text, re.S)
    if not textarea:
        raise RuntimeError("Could not find functions.php editor textarea")

    current = html.unescape(textarea.group(1))
    Path("wp-backups").mkdir(exist_ok=True)
    backup = Path("wp-backups") / f"functions_before_center_orderby_options_{datetime.now():%Y%m%d_%H%M%S}.php"
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
