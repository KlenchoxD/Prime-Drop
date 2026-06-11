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

MARKER_START = "/* PRIME_DROP_FINAL_FOOTER_HEADER_LAYOUT_START */"
MARKER_END = "/* PRIME_DROP_FINAL_FOOTER_HEADER_LAYOUT_END */"

BLOCK = r"""
/* PRIME_DROP_FINAL_FOOTER_HEADER_LAYOUT_START */
add_action('wp_footer', function() {
    ?>
    <style id="prime-drop-final-footer-header-layout-css">
    body,
    body * {
      font-family: 'Roboto Serif', Georgia, serif !important;
    }

    @media (min-width: 1000px) {
      [data-header*="type-1"] {
        --header-height: 124px !important;
        --header-sticky-height: 0px !important;
        --header-sticky-offset: 0px !important;
      }

      body[data-header*="sticky"] {
        --header-sticky-height: 0px !important;
        --header-sticky-offset: 0px !important;
      }

      #header,
      #header.ct-header {
        position: relative !important;
        top: auto !important;
        transform: none !important;
        display: block !important;
        height: 124px !important;
        min-height: 124px !important;
        max-height: 124px !important;
        background: #ffffff !important;
      }

      #header [data-device="desktop"],
      #header .ct-sticky-container,
      #header [data-sticky] {
        position: static !important;
        top: auto !important;
        transform: none !important;
        display: block !important;
        height: 124px !important;
        min-height: 124px !important;
        max-height: 124px !important;
        background: #ffffff !important;
      }

      #header [data-device="desktop"] [data-row="middle"] {
        --height: 124px !important;
        min-height: 124px !important;
        height: 124px !important;
        max-height: 124px !important;
        background: #ffffff !important;
      }

      #header [data-device="desktop"] .ct-container {
        position: relative !important;
        display: grid !important;
        grid-template-columns: 1fr auto 1fr !important;
        grid-template-rows: 54px 44px !important;
        align-items: center !important;
        height: 124px !important;
        min-height: 124px !important;
        max-height: 124px !important;
        padding: 0 16px !important;
        column-gap: 16px !important;
        row-gap: 0 !important;
      }

      #header [data-device="desktop"] [data-column="start"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: auto !important;
        grid-column: 2 !important;
        grid-row: 1 !important;
      }

      #header [data-device="desktop"] [data-id="logo"] {
        display: flex !important;
        justify-content: center !important;
        width: auto !important;
        z-index: 3 !important;
      }

      #header [data-device="desktop"] [data-column="middle"] {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        grid-column: 1 / 4 !important;
        grid-row: 2 !important;
      }

      #header [data-device="desktop"] [data-id="menu"] {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        z-index: 2 !important;
        grid-column: 1 / 4 !important;
        grid-row: 2 !important;
      }

      #header [data-device="desktop"] .header-menu-1 {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        z-index: 4 !important;
        grid-column: 1 / 4 !important;
        grid-row: 2 !important;
      }

      #header [data-device="desktop"] [data-column="end"] {
        display: flex !important;
        justify-content: flex-end !important;
        grid-column: 3 !important;
        grid-row: 1 !important;
        align-self: start !important;
      }

      #header [data-device="desktop"] [data-id="menu"] {
        --menu-items-spacing: 70px !important;
      }

      #header [data-device="desktop"] .header-menu-1 > ul,
      #header [data-device="desktop"] .header-menu-1 .menu {
        justify-content: center !important;
        gap: 70px !important;
        width: auto !important;
      }

      #header [data-device="desktop"] .header-menu-1 .menu > li,
      #header [data-device="desktop"] .header-menu-1 > ul > li {
        margin: 0 !important;
      }

      #header [data-device="desktop"] .site-branding,
      #header [data-device="desktop"] .site-logo-container {
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        text-align: left !important;
        width: 190px !important;
        min-width: 190px !important;
      }

      #header [data-device="desktop"] .site-logo-container {
        display: block !important;
        width: 100% !important;
        min-width: 0 !important;
      }

      #header [data-device="desktop"] .site-logo-container img {
        display: block !important;
        opacity: 1 !important;
        width: 100% !important;
        height: auto !important;
      }

      #header [data-device="desktop"] .site-logo-container::before {
        content: none !important;
        display: none !important;
      }

      #header [data-device="desktop"] .site-branding .site-title,
      #header [data-device="desktop"] .site-branding .site-title-text,
      #header [data-device="desktop"] .site-branding > a:not(.site-logo-container) {
        display: none !important;
      }

      @media (max-width: 689.98px) {
        #header [data-device="desktop"] .site-branding {
          width: 130px !important;
          min-width: 130px !important;
        }
      }

      #header [data-device="desktop"] .header-menu-1 .ct-menu-link {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        line-height: 1 !important;
      }
    }

    body.page-id-14 .pd-products-title,
    body.home .pd-products-title {
      display: none !important;
    }

    body.page-id-14 .pd-story-logo {
      width: clamp(260px, 22vw, 320px) !important;
      max-width: 100% !important;
      height: auto !important;
      margin: 38px auto 0 !important;
      display: block !important;
      object-fit: contain !important;
    }

    body.page-id-14 .pd-instagram-feed {
      width: min(1224px, calc(100vw - 64px)) !important;
      margin: 0 auto 76px !important;
      padding-top: 0 !important;
      text-align: center !important;
      overflow: hidden !important;
    }

    body.page-id-14 .pd-instagram-feed h2 {
      display: none !important;
    }

    body.page-id-14 .pd-instagram-grid {
      display: grid !important;
      grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
      gap: 24px !important;
      align-items: start !important;
      width: 100% !important;
    }

    body.page-id-14 .pd-instagram-grid a:nth-child(n+4) {
      display: none !important;
    }

    body.page-id-14 .pd-instagram-grid a {
      display: block !important;
      width: 100% !important;
      aspect-ratio: 4 / 5 !important;
      min-height: clamp(420px, 48vw, 650px) !important;
      border-radius: 0 !important;
      overflow: hidden !important;
      background: #ffffff !important;
    }

    body.page-id-14 .pd-instagram-grid img,
    body.page-id-14 .pd-instagram-grid video {
      width: 100% !important;
      height: 100% !important;
      aspect-ratio: 4 / 5 !important;
      min-height: clamp(420px, 48vw, 650px) !important;
      object-fit: cover !important;
      object-position: center center !important;
      display: block !important;
      border-radius: 0 !important;
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

    body.page-id-14 .elementor-element-741b26a a.button,
    body.home .elementor-element-741b26a a.button {
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      visibility: visible !important;
      opacity: 1 !important;
      min-width: 180px !important;
      max-width: calc(100% - 28px) !important;
      min-height: 42px !important;
      margin: 0 auto !important;
      padding: 11px 24px !important;
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
      position: static !important;
      transform: none !important;
    }

    .pd-footer {
      background: #000000 !important;
      color: #ffffff !important;
      padding: clamp(58px, 7vw, 88px) 0 28px !important;
      overflow: hidden !important;
    }

    .pd-footer-final-main {
      width: min(1224px, calc(100vw - 140px)) !important;
      margin: 0 auto !important;
      display: grid !important;
      grid-template-columns: minmax(260px, 1fr) minmax(230px, .8fr) minmax(320px, 1fr) !important;
      column-gap: clamp(62px, 9vw, 150px) !important;
      align-items: start !important;
      text-align: left !important;
    }

    .pd-footer-final h3,
    .pd-footer-final h4 {
      margin: 0 0 18px !important;
      color: #ffffff !important;
      font-family: 'Roboto Serif', Georgia, serif !important;
      font-weight: 800 !important;
      letter-spacing: .4px !important;
      text-transform: uppercase !important;
    }

    .pd-footer-final h3 {
      font-size: clamp(24px, 2vw, 30px) !important;
      line-height: 1.05 !important;
    }

    .pd-footer-final h4 {
      font-size: 15px !important;
      line-height: 1.25 !important;
    }

    .pd-footer-final p,
    .pd-footer-final a {
      color: #ffffff !important;
      font-family: 'Roboto Serif', Georgia, serif !important;
      font-size: 15px !important;
      line-height: 1.45 !important;
      text-decoration: none !important;
    }

    .pd-footer-final-brand p {
      max-width: 330px !important;
      margin: 0 0 26px !important;
    }

    .pd-footer-final-policies {
      display: grid !important;
      gap: 8px !important;
    }

    .pd-footer-final-policies-wrap {
      align-self: start !important;
    }

    .pd-brand-filter a {
      text-transform: uppercase !important;
      font-weight: 400 !important;
      color: #1a1a1a !important;
    }

    .pd-brand-filter a:hover,
    .pd-brand-filter a:focus {
      color: #1a1a1a !important;
      font-weight: 900 !important;
      background: transparent !important;
    }

    .pd-footer-final-socials {
      display: flex !important;
      align-items: center !important;
      gap: 14px !important;
      margin: 0 0 28px !important;
    }

    .pd-footer-final-socials a {
      width: 36px !important;
      height: 36px !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      border: 1px solid rgba(255,255,255,.46) !important;
      border-radius: 50% !important;
      background: transparent !important;
    }

    .pd-footer-final-socials svg {
      width: 18px !important;
      height: 18px !important;
      fill: #ffffff !important;
    }

    .pd-footer-final-newsletter p {
      margin: 0 0 10px !important;
      color: rgba(255,255,255,.86) !important;
      font-size: 15px !important;
    }

    .pd-footer-final-newsletter .pd-newsletter-disclaimer {
      margin: 12px 0 0 !important;
      color: rgba(255,255,255,.86) !important;
      font-size: 13px !important;
      line-height: 1.6 !important;
    }

    .pd-footer-final-newsletter form {
      display: grid !important;
      gap: 14px !important;
      max-width: 470px !important;
    }

    .pd-footer-final-newsletter label,
    .pd-footer-final-newsletter label span {
      display: block !important;
      width: 100% !important;
    }

    .pd-footer-final-newsletter input {
      width: 100% !important;
      min-height: 52px !important;
      border: 1px solid rgba(255,255,255,.5) !important;
      border-radius: 8px !important;
      background: #ffffff !important;
      color: #0d141a !important;
      padding: 0 12px !important;
      font-family: 'Roboto Serif', Georgia, serif !important;
      font-size: 13px !important;
      box-shadow: none !important;
      box-sizing: border-box !important;
      text-overflow: clip !important;
    }

    .pd-footer-final-newsletter input::placeholder {
      color: #777777 !important;
      opacity: 1 !important;
      font-size: 13px !important;
    }

    .pd-footer-final-newsletter button {
      width: 184px !important;
      min-height: 48px !important;
      border: 1px solid #ffffff !important;
      border-radius: 28px !important;
      background: #0d141a !important;
      color: #ffffff !important;
      font-family: 'Roboto Serif', Georgia, serif !important;
      font-size: 13px !important;
      font-weight: 700 !important;
      text-transform: uppercase !important;
      cursor: pointer !important;
    }

    .pd-footer-final-bottom {
      width: min(1224px, calc(100vw - 140px)) !important;
      margin: 72px auto 0 !important;
      display: grid !important;
      gap: 10px !important;
      text-align: left !important;
    }

    .pd-footer-final-bottom p,
    .pd-footer-final-bottom a {
      margin: 0 !important;
      color: #ffffff !important;
      font-size: 13px !important;
    }

    .pd-footer-final-bottom a {
      text-decoration: underline !important;
    }

    .pd-footer-final-bottom::before {
      content: none !important;
      display: none !important;
    }

    .pd-cart-drawer,
    .pd-cart-drawer *,
    .ct-cart-content,
    .ct-cart-content * {
      font-family: 'Roboto Serif', Georgia, serif !important;
    }

    @media (max-width: 900px) {
      .pd-footer-final-main,
      .pd-footer-final-bottom {
        width: min(100%, calc(100vw - 44px)) !important;
      }

      .pd-footer-final-main {
        grid-template-columns: 1fr !important;
        row-gap: 34px !important;
      }

      .pd-footer-final-newsletter form {
        max-width: 100% !important;
      }

      .pd-footer-final-bottom {
        margin-top: 56px !important;
      }

      body.page-id-14 .pd-instagram-feed {
        width: min(100%, calc(100vw - 28px)) !important;
      }

      body.page-id-14 .pd-instagram-grid {
        display: flex !important;
        gap: 16px !important;
        overflow: hidden !important;
      }

      body.page-id-14 .pd-instagram-grid a {
        flex: 0 0 78vw !important;
      }

      body.page-id-14 .pd-instagram-grid img,
      body.page-id-14 .pd-instagram-grid video {
        min-height: 96vw !important;
      }
    }
    </style>
    <script id="prime-drop-final-footer-header-layout-js">
    (function() {
      function icon(kind) {
        var icons = {
          instagram: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7.8 2h8.4A5.8 5.8 0 0 1 22 7.8v8.4a5.8 5.8 0 0 1-5.8 5.8H7.8A5.8 5.8 0 0 1 2 16.2V7.8A5.8 5.8 0 0 1 7.8 2Zm0 2A3.8 3.8 0 0 0 4 7.8v8.4A3.8 3.8 0 0 0 7.8 20h8.4a3.8 3.8 0 0 0 3.8-3.8V7.8A3.8 3.8 0 0 0 16.2 4H7.8Zm4.2 3.4A4.6 4.6 0 1 1 12 16.6 4.6 4.6 0 0 1 12 7.4Zm0 2A2.6 2.6 0 1 0 14.6 12 2.6 2.6 0 0 0 12 9.4ZM17 6.8a1.1 1.1 0 1 1-1.1 1.1A1.1 1.1 0 0 1 17 6.8Z"/></svg>',
          tiktok: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15.6 2c.4 3 2.1 4.8 5 5.1v3.3a8 8 0 0 1-4.8-1.6v6.8A6.4 6.4 0 1 1 9.4 9.2c.5 0 .9.1 1.4.2v3.5a3 3 0 1 0 1.7 2.7V2h3.1Z"/></svg>',
          whatsapp: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a9.8 9.8 0 0 0-8.4 14.9L2.3 22l5.3-1.4A9.8 9.8 0 1 0 12 2Zm0 2a7.8 7.8 0 0 1 0 15.6 7.6 7.6 0 0 1-3.9-1.1l-.4-.2-2.5.7.7-2.4-.3-.4A7.8 7.8 0 0 1 12 4Zm-3.1 4.2c-.2 0-.5.1-.7.4-.3.3-.9.9-.9 2.1s.9 2.4 1 2.6c.1.2 1.8 2.9 4.4 4 .6.2 1 .4 1.4.4.6.2 1.1.1 1.5.1.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.1-1.2-.1-.1-.2-.2-.5-.4l-1.7-.8c-.2-.1-.4-.1-.6.2l-.8 1c-.1.2-.3.2-.5.1-1.4-.6-2.4-1.5-3.1-2.8-.1-.2 0-.4.1-.5l.4-.5c.1-.2.2-.3.3-.5.1-.2.1-.4 0-.6l-.8-1.9c-.2-.4-.4-.4-.6-.4h-.7Z"/></svg>',
          gmail: '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M6 12h36v24H6z" fill="none"/><path d="M8 14l16 12L40 14v20H8V14Z" fill="#fff"/><path d="M8 14l16 12 16-12" fill="none" stroke="#000" stroke-width="4" stroke-linejoin="round"/></svg>'
        };
        return icons[kind] || '';
      }

      function social(url, label, kind) {
        return '<a href="' + url + '" target="_blank" rel="noopener" aria-label="' + label + '">' + icon(kind) + '</a>';
      }

      function arrangeFooter() {
        var footer = document.querySelector('.pd-footer');
        if (!footer) return;
        footer.classList.add('pd-footer-final');
        footer.innerHTML =
          '<div class="pd-footer-final-main">' +
            '<div class="pd-footer-final-brand">' +
              '<h3>PRIME DROP</h3>' +
              '<p>Descubre nuestra tienda de bolsos, donde traemos lo mejor de las ultimas tendencias importadas desde Estados Unidos.</p>' +
              '<div class="pd-footer-final-socials">' +
                social('https://www.instagram.com/primedrop_elite/', 'Instagram', 'instagram') +
                social('https://www.tiktok.com/@primedrop_elite', 'TikTok', 'tiktok') +
                social('https://wa.me/573160685555', 'WhatsApp', 'whatsapp') +
                social('mailto:primedropelite@gmail.com', 'Gmail', 'gmail') +
              '</div>' +
            '</div>' +
            '<div class="pd-footer-final-policies-wrap">' +
              '<h4>POLÍTICAS</h4>' +
              '<div class="pd-footer-final-policies">' +
                '<a href="/terminos-y-condiciones/">Términos y condiciones</a>' +
                '<a href="/politica-de-privacidad/">Política de Privacidad</a>' +
                '<a href="/politica-de-reembolso/">Política de Reembolso</a>' +
              '</div>' +
            '</div>' +
            '<div class="pd-footer-final-newsletter">' +
              '<h4>ÚNETE A PRIME DROP</h4>' +
              '<form><label><span>Recibe ofertas exclusivas y novedades</span><input type="email" placeholder="Introducir dirección de correo electrónico" aria-label="Correo electrónico"></label><button type="submit">REGISTRARSE</button></form>' +
            '</div>' +
          '</div>' +
          '<div class="pd-footer-final-bottom">' +
            '<p>© 2026 Prime Drop Elite. Todos los derechos reservados.</p>' +
          '</div>';
      }

      function restoreFeaturedButtons() {
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

      function fixCartEmptyText() {
        document.querySelectorAll('.pd-cart-drawer, .ct-cart-content, .cart-drawer, [class*="cart"]').forEach(function(scope) {
          scope.querySelectorAll('p, div, span, h2, h3').forEach(function(el) {
            var text = (el.textContent || '').replace(/\s+/g, ' ').trim();
            if (text === 'El carrito de compras está vacío' || text === 'El carrito de compras esta vacio') {
              el.textContent = 'La bolsa de compras está vacía';
            }
          });
        });
      }

      function tuneHomeSections() {
        document.querySelectorAll('body.page-id-14 .pd-products-title, body.home .pd-products-title').forEach(function(el) {
          el.style.setProperty('display', 'none', 'important');
        });
        var storyLogo = document.querySelector('body.page-id-14 .pd-story-logo');
        if (storyLogo) {
          storyLogo.style.setProperty('margin-left', 'auto', 'important');
          storyLogo.style.setProperty('margin-right', 'auto', 'important');
        }
        document.querySelectorAll('body.page-id-14 .pd-instagram-feed h2').forEach(function(el) {
          el.remove();
        });
        document.querySelectorAll('body.page-id-14 .pd-instagram-grid a:nth-child(n+4)').forEach(function(el) {
          el.remove();
        });
        document.querySelectorAll('body.page-id-14 .pd-instagram-grid video').forEach(function(video) {
          video.setAttribute('autoplay', '');
          video.setAttribute('muted', '');
          video.muted = true;
          video.setAttribute('loop', '');
          video.setAttribute('playsinline', '');
          video.setAttribute('preload', 'metadata');
          if (!video.getAttribute('poster')) {
            video.setAttribute('poster', 'https://primedropelite.com/wp-content/uploads/2026/06/SaveClip.App_587104948_17864405985517476_4398825993832880462_n.jpg');
          }
        });
      }

      function disableStickyHeader() {
        document.querySelectorAll('[data-header*="type-1"]').forEach(function(el) {
          el.style.setProperty('--header-height', '124px', 'important');
          el.style.setProperty('--header-sticky-height', '0px', 'important');
          el.style.setProperty('--header-sticky-offset', '0px', 'important');
        });
        document.querySelectorAll('#header [data-sticky]').forEach(function(el) {
          el.removeAttribute('data-sticky');
          el.style.setProperty('position', 'static', 'important');
          el.style.setProperty('transform', 'none', 'important');
          el.style.setProperty('top', 'auto', 'important');
          el.style.setProperty('height', '124px', 'important');
          el.style.setProperty('min-height', '124px', 'important');
          el.style.setProperty('max-height', '124px', 'important');
        });
        document.querySelectorAll('#header .ct-sticky-container').forEach(function(el) {
          el.style.setProperty('position', 'static', 'important');
          el.style.setProperty('transform', 'none', 'important');
          el.style.setProperty('top', 'auto', 'important');
          el.style.setProperty('height', '124px', 'important');
          el.style.setProperty('min-height', '124px', 'important');
          el.style.setProperty('max-height', '124px', 'important');
        });
        document.querySelectorAll('#header.ct-header, #header').forEach(function(el) {
          el.style.setProperty('position', 'relative', 'important');
          el.style.setProperty('transform', 'none', 'important');
          el.style.setProperty('top', 'auto', 'important');
          el.style.setProperty('height', '124px', 'important');
          el.style.setProperty('min-height', '124px', 'important');
          el.style.setProperty('max-height', '124px', 'important');
        });
        document.body.removeAttribute('data-header-sticky');
      }

      function patchBrandLogo() {
        var logoSrc = 'https://primedropelite.com/wp-content/uploads/2026/05/LOGO-NEGRO.png';
        [
          { id: 'brand-logo-mobile', w: '132px', h: '34px' },
          { id: 'brand-logo-desktop', w: '172px', h: '44px' }
        ].forEach(function(item) {
          var el = document.getElementById(item.id);
          if (!el) return;
          el.setAttribute('aria-label', 'Prime Drop');
          el.innerHTML = '<img src="' + logoSrc + '" alt="Prime Drop" style="display:block;width:' + item.w + ';height:' + item.h + ';object-fit:contain;">';
        });
      }

      function run() {
        disableStickyHeader();
        patchBrandLogo();
        arrangeFooter();
        restoreFeaturedButtons();
        fixCartEmptyText();
        tuneHomeSections();
      }

      run();
      document.addEventListener('DOMContentLoaded', run);
      window.addEventListener('pageshow', run);
      window.addEventListener('scroll', disableStickyHeader, { passive: true });
      setTimeout(run, 300);
      setTimeout(run, 1200);
      setTimeout(run, 2600);
      setInterval(patchBrandLogo, 800);
      new MutationObserver(patchBrandLogo).observe(document.documentElement, { childList: true, subtree: true });
    })();
    </script>
    <?php
}, 100000);
/* PRIME_DROP_FINAL_FOOTER_HEADER_LAYOUT_END */
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
    session.headers.update({"User-Agent": "PrimeDropFinalFooterHeaderLayout/1.0"})
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
    backup = Path("wp-backups") / f"functions_before_final_footer_header_layout_{datetime.now():%Y%m%d_%H%M%S}.php"
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
