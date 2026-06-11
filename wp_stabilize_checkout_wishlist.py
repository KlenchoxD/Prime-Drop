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

CHECKOUT_START = "/* PRIME_DROP_CHECKOUT_MOBILE_PAYMENT_DRAWER_START */"
CHECKOUT_END = "/* PRIME_DROP_CHECKOUT_MOBILE_PAYMENT_DRAWER_END */"

NAV_START = "/* PRIME_DROP_CHECKOUT_WISHLIST_CART_NAV_START */"
NAV_END = "/* PRIME_DROP_CHECKOUT_WISHLIST_CART_NAV_END */"

CHECKOUT_BLOCK = r"""
/* PRIME_DROP_CHECKOUT_MOBILE_PAYMENT_DRAWER_START */
add_action('wp_footer', function() {
    if (!is_checkout()) {
        return;
    }
    ?>
    <style id="prime-drop-checkout-stable">
    body.woocommerce-checkout .entry-header,
    body.woocommerce-checkout header.entry-header {
      width: 100% !important;
      max-width: 1180px !important;
      margin: 0 auto !important;
      padding: 34px 24px 20px !important;
      text-align: center !important;
      box-sizing: border-box !important;
    }

    body.woocommerce-checkout .entry-title,
    body.woocommerce-checkout .page-title,
    body.woocommerce-checkout h1 {
      width: 100% !important;
      max-width: 100% !important;
      margin: 0 auto !important;
      text-align: center !important;
    }

    body.woocommerce-checkout .woocommerce-form-login-toggle .woocommerce-info {
      display: flex !important;
      align-items: center !important;
      justify-content: space-between !important;
      gap: 18px !important;
      border: 1px solid #eeeeee !important;
      border-radius: 14px !important;
      background: #fafafa !important;
      padding: 16px 22px !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      line-height: 1.35 !important;
    }

    body.woocommerce-checkout .woocommerce-form-login-toggle .woocommerce-info::before,
    body.woocommerce-checkout .woocommerce-info::before {
      display: none !important;
      content: none !important;
    }

    body.woocommerce-checkout .woocommerce-form-login-toggle .woocommerce-info a {
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      text-decoration: underline !important;
      text-underline-offset: 3px !important;
      white-space: nowrap !important;
    }

    body.woocommerce-checkout #payment,
    body.woocommerce-checkout #payment ul.payment_methods {
      width: 100% !important;
      max-width: 100% !important;
      box-sizing: border-box !important;
      overflow-x: hidden !important;
    }

    body.woocommerce-checkout #payment .pd-payment-title {
      display: block !important;
      margin: 0 0 14px !important;
      padding: 0 !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      font-size: 16px !important;
      font-weight: 800 !important;
      line-height: 1.3 !important;
      text-align: left !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods {
      border: 1px solid #eeeeee !important;
      border-radius: 14px !important;
      background: #ffffff !important;
      padding: 0 !important;
      margin: 0 0 22px !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method {
      width: 100% !important;
      max-width: 100% !important;
      margin: 0 !important;
      padding: 0 !important;
      overflow: visible !important;
      background: #ffffff !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      border-bottom: 1px solid #f0f0f0 !important;
      box-sizing: border-box !important;
      position: relative !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > input.input-radio,
    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > input[name="payment_method"] {
      position: absolute !important;
      width: 0 !important;
      height: 0 !important;
      opacity: 0 !important;
      pointer-events: none !important;
      clip: rect(0 0 0 0) !important;
      clip-path: inset(50%) !important;
      margin: 0 !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > label {
      display: flex !important;
      align-items: center !important;
      width: 100% !important;
      min-height: 58px !important;
      margin: 0 !important;
      padding: 15px 16px 15px 58px !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      background: #ffffff !important;
      line-height: 1.35 !important;
      box-sizing: border-box !important;
      position: relative !important;
      cursor: pointer !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > label::before {
      content: "" !important;
      position: absolute !important;
      left: 22px !important;
      top: 50% !important;
      transform: translateY(-50%) !important;
      width: 18px !important;
      height: 18px !important;
      border: 1.5px solid #d1d1d1 !important;
      border-radius: 50% !important;
      background: #ffffff !important;
      box-sizing: border-box !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > input:checked + label::before {
      border-color: #000000 !important;
      background: radial-gradient(circle at center, #ffffff 0 2.5px, #000000 3px 100%) !important;
    }

    body.woocommerce-checkout #payment .payment_box {
      margin: 0 !important;
      padding: 18px !important;
      border-top: 1px solid #f2f2f2 !important;
      background: #ffffff !important;
      overflow-x: hidden !important;
      box-sizing: border-box !important;
    }
    </style>
    <script id="prime-drop-checkout-stable-js">
    (function() {
      function ensurePaymentTitle() {
        var payment = document.querySelector('#payment');
        if (!payment) return;
        var methods = payment.querySelector('ul.payment_methods');
        if (!methods || payment.querySelector('.pd-payment-title')) return;
        var title = document.createElement('h3');
        title.className = 'pd-payment-title';
        title.textContent = 'Metodos de pago:';
        payment.insertBefore(title, methods);
      }

      function closeCheckoutDrawerOnce() {
        if (!document.body.classList.contains('woocommerce-checkout')) return;
        document.querySelectorAll('#cart-drawer, .cart-drawer, .pd-cart-drawer').forEach(function(el) {
          el.classList.remove('active', 'open', 'show', 'is-open', 'ct-open');
          el.setAttribute('aria-hidden', 'true');
        });
        document.querySelectorAll('#cart-drawer-overlay, .cart-drawer-overlay, .pd-cart-overlay, .pd-cart-drawer-overlay').forEach(function(el) {
          el.classList.remove('active', 'open', 'show', 'is-open', 'ct-open');
        });
        document.documentElement.style.overflow = '';
        document.body.style.overflow = '';
        document.body.style.position = '';
        document.body.style.top = '';
        document.body.style.left = '';
        document.body.style.right = '';
        document.body.style.width = '';
      }

      document.addEventListener('DOMContentLoaded', function() {
        ensurePaymentTitle();
        closeCheckoutDrawerOnce();
      });
      window.addEventListener('pageshow', function() {
        ensurePaymentTitle();
        closeCheckoutDrawerOnce();
      });
      document.body && document.body.addEventListener('updated_checkout', ensurePaymentTitle);
      [150, 700, 1600].forEach(function(delay) {
        setTimeout(function() {
          ensurePaymentTitle();
          closeCheckoutDrawerOnce();
        }, delay);
      });
    })();
    </script>
    <?php
}, 10003);
/* PRIME_DROP_CHECKOUT_MOBILE_PAYMENT_DRAWER_END */
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


def replace_block(text, start_marker, end_marker, block):
    pattern = re.compile(re.escape(start_marker) + r".*?" + re.escape(end_marker), re.S)
    if not pattern.search(text):
        return text.rstrip() + "\n\n" + block.strip() + "\n"
    return pattern.sub(block.strip(), text)


def main():
    s = requests.Session()
    s.headers.update({"User-Agent": "PrimeDropStabilizeCheckoutWishlist/1.0"})
    login(s)

    editor_url = urljoin(BASE, "/wp-admin/theme-editor.php?file=functions.php&theme=blocksy")
    page = s.get(editor_url, timeout=30)
    page.raise_for_status()

    textarea = re.search(r'<textarea[^>]+name=["\']newcontent["\'][^>]*>(.*?)</textarea>', page.text, re.S)
    if not textarea:
        raise RuntimeError("Could not find functions.php editor textarea")

    current = html.unescape(textarea.group(1))
    Path("wp-backups").mkdir(exist_ok=True)
    backup = Path("wp-backups") / f"functions_before_stabilize_checkout_wishlist_{datetime.now():%Y%m%d_%H%M%S}.php"
    backup.write_text(current, encoding="utf-8")

    updated = replace_block(current, CHECKOUT_START, CHECKOUT_END, CHECKOUT_BLOCK)

    # Remove the aggressive wishlist replacement JS from the newer nav block.
    updated = updated.replace("        cleanWishlist();\n", "")
    updated = re.sub(
        r"\n\s*function cleanWishlist\(\) \{.*?\n\s*\}\n\n\s*function runAll\(\) \{",
        "\n      function runAll() {",
        updated,
        flags=re.S,
    )

    # Keep only header-scoped observers in the newer nav block.
    updated = updated.replace(
        "        var rootObserver = new MutationObserver(function() {\n          replaceBagIconEarly();\n          var header = document.querySelector('header');\n          if (header) {\n            rootObserver.disconnect();\n            new MutationObserver(replaceBagIconEarly).observe(header, { childList: true, subtree: true });\n          }\n        });\n        rootObserver.observe(document.documentElement, { childList: true, subtree: true });\n        setTimeout(function() {\n          rootObserver.disconnect();\n        }, 3500);",
        "        var header = document.querySelector('header');\n        if (header) {\n          new MutationObserver(replaceBagIconEarly).observe(header, { childList: true, subtree: true });\n        }"
    )

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
