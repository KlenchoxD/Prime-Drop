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

MARKER_START = "/* PRIME_DROP_FINAL_PRODUCT_CHECKOUT_BUTTON_FIX_START */"
MARKER_END = "/* PRIME_DROP_FINAL_PRODUCT_CHECKOUT_BUTTON_FIX_END */"

BLOCK = r"""
/* PRIME_DROP_FINAL_PRODUCT_CHECKOUT_BUTTON_FIX_START */
add_action('wp_footer', function() {
    ?>
    <style id="prime-drop-final-product-checkout-button-fix">
    /* Producto: quitar enlace Ver carrito despues de anadir */
    .single-product a.added_to_cart,
    .single-product a.added_to_cart.wc-forward,
    .woocommerce a.added_to_cart,
    .woocommerce a.added_to_cart.wc-forward {
      display: none !important;
      visibility: hidden !important;
      opacity: 0 !important;
      width: 0 !important;
      height: 0 !important;
      margin: 0 !important;
      padding: 0 !important;
      overflow: hidden !important;
    }

    /* Producto: cantidad + boton alineados sin desbordarse */
    .single-product form.cart,
    .single-product .summary form.cart {
      display: flex !important;
      align-items: center !important;
      gap: 12px !important;
      flex-wrap: nowrap !important;
      width: 100% !important;
      max-width: 100% !important;
      box-sizing: border-box !important;
      overflow: visible !important;
    }

    .single-product form.cart .quantity {
      flex: 0 0 112px !important;
      width: 112px !important;
      min-width: 112px !important;
      margin: 0 !important;
    }

    .single-product form.cart .single_add_to_cart_button,
    .single-product form.cart button.single_add_to_cart_button {
      flex: 0 1 auto !important;
      width: auto !important;
      min-width: 205px !important;
      max-width: calc(100% - 124px) !important;
      margin: 0 !important;
      padding: 14px 28px !important;
      border-radius: 25px !important;
      box-sizing: border-box !important;
      white-space: nowrap !important;
      overflow: visible !important;
      text-overflow: clip !important;
      line-height: 1.2 !important;
      text-align: center !important;
    }

    @media (max-width: 520px) {
      .single-product form.cart,
      .single-product .summary form.cart {
        gap: 8px !important;
      }

      .single-product form.cart .quantity {
        flex-basis: 104px !important;
        width: 104px !important;
        min-width: 104px !important;
      }

      .single-product form.cart .single_add_to_cart_button,
      .single-product form.cart button.single_add_to_cart_button {
        flex: 1 1 auto !important;
        min-width: 0 !important;
        max-width: none !important;
        padding: 13px 16px !important;
        font-size: 11px !important;
        letter-spacing: 1.1px !important;
      }
    }

    /* Checkout: titulo centrado contra la pantalla */
    body.woocommerce-checkout .entry-header,
    body.woocommerce-checkout header.entry-header,
    body.woocommerce-checkout .page-title-wrapper {
      width: 100% !important;
      max-width: none !important;
      margin: 0 !important;
      padding: 34px 0 20px !important;
      box-sizing: border-box !important;
      text-align: center !important;
      display: block !important;
    }

    body.woocommerce-checkout .entry-title,
    body.woocommerce-checkout .page-title,
    body.woocommerce-checkout h1 {
      position: relative !important;
      left: 50vw !important;
      transform: translateX(-50%) !important;
      width: 100vw !important;
      max-width: 100vw !important;
      margin: 0 !important;
      padding: 0 18px !important;
      box-sizing: border-box !important;
      text-align: center !important;
      display: block !important;
    }
    </style>
    <?php
}, 10020);
/* PRIME_DROP_FINAL_PRODUCT_CHECKOUT_BUTTON_FIX_END */
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
    s.headers.update({"User-Agent": "PrimeDropFinalProductCheckoutButtonFix/1.0"})
    login(s)

    editor_url = urljoin(BASE, "/wp-admin/theme-editor.php?file=functions.php&theme=blocksy")
    page = s.get(editor_url, timeout=30)
    page.raise_for_status()

    textarea = re.search(r'<textarea[^>]+name=["\']newcontent["\'][^>]*>(.*?)</textarea>', page.text, re.S)
    if not textarea:
        raise RuntimeError("Could not find functions.php editor textarea")

    current = html.unescape(textarea.group(1))
    Path("wp-backups").mkdir(exist_ok=True)
    backup = Path("wp-backups") / f"functions_before_final_product_checkout_button_fix_{datetime.now():%Y%m%d_%H%M%S}.php"
    backup.write_text(current, encoding="utf-8")

    pattern = re.compile(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), re.S)
    if pattern.search(current):
        updated = pattern.sub(lambda _: BLOCK.strip(), current)
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
