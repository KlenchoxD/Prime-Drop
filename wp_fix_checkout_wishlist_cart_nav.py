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

MARKER_START = "/* PRIME_DROP_CHECKOUT_WISHLIST_CART_NAV_START */"
MARKER_END = "/* PRIME_DROP_CHECKOUT_WISHLIST_CART_NAV_END */"

BLOCK = r"""
/* PRIME_DROP_CHECKOUT_WISHLIST_CART_NAV_START */
add_filter('default_checkout_billing_country', function() {
    return 'CO';
});

add_filter('default_checkout_shipping_country', function() {
    return 'CO';
});

add_filter('woocommerce_checkout_fields', function($fields) {
    foreach (['billing', 'shipping'] as $section) {
        if (isset($fields[$section][$section . '_country'])) {
            $fields[$section][$section . '_country']['default'] = 'CO';
            $fields[$section][$section . '_country']['priority'] = 40;
            $fields[$section][$section . '_country']['class'] = ['form-row-wide', 'pd-country-hidden'];
        }

        if (isset($fields[$section][$section . '_state'])) {
            $fields[$section][$section . '_state']['label'] = 'Departamento';
            $fields[$section][$section . '_state']['priority'] = 55;
            $fields[$section][$section . '_state']['class'] = ['form-row-wide'];
        }

        if (isset($fields[$section][$section . '_city'])) {
            $fields[$section][$section . '_city']['label'] = 'Localidad / Ciudad';
            $fields[$section][$section . '_city']['priority'] = 60;
            $fields[$section][$section . '_city']['class'] = ['form-row-wide'];
        }

        if (isset($fields[$section][$section . '_address_1'])) {
            $fields[$section][$section . '_address_1']['priority'] = 65;
        }

        if (isset($fields[$section][$section . '_address_2'])) {
            $fields[$section][$section . '_address_2']['priority'] = 70;
        }
    }

    return $fields;
}, 30);

add_filter('woocommerce_default_address_fields', function($fields) {
    if (isset($fields['state'])) {
        $fields['state']['label'] = 'Departamento';
        $fields['state']['priority'] = 55;
    }

    if (isset($fields['city'])) {
        $fields['city']['label'] = 'Localidad / Ciudad';
        $fields['city']['priority'] = 60;
    }

    return $fields;
}, 40);

add_filter('woocommerce_get_country_locale', function($locale) {
    if (!isset($locale['CO'])) {
        $locale['CO'] = [];
    }

    $locale['CO']['state']['label'] = 'Departamento';
    $locale['CO']['state']['priority'] = 55;
    $locale['CO']['city']['label'] = 'Localidad / Ciudad';
    $locale['CO']['city']['priority'] = 60;

    return $locale;
}, 40);

add_filter('woocommerce_product_get_name', function($name) {
    return html_entity_decode($name, ENT_QUOTES | ENT_HTML5, 'UTF-8');
}, 20);

add_filter('the_title', function($title, $post_id = null) {
    if ($post_id && get_post_type($post_id) === 'product') {
        return html_entity_decode($title, ENT_QUOTES | ENT_HTML5, 'UTF-8');
    }

    return $title;
}, 20, 2);

function prime_drop_checkout_policy_text() {
    return 'Tus datos personales se utilizarán para procesar tu pedido, gestionar tu experiencia en esta tienda y otros fines descritos en nuestra <a href="' . esc_url(home_url('/politica-de-privacidad/')) . '">Política de Privacidad</a> y <a href="' . esc_url(home_url('/politica-de-reembolso/')) . '">Política de Reembolso</a>.';
}

add_filter('woocommerce_get_privacy_policy_text', function($text, $type = '') {
    if ($type === 'checkout') {
        return prime_drop_checkout_policy_text();
    }

    return $text;
}, 20, 2);

add_filter('woocommerce_checkout_privacy_policy_text', function() {
    return prime_drop_checkout_policy_text();
}, 20);

add_filter('woocommerce_ship_to_different_address_checked', '__return_false');

add_action('wp_head', function() {
    ?>
    <style id="prime-drop-head-bag-guard">
    header [data-id="cart"] svg:not(.pd-bag-icon),
    .ct-header-cart svg:not(.pd-bag-icon),
    header a[href*="cart"] svg:not(.pd-bag-icon),
    .ct-cart-item svg:not(.pd-bag-icon) {
      opacity: 0 !important;
      transition: none !important;
    }

    header [data-id="cart"] svg.pd-bag-icon,
    .ct-header-cart svg.pd-bag-icon,
    header a[href*="cart"] svg.pd-bag-icon,
    .ct-cart-item svg.pd-bag-icon {
      opacity: 1 !important;
    }
    </style>
    <script id="prime-drop-head-bag-guard-js">
    (function() {
      var bagSvg = '<svg class="ct-icon pd-bag-icon" aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.45" stroke-linecap="round" stroke-linejoin="round"><path d="M7 9V7a5 5 0 0 1 10 0v2"/><path d="M5.4 8.5h13.2l.9 11.2a2 2 0 0 1-2 2.1H6.5a2 2 0 0 1-2-2.1l.9-11.2Z"/></svg>';

      function replaceBagIconEarly() {
        document.querySelectorAll('header [data-id="cart"] svg, .ct-header-cart svg, header a[href*="cart"] svg, .ct-cart-item svg').forEach(function(svg) {
          if (svg.classList.contains('pd-bag-icon')) return;
          var holder = document.createElement('span');
          holder.innerHTML = bagSvg;
          svg.replaceWith(holder.firstChild);
        });
      }

      replaceBagIconEarly();
      document.addEventListener('DOMContentLoaded', replaceBagIconEarly);
      window.addEventListener('pageshow', replaceBagIconEarly);
      [25, 75, 150, 300, 600, 1200].forEach(function(delay) {
        setTimeout(replaceBagIconEarly, delay);
      });

      if (window.MutationObserver) {
        var rootObserver = new MutationObserver(function() {
          replaceBagIconEarly();
          var header = document.querySelector('header');
          if (header) {
            rootObserver.disconnect();
            new MutationObserver(replaceBagIconEarly).observe(header, { childList: true, subtree: true });
          }
        });
        rootObserver.observe(document.documentElement, { childList: true, subtree: true });
        setTimeout(function() {
          rootObserver.disconnect();
        }, 3500);
      }
    })();
    </script>
    <?php
}, 1);

add_action('woocommerce_thankyou', function($order_id) {
    if (!$order_id) {
        return;
    }

    $order = wc_get_order($order_id);
    if (!$order) {
        return;
    }

    $paid = $order->is_paid();
    ?>
    <div class="pd-thankyou-finish">
      <h2><?php echo esc_html($paid ? 'Pago realizado' : 'Pedido recibido'); ?></h2>
      <p><?php echo esc_html($paid ? 'Te enviamos el comprobante y los detalles de tu pedido al correo registrado.' : 'Cuando el pago sea confirmado, recibirás el comprobante en tu correo.'); ?></p>
      <a href="<?php echo esc_url(home_url('/bolsos/')); ?>">Finalizar</a>
    </div>
    <?php
}, 25);

add_action('wp_footer', function() {
    ?>
    <style id="prime-drop-checkout-wishlist-cart-nav">
    /* Checkout: campos, selectores y selects */
    body.woocommerce-checkout .pd-country-hidden {
      display: none !important;
    }

    body.woocommerce-checkout .select2-search,
    body.woocommerce-checkout .select2-search--dropdown {
      display: none !important;
    }

    body.woocommerce-checkout .select2-container,
    body.woocommerce-checkout .select2-selection,
    body.woocommerce-checkout select,
    body.woocommerce-checkout input,
    body.woocommerce-checkout textarea {
      border-radius: 25px !important;
      box-sizing: border-box !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method {
      overflow: visible !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > label {
      padding-left: 62px !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > label::before {
      left: 24px !important;
      width: 18px !important;
      height: 18px !important;
      border-color: #cfcfcf !important;
      background: #ffffff !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > input.input-radio:checked + label::before,
    body.woocommerce-checkout #payment ul.payment_methods li.wc_payment_method > input[name="payment_method"]:checked + label::before {
      border-color: #000000 !important;
      background: radial-gradient(circle at center, #ffffff 0 2.4px, #000000 2.8px 100%) !important;
    }

    body.woocommerce-checkout input[type="checkbox"].input-checkbox:checked,
    body.woocommerce-checkout input[type="checkbox"].woocommerce-form__input-checkbox:checked {
      background-color: #000000 !important;
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 6 9 17l-5-5'/%3E%3C/svg%3E") !important;
      background-repeat: no-repeat !important;
      background-position: center !important;
      background-size: 12px 12px !important;
      border-color: #000000 !important;
    }

    body.woocommerce-checkout .woocommerce-form-login-toggle .woocommerce-info {
      align-items: center !important;
      border: 1px solid #eeeeee !important;
      border-radius: 14px !important;
      background: #fafafa !important;
      padding: 18px 22px !important;
      gap: 12px !important;
    }

    body.woocommerce-checkout .woocommerce-privacy-policy-text {
      margin-top: 22px !important;
      color: #111111 !important;
      -webkit-text-fill-color: #111111 !important;
      font-size: 14px !important;
      line-height: 1.55 !important;
    }

    body.woocommerce-checkout .woocommerce-privacy-policy-text a {
      color: #000000 !important;
      font-weight: 800 !important;
      text-decoration: underline !important;
      text-underline-offset: 3px !important;
    }

    body.woocommerce-checkout label[for="createaccount"],
    body.woocommerce-checkout label[for="ship-to-different-address-checkbox"] {
      line-height: 1.4 !important;
      color: #111111 !important;
      -webkit-text-fill-color: #111111 !important;
    }

    @media (max-width: 1024px) {
      body.woocommerce-checkout .select2-container {
        display: none !important;
      }

      body.woocommerce-checkout select.select2-hidden-accessible {
        position: static !important;
        width: 100% !important;
        height: auto !important;
        opacity: 1 !important;
        clip: auto !important;
        clip-path: none !important;
        pointer-events: auto !important;
        display: block !important;
      }
    }

    /* Wishlist limpio */
    body.pd-wishlist-page .entry-header,
    body.pd-wishlist-page .page-title,
    body.pd-wishlist-page h1.entry-title,
    body.pd-wishlist-page .ct-breadcrumbs {
      display: none !important;
    }

    body.pd-wishlist-page .site-main,
    body.pd-wishlist-page main {
      padding-top: 48px !important;
    }

    .pd-wishlist-empty-clean {
      max-width: 880px !important;
      margin: 30px auto 90px !important;
      padding: 56px 28px !important;
      border: 1px solid #eeeeee !important;
      border-radius: 18px !important;
      background: #ffffff !important;
      box-shadow: 0 18px 55px rgba(0,0,0,0.06) !important;
      text-align: center !important;
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      gap: 18px !important;
    }

    .pd-wishlist-empty-clean .pd-wishlist-icon {
      width: 56px !important;
      height: 56px !important;
      border: 1px solid #e5e5e5 !important;
      border-radius: 50% !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      font-size: 24px !important;
      line-height: 1 !important;
    }

    .pd-wishlist-empty-clean h2 {
      margin: 0 !important;
      font-family: 'Roboto Serif', Georgia, serif !important;
      font-size: clamp(28px, 4vw, 44px) !important;
      line-height: 1.1 !important;
      color: #000000 !important;
    }

    .pd-wishlist-empty-clean p {
      max-width: 520px !important;
      margin: 0 !important;
      font-size: 16px !important;
      line-height: 1.6 !important;
      color: #333333 !important;
    }

    .pd-wishlist-empty-clean a {
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      min-width: 150px !important;
      min-height: 44px !important;
      padding: 12px 28px !important;
      border-radius: 25px !important;
      background: #000000 !important;
      color: #ffffff !important;
      text-decoration: none !important;
      font-size: 12px !important;
      font-weight: 800 !important;
      letter-spacing: 1.5px !important;
      text-transform: uppercase !important;
    }

    /* Pagina carrito */
    body.woocommerce-cart .entry-header,
    body.woocommerce-cart .page-title,
    body.woocommerce-cart h1.entry-title {
      text-align: center !important;
    }

    body.woocommerce-cart .woocommerce {
      max-width: 1180px !important;
      margin: 0 auto !important;
      padding: 36px 24px 80px !important;
      box-sizing: border-box !important;
    }

    body.woocommerce-cart table.shop_table {
      border: 1px solid #eeeeee !important;
      border-radius: 16px !important;
      overflow: hidden !important;
      background: #ffffff !important;
      box-shadow: 0 16px 45px rgba(0,0,0,0.05) !important;
    }

    body.woocommerce-cart table.shop_table th,
    body.woocommerce-cart table.shop_table td {
      padding: 18px !important;
      border-color: #eeeeee !important;
      vertical-align: middle !important;
    }

    body.woocommerce-cart table.shop_table img {
      width: 92px !important;
      height: 92px !important;
      object-fit: contain !important;
      background: #ffffff !important;
      border-radius: 12px !important;
    }

    body.woocommerce-cart .cart_totals {
      border: 1px solid #eeeeee !important;
      border-radius: 16px !important;
      padding: 24px !important;
      background: #ffffff !important;
      box-shadow: 0 16px 45px rgba(0,0,0,0.05) !important;
    }

    body.woocommerce-cart .cart_totals h2 {
      margin-top: 0 !important;
      font-size: 24px !important;
    }

    body.woocommerce-cart .wc-proceed-to-checkout a.checkout-button,
    body.woocommerce-cart .return-to-shop a.button,
    body.woocommerce-cart button.button,
    body.woocommerce-cart a.button {
      border-radius: 25px !important;
      background: #000000 !important;
      color: #ffffff !important;
      border: none !important;
      text-transform: uppercase !important;
      letter-spacing: 1.4px !important;
    }

    body.woocommerce-cart .cart-empty {
      max-width: 720px !important;
      margin: 40px auto 18px !important;
      padding: 44px 24px !important;
      border: 1px solid #eeeeee !important;
      border-radius: 18px !important;
      text-align: center !important;
      box-shadow: 0 16px 45px rgba(0,0,0,0.05) !important;
      background: #ffffff !important;
    }

    .pd-thankyou-finish {
      max-width: 760px !important;
      margin: 32px auto !important;
      padding: 34px 28px !important;
      border: 1px solid #eeeeee !important;
      border-radius: 18px !important;
      text-align: center !important;
      background: #ffffff !important;
      box-shadow: 0 16px 45px rgba(0,0,0,0.05) !important;
    }

    .pd-thankyou-finish h2 {
      margin: 0 0 10px !important;
      font-size: 34px !important;
    }

    .pd-thankyou-finish a {
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      margin-top: 18px !important;
      padding: 13px 34px !important;
      border-radius: 25px !important;
      background: #000000 !important;
      color: #ffffff !important;
      text-decoration: none !important;
      text-transform: uppercase !important;
      letter-spacing: 1.5px !important;
      font-size: 12px !important;
      font-weight: 800 !important;
    }
    </style>

    <script id="prime-drop-checkout-wishlist-cart-nav-js">
    (function() {
      var bagSvg = '<svg class="ct-icon pd-bag-icon" aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.45" stroke-linecap="round" stroke-linejoin="round"><path d="M7 9V7a5 5 0 0 1 10 0v2"/><path d="M5.4 8.5h13.2l.9 11.2a2 2 0 0 1-2 2.1H6.5a2 2 0 0 1-2-2.1l.9-11.2Z"/></svg>';

      function replaceBagIcon() {
        document.querySelectorAll('header [data-id="cart"] svg, .ct-header-cart svg, header a[href*="cart"] svg, .ct-cart-item svg').forEach(function(svg) {
          if (svg.classList.contains('pd-bag-icon')) return;
          var holder = document.createElement('span');
          holder.innerHTML = bagSvg;
          svg.replaceWith(holder.firstChild);
        });
      }

      function fixBolsosClick() {
        document.querySelectorAll('header a, .ct-header a, .site-header a').forEach(function(a) {
          if ((a.textContent || '').trim().toUpperCase() !== 'BOLSOS') return;
          if (a.dataset.pdBolsosFixed === '1') return;
          a.dataset.pdBolsosFixed = '1';
          a.setAttribute('href', '/bolsos/');
          a.addEventListener('click', function(event) {
            event.preventDefault();
            event.stopImmediatePropagation();
            window.location.href = '/bolsos/';
          }, true);
        });
      }

      function fixCheckoutLabels() {
        function setLabel(label, input, text) {
          if (!label) return;
          var inputInside = input && label.contains(input) ? input : null;
          label.textContent = '';
          if (inputInside) {
            label.appendChild(inputInside);
            label.appendChild(document.createTextNode(' '));
          }
          label.appendChild(document.createTextNode(text + ' '));
          var optional = document.createElement('span');
          optional.className = 'pd-optional';
          optional.textContent = '(opcional)';
          label.appendChild(optional);
        }

        var accountInput = document.querySelector('#createaccount, input[name="createaccount"]');
        var account = document.querySelector('label[for="createaccount"]') || accountInput?.closest('label') || accountInput?.parentElement?.querySelector('label');
        setLabel(account, accountInput, 'Crear cuenta para guardar tus pedidos');

        var shipInput = document.querySelector('#ship-to-different-address-checkbox, input[name="ship_to_different_address"]');
        var ship = document.querySelector('label[for="ship-to-different-address-checkbox"]') || shipInput?.closest('label') || shipInput?.parentElement?.querySelector('label');
        setLabel(ship, shipInput, 'Enviar a otra direccion');

        [['billing_state_field', 'billing_city_field'], ['shipping_state_field', 'shipping_city_field']].forEach(function(pair) {
          var state = document.getElementById(pair[0]);
          var city = document.getElementById(pair[1]);
          if (state && city && state.compareDocumentPosition(city) & Node.DOCUMENT_POSITION_PRECEDING) {
            city.parentNode.insertBefore(state, city);
          }
        });

        if (window.innerWidth <= 1024 && window.jQuery) {
          jQuery('#billing_state, #shipping_state, #billing_country, #shipping_country').each(function() {
            var $el = jQuery(this);
            try {
              if ($el.data('select2')) $el.select2('destroy');
              if ($el.data('selectWoo')) $el.selectWoo('destroy');
            } catch (e) {}
            $el.removeClass('select2-hidden-accessible').show();
            $el.next('.select2-container').remove();
          });
        }
      }

      function cleanWishlist() {
        if (!/\/wishlist\/?/.test(window.location.pathname)) return;
        document.body.classList.add('pd-wishlist-page');

        document.querySelectorAll('h1,h2,h3').forEach(function(h) {
          var text = (h.textContent || '').trim().toLowerCase();
          if (text === 'lista de deseos' || text === 'mi lista de deseos') {
            h.style.display = 'none';
          }
        });

        var existing = document.querySelector('.pd-wishlist-empty-clean');
        if (existing) return;

        var target = document.querySelector('.woocommerce') || document.querySelector('.yith-wcwl-form') || document.querySelector('main');
        if (!target) return;

        var text = target.textContent || '';
        if (!/vac[ií]a|no se ha añadido|no products/i.test(text)) return;

        target.innerHTML = '<div class="pd-wishlist-empty-clean"><div class="pd-wishlist-icon">♡</div><h2>Tu lista de deseos esta vacia</h2><p>Guarda aqui tus bolsos favoritos para encontrarlos rapido cuando quieras comprarlos.</p><a href="/bolsos/">VER BOLSOS</a></div>';
      }

      function runAll() {
        replaceBagIcon();
        fixBolsosClick();
        fixCheckoutLabels();
        cleanWishlist();
      }

      document.addEventListener('DOMContentLoaded', runAll);
      window.addEventListener('pageshow', runAll);
      window.addEventListener('load', runAll);
      [100, 300, 700, 1400, 2600].forEach(function(delay) {
        setTimeout(runAll, delay);
      });

      if (document.body && window.MutationObserver) {
        var header = document.querySelector('header');
        if (header) {
          new MutationObserver(function() {
            replaceBagIcon();
            fixBolsosClick();
          }).observe(header, { childList: true, subtree: true });
        }
      }
    })();
    </script>
    <?php
}, 10006);
/* PRIME_DROP_CHECKOUT_WISHLIST_CART_NAV_END */
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
    s.headers.update({"User-Agent": "PrimeDropCheckoutWishlistCartNav/1.0"})
    login(s)

    editor_url = urljoin(BASE, "/wp-admin/theme-editor.php?file=functions.php&theme=blocksy")
    page = s.get(editor_url, timeout=30)
    page.raise_for_status()

    textarea = re.search(r'<textarea[^>]+name=["\']newcontent["\'][^>]*>(.*?)</textarea>', page.text, re.S)
    if not textarea:
        raise RuntimeError("Could not find functions.php editor textarea")

    current = html.unescape(textarea.group(1))
    Path("wp-backups").mkdir(exist_ok=True)
    backup = Path("wp-backups") / f"functions_before_checkout_wishlist_cart_nav_{datetime.now():%Y%m%d_%H%M%S}.php"
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
