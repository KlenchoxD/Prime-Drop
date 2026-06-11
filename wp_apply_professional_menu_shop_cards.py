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

MARKER_START = "/* PRIME_DROP_PROFESSIONAL_MENU_SHOP_CARDS_START */"
MARKER_END = "/* PRIME_DROP_PROFESSIONAL_MENU_SHOP_CARDS_END */"

BLOCK = r"""
/* PRIME_DROP_PROFESSIONAL_MENU_SHOP_CARDS_START */
add_action('woocommerce_before_shop_loop', function() {
    if (!(is_shop() || is_product_category() || is_page(547))) {
        return;
    }
    ?>
    <div class="pd-professional-shop-search">
      <form role="search" method="get" action="<?php echo esc_url(home_url('/')); ?>">
        <label class="screen-reader-text" for="pd-professional-product-search">Buscar bolsos</label>
        <input id="pd-professional-product-search" type="search" name="s" value="<?php echo esc_attr(get_search_query()); ?>" placeholder="Buscar bolsos..." autocomplete="off">
        <input type="hidden" name="post_type" value="product">
        <button type="submit" aria-label="Buscar">
          <svg aria-hidden="true" viewBox="0 0 24 24" fill="none">
            <circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="1.8"></circle>
            <path d="m16.2 16.2 4.1 4.1" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"></path>
          </svg>
        </button>
      </form>
    </div>
    <?php
}, 21);

add_action('wp_footer', function() {
    if (is_admin()) {
        return;
    }
    ?>
    <style id="prime-drop-professional-menu-shop-cards-css">
    /* Un solo control de categorías: el desplegable BOLSOS del header */
    body.page-id-547 .pd-shop-filters,
    body.page-id-547 .pd-brand-filter,
    body.page-id-547 .pd-listing-brand-rail,
    body.tax-product_cat .pd-brand-filter,
    body.tax-product_cat .pd-listing-brand-rail,
    body.woocommerce-shop .pd-brand-filter,
    body.woocommerce-shop .pd-listing-brand-rail,
    body.post-type-archive-product .pd-brand-filter,
    body.post-type-archive-product .pd-listing-brand-rail {
      display: none !important;
    }

    body.page-id-547 .elementor-element-2fc690d {
      display: none !important;
    }

    body.page-id-547 .elementor-element-9884376 {
      width: 100% !important;
      max-width: 100% !important;
      flex: 0 0 100% !important;
    }

    /* Fila de tienda: resultados | buscador | ordenar */
    body.page-id-547 .woo-listing-top,
    body.tax-product_cat .woo-listing-top,
    body.woocommerce-shop .woo-listing-top,
    body.post-type-archive-product .woo-listing-top {
      width: min(1180px, calc(100% - 48px)) !important;
      max-width: 1180px !important;
      min-height: 80px !important;
      margin: 0 auto 34px !important;
      padding: 16px 0 !important;
      display: grid !important;
      grid-template-columns: minmax(180px, 1fr) minmax(280px, 390px) minmax(190px, 1fr) !important;
      grid-template-areas: "count search order" !important;
      gap: 24px !important;
      align-items: center !important;
      border-top: 1px solid #ececec !important;
      border-bottom: 1px solid #ececec !important;
      box-sizing: border-box !important;
    }

    body.page-id-547 .woo-listing-top .woocommerce-result-count,
    body.tax-product_cat .woo-listing-top .woocommerce-result-count,
    body.woocommerce-shop .woo-listing-top .woocommerce-result-count,
    body.post-type-archive-product .woo-listing-top .woocommerce-result-count {
      grid-area: count !important;
      justify-self: start !important;
      display: block !important;
      float: none !important;
      width: auto !important;
      margin: 0 !important;
      color: #111 !important;
      font-size: 11px !important;
      font-weight: 750 !important;
      letter-spacing: .09em !important;
      line-height: 1.4 !important;
      text-align: left !important;
      text-transform: uppercase !important;
      white-space: normal !important;
    }

    body.page-id-547 .pd-professional-shop-search,
    body.tax-product_cat .pd-professional-shop-search,
    body.woocommerce-shop .pd-professional-shop-search,
    body.post-type-archive-product .pd-professional-shop-search {
      grid-area: search !important;
      justify-self: center !important;
      display: block !important;
      width: 100% !important;
      max-width: 390px !important;
      margin: 0 !important;
      padding: 0 !important;
    }

    .pd-professional-shop-search form {
      width: 100% !important;
      height: 46px !important;
      display: flex !important;
      align-items: center !important;
      padding: 4px 4px 4px 18px !important;
      background: #fff !important;
      border: 1px solid #dedede !important;
      border-radius: 999px !important;
      box-shadow: 0 8px 24px rgba(0, 0, 0, .055) !important;
      box-sizing: border-box !important;
      overflow: hidden !important;
    }

    .pd-professional-shop-search form:focus-within {
      border-color: #111 !important;
      box-shadow: 0 8px 26px rgba(0, 0, 0, .09) !important;
    }

    .pd-professional-shop-search input[type="search"] {
      flex: 1 1 auto !important;
      min-width: 0 !important;
      height: 38px !important;
      margin: 0 !important;
      padding: 0 10px 0 0 !important;
      color: #111 !important;
      background: transparent !important;
      border: 0 !important;
      border-radius: 0 !important;
      box-shadow: none !important;
      outline: 0 !important;
      font-size: 13px !important;
    }

    .pd-professional-shop-search button {
      flex: 0 0 38px !important;
      width: 38px !important;
      min-width: 38px !important;
      height: 38px !important;
      min-height: 38px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      margin: 0 !important;
      padding: 0 !important;
      color: #fff !important;
      background: #0a0a0a !important;
      border: 0 !important;
      border-radius: 50% !important;
      box-shadow: none !important;
    }

    .pd-professional-shop-search button svg {
      width: 17px !important;
      height: 17px !important;
    }

    body.page-id-547 .woo-listing-top .woocommerce-ordering,
    body.tax-product_cat .woo-listing-top .woocommerce-ordering,
    body.woocommerce-shop .woo-listing-top .woocommerce-ordering,
    body.post-type-archive-product .woo-listing-top .woocommerce-ordering {
      grid-area: order !important;
      justify-self: end !important;
      display: flex !important;
      float: none !important;
      width: min(100%, 240px) !important;
      margin: 0 !important;
    }

    /* Menú BOLSOS estable, sin hueco entre enlace y desplegable */
    @media (min-width: 1000px) {
      #header [data-device="desktop"] .pd-bolsos-menu-parent {
        position: relative !important;
      }

      #header [data-device="desktop"] .pd-bolsos-menu-parent > .pd-bolsos-submenu {
        position: absolute !important;
        top: 100% !important;
        left: 50% !important;
        z-index: 100000 !important;
        min-width: 238px !important;
        margin: 0 !important;
        padding: 10px 8px 8px !important;
        background: #0b0b0b !important;
        border: 0 !important;
        border-radius: 0 0 4px 4px !important;
        box-shadow: 0 18px 38px rgba(0,0,0,.18) !important;
        opacity: 0 !important;
        visibility: hidden !important;
        pointer-events: none !important;
        transform: translateX(-50%) !important;
        transition: opacity .12s ease, visibility .12s ease !important;
      }

      #header [data-device="desktop"] .pd-bolsos-menu-parent > .pd-bolsos-submenu::before {
        content: "" !important;
        position: absolute !important;
        left: 0 !important;
        right: 0 !important;
        top: -14px !important;
        height: 16px !important;
      }

      #header [data-device="desktop"] .pd-bolsos-menu-parent:hover > .pd-bolsos-submenu,
      #header [data-device="desktop"] .pd-bolsos-menu-parent:focus-within > .pd-bolsos-submenu,
      #header [data-device="desktop"] .pd-bolsos-menu-parent.pd-submenu-open > .pd-bolsos-submenu {
        opacity: 1 !important;
        visibility: visible !important;
        pointer-events: auto !important;
        transform: translateX(-50%) !important;
      }

      #header [data-device="desktop"] .pd-bolsos-submenu li {
        display: block !important;
        margin: 0 !important;
        padding: 0 !important;
      }

      #header [data-device="desktop"] .pd-bolsos-submenu a {
        min-height: 42px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        padding: 0 14px !important;
        color: #fff !important;
        background: transparent !important;
        font-size: 11px !important;
        font-weight: 750 !important;
        letter-spacing: .08em !important;
        text-decoration: none !important;
        text-transform: uppercase !important;
        white-space: nowrap !important;
      }

      #header [data-device="desktop"] .pd-bolsos-submenu a:hover,
      #header [data-device="desktop"] .pd-bolsos-submenu a:focus {
        color: #000 !important;
        background: #fff !important;
        font-weight: 900 !important;
      }
    }

    /* Cards profesionales y simétricas */
    body:not(.single-product) .woocommerce ul.products {
      align-items: stretch !important;
    }

    body:not(.single-product) .woocommerce ul.products li.product {
      display: flex !important;
      flex-direction: column !important;
      align-items: stretch !important;
      height: auto !important;
      min-height: 0 !important;
      padding: 0 !important;
      color: #111 !important;
      background: #fff !important;
      border: 0 !important;
      border-radius: 0 !important;
      box-shadow: none !important;
      overflow: visible !important;
      text-align: center !important;
    }

    body:not(.single-product) .woocommerce ul.products li.product figure,
    body:not(.single-product) .woocommerce ul.products li.product .ct-media-container {
      width: 100% !important;
      aspect-ratio: 4 / 5 !important;
      height: auto !important;
      min-height: 0 !important;
      max-height: none !important;
      margin: 0 0 14px !important;
      padding: 0 !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      background: #f6f6f5 !important;
      border: 0 !important;
      border-radius: 0 !important;
      box-shadow: none !important;
      overflow: hidden !important;
      box-sizing: border-box !important;
    }

    body:not(.single-product) .woocommerce ul.products li.product figure img,
    body:not(.single-product) .woocommerce ul.products li.product .ct-media-container img,
    body:not(.single-product) .woocommerce ul.products li.product img {
      width: 100% !important;
      height: 100% !important;
      min-height: 0 !important;
      max-height: none !important;
      margin: 0 !important;
      padding: 16px !important;
      object-fit: contain !important;
      object-position: center !important;
      background: transparent !important;
      border: 0 !important;
      border-radius: 0 !important;
      box-shadow: none !important;
      transform: none !important;
      box-sizing: border-box !important;
    }

    body:not(.single-product) .woocommerce ul.products li.product .woocommerce-loop-product__title {
      min-height: 50px !important;
      margin: 0 !important;
      padding: 0 8px !important;
      display: flex !important;
      align-items: flex-start !important;
      justify-content: center !important;
      color: #111 !important;
      font-size: 14px !important;
      font-weight: 750 !important;
      line-height: 1.25 !important;
      letter-spacing: 0 !important;
      text-align: center !important;
      text-transform: none !important;
    }

    body:not(.single-product) .woocommerce ul.products li.product .woocommerce-loop-product__title a {
      color: inherit !important;
      text-align: center !important;
    }

    body:not(.single-product) .woocommerce ul.products li.product .price {
      min-height: 24px !important;
      margin: 4px 0 14px !important;
      padding: 0 8px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      color: #111 !important;
      font-size: 14px !important;
      font-weight: 600 !important;
      line-height: 1.3 !important;
      letter-spacing: 0 !important;
      text-align: center !important;
      white-space: nowrap !important;
    }

    body:not(.single-product) .woocommerce ul.products li.product .entry-meta {
      display: none !important;
    }

    body:not(.single-product) .woocommerce ul.products li.product .ct-woo-card-actions {
      min-height: 42px !important;
      margin: auto 0 0 !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      opacity: 1 !important;
      visibility: visible !important;
      transform: none !important;
    }

    body:not(.single-product) .woocommerce ul.products li.product .button,
    body:not(.single-product) .woocommerce ul.products li.product:not(:hover) .button,
    body:not(.single-product) .woocommerce ul.products li.product:hover .button {
      width: auto !important;
      min-width: 164px !important;
      max-width: calc(100% - 20px) !important;
      min-height: 40px !important;
      margin: 0 auto !important;
      padding: 10px 20px !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      color: #fff !important;
      background: #080808 !important;
      border: 1px solid #080808 !important;
      border-radius: 999px !important;
      box-shadow: none !important;
      opacity: 1 !important;
      visibility: visible !important;
      transform: none !important;
      font-size: 10.5px !important;
      font-weight: 750 !important;
      letter-spacing: .08em !important;
      line-height: 1.25 !important;
      text-align: center !important;
      text-transform: uppercase !important;
      white-space: normal !important;
    }

    @media (max-width: 900px) {
      body.page-id-547 .woo-listing-top,
      body.tax-product_cat .woo-listing-top,
      body.woocommerce-shop .woo-listing-top,
      body.post-type-archive-product .woo-listing-top {
        width: min(100% - 28px, 560px) !important;
        grid-template-columns: 1fr !important;
        grid-template-areas:
          "search"
          "count"
          "order" !important;
        gap: 14px !important;
        justify-items: center !important;
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

      body:not(.single-product) .woocommerce ul.products li.product .woocommerce-loop-product__title {
        min-height: 44px !important;
        font-size: 12px !important;
      }

      body:not(.single-product) .woocommerce ul.products li.product .button {
        min-width: 0 !important;
        width: calc(100% - 12px) !important;
        max-width: calc(100% - 12px) !important;
        padding: 10px 8px !important;
        font-size: 9.5px !important;
      }
    }
    </style>
    <script id="prime-drop-professional-menu-shop-cards-js">
    (function() {
      var menuItems = [
        ['TODOS LOS BOLSOS', '/bolsos/'],
        ['KARL LAGERFELD', '/product-category/karl-lagerfeld/'],
        ['MICHAEL KORS', '/product-category/michael-kors/'],
        ['STEVE MADDEN', '/product-category/steve-madden/'],
        ['TOMMY HILFIGER', '/product-category/tommy-hilfiger/']
      ];
      var closeTimers = new WeakMap();

      function menuHtml() {
        return menuItems.map(function(item) {
          return '<li><a href="' + item[1] + '">' + item[0] + '</a></li>';
        }).join('');
      }

      function normalizeMenu() {
        document.querySelectorAll('.pd-bolsos-menu-parent > .pd-bolsos-submenu').forEach(function(submenu) {
          var signature = Array.from(submenu.querySelectorAll(':scope > li > a')).map(function(link) {
            return (link.textContent || '').trim() + '|' + (link.getAttribute('href') || '');
          }).join('::');
          var expected = menuItems.map(function(item) { return item[0] + '|' + item[1]; }).join('::');
          if (signature !== expected) submenu.innerHTML = menuHtml();

          var parent = submenu.parentElement;
          if (!parent || parent.dataset.pdProfessionalHover === '1') return;
          parent.dataset.pdProfessionalHover = '1';

          function open() {
            clearTimeout(closeTimers.get(parent));
            parent.classList.add('pd-submenu-open');
          }

          function delayedClose() {
            clearTimeout(closeTimers.get(parent));
            closeTimers.set(parent, setTimeout(function() {
              if (!parent.matches(':hover') && !submenu.matches(':hover') && !parent.contains(document.activeElement)) {
                parent.classList.remove('pd-submenu-open');
              }
            }, 260));
          }

          parent.addEventListener('mouseenter', open);
          submenu.addEventListener('mouseenter', open);
          parent.addEventListener('mouseleave', delayedClose);
          submenu.addEventListener('mouseleave', delayedClose);
          parent.addEventListener('focusin', open);
          parent.addEventListener('focusout', delayedClose);
        });
      }

      function normalizeListing() {
        document.querySelectorAll('.pd-listing-brand-rail, .pd-brand-filter').forEach(function(el) {
          el.setAttribute('aria-hidden', 'true');
          el.style.setProperty('display', 'none', 'important');
          el.style.setProperty('visibility', 'hidden', 'important');
          el.style.setProperty('height', '0', 'important');
          el.style.setProperty('min-height', '0', 'important');
          el.style.setProperty('margin', '0', 'important');
          el.style.setProperty('padding', '0', 'important');
          el.style.setProperty('overflow', 'hidden', 'important');
        });

        document.querySelectorAll('.woo-listing-top').forEach(function(top) {
          var search = top.querySelector('.pd-professional-shop-search');
          var count = top.querySelector('.woocommerce-result-count');
          var ordering = top.querySelector('.woocommerce-ordering');
          if (!search || !count || !ordering) return;
          top.insertBefore(count, top.firstElementChild);
          count.insertAdjacentElement('afterend', search);
          top.appendChild(ordering);
        });

        document.querySelectorAll('body:not(.single-product) .woocommerce ul.products li.product').forEach(function(card) {
          card.querySelectorAll('.entry-meta').forEach(function(meta) { meta.remove(); });
          var actions = card.querySelector('.ct-woo-card-actions');
          if (actions) {
            actions.removeAttribute('data-add-to-cart');
            actions.style.setProperty('opacity', '1', 'important');
            actions.style.setProperty('visibility', 'visible', 'important');
            actions.style.setProperty('transform', 'none', 'important');
          }
        });
      }

      function injectLateOverrides() {
        var style = document.getElementById('prime-drop-professional-menu-shop-cards-late-css');
        if (style) style.remove();
        style = document.createElement('style');
        style.id = 'prime-drop-professional-menu-shop-cards-late-css';
        style.textContent = [
          'body.page-id-547 .pd-brand-filter,body.tax-product_cat .pd-brand-filter,body.page-id-547 .pd-listing-brand-rail,body.tax-product_cat .pd-listing-brand-rail{display:none!important;visibility:hidden!important;height:0!important;min-height:0!important;margin:0!important;padding:0!important;overflow:hidden!important}',
          'body.page-id-547 .pd-shop-filters{display:none!important}',
          'body.page-id-547 .pd-professional-shop-search,body.tax-product_cat .pd-professional-shop-search,body.woocommerce-shop .pd-professional-shop-search,body.post-type-archive-product .pd-professional-shop-search{display:block!important;visibility:visible!important;opacity:1!important;grid-area:search!important}',
          'body:not(.single-product) .woocommerce ul.products li.product .ct-woo-card-actions,body:not(.single-product) .woocommerce ul.products li.product:not(:hover) .ct-woo-card-actions,body:not(.single-product) .woocommerce ul.products li.product:hover .ct-woo-card-actions{display:flex!important;opacity:1!important;visibility:visible!important;transform:none!important}',
          'body:not(.single-product) .woocommerce ul.products li.product .button,body:not(.single-product) .woocommerce ul.products li.product:not(:hover) .button,body:not(.single-product) .woocommerce ul.products li.product:hover .button{display:inline-flex!important;opacity:1!important;visibility:visible!important;transform:none!important;background:#080808!important;color:#fff!important;border-color:#080808!important;border-radius:999px!important}',
          '#header [data-device="desktop"] .pd-bolsos-submenu a:hover,#header [data-device="desktop"] .pd-bolsos-submenu a:focus{color:#000!important;background:#fff!important;font-weight:900!important}',
          '#header [data-device="desktop"] .pd-bolsos-menu-parent:hover>.pd-bolsos-submenu,#header [data-device="desktop"] .pd-bolsos-menu-parent:focus-within>.pd-bolsos-submenu,#header [data-device="desktop"] .pd-bolsos-menu-parent.pd-submenu-open>.pd-bolsos-submenu{opacity:1!important;visibility:visible!important;pointer-events:auto!important}'
        ].join('\n');
        (document.body || document.documentElement).appendChild(style);
      }

      function run() {
        injectLateOverrides();
        normalizeMenu();
        normalizeListing();
      }

      run();
      document.addEventListener('DOMContentLoaded', run);
      window.addEventListener('pageshow', run);
      window.addEventListener('load', run);
      document.addEventListener('click', function() { setTimeout(run, 80); }, true);
      setTimeout(run, 180);
      setTimeout(run, 700);
      setTimeout(run, 1600);
      setTimeout(run, 2300);
      setTimeout(run, 3800);
      if (window.MutationObserver) {
        var scheduled = false;
        new MutationObserver(function() {
          if (scheduled) return;
          scheduled = true;
          setTimeout(function() {
            scheduled = false;
            run();
          }, 60);
        }).observe(document.documentElement, { childList: true, subtree: true });
      }
    })();
    </script>
    <?php
}, PHP_INT_MAX);
/* PRIME_DROP_PROFESSIONAL_MENU_SHOP_CARDS_END */
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


def remove_marker_block(content, marker_name):
    pattern = re.compile(
        re.escape(f"/* {marker_name}_START */") + r".*?" + re.escape(f"/* {marker_name}_END */"),
        re.S,
    )
    return pattern.sub("", content), bool(pattern.search(content))


def purge_cache(session):
    dashboard = session.get(urljoin(BASE, "/wp-admin/"), timeout=30)
    purged = False
    for href in re.findall(r'href=["\']([^"\']+)["\']', dashboard.text):
        raw = html.unescape(href)
        if "litespeed" in raw.lower() and "purge" in raw.lower():
            session.get(urljoin(BASE, raw), timeout=25)
            purged = True
    return purged


def main():
    session = requests.Session()
    session.headers.update({"User-Agent": "PrimeDropProfessionalMenuShopCards/1.0"})
    login(session)

    editor_url = urljoin(BASE, "/wp-admin/theme-editor.php?file=functions.php&theme=blocksy")
    page = session.get(editor_url, timeout=30)
    page.raise_for_status()
    textarea = re.search(r'<textarea[^>]+name=["\']newcontent["\'][^>]*>(.*?)</textarea>', page.text, re.S)
    if not textarea:
        raise RuntimeError("Could not find functions.php editor textarea")

    current = html.unescape(textarea.group(1))
    Path("wp-backups").mkdir(exist_ok=True)
    backup = Path("wp-backups") / f"functions_before_professional_menu_shop_cards_{datetime.now():%Y%m%d_%H%M%S}.php"
    backup.write_text(current, encoding="utf-8")

    updated = current
    removed = []
    for marker in ["PRIME_DROP_VISUAL_POLISH_20260606"]:
        updated, did_remove = remove_marker_block(updated, marker)
        if did_remove:
            removed.append(marker)

    pattern = re.compile(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), re.S)
    if pattern.search(updated):
        updated = pattern.sub(lambda _: BLOCK.strip(), updated)
    else:
        updated = updated.rstrip() + "\n\n" + BLOCK.strip() + "\n"

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
        timeout=50,
        allow_redirects=True,
    )
    if resp.status_code >= 400:
        raise RuntimeError(f"Update failed: {resp.status_code}")

    print(f"updated=true backup={backup} removed={removed} purged={purge_cache(session)}")


if __name__ == "__main__":
    main()
