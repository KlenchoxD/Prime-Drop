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

MARKER_START = "/* PRIME_DROP_FONT_IMAGES_LOGIN_TRANSLATIONS_START */"
MARKER_END = "/* PRIME_DROP_FONT_IMAGES_LOGIN_TRANSLATIONS_END */"

BLOCK = r"""
/* PRIME_DROP_FONT_IMAGES_LOGIN_TRANSLATIONS_START */
function primedrop_roboto_serif() {
    wp_enqueue_style(
        'roboto-serif',
        'https://fonts.googleapis.com/css2?family=Roboto+Serif:ital,opsz,wght@0,8..144,100..900;1,8..144,100..900&display=swap',
        array(),
        null
    );
}
add_action('wp_enqueue_scripts', 'primedrop_roboto_serif', 5);

add_filter('gettext', function($translated, $text, $domain) {
    $strings = array(
        'A link to set a new password will be sent to your email address.' => 'Te enviaremos un enlace para crear tu contraseña.',
        'Your personal data will be used to support your experience throughout this website, to manage access to your account, and for other purposes described in our' => 'Tus datos personales se usarán para gestionar tu cuenta y otros propósitos descritos en nuestra',
        'Your personal data will be used to support your experience throughout this website, to manage access to your account, and for other purposes described in our %s.' => 'Tus datos personales se usarán para gestionar tu cuenta y otros propósitos descritos en nuestra %s.',
        'privacy policy' => 'política de privacidad',
        'Privacy policy' => 'Política de privacidad',
        'Lost your password?' => '¿Olvidaste tu contraseña?',
        'Remember me' => 'Recuérdame',
        'Log in' => 'Acceder',
        'Register' => 'Registrarse',
        'Username or email address' => 'Correo electrónico o usuario',
        'Username or email address *' => 'Correo electrónico o usuario *',
        'Email' => 'Correo electrónico',
        'Password' => 'Contraseña',
        'Shipment' => 'Envío',
        'Shipping' => 'Envío',
        'Cart' => 'Bolsa',
        'Add to cart' => 'Añadir a la bolsa',
        'View cart' => 'Ver bolsa',
        'Proceed to checkout' => 'Finalizar compra',
        'Place order' => 'Realizar pedido',
        'Billing details' => 'Datos de facturación',
        'Your order' => 'Tu pedido',
        'Order total' => 'Total del pedido',
        'Payment method' => 'Método de pago',
        'First name' => 'Nombre',
        'Last name' => 'Apellido',
        'Company name' => 'Empresa (opcional)',
        'Country / Region' => 'País / Región',
        'Street address' => 'Dirección',
        'Apartment, suite, unit, etc.' => 'Apartamento, suite, etc. (opcional)',
        'Town / City' => 'Ciudad',
        'State / County' => 'Departamento',
        'Phone' => 'Teléfono',
        'Email address' => 'Correo electrónico',
        'Order notes' => 'Notas del pedido',
        'Notes about your order' => 'Notas sobre tu pedido',
    );

    return isset($strings[$text]) ? $strings[$text] : $translated;
}, 40, 3);

add_filter('woocommerce_get_privacy_policy_text', function($text, $type) {
    if ($type !== 'registration') {
        return $text;
    }

    $text = str_replace(
        'Your personal data will be used to support your experience throughout this website, to manage access to your account, and for other purposes described in our',
        'Tus datos personales se usarán para gestionar tu cuenta y otros propósitos descritos en nuestra',
        $text
    );

    return $text;
}, 40, 2);

add_action('wp_head', function() {
    ?>
    <style id="prime-drop-font-images-login-translations-css">
    *,
    *::before,
    *::after {
      font-family: 'Roboto Serif', Georgia, serif !important;
    }

    .woocommerce ul.products li.product figure,
    .woocommerce ul.products li.product figure > a.ct-media-container,
    .woocommerce ul.products li.product .ct-media-container {
      aspect-ratio: 4 / 5 !important;
      background: #f8f8f8 !important;
      border-radius: 12px !important;
      overflow: hidden !important;
    }

    .woocommerce ul.products li.product img,
    .woocommerce .products img {
      width: 100% !important;
      height: 100% !important;
      aspect-ratio: 4 / 5 !important;
      object-fit: contain !important;
      object-position: center center !important;
      background: #f8f8f8 !important;
      padding: 12px !important;
      border-radius: 12px !important;
      box-sizing: border-box !important;
      mix-blend-mode: normal !important;
    }

    .ct-login-form input,
    .ct-register-form input,
    #account-modal input[type="email"],
    #account-modal input[type="text"],
    #account-modal input[type="password"] {
      background: #ffffff !important;
      border: 1px solid #dddddd !important;
      border-radius: 25px !important;
      color: #000000 !important;
      font-family: 'Roboto Serif', Georgia, serif !important;
      box-shadow: none !important;
    }

    #account-modal,
    #account-modal *,
    .woocommerce-cart,
    .woocommerce-cart *,
    .woocommerce-checkout,
    .woocommerce-checkout * {
      font-family: 'Roboto Serif', Georgia, serif !important;
    }

    #account-modal .woocommerce-privacy-policy-text {
      margin: 14px 0 0 !important;
      color: #555555 !important;
      font-size: 12px !important;
      line-height: 1.55 !important;
    }

    #account-modal form.register {
      display: flex !important;
      flex-direction: column !important;
    }

    #account-modal form.register p:has(.ct-account-register-submit) {
      order: 90 !important;
    }

    #account-modal form.register .woocommerce-privacy-policy-text {
      order: 100 !important;
    }

    #account-modal form.register > input[type="hidden"],
    #account-modal form.register > wc-order-attribution-inputs {
      order: 110 !important;
    }
    </style>
    <?php
}, 2000);

add_action('wp_footer', function() {
    ?>
    <script id="prime-drop-account-privacy-order-js">
    (function() {
      function movePrivacyBelowRegister() {
        var modal = document.querySelector('#account-modal');
        if (!modal) return;

        modal.querySelectorAll('form.register, form.woocommerce-form-register').forEach(function(form) {
          var privacy = form.querySelector('.woocommerce-privacy-policy-text');
          var submit = form.querySelector('.ct-account-register-submit, button[type="submit"], input[type="submit"], .ct-button[type="submit"]');
          if (!privacy || !submit) return;

          var submitRow = submit.closest('p, .form-row') || submit;
          if (submitRow.nextElementSibling !== privacy) {
            submitRow.insertAdjacentElement('afterend', privacy);
          }
        });
      }

      document.addEventListener('DOMContentLoaded', movePrivacyBelowRegister);
      document.addEventListener('click', function() {
        setTimeout(movePrivacyBelowRegister, 80);
      });
      window.addEventListener('pageshow', movePrivacyBelowRegister);
      setTimeout(movePrivacyBelowRegister, 300);
    })();
    </script>
    <?php
}, 300);
/* PRIME_DROP_FONT_IMAGES_LOGIN_TRANSLATIONS_END */
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
    for href in re.findall(r"href=[\"']([^\"']+)[\"']", dashboard.text):
        raw = html.unescape(href)
        if "litespeed" in raw.lower() and "purge" in raw.lower():
            session.get(urljoin(BASE, raw), timeout=25)
            return True
    return False


def main():
    session = requests.Session()
    session.trust_env = False
    session.headers.update({"User-Agent": "PrimeDropFontImagesLoginTranslations/1.0"})
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
    backup = Path("wp-backups") / f"functions_before_font_images_login_translations_{datetime.now():%Y%m%d_%H%M%S}.php"
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
