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

for key in [
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "ALL_PROXY",
    "http_proxy",
    "https_proxy",
    "all_proxy",
]:
    os.environ.pop(key, None)

MARKER_START = "/* PRIME_DROP_FOOTER_CARDS_PRICE_FINAL_START */"
MARKER_END = "/* PRIME_DROP_FOOTER_CARDS_PRICE_FINAL_END */"

BLOCK = r"""
/* PRIME_DROP_FOOTER_CARDS_PRICE_FINAL_START */
add_filter('woocommerce_currency_symbol', function($currency_symbol, $currency) {
    if ($currency === 'COP') {
        return '$';
    }

    return $currency_symbol;
}, 100, 2);

add_filter('woocommerce_price_num_decimals', function() {
    return 0;
}, 100);

add_filter('woocommerce_price_thousand_separator', function() {
    return '.';
}, 100);

add_filter('woocommerce_price_decimal_separator', function() {
    return ',';
}, 100);

add_filter('woocommerce_price_format', function() {
    return '%1$s%2$s';
}, 100);

add_action('init', function() {
    update_option('woocommerce_price_num_decimals', '0');
    update_option('woocommerce_price_thousand_sep', '.');
    update_option('woocommerce_price_decimal_sep', ',');
    update_option('woocommerce_currency_pos', 'left');
}, 30);

add_action('wp_head', function() {
    ?>
    <style id="prime-drop-footer-cards-price-final-css">
    /* Footer Gmail: blanco como los demas iconos */
    .pd-footer .pd-social-icons a img,
    .pd-footer .pd-social-icons a svg,
    footer .pd-social-icons a img,
    footer .pd-social-icons a svg {
      filter: brightness(0) invert(1) !important;
    }

    .pd-footer .pd-social-icons a,
    footer .pd-social-icons a {
      background: transparent !important;
      border: 1px solid rgba(255,255,255,0.4) !important;
    }

    /* Cards de producto - estilo Zyro */
    .woocommerce ul.products {
      display: grid !important;
      grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
      gap: 24px !important;
      align-items: start !important;
    }

    .home .pd-products-wrap .woocommerce ul.products,
    .home .woocommerce ul.products,
    body.page-id-14 .woocommerce ul.products {
      grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
    }

    .woocommerce ul.products li.product {
      background: #ffffff !important;
      border: none !important;
      border-radius: 0 !important;
      padding: 0 !important;
      overflow: hidden !important;
      box-shadow: none !important;
      min-height: 0 !important;
      height: auto !important;
      display: flex !important;
      flex-direction: column !important;
      align-items: stretch !important;
      text-align: center !important;
      contain: none !important;
      content-visibility: visible !important;
    }

    .woocommerce ul.products li.product figure,
    .woocommerce ul.products li.product figure > a.ct-media-container,
    .woocommerce ul.products li.product .ct-media-container {
      width: 100% !important;
      aspect-ratio: 3 / 4 !important;
      height: auto !important;
      min-height: 0 !important;
      max-height: none !important;
      margin: 0 !important;
      padding: 0 !important;
      background: #f5f5f5 !important;
      border: 0 !important;
      border-radius: 0 !important;
      overflow: hidden !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      box-shadow: none !important;
    }

    .woocommerce ul.products li.product img,
    .woocommerce .products img {
      aspect-ratio: 3 / 4 !important;
      object-fit: contain !important;
      object-position: center center !important;
      background: #f5f5f5 !important;
      padding: 0 !important;
      border-radius: 0 !important;
      width: 100% !important;
      height: 100% !important;
      min-height: 0 !important;
      max-height: none !important;
      display: block !important;
      box-sizing: border-box !important;
      mix-blend-mode: normal !important;
      transform: none !important;
      filter: none !important;
    }

    .woocommerce ul.products li.product .woocommerce-loop-product__title {
      font-size: 13px !important;
      line-height: 1.25 !important;
      text-transform: uppercase !important;
      letter-spacing: 0.5px !important;
      padding: 12px 8px 4px !important;
      margin: 0 !important;
      min-height: 0 !important;
      height: auto !important;
      text-align: center !important;
      display: block !important;
      overflow: visible !important;
      -webkit-line-clamp: unset !important;
      -webkit-box-orient: unset !important;
    }

    .woocommerce ul.products li.product .price {
      text-align: center !important;
      font-size: 14px !important;
      line-height: 1.3 !important;
      padding: 0 8px 8px !important;
      margin: 0 !important;
      min-height: 0 !important;
      height: auto !important;
      display: block !important;
      color: #000000 !important;
      font-weight: 700 !important;
      white-space: nowrap !important;
    }

    .woocommerce ul.products li.product .price .woocommerce-Price-amount::after,
    .woocommerce ul.products li.product .price::after {
      content: none !important;
      display: none !important;
    }

    .woocommerce ul.products li.product .posted_in,
    .woocommerce ul.products li.product [class*="posted_in"],
    .woocommerce ul.products li.product .product_meta,
    .woocommerce ul.products li.product ul.entry-meta,
    .woocommerce ul.products li.product .entry-meta,
    .woocommerce ul.products li.product .meta-categories {
      display: none !important;
    }

    .woocommerce ul.products li.product .ct-woo-card-actions {
      display: flex !important;
      justify-content: center !important;
      opacity: 1 !important;
      visibility: visible !important;
      transform: none !important;
      margin-top: 0 !important;
      position: static !important;
    }

    .woocommerce ul.products li.product .button,
    .woocommerce ul.products li.product a.button {
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      align-self: center !important;
      margin: 8px auto 0 !important;
      width: auto !important;
      min-width: 0 !important;
      max-width: calc(100% - 24px) !important;
      border-radius: 999px !important;
      white-space: nowrap !important;
    }

    @media (max-width: 768px) {
      .woocommerce ul.products,
      .home .pd-products-wrap .woocommerce ul.products,
      .home .woocommerce ul.products,
      body.page-id-14 .woocommerce ul.products {
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
      }
    }
    </style>
    <script id="prime-drop-price-cop-clean-final-js">
    (function() {
      function cleanPrices() {
        document.querySelectorAll('.woocommerce ul.products li.product .price').forEach(function(price) {
          var text = price.textContent.replace(/\s+/g, ' ').trim();
          if (!text) return;
          text = text.replace(/CO\$/gi, '$');
          text = text.replace(/\s*COP\s*$/i, '');
          text = text.replace(/(\$?\d[\d.]*)[,.]00\b/g, '$1');
          text = text.replace(/\$(\d{1,3})(\d{3})(?![\d.])/g, function(_, a, b) { return '$' + a + '.' + b; });
          text = text.replace(/\$(\d{1,3})(\d{3})(\d{3})(?![\d.])/g, function(_, a, b, c) { return '$' + a + '.' + b + '.' + c; });
          price.textContent = text;
        });
      }

      cleanPrices();
      document.addEventListener('DOMContentLoaded', cleanPrices);
      window.addEventListener('pageshow', cleanPrices);
      setTimeout(cleanPrices, 400);
    })();
    </script>
    <?php
}, 3000);
/* PRIME_DROP_FOOTER_CARDS_PRICE_FINAL_END */
"""


