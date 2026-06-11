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

MARKER_START = "/* PRIME_DROP_BOLSOS_IMAGES_COMPLETE_START */"
MARKER_END = "/* PRIME_DROP_BOLSOS_IMAGES_COMPLETE_END */"

BLOCK = r"""
/* PRIME_DROP_BOLSOS_IMAGES_COMPLETE_START */
add_action('wp_footer', function() {
    ?>
    <style id="prime-drop-bolsos-images-complete-css">
    /* /bolsos/: mostrar bolsos completos, sin recorte */
    body.page-id-547 .woocommerce ul.products li.product {
      overflow: visible !important;
      text-align: center !important;
    }

    body.page-id-547 .woocommerce ul.products li.product a.woocommerce-loop-product__link {
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      width: 100% !important;
      background: #ffffff !important;
      text-decoration: none !important;
    }

    body.page-id-547 .woocommerce ul.products li.product a img,
    body.page-id-547 .woocommerce ul.products li.product img,
    body.page-id-547 .woocommerce-page ul.products li.product a img,
    body.page-id-547 .woocommerce-page ul.products li.product img {
      width: 100% !important;
      height: 320px !important;
      min-height: 320px !important;
      max-height: 320px !important;
      aspect-ratio: auto !important;
      object-fit: contain !important;
      object-position: center center !important;
      background: #ffffff !important;
      border-radius: 8px !important;
      padding: 16px !important;
      box-sizing: border-box !important;
      display: block !important;
      transform: none !important;
      filter: none !important;
    }

    body.page-id-547 .woocommerce ul.products li.product figure {
      background: #ffffff !important;
      border-radius: 8px !important;
      overflow: visible !important;
    }

    @media (min-width: 768px) and (max-width: 1024px) {
      body.page-id-547 .woocommerce ul.products li.product a img,
      body.page-id-547 .woocommerce ul.products li.product img,
      body.page-id-547 .woocommerce-page ul.products li.product a img,
      body.page-id-547 .woocommerce-page ul.products li.product img {
        height: 285px !important;
        min-height: 285px !important;
        max-height: 285px !important;
        padding: 14px !important;
      }
    }

    @media (max-width: 767px) {
      body.page-id-547 .woocommerce ul.products li.product a img,
      body.page-id-547 .woocommerce ul.products li.product img,
      body.page-id-547 .woocommerce-page ul.products li.product a img,
      body.page-id-547 .woocommerce-page ul.products li.product img {
        height: 235px !important;
        min-height: 235px !important;
        max-height: 235px !important;
        padding: 12px !important;
      }
    }
    </style>
    <?php
}, 10060);
/* PRIME_DROP_BOLSOS_IMAGES_COMPLETE_END */
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
    session.headers.update({"User-Agent": "PrimeDropBolsosImagesComplete/1.0"})
    login(session)

    editor_url = urljoin(BASE, "/wp-admin/theme-editor.php?file=functions.php&theme=blocksy")
    page = session.get(editor_url, timeout=30)
    page.raise_for_status()

    textarea = re.search(r'<textarea[^>]+name=["\']newcontent["\'][^>]*>(.*?)</textarea>', page.text, re.S)
    if not textarea:
        raise RuntimeError("Could not find functions.php editor textarea")

    current = html.unescape(textarea.group(1))
    Path("wp-backups").mkdir(exist_ok=True)
    backup = Path("wp-backups") / f"functions_before_bolsos_images_complete_{datetime.now():%Y%m%d_%H%M%S}.php"
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
