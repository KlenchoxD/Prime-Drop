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

MARKER_START = "/* PRIME_DROP_CATEGORY_SEARCH_CART_EMPTY_FIXES_START */"
MARKER_END = "/* PRIME_DROP_CATEGORY_SEARCH_CART_EMPTY_FIXES_END */"

BLOCK = r"""
/* PRIME_DROP_CATEGORY_SEARCH_CART_EMPTY_FIXES_START */
add_filter('woocommerce_return_to_shop_redirect', function() {
    return home_url('/');
}, 99);

add_filter('woocommerce_return_to_shop_text', function() {
    return 'Volver al inicio';
}, 99);

add_filter('wc_empty_cart_message', function() {
    return 'Tu bolsa de compra está vacía.';
}, 99);

add_action('wp_head', function() {
    ?>
    <style id="prime-drop-category-search-cart-empty-fixes-css">
    /* Productos: eliminar cuadros/fondos que se ven como parches blancos */
    body.page-id-14 ul.products li.product,
    body.page-id-547 ul.products li.product,
    body.tax-product_cat ul.products li.product {
      background: transparent !important;
      box-shadow: none !important;
      border: 0 !important;
    }

    body.page-id-14 .woocommerce ul.products li.product figure,
    body.page-id-14 .woocommerce ul.products li.product .ct-media-container,
    body.page-id-14 .woocommerce ul.products li.product a.ct-media-container,
    body.page-id-14 ul.products li.product a.woocommerce-loop-product__link,
    body.page-id-547 .woocommerce ul.products li.product figure,
    body.tax-product_cat .woocommerce ul.products li.product figure,
    body.page-id-547 .woocommerce ul.products li.product .ct-media-container,
    body.tax-product_cat .woocommerce ul.products li.product .ct-media-container,
    body.page-id-547 .woocommerce ul.products li.product a.ct-media-container,
    body.tax-product_cat .woocommerce ul.products li.product a.ct-media-container,
    body.page-id-547 ul.products li.product a.woocommerce-loop-product__link,
    body.tax-product_cat ul.products li.product a.woocommerce-loop-product__link {
      background: #f5f5f5 !important;
      background-color: #f5f5f5 !important;
      border: 0 !important;
      box-shadow: none !important;
      outline: 0 !important;
      border-radius: 0 !important;
    }

    body.page-id-14 .woocommerce ul.products li.product img,
    body.page-id-14 .woocommerce ul.products li.product a img,
    body.page-id-547 .woocommerce ul.products li.product img,
    body.tax-product_cat .woocommerce ul.products li.product img,
    body.page-id-547 .woocommerce ul.products li.product a img,
    body.tax-product_cat .woocommerce ul.products li.product a img {
      background: transparent !important;
      background-color: transparent !important;
      box-shadow: none !important;
      border: 0 !important;
      object-fit: contain !important;
      object-position: center center !important;
      mix-blend-mode: multiply !important;
    }

    body.page-id-14.woocommerce-page ul.products.products li.product figure,
    body.page-id-14.woocommerce-page ul.products.products li.product .ct-media-container,
    body.page-id-14.woocommerce-page ul.products.products li.product a.ct-media-container,
    body.page-id-14 ul.products.products li.product figure,
    body.page-id-14 ul.products.products li.product .ct-media-container,
    body.page-id-14 ul.products.products li.product a.ct-media-container,
    body.page-id-547.woocommerce-page ul.products.products li.product figure,
    body.page-id-547.woocommerce-page ul.products.products li.product .ct-media-container,
    body.page-id-547.woocommerce-page ul.products.products li.product a.ct-media-container,
    body.tax-product_cat.woocommerce ul.products.products li.product figure,
    body.tax-product_cat.woocommerce ul.products.products li.product .ct-media-container,
    body.tax-product_cat.woocommerce ul.products.products li.product a.ct-media-container,
    body.tax-product_cat.woocommerce-page ul.products.products li.product figure,
    body.tax-product_cat.woocommerce-page ul.products.products li.product .ct-media-container,
    body.tax-product_cat.woocommerce-page ul.products.products li.product a.ct-media-container {
      background: #f5f5f5 !important;
      background-color: #f5f5f5 !important;
      box-shadow: none !important;
      border-color: transparent !important;
    }

    body.page-id-14.woocommerce-page ul.products.products li.product figure img,
    body.page-id-14.woocommerce-page ul.products.products li.product img,
    body.page-id-14 ul.products.products li.product figure img,
    body.page-id-14 ul.products.products li.product img,
    body.page-id-547.woocommerce-page ul.products.products li.product figure img,
    body.page-id-547.woocommerce-page ul.products.products li.product img,
    body.tax-product_cat.woocommerce ul.products.products li.product figure img,
    body.tax-product_cat.woocommerce ul.products.products li.product img,
    body.tax-product_cat.woocommerce-page ul.products.products li.product figure img,
    body.tax-product_cat.woocommerce-page ul.products.products li.product img {
      background: transparent !important;
      background-color: transparent !important;
      mix-blend-mode: multiply !important;
      box-shadow: none !important;
      border-color: transparent !important;
    }

    body.page-id-14 .woocommerce ul.products,
    body.page-id-547 .woocommerce ul.products,
    body.tax-product_cat .woocommerce ul.products,
    body.post-type-archive-product .woocommerce ul.products {
      align-items: stretch !important;
    }

    body.page-id-14 .woocommerce ul.products li.product,
    body.page-id-547 .woocommerce ul.products li.product,
    body.tax-product_cat .woocommerce ul.products li.product,
    body.post-type-archive-product .woocommerce ul.products li.product {
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      justify-content: flex-start !important;
      min-height: 0 !important;
      height: auto !important;
      text-align: center !important;
    }

    body.page-id-14 .woocommerce ul.products li.product figure,
    body.page-id-547 .woocommerce ul.products li.product figure,
    body.tax-product_cat .woocommerce ul.products li.product figure,
    body.post-type-archive-product .woocommerce ul.products li.product figure {
      width: 100% !important;
      margin: 0 0 16px !important;
      padding: 0 !important;
      background: #f5f5f5 !important;
      background-color: #f5f5f5 !important;
      overflow: hidden !important;
      border: 0 !important;
      box-shadow: none !important;
    }

    body.page-id-14 .woocommerce ul.products li.product figure > a.ct-media-container,
    body.page-id-547 .woocommerce ul.products li.product figure > a.ct-media-container,
    body.tax-product_cat .woocommerce ul.products li.product figure > a.ct-media-container,
    body.post-type-archive-product .woocommerce ul.products li.product figure > a.ct-media-container {
      width: 100% !important;
      aspect-ratio: 4 / 5 !important;
      height: auto !important;
      min-height: 0 !important;
      max-height: none !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      background: #f5f5f5 !important;
      background-color: #f5f5f5 !important;
      overflow: hidden !important;
    }

    body.page-id-14 .woocommerce ul.products li.product figure img,
    body.page-id-14 .woocommerce ul.products li.product a img,
    body.page-id-14 .woocommerce ul.products li.product img,
    body.page-id-547 .woocommerce ul.products li.product figure img,
    body.page-id-547 .woocommerce ul.products li.product a img,
    body.page-id-547 .woocommerce ul.products li.product img,
    body.tax-product_cat .woocommerce ul.products li.product figure img,
    body.tax-product_cat .woocommerce ul.products li.product a img,
    body.tax-product_cat .woocommerce ul.products li.product img,
    body.post-type-archive-product .woocommerce ul.products li.product figure img,
    body.post-type-archive-product .woocommerce ul.products li.product a img,
    body.post-type-archive-product .woocommerce ul.products li.product img {
      width: 100% !important;
      height: 100% !important;
      min-height: 0 !important;
      max-height: none !important;
      aspect-ratio: auto !important;
      object-fit: contain !important;
      object-position: center center !important;
      margin: 0 !important;
      padding: 24px 18px 18px !important;
      background: transparent !important;
      background-color: transparent !important;
      border: 0 !important;
      border-radius: 0 !important;
      box-shadow: none !important;
      display: block !important;
      box-sizing: border-box !important;
      transform: none !important;
      filter: none !important;
      mix-blend-mode: multiply !important;
    }

    body.page-id-14 .woocommerce ul.products li.product .woocommerce-loop-product__title,
    body.page-id-547 .woocommerce ul.products li.product .woocommerce-loop-product__title,
    body.tax-product_cat .woocommerce ul.products li.product .woocommerce-loop-product__title,
    body.post-type-archive-product .woocommerce ul.products li.product .woocommerce-loop-product__title {
      width: 100% !important;
      min-height: 54px !important;
      display: flex !important;
      align-items: flex-start !important;
      justify-content: center !important;
      text-align: center !important;
    }

    body.page-id-14 .woocommerce ul.products li.product .price,
    body.page-id-547 .woocommerce ul.products li.product .price,
    body.tax-product_cat .woocommerce ul.products li.product .price,
    body.post-type-archive-product .woocommerce ul.products li.product .price {
      width: 100% !important;
      min-height: 24px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      text-align: center !important;
      white-space: nowrap !important;
    }

    body.page-id-14 .woocommerce ul.products li.product .button,
    body.page-id-547 .woocommerce ul.products li.product .button,
    body.tax-product_cat .woocommerce ul.products li.product .button,
    body.post-type-archive-product .woocommerce ul.products li.product .button {
      margin-top: auto !important;
      align-self: center !important;
    }

    body.page-id-547 .woocommerce ul.products li.product .price,
    body.tax-product_cat .woocommerce ul.products li.product .price,
    body.page-id-547 ul.products li.product .price,
    body.tax-product_cat ul.products li.product .price {
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      min-height: 24px !important;
      color: #000000 !important;
      font-family: 'Roboto Serif', serif !important;
      font-size: 13px !important;
      font-weight: 700 !important;
      line-height: 1.25 !important;
      text-align: center !important;
      white-space: nowrap !important;
      opacity: 1 !important;
      visibility: visible !important;
    }

    /* Buscador centrado para todos los listados y categorias */
    body.page-id-547 .woo-listing-top,
    body.tax-product_cat .woo-listing-top,
    body.woocommerce-shop .woo-listing-top,
    body.post-type-archive-product .woo-listing-top {
      display: grid !important;
      grid-template-columns: minmax(160px, 1fr) minmax(260px, 430px) minmax(160px, 1fr) !important;
      grid-template-areas: "count search order" !important;
      gap: 24px !important;
      align-items: center !important;
      width: 100% !important;
    }

    body.page-id-547 .woo-listing-top .woocommerce-result-count,
    body.tax-product_cat .woo-listing-top .woocommerce-result-count,
    body.woocommerce-shop .woo-listing-top .woocommerce-result-count,
    body.post-type-archive-product .woo-listing-top .woocommerce-result-count {
      grid-area: count !important;
      margin: 0 !important;
      justify-self: start !important;
    }

    body.page-id-547 .pd-shop-search,
    body.tax-product_cat .pd-shop-search,
    body.woocommerce-shop .pd-shop-search,
    body.post-type-archive-product .pd-shop-search {
      grid-area: search !important;
      width: min(100%, 430px) !important;
      margin: 0 auto !important;
      justify-self: center !important;
      display: block !important;
    }

    body.woocommerce.woocommerce-page.tax-product_cat .woo-listing-top > div.pd-shop-search,
    body.archive.tax-product_cat .woo-listing-top > div.pd-shop-search,
    body.page-id-547 .woo-listing-top > div.pd-shop-search {
      display: block !important;
      visibility: visible !important;
      opacity: 1 !important;
      height: auto !important;
      overflow: visible !important;
      pointer-events: auto !important;
    }

    body.page-id-547 .pd-shop-search form,
    body.tax-product_cat .pd-shop-search form,
    body.woocommerce-shop .pd-shop-search form,
    body.post-type-archive-product .pd-shop-search form {
      width: 100% !important;
      height: 46px !important;
      display: flex !important;
      align-items: center !important;
      background: #ffffff !important;
      border: 0 !important;
      border-radius: 25px !important;
      overflow: hidden !important;
      box-shadow: 0 8px 24px rgba(0,0,0,.08), inset 0 0 0 1px rgba(0,0,0,.08) !important;
    }

    body.page-id-547 .pd-shop-search input[type="search"],
    body.tax-product_cat .pd-shop-search input[type="search"],
    body.woocommerce-shop .pd-shop-search input[type="search"],
    body.post-type-archive-product .pd-shop-search input[type="search"] {
      height: 46px !important;
      flex: 1 1 auto !important;
      min-width: 0 !important;
      border: 0 !important;
      outline: 0 !important;
      box-shadow: none !important;
      background: transparent !important;
      color: #111111 !important;
      padding: 0 20px !important;
      font-family: 'Roboto Serif', serif !important;
      font-size: 13.5px !important;
    }

    body.page-id-547 .pd-shop-search button[type="submit"],
    body.tax-product_cat .pd-shop-search button[type="submit"],
    body.woocommerce-shop .pd-shop-search button[type="submit"],
    body.post-type-archive-product .pd-shop-search button[type="submit"] {
      width: 46px !important;
      height: 46px !important;
      min-width: 46px !important;
      padding: 0 !important;
      border: 0 !important;
      border-radius: 50% !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      background: #000000 !important;
      color: #ffffff !important;
      box-shadow: none !important;
    }

    body.page-id-547 .pd-shop-search input[type="search"]::placeholder,
    body.tax-product_cat .pd-shop-search input[type="search"]::placeholder,
    body.woocommerce-shop .pd-shop-search input[type="search"]::placeholder,
    body.post-type-archive-product .pd-shop-search input[type="search"]::placeholder {
      color: #8b8b8b !important;
      opacity: 1 !important;
    }

    body.page-id-547 .pd-shop-search form:focus-within,
    body.tax-product_cat .pd-shop-search form:focus-within,
    body.woocommerce-shop .pd-shop-search form:focus-within,
    body.post-type-archive-product .pd-shop-search form:focus-within {
      box-shadow: 0 10px 28px rgba(0,0,0,.12), inset 0 0 0 1px #000000 !important;
    }

    body.page-id-547 .pd-shop-search button[type="submit"] svg,
    body.tax-product_cat .pd-shop-search button[type="submit"] svg,
    body.woocommerce-shop .pd-shop-search button[type="submit"] svg,
    body.post-type-archive-product .pd-shop-search button[type="submit"] svg {
      width: 15px !important;
      height: 15px !important;
      stroke: currentColor !important;
    }

    body.page-id-547 .woo-listing-top .woocommerce-ordering,
    body.tax-product_cat .woo-listing-top .woocommerce-ordering,
    body.woocommerce-shop .woo-listing-top .woocommerce-ordering,
    body.post-type-archive-product .woo-listing-top .woocommerce-ordering {
      grid-area: order !important;
      justify-self: end !important;
      margin: 0 !important;
      width: 240px !important;
      position: relative !important;
      display: flex !important;
      align-items: center !important;
    }

    /* Orden por defecto: seleccionado y opciones centradas */
    body.page-id-547 .woocommerce-ordering select.orderby,
    body.tax-product_cat .woocommerce-ordering select.orderby,
    body.woocommerce-shop .woocommerce-ordering select.orderby,
    body.post-type-archive-product .woocommerce-ordering select.orderby {
      width: 100% !important;
      height: 44px !important;
      border: 0 !important;
      border-radius: 25px !important;
      background-color: #000000 !important;
      color: #ffffff !important;
      font-family: 'Roboto Serif', serif !important;
      font-size: 12px !important;
      font-weight: 700 !important;
      letter-spacing: .6px !important;
      text-transform: uppercase !important;
      text-align: center !important;
      text-align-last: center !important;
      -moz-text-align-last: center !important;
      appearance: none !important;
      -webkit-appearance: none !important;
      -moz-appearance: none !important;
      padding: 0 42px !important;
      line-height: 44px !important;
      cursor: pointer !important;
      box-shadow: none !important;
    }

    body.page-id-547 .woocommerce-ordering select.orderby option,
    body.tax-product_cat .woocommerce-ordering select.orderby option,
    body.woocommerce-shop .woocommerce-ordering select.orderby option,
    body.post-type-archive-product .woocommerce-ordering select.orderby option {
      background: #ffffff !important;
      color: #000000 !important;
      font-family: 'Roboto Serif', serif !important;
      font-size: 13px !important;
      font-weight: 500 !important;
      text-align: center !important;
      text-align-last: center !important;
      padding: 10px 0 !important;
    }

    body.page-id-547 .woocommerce-ordering::after,
    body.tax-product_cat .woocommerce-ordering::after,
    body.woocommerce-shop .woocommerce-ordering::after,
    body.post-type-archive-product .woocommerce-ordering::after {
      content: "" !important;
      position: absolute !important;
      right: 18px !important;
      top: 50% !important;
      width: 6px !important;
      height: 6px !important;
      border-right: 1.5px solid #ffffff !important;
      border-bottom: 1.5px solid #ffffff !important;
      transform: translateY(-65%) rotate(45deg) !important;
      pointer-events: none !important;
      z-index: 3 !important;
    }

    body.page-id-547 .woocommerce-ordering .ct-sort-icon,
    body.tax-product_cat .woocommerce-ordering .ct-sort-icon,
    body.woocommerce-shop .woocommerce-ordering .ct-sort-icon,
    body.post-type-archive-product .woocommerce-ordering .ct-sort-icon {
      display: none !important;
    }

    @media (max-width: 768px) {
      body.page-id-547 .woo-listing-top,
      body.tax-product_cat .woo-listing-top,
      body.woocommerce-shop .woo-listing-top,
      body.post-type-archive-product .woo-listing-top {
        grid-template-columns: 1fr !important;
        grid-template-areas:
          "search"
          "count"
          "order" !important;
        gap: 14px !important;
      }

      body.page-id-547 .woo-listing-top .woocommerce-result-count,
      body.tax-product_cat .woo-listing-top .woocommerce-result-count,
      body.woocommerce-shop .woo-listing-top .woocommerce-result-count,
      body.post-type-archive-product .woo-listing-top .woocommerce-result-count,
      body.page-id-547 .woo-listing-top .woocommerce-ordering,
      body.tax-product_cat .woo-listing-top .woocommerce-ordering,
      body.woocommerce-shop .woo-listing-top .woocommerce-ordering,
      body.post-type-archive-product .woo-listing-top .woocommerce-ordering {
        justify-self: center !important;
      }
    }

    /* Carrito vacio */
    body.woocommerce-cart .entry-content > .woocommerce {
      max-width: 760px !important;
      margin: 40px auto 70px !important;
      padding: 0 18px !important;
      text-align: center !important;
    }

    body.woocommerce-cart .wc-empty-cart-message {
      margin: 0 !important;
    }

    body.woocommerce-cart .cart-empty.woocommerce-info {
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      min-height: 210px !important;
      padding: 38px 24px !important;
      margin: 0 0 22px !important;
      border: 1px solid rgba(0,0,0,.08) !important;
      border-radius: 18px !important;
      background: #ffffff !important;
      box-shadow: 0 18px 50px rgba(0,0,0,.06) !important;
      color: #111111 !important;
      font-family: 'Roboto Serif', serif !important;
      font-size: clamp(22px, 3vw, 34px) !important;
      font-weight: 700 !important;
      line-height: 1.2 !important;
    }

    body.woocommerce-cart .cart-empty.woocommerce-info::before {
      display: none !important;
    }

    body.woocommerce-cart p.return-to-shop {
      margin: 0 !important;
      text-align: center !important;
    }

    body.woocommerce-cart p.return-to-shop a.button.wc-backward {
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      min-width: 190px !important;
      height: 46px !important;
      padding: 0 28px !important;
      border: 1px solid #000000 !important;
      border-radius: 25px !important;
      background: #000000 !important;
      color: #ffffff !important;
      font-family: 'Roboto Serif', serif !important;
      font-size: 12px !important;
      font-weight: 700 !important;
      letter-spacing: 1px !important;
      text-transform: uppercase !important;
      text-decoration: none !important;
    }

    body.woocommerce-cart p.return-to-shop a.button.wc-backward:hover {
      background: #333333 !important;
      border-color: #333333 !important;
      color: #ffffff !important;
    }
    </style>
    <script id="prime-drop-product-card-bg-clean-js">
    (function() {
      function cleanProductCardBackgrounds() {
        document.querySelectorAll(
          'body.page-id-14 ul.products li.product figure,' +
          'body.page-id-14 ul.products li.product .ct-media-container,' +
          'body.page-id-14 ul.products li.product img,' +
          'body.page-id-547 ul.products li.product figure,' +
          'body.page-id-547 ul.products li.product .ct-media-container,' +
          'body.page-id-547 ul.products li.product img,' +
          'body.tax-product_cat ul.products li.product figure,' +
          'body.tax-product_cat ul.products li.product .ct-media-container,' +
          'body.tax-product_cat ul.products li.product img'
        ).forEach(function(el) {
          var isImg = el.tagName && el.tagName.toLowerCase() === 'img';
          el.style.setProperty('background', isImg ? 'transparent' : '#f5f5f5', 'important');
          el.style.setProperty('background-color', isImg ? 'transparent' : '#f5f5f5', 'important');
          el.style.setProperty('box-shadow', 'none', 'important');
          el.style.setProperty('border-color', 'transparent', 'important');
          if (isImg) {
            el.style.setProperty('mix-blend-mode', 'multiply', 'important');
            el.style.setProperty('object-fit', 'contain', 'important');
            el.style.setProperty('object-position', 'center center', 'important');
          }
        });

        document.querySelectorAll(
          'body.page-id-14 ul.products li.product .price,' +
          'body.page-id-547 ul.products li.product .price,' +
          'body.tax-product_cat ul.products li.product .price'
        ).forEach(function(price) {
          var amount = price.querySelector('.woocommerce-Price-amount');
          if (!amount) return;
          var text = amount.textContent.replace(/\s+/g, ' ').trim();
          if (!text) return;
          price.textContent = text.replace(/\s*COP\s*$/i, '') + ' COP';
          price.style.setProperty('display', 'block', 'important');
          price.style.setProperty('width', '100%', 'important');
          price.style.setProperty('text-align', 'center', 'important');
          price.style.setProperty('font-weight', '700', 'important');
          price.style.setProperty('visibility', 'visible', 'important');
          price.style.setProperty('opacity', '1', 'important');
        });
      }

      cleanProductCardBackgrounds();
      document.addEventListener('DOMContentLoaded', cleanProductCardBackgrounds);
      window.addEventListener('load', cleanProductCardBackgrounds);
      window.addEventListener('pageshow', cleanProductCardBackgrounds);
      setTimeout(cleanProductCardBackgrounds, 250);
      setTimeout(cleanProductCardBackgrounds, 800);
    })();
    </script>
    <?php
}, 20);
/* PRIME_DROP_CATEGORY_SEARCH_CART_EMPTY_FIXES_END */
"""


