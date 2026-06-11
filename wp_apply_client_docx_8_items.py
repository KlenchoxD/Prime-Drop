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

MARKER_START = "/* PRIME_DROP_CLIENT_DOCX_8_ITEMS_START */"
MARKER_END = "/* PRIME_DROP_CLIENT_DOCX_8_ITEMS_END */"

BLOCK = r"""
/* PRIME_DROP_CLIENT_DOCX_8_ITEMS_START */
add_action('wp_enqueue_scripts', function() {
    wp_enqueue_style(
        'roboto-serif-client-final',
        'https://fonts.googleapis.com/css2?family=Roboto+Serif:ital,opsz,wght@0,8..144,100..900;1,8..144,100..900&display=swap',
        array(),
        null
    );
}, 3);

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
        'Username or email address *' => 'Correo electrónico o usuario *',
        'Username or email address&nbsp;*' => 'Correo electrónico o usuario *',
        'Email' => 'Correo electrónico',
        'Password' => 'Contraseña',
        'Shipment' => 'Envío',
        'Shipping' => 'Envío',
        'Cart' => 'Bolsa',
        'Cart totals' => 'Total de la bolsa',
        'Shopping cart' => 'Bolsa de compra',
        'Add to cart' => 'Añadir a la bolsa',
        'View cart' => 'Ver bolsa',
        'Proceed to checkout' => 'Finalizar compra',
        'Place order' => 'Realizar pedido',
        'Billing details' => 'Datos de facturación',
        'Your order' => 'Tu pedido',
        'Order total' => 'Total del pedido',
        'Payment method' => 'Método de pago',
        'Payment methods' => 'Métodos de pago',
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
}, 100, 3);

add_filter('woocommerce_product_add_to_cart_text', function() {
    return 'AÑADIR A LA BOLSA';
}, 100);

add_filter('woocommerce_product_single_add_to_cart_text', function() {
    return 'AÑADIR A LA BOLSA';
}, 100);

add_filter('woocommerce_currency_symbol', function($currency_symbol, $currency) {
    return $currency === 'COP' ? '$' : $currency_symbol;
}, 100, 2);

add_filter('wc_price_args', function($args) {
    $args['decimals'] = 0;
    $args['thousand_separator'] = '.';
    $args['decimal_separator'] = ',';
    return $args;
}, 100);

add_filter('wc_price', function($return) {
    $return = str_replace(array(' COP', 'COP', 'CO$'), array('', '', '$'), $return);
    return $return;
}, 100, 1);

add_filter('woocommerce_get_price_html', function($price) {
    return str_replace(array(' COP', 'COP', 'CO$'), array('', '', '$'), $price);
}, 100, 1);

add_action('wp_body_open', function() {
    if (is_admin()) {
        return;
    }
    ?>
    <div id="pd-client-topbar" aria-label="Información Prime Drop">
      <a class="pd-client-topbar-email" href="mailto:primedropelite@gmail.com">primedropelite@gmail.com</a>
      <div class="pd-client-topbar-phrases" aria-live="polite">
        <span>BOLSOS 100% ORIGINALES.</span>
        <span>GARANTÍA DE AUTENTICIDAD.</span>
        <span>ENVÍOS A TODA COLOMBIA | RÁPIDO Y SEGURO</span>
      </div>
      <div class="pd-client-topbar-socials">
        <span>Síguenos:</span>
        <a href="https://www.facebook.com/primedropelite" target="_blank" rel="noopener" aria-label="Facebook">f</a>
        <a href="https://www.tiktok.com/@primedrop_elite" target="_blank" rel="noopener" aria-label="TikTok">♪</a>
        <a href="https://www.instagram.com/primedrop_elite/" target="_blank" rel="noopener" aria-label="Instagram">◎</a>
      </div>
    </div>
    <?php
}, 1);

add_action('woocommerce_single_product_summary', function() {
    global $product;
    if (!$product) {
        return;
    }

    $terms = get_the_terms($product->get_id(), 'product_cat');
    if (!$terms || is_wp_error($terms)) {
        return;
    }

    $brands = array();
    foreach ($terms as $term) {
        if (strtolower($term->slug) === 'bolsos') {
            continue;
        }
        $brands[] = $term->name;
    }

    if (!$brands) {
        return;
    }

    echo '<div class="pd-product-brand-line">' . esc_html(implode(', ', $brands)) . '</div>';
}, 6);

add_action('woocommerce_after_add_to_cart_button', function() {
    echo '<button type="submit" name="pd_buy_now" value="1" class="button pd-buy-now-button">COMPRAR AHORA</button>';
}, 20);

add_filter('woocommerce_add_to_cart_redirect', function($url) {
    if (isset($_REQUEST['pd_buy_now'])) {
        return wc_get_checkout_url();
    }
    return $url;
}, 100);

add_filter('woocommerce_cart_item_name', function($name, $cart_item, $cart_item_key) {
    if (!is_checkout() || empty($cart_item['data'])) {
        return $name;
    }

    $product = $cart_item['data'];
    $thumb = $product->get_image(array(54, 54), array('class' => 'pd-checkout-item-thumb'));
    return '<span class="pd-checkout-item-name">' . $thumb . '<span>' . $name . '</span></span>';
}, 100, 3);

add_action('wp_footer', function() {
    if (is_admin()) {
        return;
    }
    ?>
    <footer class="pd-client-footer pd-footer" aria-label="Footer Prime Drop">
      <div class="pd-client-footer-inner">
        <div class="pd-client-footer-brand">
          <h2>PRIME DROP</h2>
          <p>Bolsos exclusivos, originales y seleccionados para elevar tu estilo diario con marcas internacionales.</p>
        </div>

        <div class="pd-client-footer-policies">
          <h3>POLÍTICAS</h3>
          <a href="/terminos-y-condiciones/">Términos y condiciones</a>
          <a href="/politica-de-privacidad/">Política de privacidad</a>
          <a href="/politica-de-reembolso/">Política de reembolso</a>
        </div>

        <div class="pd-client-footer-social">
          <h3>REDES SOCIALES</h3>
          <div class="pd-client-footer-icons">
            <a href="mailto:primedropelite@gmail.com" aria-label="Correo electrónico">
              <svg aria-hidden="true" viewBox="0 0 24 24"><path d="M4 6h16v12H4z"/><path d="m4 7 8 6 8-6"/></svg>
            </a>
            <a href="https://www.instagram.com/primedrop_elite/" target="_blank" rel="noopener" aria-label="Instagram">
              <svg aria-hidden="true" viewBox="0 0 24 24"><rect x="5" y="5" width="14" height="14" rx="4"/><circle cx="12" cy="12" r="3.2"/><path d="M16.8 7.6h.01"/></svg>
            </a>
            <a href="https://www.tiktok.com/@primedrop_elite" target="_blank" rel="noopener" aria-label="TikTok">
              <svg aria-hidden="true" viewBox="0 0 24 24"><path d="M14 4v10.2a4.2 4.2 0 1 1-4.2-4.2"/><path d="M14 4c.6 3.2 2.5 5 5.2 5.4"/></svg>
            </a>
            <a href="https://wa.me/573160685555" target="_blank" rel="noopener" aria-label="WhatsApp">
              <svg aria-hidden="true" viewBox="0 0 24 24"><path d="M5.5 19 6.7 15.5a7.3 7.3 0 1 1 2 2Z"/><path d="M9.2 8.7c.3 2.5 2.1 4.4 4.5 5.1l1.3-1.2 2 .5"/></svg>
            </a>
          </div>
        </div>
      </div>

      <div class="pd-client-newsletter">
        <h3>ÚNETE A PRIME DROP</h3>
        <p>Recibe ofertas exclusivas y novedades.</p>
        <form action="/" method="post">
          <input type="email" name="email" placeholder="Introducir dirección de correo electrónico" aria-label="Correo electrónico">
          <button type="submit">REGISTRARSE</button>
        </form>
      </div>

      <div class="pd-client-copyright">© 2026 Prime Drop Elite. Todos los derechos reservados.</div>
    </footer>
    <?php
}, 2147482000);

add_action('wp_footer', function() {
    if (is_admin()) {
        return;
    }
    ?>
    <style id="prime-drop-client-docx-8-items-css">
    *,
    *::before,
    *::after {
      font-family: 'Roboto Serif', Georgia, serif !important;
    }

    body {
      font-family: 'Roboto Serif', Georgia, serif !important;
      text-rendering: optimizeLegibility;
    }

    /* Barra superior del cliente */
    #pd-client-topbar {
      min-height: 34px;
      display: grid;
      grid-template-columns: minmax(180px, 1fr) auto minmax(180px, 1fr);
      align-items: center;
      gap: 18px;
      padding: 7px clamp(16px, 4vw, 56px);
      background: #f4f4f4;
      color: #0b0b0b;
      border-bottom: 1px solid #e5e5e5;
      font-size: 12px;
      line-height: 1.2;
      letter-spacing: .03em;
      position: relative;
      z-index: 1001;
    }

    #pd-client-topbar a {
      color: #0b0b0b !important;
      text-decoration: none !important;
    }

    .pd-global-topbar {
      display: none !important;
    }

    .pd-client-topbar-email {
      justify-self: start;
      text-transform: none;
    }

    .pd-client-topbar-phrases {
      position: relative;
      min-width: min(420px, 44vw);
      min-height: 16px;
      text-align: center;
      overflow: hidden;
      font-weight: 700;
      text-transform: uppercase;
    }

    .pd-client-topbar-phrases span {
      position: absolute;
      inset: 0;
      opacity: 0;
      transform: translateY(8px);
      animation: pdTopbarPhrase 12s infinite;
      white-space: nowrap;
    }

    .pd-client-topbar-phrases span:nth-child(2) { animation-delay: 4s; }
    .pd-client-topbar-phrases span:nth-child(3) { animation-delay: 8s; }

    @keyframes pdTopbarPhrase {
      0%, 8% { opacity: 0; transform: translateY(8px); }
      12%, 30% { opacity: 1; transform: translateY(0); }
      36%, 100% { opacity: 0; transform: translateY(-8px); }
    }

    .pd-client-topbar-socials {
      justify-self: end;
      display: inline-flex;
      align-items: center;
      gap: 13px;
      white-space: nowrap;
    }

    .pd-client-topbar-socials span {
      text-transform: none;
    }

    .pd-client-topbar-socials a {
      font-size: 15px;
      font-weight: 800;
      line-height: 1;
    }

    @media (max-width: 768px) {
      #pd-client-topbar {
        grid-template-columns: 1fr;
        gap: 4px;
        justify-items: center;
        padding: 7px 14px;
        font-size: 10px;
      }

      .pd-client-topbar-email,
      .pd-client-topbar-socials {
        justify-self: center;
      }

      .pd-client-topbar-phrases {
        min-width: 100%;
      }
    }

    /* Header: conservar menús actuales, añadir búsqueda y centrar logo */
    #header [data-device="desktop"] .site-logo-container,
    #header [data-device="desktop"] [data-id="logo"] {
      justify-content: center !important;
      text-align: center !important;
    }

    .pd-header-search-link {
      width: 28px;
      height: 28px;
      display: inline-flex !important;
      align-items: center;
      justify-content: center;
      color: #000 !important;
      text-decoration: none !important;
      margin-right: 12px;
      opacity: 1;
    }

    .pd-header-search-link:hover {
      opacity: .65;
    }

    .pd-header-search-link svg {
      width: 20px;
      height: 20px;
      fill: none;
      stroke: currentColor;
      stroke-width: 1.7;
    }

    /* Fila de beneficios despues del hero */
    .pd-client-benefits {
      width: 100%;
      background: #f7f7f7;
      border-top: 1px solid #eeeeee;
      border-bottom: 1px solid #eeeeee;
      padding: 26px clamp(18px, 5vw, 76px);
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 18px;
    }

    .pd-client-benefit {
      display: grid;
      grid-template-columns: 42px 1fr;
      align-items: center;
      gap: 14px;
      min-width: 0;
    }

    .pd-client-benefit svg {
      width: 38px;
      height: 38px;
      stroke: #111;
      fill: none;
      stroke-width: 1.8;
    }

    .pd-client-benefit strong {
      display: block;
      color: #111;
      font-size: 14px;
      line-height: 1.25;
      font-weight: 800;
    }

    .pd-client-benefit span {
      display: block;
      color: #333;
      font-size: 13px;
      line-height: 1.35;
      margin-top: 3px;
    }

    .pd-kicker,
    .pd-hero .pd-kicker,
    .hero-section .pd-kicker {
      display: none !important;
    }

    @media (max-width: 900px) {
      .pd-client-benefits {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
    }

    @media (max-width: 560px) {
      .pd-client-benefits {
        grid-template-columns: 1fr;
        padding: 20px 18px;
      }
    }

    /* Tendencia / cards estilo tienda anterior */
    body.home .pd-products-title,
    body.page-id-14 .pd-products-title,
    body.home h2,
    body.page-id-14 h2 {
      font-family: 'Roboto Serif', Georgia, serif !important;
    }

    body.home .pd-products-title,
    body.page-id-14 .pd-products-title {
      display: block !important;
      visibility: visible !important;
      text-align: center !important;
      font-size: clamp(30px, 3vw, 42px) !important;
      line-height: 1.05 !important;
      font-weight: 800 !important;
      letter-spacing: .01em !important;
      text-transform: uppercase !important;
      margin: 0 0 34px !important;
    }

    body.home .elementor-element-741b26a .woocommerce,
    body.page-id-14 .elementor-element-741b26a .woocommerce {
      width: min(1240px, calc(100vw - 64px)) !important;
      margin: 0 auto !important;
      overflow: hidden !important;
    }

    body.home .elementor-element-741b26a ul.products,
    body.page-id-14 .elementor-element-741b26a ul.products {
      display: flex !important;
      gap: 24px !important;
      overflow-x: auto !important;
      scroll-behavior: smooth !important;
      scrollbar-width: none !important;
      padding: 0 0 52px !important;
      margin: 0 !important;
      scroll-snap-type: x mandatory !important;
    }

    body.home .elementor-element-741b26a ul.products::-webkit-scrollbar,
    body.page-id-14 .elementor-element-741b26a ul.products::-webkit-scrollbar {
      display: none !important;
    }

    body.home .elementor-element-741b26a ul.products li.product,
    body.page-id-14 .elementor-element-741b26a ul.products li.product {
      flex: 0 0 calc(25% - 18px) !important;
      width: auto !important;
      min-width: 0 !important;
      max-width: none !important;
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      text-align: center !important;
      background: #fff !important;
      border: 0 !important;
      box-shadow: none !important;
      padding: 0 !important;
      margin: 0 !important;
      scroll-snap-align: start !important;
      overflow: visible !important;
    }

    body.home .elementor-element-741b26a ul.products li.product:nth-child(n+1),
    body.page-id-14 .elementor-element-741b26a ul.products li.product:nth-child(n+1) {
      display: flex !important;
    }

    @media (max-width: 1024px) {
      body.home .elementor-element-741b26a ul.products li.product,
      body.page-id-14 .elementor-element-741b26a ul.products li.product {
        flex-basis: calc(33.333% - 16px) !important;
      }
    }

    @media (max-width: 768px) {
      body.home .elementor-element-741b26a ul.products li.product,
      body.page-id-14 .elementor-element-741b26a ul.products li.product {
        flex-basis: 72% !important;
      }
    }

    .woocommerce ul.products,
    [data-products] {
      gap: 26px !important;
    }

    .woocommerce ul.products li.product,
    [data-products] .product {
      background: #fff !important;
      border: none !important;
      border-radius: 0 !important;
      box-shadow: none !important;
      padding: 0 !important;
      text-align: center !important;
      overflow: visible !important;
    }

    .woocommerce ul.products li.product figure,
    .woocommerce ul.products li.product figure > a.ct-media-container,
    .woocommerce ul.products li.product .ct-media-container,
    [data-products] .product figure,
    [data-products] .product .ct-media-container {
      width: 100% !important;
      aspect-ratio: 4 / 5 !important;
      min-height: 0 !important;
      height: auto !important;
      background: #f6f6f6 !important;
      border: none !important;
      border-radius: 0 !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      overflow: hidden !important;
      padding: 0 !important;
      box-shadow: none !important;
    }

    .woocommerce ul.products li.product img,
    .woocommerce .products img,
    [data-products] .product img {
      width: 100% !important;
      height: 100% !important;
      object-fit: contain !important;
      object-position: center center !important;
      background: transparent !important;
      padding: 0 !important;
      margin: 0 !important;
      border: none !important;
      border-radius: 0 !important;
      box-shadow: none !important;
      transform: none !important;
      mix-blend-mode: normal !important;
    }

    .woocommerce ul.products li.product .woocommerce-loop-product__title,
    [data-products] .woocommerce-loop-product__title {
      min-height: 0 !important;
      height: auto !important;
      margin: 18px auto 8px !important;
      padding: 0 8px !important;
      font-size: clamp(14px, 1.2vw, 18px) !important;
      line-height: 1.15 !important;
      font-weight: 800 !important;
      text-align: center !important;
      text-transform: none !important;
      letter-spacing: 0 !important;
      color: #000 !important;
      overflow: visible !important;
      display: block !important;
      -webkit-line-clamp: unset !important;
      -webkit-box-orient: initial !important;
    }

    .woocommerce ul.products li.product .price,
    [data-products] .product .price {
      display: block !important;
      width: 100% !important;
      margin: 0 auto 16px !important;
      padding: 0 !important;
      color: #000 !important;
      text-align: center !important;
      font-size: 14px !important;
      line-height: 1.35 !important;
      font-weight: 400 !important;
      letter-spacing: 0 !important;
      visibility: visible !important;
      opacity: 1 !important;
    }

    .woocommerce ul.products li.product .price bdi,
    .woocommerce ul.products li.product .price .woocommerce-Price-amount,
    [data-products] .product .price bdi,
    [data-products] .product .price .woocommerce-Price-amount {
      font-weight: 400 !important;
    }

    .woocommerce ul.products li.product .price::after,
    [data-products] .product .price::after,
    .woocommerce ul.products li.product .woocommerce-Price-amount::after,
    [data-products] .product .woocommerce-Price-amount::after {
      content: "" !important;
      display: none !important;
    }

    .woocommerce ul.products li.product .entry-meta,
    .woocommerce ul.products li.product .posted_in,
    .woocommerce ul.products li.product [class*="brand"] {
      display: none !important;
    }

    @media (hover: hover) and (pointer: fine) {
      .woocommerce ul.products li.product .ct-woo-card-actions,
      .woocommerce ul.products li.product .button {
        opacity: 0 !important;
        visibility: hidden !important;
        transform: translateY(8px) !important;
        transition: opacity .2s ease, transform .2s ease, visibility .2s ease !important;
      }

      .woocommerce ul.products li.product:hover .ct-woo-card-actions,
      .woocommerce ul.products li.product:hover .button {
        opacity: 1 !important;
        visibility: visible !important;
        transform: translateY(0) !important;
      }
    }

    .woocommerce ul.products li.product .button,
    [data-products] .product .button {
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      min-height: 36px !important;
      width: auto !important;
      min-width: 150px !important;
      padding: 10px 22px !important;
      border: 1px solid #000 !important;
      border-radius: 999px !important;
      background: #000 !important;
      color: #fff !important;
      font-size: 11px !important;
      line-height: 1.15 !important;
      letter-spacing: .08em !important;
      text-transform: uppercase !important;
      text-align: center !important;
      margin: 0 auto !important;
      white-space: nowrap !important;
      box-sizing: border-box !important;
    }

    /* Tienda / categorias */
    body.woocommerce-shop .woo-listing-top,
    body.post-type-archive-product .woo-listing-top,
    body.tax-product_cat .woo-listing-top,
    body.page-id-547 .woo-listing-top {
      width: min(1150px, calc(100vw - 48px)) !important;
      margin: 36px auto 32px !important;
      padding: 20px 0 !important;
      border-top: 1px solid #eee !important;
      border-bottom: 1px solid #eee !important;
      display: grid !important;
      grid-template-columns: minmax(180px, 1fr) minmax(260px, 360px) minmax(180px, 1fr) !important;
      align-items: center !important;
      gap: 24px !important;
    }

    body.woocommerce-shop .woocommerce-result-count,
    body.post-type-archive-product .woocommerce-result-count,
    body.tax-product_cat .woocommerce-result-count,
    body.page-id-547 .woocommerce-result-count {
      grid-column: 1 !important;
      justify-self: start !important;
      margin: 0 !important;
      font-size: 11px !important;
      letter-spacing: .08em !important;
      font-weight: 700 !important;
      color: #000 !important;
      text-transform: uppercase !important;
      white-space: nowrap !important;
    }

    body.woocommerce-shop .pd-shop-search,
    body.post-type-archive-product .pd-shop-search,
    body.tax-product_cat .pd-shop-search,
    body.page-id-547 .pd-shop-search {
      grid-column: 2 !important;
      justify-self: center !important;
      width: 100% !important;
      max-width: 360px !important;
      margin: 0 !important;
    }

    body.woocommerce-shop .pd-shop-search form,
    body.post-type-archive-product .pd-shop-search form,
    body.tax-product_cat .pd-shop-search form,
    body.page-id-547 .pd-shop-search form {
      width: 100% !important;
      height: 46px !important;
      display: flex !important;
      align-items: center !important;
      border: 1px solid #e4e4e4 !important;
      border-radius: 999px !important;
      background: #fff !important;
      box-shadow: 0 10px 30px rgba(0,0,0,.04) !important;
      overflow: hidden !important;
    }

    body.woocommerce-shop .pd-shop-search input[type="search"],
    body.post-type-archive-product .pd-shop-search input[type="search"],
    body.tax-product_cat .pd-shop-search input[type="search"],
    body.page-id-547 .pd-shop-search input[type="search"] {
      flex: 1 1 auto !important;
      height: 100% !important;
      padding: 0 18px !important;
      border: 0 !important;
      outline: 0 !important;
      background: transparent !important;
      color: #000 !important;
      font-size: 14px !important;
      font-weight: 400 !important;
    }

    body.woocommerce-shop .pd-shop-search button,
    body.post-type-archive-product .pd-shop-search button,
    body.tax-product_cat .pd-shop-search button,
    body.page-id-547 .pd-shop-search button {
      width: 44px !important;
      height: 44px !important;
      min-width: 44px !important;
      padding: 0 !important;
      border: 0 !important;
      border-radius: 50% !important;
      background: #000 !important;
      color: #fff !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
    }

    body.woocommerce-shop .woocommerce-ordering,
    body.post-type-archive-product .woocommerce-ordering,
    body.tax-product_cat .woocommerce-ordering,
    body.page-id-547 .woocommerce-ordering {
      grid-column: 3 !important;
      justify-self: end !important;
      width: 260px !important;
      margin: 0 !important;
      position: relative !important;
    }

    body.woocommerce-shop .woocommerce-ordering select.orderby,
    body.post-type-archive-product .woocommerce-ordering select.orderby,
    body.tax-product_cat .woocommerce-ordering select.orderby,
    body.page-id-547 .woocommerce-ordering select.orderby {
      width: 100% !important;
      height: 46px !important;
      border: 1px solid #111 !important;
      border-radius: 999px !important;
      background: #ffffff !important;
      color: #000000 !important;
      padding: 0 42px 0 22px !important;
      font-size: 13px !important;
      font-weight: 700 !important;
      letter-spacing: .04em !important;
      text-transform: uppercase !important;
      text-align: center !important;
      text-align-last: center !important;
      appearance: auto !important;
      -webkit-appearance: menulist !important;
      box-shadow: none !important;
      cursor: pointer !important;
    }

    body.woocommerce-shop .woocommerce-ordering select.orderby option,
    body.post-type-archive-product .woocommerce-ordering select.orderby option,
    body.tax-product_cat .woocommerce-ordering select.orderby option,
    body.page-id-547 .woocommerce-ordering select.orderby option {
      background: #fff !important;
      color: #000 !important;
      text-align: center !important;
      font-size: 13px !important;
      font-weight: 500 !important;
    }

    @media (max-width: 900px) {
      body.woocommerce-shop .woo-listing-top,
      body.post-type-archive-product .woo-listing-top,
      body.tax-product_cat .woo-listing-top,
      body.page-id-547 .woo-listing-top {
        grid-template-columns: 1fr !important;
        gap: 14px !important;
        width: min(620px, calc(100vw - 32px)) !important;
      }

      body.woocommerce-shop .woocommerce-result-count,
      body.post-type-archive-product .woocommerce-result-count,
      body.tax-product_cat .woocommerce-result-count,
      body.page-id-547 .woocommerce-result-count,
      body.woocommerce-shop .pd-shop-search,
      body.post-type-archive-product .pd-shop-search,
      body.tax-product_cat .pd-shop-search,
      body.page-id-547 .pd-shop-search,
      body.woocommerce-shop .woocommerce-ordering,
      body.post-type-archive-product .woocommerce-ordering,
      body.tax-product_cat .woocommerce-ordering,
      body.page-id-547 .woocommerce-ordering {
        grid-column: 1 !important;
        justify-self: center !important;
        text-align: center !important;
        width: 100% !important;
        max-width: 360px !important;
      }
    }

    /* Producto individual */
    .single-product .entry-summary .product_title,
    .single-product .entry-summary h1 {
      font-size: clamp(34px, 3.6vw, 52px) !important;
      line-height: 1.05 !important;
      font-weight: 800 !important;
      margin-bottom: 8px !important;
    }

    .pd-product-brand-line {
      color: #555 !important;
      font-size: 13px !important;
      text-transform: uppercase !important;
      letter-spacing: .1em !important;
      font-weight: 700 !important;
      margin: 0 0 16px !important;
    }

    .single-product .entry-summary .price {
      font-weight: 400 !important;
      font-size: 24px !important;
      margin: 0 0 28px !important;
    }

    .single-product .entry-summary .price bdi,
    .single-product .entry-summary .price .woocommerce-Price-amount {
      font-weight: 400 !important;
    }

    .single-product .product_meta,
    .single-product .sku_wrapper,
    .single-product .posted_in {
      display: none !important;
    }

    .single-product .entry-summary form.cart {
      display: flex !important;
      align-items: center !important;
      flex-wrap: wrap !important;
      gap: 12px !important;
    }

    .single-product .entry-summary .quantity {
      min-width: 118px !important;
      height: 44px !important;
      border: 1px solid #000 !important;
      border-radius: 999px !important;
      display: inline-grid !important;
      grid-template-columns: 34px 1fr 34px !important;
      align-items: center !important;
      overflow: hidden !important;
      background: #fff !important;
      flex: 0 0 auto !important;
    }

    .single-product .entry-summary .quantity input.qty {
      width: 42px !important;
      min-width: 42px !important;
      height: 42px !important;
      padding: 0 !important;
      border: 0 !important;
      text-align: center !important;
      font-weight: 700 !important;
      color: #000 !important;
      background: transparent !important;
      opacity: 1 !important;
      visibility: visible !important;
      grid-column: 2 !important;
    }

    .single-product .entry-summary .quantity .ct-decrease,
    .single-product .entry-summary .quantity .ct-increase {
      position: static !important;
      width: 34px !important;
      height: 42px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      opacity: 1 !important;
      visibility: visible !important;
      color: #000 !important;
      transform: none !important;
    }

    .single-product .entry-summary .single_add_to_cart_button,
    .single-product .entry-summary .pd-buy-now-button {
      min-height: 44px !important;
      border-radius: 999px !important;
      padding: 0 28px !important;
      background: #000 !important;
      color: #fff !important;
      border: 1px solid #000 !important;
      font-size: 12px !important;
      font-weight: 800 !important;
      letter-spacing: .08em !important;
      text-transform: uppercase !important;
      white-space: nowrap !important;
      flex: 0 1 auto !important;
    }

    .single-product .entry-summary .pd-buy-now-button {
      background: #fff !important;
      color: #000 !important;
    }

    .single-product .entry-summary .yith-add-to-wishlist-button-block,
    .single-product .entry-summary .yith-wcwl-add-to-wishlist {
      width: 100% !important;
      max-width: 360px !important;
      margin: 18px 0 0 !important;
    }

    .pd-client-payment-notes {
      display: grid;
      gap: 8px;
      margin: 18px 0 24px;
      max-width: 420px;
    }

    .pd-client-payment-note {
      display: flex;
      align-items: center;
      gap: 10px;
      border: 1px solid #eeeeee;
      border-radius: 12px;
      padding: 11px 13px;
      color: #111;
      background: #fff;
      font-size: 13px;
    }

    .pd-client-payment-note strong {
      font-weight: 800;
    }

    .pd-client-reviews {
      width: min(1180px, calc(100vw - 48px));
      margin: 56px auto 34px;
      padding: 28px 0;
      border-top: 1px solid #ddd;
      border-bottom: 1px solid #ddd;
      display: grid;
      grid-template-columns: 1.2fr 1fr 1fr;
      gap: 28px;
      align-items: center;
    }

    .pd-client-reviews h2 {
      margin: 0 0 10px !important;
      font-size: 28px !important;
      line-height: 1.1 !important;
      font-weight: 500 !important;
    }

    .pd-client-stars {
      letter-spacing: 3px;
      font-size: 18px;
      color: #000;
    }

    .pd-client-review-box {
      border: 1px solid #111;
      border-radius: 6px;
      min-height: 44px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
    }

    .pd-client-share {
      width: min(1180px, calc(100vw - 48px));
      margin: 18px auto 48px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 18px;
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: .08em;
      font-weight: 700;
    }

    .pd-client-share a {
      color: #000 !important;
      text-decoration: none !important;
      border: 1px solid #ddd;
      border-radius: 50%;
      width: 34px;
      height: 34px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
    }

    @media (max-width: 768px) {
      .single-product .entry-summary form.cart {
        justify-content: center !important;
      }

      .pd-client-reviews {
        grid-template-columns: 1fr;
        text-align: center;
      }
    }

    /* Modal login */
    #account-modal input[type="email"],
    #account-modal input[type="text"],
    #account-modal input[type="password"],
    .ct-login-form input,
    .ct-register-form input {
      background: #fff !important;
      border: 1px solid #ddd !important;
      border-radius: 25px !important;
      color: #000 !important;
      box-shadow: none !important;
    }

    #account-modal .woocommerce-privacy-policy-text {
      margin: 14px 0 0 !important;
      color: #555 !important;
      font-size: 12px !important;
      line-height: 1.55 !important;
    }

    /* Checkout */
    body.woocommerce-checkout .entry-header,
    body.woocommerce-checkout .hero-section {
      text-align: center !important;
    }

    body.woocommerce-checkout .page-title,
    body.woocommerce-checkout h1 {
      text-align: center !important;
      font-size: clamp(34px, 4vw, 48px) !important;
      line-height: 1.1 !important;
    }

    body.woocommerce-checkout form.checkout {
      width: min(1180px, calc(100vw - 32px)) !important;
      margin: 0 auto !important;
      display: grid !important;
      grid-template-columns: minmax(0, 1fr) minmax(340px, 450px) !important;
      gap: 42px !important;
      align-items: start !important;
    }

    .pd-checkout-item-name {
      display: grid !important;
      grid-template-columns: 54px minmax(0, 1fr) !important;
      align-items: center !important;
      gap: 12px !important;
    }

    .pd-checkout-item-thumb {
      width: 54px !important;
      height: 54px !important;
      object-fit: contain !important;
      background: #f7f7f7 !important;
      border-radius: 8px !important;
      padding: 4px !important;
    }

    body.woocommerce-checkout #payment,
    body.woocommerce-checkout .woocommerce-checkout-payment {
      border: 1px solid #e5e5e5 !important;
      border-radius: 14px !important;
      overflow: hidden !important;
      background: #fff !important;
    }

    body.woocommerce-checkout #payment ul.payment_methods li,
    body.woocommerce-checkout .wc_payment_method {
      border-bottom: 1px solid #ededed !important;
      padding: 16px !important;
      margin: 0 !important;
    }

    body.woocommerce-checkout input[type="radio"],
    body.woocommerce-checkout input[type="checkbox"] {
      accent-color: #000 !important;
      width: 18px !important;
      height: 18px !important;
      vertical-align: middle !important;
      margin-right: 10px !important;
    }

    body.woocommerce-checkout .wc_payment_method.payment_method_selected,
    body.woocommerce-checkout .wc_payment_method:has(input:checked),
    body.woocommerce-checkout li:has(input[type="radio"]:checked) {
      background: #f5faf6 !important;
      box-shadow: inset 3px 0 0 #0a8a3b !important;
    }

    body.woocommerce-checkout .payment_box {
      background: #f7f7f7 !important;
      color: #111 !important;
      border-radius: 10px !important;
      margin: 12px 0 0 !important;
      padding: 14px !important;
      font-size: 13px !important;
      line-height: 1.5 !important;
    }

    body.woocommerce-checkout .select2-container .select2-selection,
    body.woocommerce-checkout select,
    body.woocommerce-checkout input,
    body.woocommerce-checkout textarea {
      border-radius: 25px !important;
      background: #fff !important;
      color: #000 !important;
    }

    body.woocommerce-checkout .select2-results__option {
      color: #000 !important;
      background: #fff !important;
      font-family: 'Roboto Serif', Georgia, serif !important;
    }

    body.woocommerce-checkout .select2-results__option--highlighted {
      background: #f1f1f1 !important;
      color: #000 !important;
    }

    @media (max-width: 900px) {
      body.woocommerce-checkout form.checkout {
        grid-template-columns: 1fr !important;
        gap: 24px !important;
      }
    }

    /* Footer final */
    body > footer:not(.pd-client-footer),
    .ct-footer:not(.pd-client-footer),
    #footer:not(.pd-client-footer),
    .site-footer:not(.pd-client-footer),
    .pd-footer:not(.pd-client-footer),
    .elementor-location-footer:not(.pd-client-footer) {
      display: none !important;
    }

    .pd-client-footer {
      background: #000 !important;
      color: #fff !important;
      padding: 46px clamp(18px, 8vw, 120px) 22px !important;
      margin: 0 !important;
      font-size: 13px !important;
      line-height: 1.55 !important;
      clear: both !important;
    }

    .pd-client-footer a {
      color: #fff !important;
      text-decoration: none !important;
    }

    .pd-client-footer-inner {
      display: grid;
      grid-template-columns: 1.4fr .9fr 1fr;
      gap: clamp(24px, 5vw, 78px);
      max-width: 1040px;
      margin: 0 auto;
      align-items: start;
    }

    .pd-client-footer h2,
    .pd-client-footer h3 {
      color: #fff !important;
      margin: 0 0 14px !important;
      line-height: 1.1 !important;
      letter-spacing: .02em !important;
      font-weight: 800 !important;
    }

    .pd-client-footer h2 { font-size: 26px !important; }
    .pd-client-footer h3 { font-size: 17px !important; }

    .pd-client-footer p {
      margin: 0 !important;
      color: rgba(255,255,255,.92) !important;
    }

    .pd-client-footer-policies {
      display: flex;
      flex-direction: column;
      gap: 7px;
    }

    .pd-client-footer-icons {
      display: flex;
      gap: 10px;
      align-items: center;
      flex-wrap: wrap;
    }

    .pd-client-footer-icons a {
      width: 34px;
      height: 34px;
      border-radius: 50%;
      border: 1px solid rgba(255,255,255,.42);
      display: inline-flex;
      align-items: center;
      justify-content: center;
    }

    .pd-client-footer-icons svg {
      width: 16px;
      height: 16px;
      fill: none;
      stroke: #fff;
      stroke-width: 1.8;
      stroke-linecap: round;
      stroke-linejoin: round;
      filter: none !important;
    }

    .pd-client-newsletter {
      max-width: 640px;
      margin: 36px auto 28px;
      text-align: center;
    }

    .pd-client-newsletter form {
      margin-top: 14px;
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 10px;
    }

    .pd-client-newsletter input {
      height: 44px;
      border-radius: 999px !important;
      border: 1px solid rgba(255,255,255,.45) !important;
      background: transparent !important;
      color: #fff !important;
      padding: 0 18px !important;
      font-size: 13px !important;
    }

    .pd-client-newsletter input::placeholder {
      color: rgba(255,255,255,.62) !important;
    }

    .pd-client-newsletter button {
      height: 44px;
      border-radius: 999px !important;
      border: 0 !important;
      background: #fff !important;
      color: #000 !important;
      padding: 0 22px !important;
      font-size: 12px !important;
      font-weight: 800 !important;
      letter-spacing: .05em !important;
    }

    .pd-client-copyright {
      max-width: 1040px;
      margin: 0 auto;
      border-top: 1px solid rgba(255,255,255,.22);
      padding-top: 18px;
      text-align: center;
      font-size: 12px;
      color: rgba(255,255,255,.9);
    }

    @media (max-width: 760px) {
      .pd-client-footer-inner {
        grid-template-columns: 1fr;
        text-align: center;
      }

      .pd-client-footer-icons,
      .pd-client-footer-policies {
        justify-content: center;
        align-items: center;
      }

      .pd-client-newsletter form {
        grid-template-columns: 1fr;
      }
    }
    </style>

    <script id="prime-drop-client-docx-8-items-js">
    (function() {
      var moneyRe = /\s*(COP|CO\$)\s*/gi;

      function ensureTopbarFallback() {
        if (document.getElementById('pd-client-topbar')) return;
        var header = document.getElementById('header') || document.querySelector('header');
        if (!header || !header.parentNode) return;
        var topbar = document.createElement('div');
        topbar.id = 'pd-client-topbar';
        topbar.innerHTML =
          '<a class="pd-client-topbar-email" href="mailto:primedropelite@gmail.com">primedropelite@gmail.com</a>' +
          '<div class="pd-client-topbar-phrases"><span>BOLSOS 100% ORIGINALES.</span><span>GARANTÍA DE AUTENTICIDAD.</span><span>ENVÍOS A TODA COLOMBIA | RÁPIDO Y SEGURO</span></div>' +
          '<div class="pd-client-topbar-socials"><span>Síguenos:</span><a href="https://www.facebook.com/primedropelite">f</a><a href="https://www.tiktok.com/@primedrop_elite">♪</a><a href="https://www.instagram.com/primedrop_elite/">◎</a></div>';
        header.parentNode.insertBefore(topbar, header);
      }

      function addHeaderSearchIcon() {
        var account = document.querySelector('#header [data-id="account"], header [data-id="account"], .ct-header-account');
        if (!account || document.querySelector('.pd-header-search-link')) return;
        var link = document.createElement('a');
        link.className = 'pd-header-search-link';
        link.href = '/bolsos/';
        link.setAttribute('aria-label', 'Buscar bolsos');
        link.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><path d="m16.5 16.5 4 4"></path></svg>';
        account.parentNode.insertBefore(link, account);
      }

      function findHomeHero() {
        if (!document.body.classList.contains('home') && !document.body.classList.contains('page-id-14')) return null;
        var candidates = Array.prototype.slice.call(document.querySelectorAll('section, .elementor-section, .elementor-top-section'));
        return candidates.find(function(el) { return el.querySelector('video'); });
      }

      function addBenefitsAfterHero() {
        if (document.querySelector('.pd-client-benefits')) return;
        var hero = findHomeHero();
        if (!hero || !hero.parentNode) return;
        var benefits = document.createElement('section');
        benefits.className = 'pd-client-benefits';
        benefits.innerHTML =
          '<div class="pd-client-benefit"><svg viewBox="0 0 24 24"><rect x="7" y="3" width="10" height="18" rx="2"/><path d="M11 18h2"/></svg><div><strong>SOPORTE EN VIVO</strong><span>+57 316 068 5555</span></div></div>' +
          '<div class="pd-client-benefit"><svg viewBox="0 0 24 24"><path d="M3 7h11v9H3z"/><path d="M14 10h4l3 3v3h-7z"/><circle cx="7" cy="18" r="1.8"/><circle cx="18" cy="18" r="1.8"/></svg><div><strong>ENVÍOS A TODA COLOMBIA</strong><span>Rápido y seguro</span></div></div>' +
          '<div class="pd-client-benefit"><svg viewBox="0 0 24 24"><path d="M12 3 4.5 6v5.5c0 4.5 3.1 7.8 7.5 9.5 4.4-1.7 7.5-5 7.5-9.5V6z"/><path d="m8.5 12 2.2 2.2 4.8-5"/></svg><div><strong>GARANTÍA</strong><span>Garantía de autenticidad</span></div></div>' +
          '<div class="pd-client-benefit"><svg viewBox="0 0 24 24"><rect x="3" y="6" width="18" height="12" rx="1.8"/><path d="M3 10h18"/><path d="M7 15h4"/></svg><div><strong>COMPRAS SEGURAS</strong><span>Supervisado por la SIC</span></div></div>';
        hero.insertAdjacentElement('afterend', benefits);
      }

      function renameFeatured() {
        document.querySelectorAll('.pd-products-title, h2, .elementor-heading-title').forEach(function(el) {
          var text = (el.textContent || '').replace(/\s+/g, ' ').trim().toUpperCase();
          if (text === 'DESTACADAS' || text === 'PRODUCTOS DESTACADOS') {
            el.textContent = 'TENDENCIA';
            el.classList.add('pd-products-title');
          }
        });
      }

      function setupTrendCarousel() {
        var list = document.querySelector('body.home .elementor-element-741b26a ul.products, body.page-id-14 .elementor-element-741b26a ul.products');
        if (!list || list.dataset.pdTrendReady === 'yes') return;
        list.dataset.pdTrendReady = 'yes';
        var originals = Array.prototype.slice.call(list.children).filter(function(el) { return el.classList.contains('product'); });
        if (originals.length > 0 && originals.length < 8) {
          originals.forEach(function(item) {
            var clone = item.cloneNode(true);
            clone.classList.add('pd-trend-clone');
            list.appendChild(clone);
          });
        }
        var paused = false;
        list.addEventListener('mouseenter', function() { paused = true; });
        list.addEventListener('mouseleave', function() { paused = false; });
        list.addEventListener('touchstart', function() { paused = true; }, { passive: true });
        list.addEventListener('touchend', function() { setTimeout(function(){ paused = false; }, 1800); }, { passive: true });
        function tick() {
          if (!paused && list.scrollWidth > list.clientWidth + 10) {
            list.scrollLeft += 0.35;
            if (list.scrollLeft >= (list.scrollWidth - list.clientWidth - 2)) list.scrollLeft = 0;
          }
          requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
      }

      function stripCopAndNormalizePrices() {
        document.querySelectorAll('.price, .woocommerce-Price-amount, .cart-subtotal, .order-total').forEach(function(el) {
          if (!el || !el.textContent) return;
          Array.prototype.slice.call(el.childNodes).forEach(function(node) {
            if (node.nodeType === 3) {
              node.nodeValue = node.nodeValue.replace(moneyRe, ' ').replace(/\s+/g, ' ');
            }
          });
          if (el.children.length === 0) {
            var txt = el.textContent.replace(moneyRe, ' ').replace(/\s+/g, ' ').trim();
            if (txt !== el.textContent.trim()) el.textContent = txt;
          }
          el.style.setProperty('font-weight', '400', 'important');
        });
      }

      function reorderModalPrivacy() {
        document.querySelectorAll('#account-modal form.register, #account-modal form.woocommerce-form-register').forEach(function(form) {
          var privacy = form.querySelector('.woocommerce-privacy-policy-text');
          var submit = form.querySelector('button[type="submit"], input[type="submit"], .ct-button[type="submit"], .ct-account-register-submit');
          if (!privacy || !submit) return;
          var submitRow = submit.closest('p, .form-row') || submit;
          if (submitRow.nextElementSibling !== privacy) submitRow.insertAdjacentElement('afterend', privacy);
        });
      }

      function productEnhancements() {
        if (!document.body.classList.contains('single-product')) return;
        var summary = document.querySelector('.entry-summary');
        if (!summary) return;
        var price = summary.querySelector('.price');
        if (price && !summary.querySelector('.pd-client-payment-notes')) {
          price.insertAdjacentHTML('afterend',
            '<div class="pd-client-payment-notes">' +
              '<div class="pd-client-payment-note"><strong>Addi disponible</strong><span>Paga tu bolso en cuotas según aprobación.</span></div>' +
              '<div class="pd-client-payment-note"><strong>Entrega estimada</strong><span>2 a 5 días hábiles después de confirmar el pago.</span></div>' +
            '</div>');
        }

        var related = document.querySelector('.related.products, section.related');
        if (related && !document.querySelector('.pd-client-reviews')) {
          var reviews = document.createElement('section');
          reviews.className = 'pd-client-reviews';
          reviews.innerHTML =
            '<div><h2>RESEÑAS</h2><div class="pd-client-stars">★★★★★</div><p>Opiniones verificadas de clientes Prime Drop.</p></div>' +
            '<div><strong>Calificación general</strong><p>4.7 basado en compras verificadas.</p></div>' +
            '<div><strong>Reseñar este producto</strong><div class="pd-client-review-box">☆ ☆ ☆ ☆ ☆</div></div>';
          related.parentNode.insertBefore(reviews, related);
        }

        var tabs = document.querySelector('.woocommerce-tabs.wc-tabs-wrapper');
        if (tabs && !document.querySelector('.pd-client-share')) {
          var share = document.createElement('div');
          share.className = 'pd-client-share';
          var url = encodeURIComponent(location.href.split('#')[0]);
          share.innerHTML = '<span>Compartir este producto</span><a href="https://www.facebook.com/sharer/sharer.php?u=' + url + '" target="_blank" rel="noopener">f</a><a href="https://www.instagram.com/primedrop_elite/" target="_blank" rel="noopener">◎</a><a href="https://wa.me/?text=' + url + '" target="_blank" rel="noopener">☏</a>';
          tabs.insertAdjacentElement('afterend', share);
        }
      }

      function cleanSelectOptions() {
        document.querySelectorAll('select.orderby option').forEach(function(opt) {
          var map = {
            'Orden por defecto': 'ORDEN POR DEFECTO',
            'Ordenar por popularidad': 'POPULARIDAD',
            'Ordenar por calificación media': 'CALIFICACIÓN',
            'Ordenar por las últimas': 'ÚLTIMAS',
            'Ordenar por precio: bajo a alto': 'MENOR PRECIO',
            'Ordenar por precio: alto a bajo': 'MAYOR PRECIO'
          };
          var key = (opt.textContent || '').trim();
          if (map[key]) opt.textContent = map[key];
        });
      }

      function injectLateStyle() {
        var existing = document.getElementById('pd-client-docx-late-style');
        if (existing) existing.remove();
        var style = document.createElement('style');
        style.id = 'pd-client-docx-late-style';
        style.textContent = [
          '.pd-global-topbar{display:none!important}',
          '.pd-kicker,.pd-hero .pd-kicker,.hero-section .pd-kicker{display:none!important}',
          'body.woocommerce-shop .woocommerce-ordering select.orderby,body.post-type-archive-product .woocommerce-ordering select.orderby,body.tax-product_cat .woocommerce-ordering select.orderby,body.page-id-547 .woocommerce-ordering select.orderby{background:#fff!important;color:#000!important;border:1px solid #111!important;text-align:center!important;text-align-last:center!important;box-shadow:none!important}',
          'body.woocommerce-shop .woocommerce-ordering select.orderby option,body.post-type-archive-product .woocommerce-ordering select.orderby option,body.tax-product_cat .woocommerce-ordering select.orderby option,body.page-id-547 .woocommerce-ordering select.orderby option{background:#fff!important;color:#000!important;text-align:center!important}',
          '.woocommerce ul.products li.product .price::after,[data-products] .product .price::after,.woocommerce ul.products li.product .woocommerce-Price-amount::after,[data-products] .product .woocommerce-Price-amount::after{content:""!important;display:none!important}',
          '@media (hover:hover) and (pointer:fine){body:not(.single-product) .woocommerce ul.products li.product:not(:hover) .ct-woo-card-actions,body:not(.single-product) .woocommerce ul.products li.product:not(:hover) .button{opacity:0!important;visibility:hidden!important;transform:translateY(8px)!important}body:not(.single-product) .woocommerce ul.products li.product:hover .ct-woo-card-actions,body:not(.single-product) .woocommerce ul.products li.product:hover .button{opacity:1!important;visibility:visible!important;transform:translateY(0)!important}}',
          '@media (max-width:900px){body:not(.single-product) .woocommerce ul.products li.product .ct-woo-card-actions,body:not(.single-product) .woocommerce ul.products li.product .button,body:not(.single-product) .woocommerce ul.products li.product:not(:hover) .ct-woo-card-actions,body:not(.single-product) .woocommerce ul.products li.product:not(:hover) .button{opacity:1!important;visibility:visible!important;transform:none!important}}'
        ].join('\n');
        (document.body || document.documentElement).appendChild(style);
        document.querySelectorAll('.pd-kicker, .pd-hero .pd-kicker, .hero-section .pd-kicker').forEach(function(el) {
          el.style.setProperty('display', 'none', 'important');
        });
        document.querySelectorAll('.pd-global-topbar').forEach(function(el) {
          el.style.setProperty('display', 'none', 'important');
        });
      }

      function run() {
        injectLateStyle();
        ensureTopbarFallback();
        addHeaderSearchIcon();
        addBenefitsAfterHero();
        renameFeatured();
        setupTrendCarousel();
        stripCopAndNormalizePrices();
        reorderModalPrivacy();
        productEnhancements();
        cleanSelectOptions();
      }

      document.addEventListener('DOMContentLoaded', run);
      window.addEventListener('pageshow', run);
      document.addEventListener('click', function() { setTimeout(run, 120); });
      setTimeout(run, 250);
      setTimeout(run, 900);
      setTimeout(run, 1800);
    })();
    </script>
    <?php
}, 2147482500);
/* PRIME_DROP_CLIENT_DOCX_8_ITEMS_END */
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

    # Fallback: visit common LiteSpeed purge endpoint if present in admin bar later.
    return purged


def main():
    session = requests.Session()
    session.trust_env = False
    session.headers.update({"User-Agent": "PrimeDropClientDocx8Items/1.0"})
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
    backup = Path("wp-backups") / f"functions_before_client_docx_8_items_{datetime.now():%Y%m%d_%H%M%S}.php"
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
        timeout=60,
        allow_redirects=True,
    )
    if response.status_code >= 400:
        raise RuntimeError(f"Update failed: {response.status_code}")

    print(f"updated=true backup={backup} purged={purge_cache(session)}")


if __name__ == "__main__":
    main()