def login(session):
    session.get(urljoin(BASE, "/wp-login.php"), timeout=30).raise_for_status()
    response = session.post(
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
    response.raise_for_status()
    if "/wp-admin/" not in response.url:
        raise RuntimeError("Login did not reach wp-admin")


def hidden_value(text, name):
    name_pattern = r"name=[\"']" + re.escape(name) + r"[\"']"
    for tag in re.findall(r"<input[^>]+>", text, re.I):
        if not re.search(name_pattern, tag, re.I):
            continue
        match = re.search(r"value=[\"']([^\"']*)", tag, re.I)
        return html.unescape(match.group(1)) if match else ""
    return ""


def purge_cache(session):
    dashboard = session.get(urljoin(BASE, "/wp-admin/"), timeout=30)
    dashboard.raise_for_status()
    for href in re.findall(r"href=[\"']([^\"']+)[\"']", dashboard.text):
        raw = html.unescape(href)
        if "litespeed" in raw.lower() and "purge" in raw.lower():
            session.get(urljoin(BASE, raw), timeout=25)
            return True
    return False


def main():
    session = requests.Session()
    session.trust_env = False
    session.headers.update({"User-Agent": "PrimeDropFooterCardsPriceFinal/1.0"})
    login(session)

    editor_url = urljoin(BASE, "/wp-admin/theme-editor.php?file=functions.php&theme=blocksy")
    page = session.get(editor_url, timeout=30)
    page.raise_for_status()

    textarea = re.search(
        r"<textarea[^>]+name=[\"']newcontent[\"'][^>]*>(.*?)</textarea>",
        page.text,
        re.S,
    )
    if not textarea:
        raise RuntimeError("Could not find functions.php editor textarea")

    current = html.unescape(textarea.group(1))
    Path("wp-backups").mkdir(exist_ok=True)
    backup = Path("wp-backups") / f"functions_before_footer_cards_price_final_{datetime.now():%Y%m%d_%H%M%S}.php"
    backup.write_text(current, encoding="utf-8")

    pattern = re.compile(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), re.S)
    if pattern.search(current):
        updated = pattern.sub(lambda _: BLOCK.strip(), current)
    else:
        updated = current.rstrip() + "\n\n" + BLOCK.strip() + "\n"

    nonce = hidden_value(page.text, "_wpnonce") or hidden_value(page.text, "nonce")
    if not nonce:
        raise RuntimeError("Could not find theme editor nonce")

    response = session.post(
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
    if response.status_code >= 400:
        raise RuntimeError(f"Update failed: {response.status_code}")

    print(f"updated=true backup={backup} purged={purge_cache(session)}")


if __name__ == "__main__":
    main()