def login(session):
    login_url = urljoin(BASE, "/wp-login.php")
    page = session.get(login_url, timeout=30)
    page.raise_for_status()

    payload = {
        "log": USER,
        "pwd": PASS,
        "wp-submit": "Acceder",
        "redirect_to": urljoin(BASE, "/wp-admin/"),
        "testcookie": "1",
    }
    resp = session.post(login_url, data=payload, timeout=30, allow_redirects=True)
    resp.raise_for_status()
    if "wp-admin" not in resp.url and "dashboard" not in resp.text.lower():
        raise RuntimeError("Login may have failed")


def purge_cache(session):
    dashboard = session.get(urljoin(BASE, "/wp-admin/"), timeout=30)
    for href in re.findall(r'href=["\']([^"\']+)["\']', dashboard.text):
        raw = html.unescape(href)
        if "litespeed" in raw.lower() and "purge" in raw.lower():
            session.get(urljoin(BASE, raw), timeout=25)
            return True
    return False


def main():
    session = requests.Session()
    session.headers.update({"User-Agent": "PrimeDropScopedFixes/1.0"})
    login(session)

    editor_url = urljoin(BASE, "/wp-admin/theme-editor.php?file=functions.php&theme=blocksy")
    page = session.get(editor_url, timeout=30)
    page.raise_for_status()

    textarea = re.search(r'<textarea[^>]+name=["\']newcontent["\'][^>]*>(.*?)</textarea>', page.text, re.S)
    if not textarea:
        raise RuntimeError("Could not find functions.php editor textarea")

    current = html.unescape(textarea.group(1))
    Path("wp-backups").mkdir(exist_ok=True)
    backup = Path("wp-backups") / f"functions_before_category_search_cart_empty_{datetime.now():%Y%m%d_%H%M%S}.php"
    backup.write_text(current, encoding="utf-8")

    pattern = re.compile(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), re.S)
    if pattern.search(current):
        updated = pattern.sub(lambda _: BLOCK.strip(), current)
    else:
        updated = current.rstrip() + "\n\n" + BLOCK.strip() + "\n"

    nonce = re.search(r'name=["\']nonce["\']\s+value=["\']([^"\']+)["\']', page.text)
    if not nonce:
        nonce = re.search(r'id=["\']nonce["\']\s+name=["\']nonce["\']\s+value=["\']([^"\']+)["\']', page.text)
    if not nonce:
        raise RuntimeError("Could not find theme editor nonce")

    resp = session.post(
        urljoin(BASE, "/wp-admin/theme-editor.php"),
        data={
            "nonce": nonce.group(1),
            "_wp_http_referer": "/wp-admin/theme-editor.php?file=functions.php&theme=blocksy",
            "newcontent": updated,
            "action": "update",
            "file": "functions.php",
            "theme": "blocksy",
            "docs-list": "",
            "scrollto": "0",
            "submit": "Actualizar archivo",
        },
        timeout=40,
        allow_redirects=True,
    )
    if resp.status_code >= 400 or "No ha sido posible" in resp.text:
        raise RuntimeError(f"Update failed: {resp.status_code}")

    print(f"updated=true backup={backup} purged={purge_cache(session)}")


if __name__ == "__main__":
    main()
