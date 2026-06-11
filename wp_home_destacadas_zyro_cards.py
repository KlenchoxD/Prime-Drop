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

MARKER_START = "/* PRIME_DROP_HOME_DESTACADAS_ZYRO_CARDS_START */"
MARKER_END = "/* PRIME_DROP_HOME_DESTACADAS_ZYRO_CARDS_END */"

BLOCK = r"""
/* PRIME_DROP_HOME_DESTACADAS_ZYRO_CARDS_START */
add_action('wp_footer', function() {
    ?>
    <style id="prime-drop-home-destacadas-zyro-cards-css">
    /* HOME: DESTACADAS igual al bloque de productos de la pagina anterior */
    body.page-id-14 .pd-products-title,
    body.home .pd-products-title {
      margin: 0 0 42px !important;
      text-align: center !important;
      font-family: 'Roboto Serif', Georgia, serif !important;
      font-size: clamp(34px, 4.2vw, 54px) !important;
      line-height: 1.1 !important;
      font-weight: 800 !important;
      letter-spacing: 0 !important;
      color: #000000 !important;
      text-transform: uppercase !important;
    }

    body.page-id-14 .elementor-element-741b26a .elementor-shortcode,
    body.home .elementor-element-741b26a .elementor-shortcode {
      width: 100% !important;
    }

    body.page-id-14 .elementor-element-741b26a .woocommerce,
    body.home .elementor-element-741b26a .woocommerce {
      width: min(1224px, calc(100vw - 64px)) !important;
      max-width: 1224px !important;
      margin: 0 auto !important;
      padding: 0 !important;
    }

    body.page-id-14 .elementor-element-741b26a .woocommerce ul.products,
    body.home .elementor-element-741b26a .woocommerce ul.products {
      display: grid !important;
      grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
      gap: 24px !important;
      align-items: start !important;
      justify-content: center !important;
      width: 100% !important;
      max-width: 1224px !important;
      margin: 0 auto !important;
      padding: 0 !important;
      overflow: visible !important;
      scroll-snap-type: none !important;
      transform: none !important;
    }

    body.page-id-14 .elementor-element-741b26a .woocommerce ul.products li.product,
    body.home .elementor-element-741b26a .woocommerce ul.products li.product {
      width: 100% !important;
      max-width: none !important;
      min-width: 0 !important;
      flex: none !important;
      float: none !important;
      margin: 0 !important;
      padding: 0 !important;
      display: flex !important;
      flex-direction: column !important;
      align-items: stretch !important;
      justify-content: flex-start !important;
      background: #ffffff !important;
      border: none !important;
      border-radius: 0 !important;
      box-shadow: none !important;
      overflow: visible !important;
      text-align: center !important;
    }

    body.page-id-14 .elementor-element-741b26a .woocommerce ul.products li.product:nth-child(n+4),
    body.home .elementor-element-741b26a .woocommerce ul.products li.product:nth-child(n+4) {
      display: none !important;
    }

    body.page-id-14 .elementor-element-741b26a .woocommerce ul.products li.product figure,
    body.home .elementor-element-741b26a .woocommerce ul.products li.product figure {
      width: 100% !important;
      margin: 0 !important;
      padding: 0 !important;
      display: block !important;
      background: #f5f5f5 !important;
      border: none !important;
      border-radius: 0 !important;
      overflow: hidden !important;
    }

    body.page-id-14 .elementor-element-741b26a .woocommerce ul.products li.product figure > a,
    body.page-id-14 .elementor-element-741b26a .woocommerce ul.products li.product .ct-media-container,
    body.home .elementor-element-741b26a .woocommerce ul.products li.product figure > a,
    body.home .elementor-element-741b26a .woocommerce ul.products li.product .ct-media-container {
      width: 100% !important;
      aspect-ratio: 4 / 5 !important;
      min-height: 0 !important;
      height: auto !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      background: #f5f5f5 !important;
      border: none !important;
      border-radius: 0 !important;
      overflow: hidden !important;
      text-decoration: none !important;
    }

    body.page-id-14 .elementor-element-741b26a .woocommerce ul.products li.product img,
    body.home .elementor-element-741b26a .woocommerce ul.products li.product img {
      width: 100% !important;
      height: 100% !important;
      max-width: 100% !important;
      max-height: 100% !important;
      min-height: 0 !important;
      aspect-ratio: auto !important;
      object-fit: contain !important;
      object-position: center center !important;
      display: block !important;
      margin: 0 !important;
      padding: 0 !important;
      background: transparent !important;
      border: none !important;
      border-radius: 0 !important;
      box-shadow: none !important;
      transform: none !important;
    }

    body.page-id-14 .elementor-element-741b26a .woocommerce ul.products li.product:hover img,
    body.home .elementor-element-741b26a .woocommerce ul.products li.product:hover img {
      transform: none !important;
    }

    body.page-id-14 .elementor-element-741b26a .woocommerce-loop-product__title,
    body.home .elementor-element-741b26a .woocommerce-loop-product__title {
      min-height: 0 !important;
      height: auto !important;
      max-width: 92% !important;
      margin: 22px auto 8px !important;
      padding: 0 !important;
      color: #000000 !important;
      text-align: center !important;
      font-family: 'Roboto Serif', Georgia, serif !important;
      font-size: clamp(18px, 1.55vw, 23px) !important;
      font-weight: 800 !important;
      line-height: 1.15 !important;
      letter-spacing: 0 !important;
      text-transform: none !important;
      overflow: visible !important;
      display: block !important;
      -webkit-line-clamp: unset !important;
      -webkit-box-orient: initial !important;
    }

    body.page-id-14 .elementor-element-741b26a .woocommerce-loop-product__title a,
    body.home .elementor-element-741b26a .woocommerce-loop-product__title a {
      color: #000000 !important;
      text-decoration: none !important;
      font-family: 'Roboto Serif', Georgia, serif !important;
    }

    body.page-id-14 .elementor-element-741b26a .price,
    body.home .elementor-element-741b26a .price {
      display: block !important;
      min-height: 0 !important;
      height: auto !important;
      margin: 0 auto !important;
      padding: 0 !important;
      color: #000000 !important;
      text-align: center !important;
      font-family: 'Roboto Serif', Georgia, serif !important;
      font-size: 13px !important;
      font-weight: 400 !important;
      line-height: 1.35 !important;
      letter-spacing: 0 !important;
    }

    body.page-id-14 .elementor-element-741b26a .entry-meta,
    body.page-id-14 .elementor-element-741b26a [class*="brand"],
    body.home .elementor-element-741b26a .entry-meta,
    body.home .elementor-element-741b26a [class*="brand"] {
      display: none !important;
    }

    body.page-id-14 .elementor-element-741b26a .ct-woo-card-actions,
    body.home .elementor-element-741b26a .ct-woo-card-actions {
      display: flex !important;
      justify-content: center !important;
      align-items: center !important;
      opacity: 1 !important;
      visibility: visible !important;
      height: auto !important;
      min-height: 0 !important;
      margin: 16px auto 0 !important;
      padding: 0 !important;
      overflow: visible !important;
      position: static !important;
      transform: none !important;
    }

    body.page-id-14 .elementor-element-741b26a .button,
    body.page-id-14 .elementor-element-741b26a a.button,
    body.home .elementor-element-741b26a .button,
    body.home .elementor-element-741b26a a.button {
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      visibility: visible !important;
      opacity: 1 !important;
      width: auto !important;
      min-width: 180px !important;
      max-width: calc(100% - 28px) !important;
      min-height: 42px !important;
      height: auto !important;
      margin: 0 auto !important;
      padding: 11px 24px !important;
      overflow: visible !important;
      border: 1px solid #0d141a !important;
      border-radius: 28px !important;
      background: #0d141a !important;
      color: #ffffff !important;
      font-family: 'Roboto Serif', Georgia, serif !important;
      font-size: 12px !important;
      font-weight: 700 !important;
      line-height: 1.1 !important;
      letter-spacing: .4px !important;
      text-transform: uppercase !important;
      text-decoration: none !important;
      box-shadow: none !important;
      position: static !important;
      transform: none !important;
    }

    @media (max-width: 900px) {
      body.page-id-14 .elementor-element-741b26a .woocommerce,
      body.home .elementor-element-741b26a .woocommerce {
        width: min(100%, calc(100vw - 28px)) !important;
      }

      body.page-id-14 .elementor-element-741b26a .woocommerce ul.products,
      body.home .elementor-element-741b26a .woocommerce ul.products {
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        gap: 18px !important;
      }
    }

    @media (max-width: 480px) {
      body.page-id-14 .elementor-element-741b26a .woocommerce ul.products,
      body.home .elementor-element-741b26a .woocommerce ul.products {
        grid-template-columns: 1fr !important;
      }
    }
    </style>
    <?php
}, 99999);

add_action('wp_footer', function() {
    ?>
    <script id="prime-drop-home-destacadas-title-js">
    (function() {
      var title = document.querySelector('body.page-id-14 .pd-products-title, body.home .pd-products-title');
      if (title) {
        title.textContent = 'DESTACADAS';
      }
      function cleanFeaturedCards() {
        document.querySelectorAll(
          'body.page-id-14 .elementor-element-741b26a ul.products li.product:nth-child(n+4), ' +
          'body.home .elementor-element-741b26a ul.products li.product:nth-child(n+4)'
        ).forEach(function(el) {
          el.style.setProperty('display', 'none', 'important');
        });
        document.querySelectorAll(
          'body.page-id-14 .elementor-element-741b26a .ct-woo-card-actions, ' +
          'body.page-id-14 .elementor-element-741b26a a.button, ' +
          'body.home .elementor-element-741b26a .ct-woo-card-actions, ' +
          'body.home .elementor-element-741b26a a.button'
        ).forEach(function(el) {
          el.style.removeProperty('display');
          el.style.removeProperty('visibility');
          el.style.removeProperty('height');
          el.style.removeProperty('min-height');
          el.style.removeProperty('margin');
          el.style.removeProperty('padding');
          el.style.removeProperty('overflow');
        });
      }
      cleanFeaturedCards();
      setTimeout(cleanFeaturedCards, 500);
      setTimeout(cleanFeaturedCards, 1600);
    })();
    </script>
    <?php
}, 99999);
/* PRIME_DROP_HOME_DESTACADAS_ZYRO_CARDS_END */
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
    pattern = r"name=[\"']" + re.escape(name) + r"[\"']"
    for tag in re.findall(r"<input[^>]+>", text, re.I):
        if not re.search(pattern, tag, re.I):
            continue
        match = re.search(r"value=[\"']([^\"']*)", tag, re.I)
        return html.unescape(match.group(1)) if match else ""
    return ""


def purge_cache(session):
    dashboard = session.get(urljoin(BASE, "/wp-admin/"), timeout=30)
    dashboard.raise_for_status()
    purged = False
    for href in re.findall(r"href=[\"']([^\"']+)[\"']", dashboard.text):
        raw = html.unescape(href)
        if "litespeed" in raw.lower() and "purge" in raw.lower():
            session.get(urljoin(BASE, raw), timeout=25)
            purged = True
            break
    return purged


def main():
    session = requests.Session()
    session.trust_env = False
    session.headers.update({"User-Agent": "PrimeDropHomeDestacadasZyroCards/1.0"})
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
    backup = Path("wp-backups") / f"functions_before_home_destacadas_zyro_cards_{datetime.now():%Y%m%d_%H%M%S}.php"
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
