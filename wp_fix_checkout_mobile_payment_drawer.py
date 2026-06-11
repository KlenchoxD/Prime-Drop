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

MARKER_START = "/* PRIME_DROP_CHECKOUT_MOBILE_PAYMENT_DRAWER_START */"
MARKER_END = "/* PRIME_DROP_CHECKOUT_MOBILE_PAYMENT_DRAWER_END */"

BLOCK = r"""
/* PRIME_DROP_CHECKOUT_MOBILE_PAYMENT_DRAWER_START */
add_action('wp_footer', function() {
    if (!is_checkout()) {
        return;
    }
    ?>
    <style id="prime-drop-checkout-mobile-payment-drawer">
    /* Checkout: titulo realmente centrado */
    body.woocommerce-checkout .entry-header,
    body.woocommerce-checkout header.entry-header,
    body.woocommerce-checkout .hero-section,
    body.woocommerce-checkout .page-title-wrapper {
      width: 100% !important;
      max-width: 1180px !important;
      margin-left: auto !important;
      margin-right: auto !important;
      padding-left: 24px !important;
      padding-right: 24px !important;
      box-sizing: border-box !important;
      display: flex !important;
      justify-content: center !important;
      align-items: center !important;
      text-align: center !important;
    }

    body.woocommerce-checkout .entry-title,
    body.woocommerce-checkout .page-title,
    body.woocommerce-checkout h1 {
      width: 100vw !important;
      max-width: 100vw !important;
      margin-left: calc(50% - 50vw) !important;
      margin-right: calc(50% - 50vw) !important;
      text-align: center !important;
      box-sizing: border-box !important;
    }

    /* Checkout: caja de pago no se desborda */
    body.woocommerce-checkout #order_review,
    body.woocommerce-checkout #payment,
    body.woocommerce-checkout #payment ul.payment_methods {
      width: 100% !important;
      max-width: 100% !important;
      box-sizing: border-box !important;
      overflow-x: hidden !important;
    }

    body.woocommerce-checkout #payment {
      position: relative !important;
    }

    /* Titulo visible de metodos de pago */
    body.woocommerce-checkout #payment::before {
      content: none !important;
      display: none !important;
    }

    body.woocommerce-checkout #payment .pd-payment-title {
      display: block !important;
      margin: 0 0 14px !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      font-size: 16px !important;
      font-weight: 700 !important;
      letter-spacing: 0.8px !important;
      text-transform: none !important;
      line-height: 1.3 !important;
      padding: 0 0 0 28px !important;
      text-align: left !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods {
      border: 1px solid #eeeeee !important;
      border-radius: 12px !important;
      background: #ffffff !important;
      padding: 0 !important;
      margin: 0 0 22px !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method {
      width: 100% !important;
      max-width: 100% !important;
      box-sizing: border-box !important;
      margin: 0 !important;
      padding: 0 !important;
      overflow: hidden !important;
      background: #ffffff !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      border-bottom: 1px solid #f2f2f2 !important;
      position: relative !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method:last-child {
      border-bottom: 0 !important;
    }

    /* Ocultar por completo el radio nativo del metodo de pago */
    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > input.input-radio,
    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > input[name="payment_method"] {
      position: absolute !important;
      width: 0 !important;
      height: 0 !important;
      min-width: 0 !important;
      opacity: 0 !important;
      overflow: hidden !important;
      clip: rect(0 0 0 0) !important;
      clip-path: inset(50%) !important;
      pointer-events: none !important;
      margin: 0 !important;
      padding: 0 !important;
      border: 0 !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > label {
      width: 100% !important;
      max-width: 100% !important;
      min-height: 58px !important;
      box-sizing: border-box !important;
      display: flex !important;
      align-items: center !important;
      gap: 10px !important;
      padding: 15px 16px 15px 52px !important;
      margin: 0 !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
      background: transparent !important;
      opacity: 1 !important;
      cursor: pointer !important;
      position: relative !important;
      line-height: 1.35 !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > label::before {
      content: "" !important;
      position: absolute !important;
      left: 18px !important;
      top: 50% !important;
      transform: translateY(-50%) !important;
      width: 18px !important;
      height: 18px !important;
      border: 1.5px solid #d7d7d7 !important;
      border-radius: 50% !important;
      background: #ffffff !important;
      box-sizing: border-box !important;
      flex: 0 0 auto !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > input.input-radio:checked + label::before,
    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > input[name="payment_method"]:checked + label::before {
      border-color: #000000 !important;
      background: radial-gradient(circle at center, #ffffff 0 3px, #000000 3.4px 100%) !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > input.input-radio:checked + label,
    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > input[name="payment_method"]:checked + label {
      font-weight: 700 !important;
    }

    body.woocommerce-checkout #payment .payment_box,
    body.woocommerce-checkout #payment .payment_box *,
    body.woocommerce-checkout #payment [class*="mercado"],
    body.woocommerce-checkout #payment [class*="Mercado"],
    body.woocommerce-checkout #payment [class*="wompi"],
    body.woocommerce-checkout #payment [class*="Wompi"] {
      max-width: 100% !important;
      box-sizing: border-box !important;
      overflow-wrap: anywhere !important;
    }

    body.woocommerce-checkout #payment .payment_box {
      margin: 0 !important;
      padding: 18px !important;
      border-top: 1px solid #f2f2f2 !important;
      background: #ffffff !important;
      overflow-x: hidden !important;
    }

    /* Checkboxes/radios generales de checkout: circulares y visibles */
    body.woocommerce-checkout input[type="checkbox"].input-checkbox,
    body.woocommerce-checkout input[type="checkbox"].woocommerce-form__input-checkbox,
    body.woocommerce-checkout input[type="radio"]:not([name="payment_method"]) {
      appearance: none !important;
      -webkit-appearance: none !important;
      width: 18px !important;
      height: 18px !important;
      min-width: 18px !important;
      border: 1.5px solid #d7d7d7 !important;
      border-radius: 50% !important;
      background: #ffffff !important;
      box-shadow: none !important;
      vertical-align: middle !important;
      margin-right: 10px !important;
      display: inline-block !important;
      box-sizing: border-box !important;
    }

    body.woocommerce-checkout input[type="checkbox"].input-checkbox:checked,
    body.woocommerce-checkout input[type="checkbox"].woocommerce-form__input-checkbox:checked,
    body.woocommerce-checkout input[type="radio"]:not([name="payment_method"]):checked {
      border-color: #000000 !important;
      background: radial-gradient(circle at center, #ffffff 0 3px, #000000 3.4px 100%) !important;
    }

    body.woocommerce-checkout .woocommerce-info,
    body.woocommerce-checkout .woocommerce-form-login-toggle {
      max-width: 100% !important;
      box-sizing: border-box !important;
      color: #000000 !important;
      -webkit-text-fill-color: #000000 !important;
    }

    @media (max-width: 1024px) {
      body.woocommerce-checkout .entry-header,
      body.woocommerce-checkout header.entry-header {
        max-width: 760px !important;
        padding-left: 22px !important;
        padding-right: 22px !important;
      }

      body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > label {
        min-height: 56px !important;
        padding-left: 50px !important;
        padding-right: 14px !important;
      }

      body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > label::before {
        left: 17px !important;
      }
    }
    </style>
    <script id="prime-drop-checkout-drawer-tablet-fix">
    (function() {
      var lastScroll = window.scrollY || 0;

      function ensurePaymentTitle() {
        var payment = document.querySelector('#payment');
        if (!payment) {
          return;
        }

        var methods = payment.querySelector('ul.payment_methods');
        if (!methods || payment.querySelector('.pd-payment-title')) {
          return;
        }

        var title = document.createElement('h3');
        title.className = 'pd-payment-title';
        title.textContent = 'Metodos de pago:';
        payment.insertBefore(title, methods);
      }

      function unlockBody(restore) {
        var top = document.body.style.top;
        var lockedY = 0;
        if (top && top.indexOf('-') === 0) {
          lockedY = Math.abs(parseInt(top, 10)) || 0;
        }

        document.documentElement.style.overflow = '';
        document.body.style.overflow = '';
        document.body.style.position = '';
        document.body.style.top = '';
        document.body.style.left = '';
        document.body.style.right = '';
        document.body.style.width = '';

        if (restore) {
          window.scrollTo(0, lockedY || lastScroll || window.scrollY || 0);
        }
      }

      function closeDrawer(restoreScroll) {
        document.querySelectorAll('#cart-drawer, .cart-drawer, .pd-cart-drawer, [id*="cart-drawer"], [class*="cart-drawer"]').forEach(function(el) {
          el.classList.remove('active', 'open', 'show', 'is-open', 'ct-open');
          el.setAttribute('aria-hidden', 'true');
        });

        document.querySelectorAll('#cart-drawer-overlay, .cart-drawer-overlay, .pd-cart-overlay, .pd-cart-drawer-overlay, [class*="cart-overlay"]').forEach(function(el) {
          el.classList.remove('active', 'open', 'show', 'is-open', 'ct-open');
        });

        unlockBody(!!restoreScroll);
      }

      function isCheckout() {
        return document.body.classList.contains('woocommerce-checkout') || /\/checkout\/?/.test(window.location.pathname);
      }

      window.addEventListener('scroll', function() {
        if (!document.body.style.position || document.body.style.position !== 'fixed') {
          lastScroll = window.scrollY || lastScroll;
        }
      }, { passive: true });

      document.addEventListener('click', function(event) {
        var checkoutLink = event.target.closest('a[href*="checkout"], a[href*="/checkout/"]');
        if (checkoutLink) {
          sessionStorage.setItem('pd_force_close_cart_checkout', '1');
          closeDrawer(false);
          setTimeout(function() { closeDrawer(false); }, 80);
          setTimeout(function() { closeDrawer(false); }, 450);
          return;
        }

        var closeClick = event.target.closest('.pd-cart-drawer-close, .cart-drawer-close, #cart-drawer-overlay, .cart-drawer-overlay, .pd-cart-overlay');
        if (closeClick) {
          setTimeout(function() { closeDrawer(true); }, 80);
          setTimeout(function() { closeDrawer(true); }, 350);
        }
      }, true);

      function checkoutGuard() {
        ensurePaymentTitle();
        if (isCheckout() || sessionStorage.getItem('pd_force_close_cart_checkout') === '1') {
          closeDrawer(false);
          if (isCheckout()) {
            setTimeout(function() { sessionStorage.removeItem('pd_force_close_cart_checkout'); }, 1800);
          }
        }
      }

      document.addEventListener('DOMContentLoaded', checkoutGuard);
      window.addEventListener('pageshow', checkoutGuard);
      window.addEventListener('load', checkoutGuard);
      document.body && document.body.addEventListener('updated_checkout', ensurePaymentTitle);
      if (document.body && window.MutationObserver) {
        new MutationObserver(function() {
          ensurePaymentTitle();
        }).observe(document.body, { childList: true, subtree: true });
      }
      [0, 50, 100, 200, 300, 500, 700, 1200, 2200, 3600, 5200].forEach(function(delay) {
        setTimeout(checkoutGuard, delay);
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


def main():
    s = requests.Session()
    s.headers.update({"User-Agent": "PrimeDropCheckoutMobilePaymentDrawer/1.0"})
    login(s)

    editor_url = urljoin(BASE, "/wp-admin/theme-editor.php?file=functions.php&theme=blocksy")
    page = s.get(editor_url, timeout=30)
    page.raise_for_status()

    textarea = re.search(r'<textarea[^>]+name=["\']newcontent["\'][^>]*>(.*?)</textarea>', page.text, re.S)
    if not textarea:
        raise RuntimeError("Could not find functions.php editor textarea")

    current = html.unescape(textarea.group(1))
    Path("wp-backups").mkdir(exist_ok=True)
    backup = Path("wp-backups") / f"functions_before_checkout_mobile_payment_drawer_{datetime.now():%Y%m%d_%H%M%S}.php"
    backup.write_text(current, encoding="utf-8")

    pattern = re.compile(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), re.S)
    if pattern.search(current):
        updated = pattern.sub(BLOCK.strip(), current)
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
