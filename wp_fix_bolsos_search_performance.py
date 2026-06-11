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

MARKER_START = "/* PRIME_DROP_BOLSOS_SEARCH_PERFORMANCE_FINAL_START */"
MARKER_END = "/* PRIME_DROP_BOLSOS_SEARCH_PERFORMANCE_FINAL_END */"
POSTER_URL = ""

BLOCK = f"""
/* PRIME_DROP_BOLSOS_SEARCH_PERFORMANCE_FINAL_START */
add_filter('the_content', function($content) {{
    if (!is_front_page() && !is_page(14)) {{
        return $content;
    }}

    $content = preg_replace_callback('/<video[^>]*class=["\\'][^"\\']*pd-hero-video-bg[^"\\']*["\\'][^>]*>/i', function($matches) {{
        $tag = $matches[0];
        if (preg_match('/\\s+preload=["\\'][^"\\']*["\\']/i', $tag)) {{
            $tag = preg_replace('/\\s+preload=["\\'][^"\\']*["\\']/i', ' preload="metadata"', $tag);
        }} else {{
            $tag = preg_replace('/>$/', ' preload="metadata">', $tag);
        }}
        $tag = preg_replace('/\\s+poster=["\\'][^"\\']*["\\']/i', '', $tag);
        return $tag;
    }}, $content);

    return $content;
}}, 1200);

add_filter('wp_get_attachment_image_attributes', function($attr) {{
    if (is_admin()) {{
        return $attr;
    }}

    if (is_front_page() || is_page(14) || is_page(547) || is_shop() || is_product_category() || is_product()) {{
        $attr['decoding'] = 'async';
        if (empty($attr['loading'])) {{
            $attr['loading'] = 'lazy';
        }}
    }}

    return $attr;
}}, 30);

add_action('wp_head', function() {{
    ?>
    <style id="prime-drop-bolsos-search-performance-final-css">
    /* Fila superior /bolsos y categorias: contador | buscador | orden */
    body.page-id-547 .woo-listing-top,
    body.tax-product_cat .woo-listing-top,
    body.woocommerce-shop .woo-listing-top,
    body.post-type-archive-product .woo-listing-top {{
      width: min(1180px, calc(100% - 56px)) !important;
      max-width: 1180px !important;
      margin: 0 auto 32px !important;
      padding: 18px 0 !important;
      display: grid !important;
      grid-template-columns: minmax(190px, 1fr) minmax(300px, 420px) minmax(220px, 1fr) !important;
      grid-template-areas: "count search order" !important;
      column-gap: 28px !important;
      row-gap: 14px !important;
      align-items: center !important;
      border-top: 1px solid #eeeeee !important;
      border-bottom: 1px solid #eeeeee !important;
      box-sizing: border-box !important;
    }}

    body.page-id-547 .woo-listing-top .woocommerce-result-count,
    body.tax-product_cat .woo-listing-top .woocommerce-result-count,
    body.woocommerce-shop .woo-listing-top .woocommerce-result-count,
    body.post-type-archive-product .woo-listing-top .woocommerce-result-count {{
      grid-area: count !important;
      justify-self: start !important;
      align-self: center !important;
      margin: 0 !important;
      padding: 0 !important;
      width: auto !important;
      min-height: 0 !important;
      display: flex !important;
      align-items: center !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 12px !important;
      font-weight: 800 !important;
      letter-spacing: 1.3px !important;
      text-transform: uppercase !important;
      color: #000000 !important;
      white-space: nowrap !important;
    }}

    body.page-id-547 .pd-shop-search,
    body.tax-product_cat .pd-shop-search,
    body.woocommerce-shop .pd-shop-search,
    body.post-type-archive-product .pd-shop-search {{
      grid-area: search !important;
      justify-self: center !important;
      align-self: center !important;
      width: 100% !important;
      max-width: 420px !important;
      margin: 0 !important;
      display: block !important;
      visibility: visible !important;
      opacity: 1 !important;
    }}

    body.page-id-547 .pd-shop-search form,
    body.tax-product_cat .pd-shop-search form,
    body.woocommerce-shop .pd-shop-search form,
    body.post-type-archive-product .pd-shop-search form {{
      width: 100% !important;
      height: 46px !important;
      display: flex !important;
      align-items: center !important;
      gap: 0 !important;
      padding: 4px !important;
      background: #ffffff !important;
      border: 0 !important;
      border-radius: 999px !important;
      overflow: hidden !important;
      box-shadow: 0 12px 28px rgba(0,0,0,.08), inset 0 0 0 1px rgba(0,0,0,.08) !important;
      box-sizing: border-box !important;
    }}

    body.page-id-547 .pd-shop-search input[type="search"],
    body.tax-product_cat .pd-shop-search input[type="search"],
    body.woocommerce-shop .pd-shop-search input[type="search"],
    body.post-type-archive-product .pd-shop-search input[type="search"] {{
      flex: 1 1 auto !important;
      min-width: 0 !important;
      height: 38px !important;
      margin: 0 !important;
      padding: 0 14px 0 18px !important;
      border: 0 !important;
      outline: 0 !important;
      box-shadow: none !important;
      background: transparent !important;
      color: #111111 !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 13.5px !important;
      line-height: 38px !important;
    }}

    body.page-id-547 .pd-shop-search input[type="search"]::placeholder,
    body.tax-product_cat .pd-shop-search input[type="search"]::placeholder,
    body.woocommerce-shop .pd-shop-search input[type="search"]::placeholder,
    body.post-type-archive-product .pd-shop-search input[type="search"]::placeholder {{
      color: #8a8a8a !important;
      opacity: 1 !important;
    }}

    body.page-id-547 .pd-shop-search button[type="submit"],
    body.tax-product_cat .pd-shop-search button[type="submit"],
    body.woocommerce-shop .pd-shop-search button[type="submit"],
    body.post-type-archive-product .pd-shop-search button[type="submit"] {{
      flex: 0 0 38px !important;
      width: 38px !important;
      min-width: 38px !important;
      height: 38px !important;
      min-height: 38px !important;
      margin: 0 !important;
      padding: 0 !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      border: 0 !important;
      border-radius: 50% !important;
      background: #000000 !important;
      color: #ffffff !important;
      box-shadow: none !important;
      cursor: pointer !important;
    }}

    body.page-id-547 .pd-shop-search button[type="submit"] svg,
    body.tax-product_cat .pd-shop-search button[type="submit"] svg,
    body.woocommerce-shop .pd-shop-search button[type="submit"] svg,
    body.post-type-archive-product .pd-shop-search button[type="submit"] svg {{
      width: 15px !important;
      height: 15px !important;
      stroke: currentColor !important;
    }}

    body.page-id-547 .woo-listing-top .woocommerce-ordering,
    body.tax-product_cat .woo-listing-top .woocommerce-ordering,
    body.woocommerce-shop .woo-listing-top .woocommerce-ordering,
    body.post-type-archive-product .woo-listing-top .woocommerce-ordering {{
      grid-area: order !important;
      justify-self: end !important;
      align-self: center !important;
      width: 240px !important;
      margin: 0 !important;
      padding: 0 !important;
      display: flex !important;
      align-items: center !important;
      position: relative !important;
    }}

    /* Cards: imagen completa, simetrica y sin cuadro blanco interno */
    body.page-id-14 .woocommerce ul.products li.product figure,
    body.page-id-547 .woocommerce ul.products li.product figure,
    body.tax-product_cat .woocommerce ul.products li.product figure,
    body.post-type-archive-product .woocommerce ul.products li.product figure {{
      width: 100% !important;
      margin: 0 0 16px !important;
      padding: 0 !important;
      background: #ffffff !important;
      background-color: #ffffff !important;
      border: 0 !important;
      border-radius: 0 !important;
      box-shadow: none !important;
      overflow: hidden !important;
    }}

    body.page-id-14 .woocommerce ul.products li.product figure > a.ct-media-container,
    body.page-id-547 .woocommerce ul.products li.product figure > a.ct-media-container,
    body.tax-product_cat .woocommerce ul.products li.product figure > a.ct-media-container,
    body.post-type-archive-product .woocommerce ul.products li.product figure > a.ct-media-container {{
      width: 100% !important;
      aspect-ratio: 4 / 5 !important;
      height: auto !important;
      min-height: 0 !important;
      max-height: none !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      background: #ffffff !important;
      background-color: #ffffff !important;
      overflow: hidden !important;
    }}

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
    body.post-type-archive-product .woocommerce ul.products li.product img {{
      width: 100% !important;
      height: 100% !important;
      min-height: 0 !important;
      max-height: none !important;
      aspect-ratio: auto !important;
      object-fit: contain !important;
      object-position: center center !important;
      margin: 0 !important;
      padding: 20px 16px 16px !important;
      background: transparent !important;
      background-color: transparent !important;
      border: 0 !important;
      box-shadow: none !important;
      display: block !important;
      box-sizing: border-box !important;
      transform: none !important;
      filter: none !important;
      mix-blend-mode: normal !important;
    }}

    body.page-id-14 .woocommerce ul.products li.product,
    body.page-id-547 .woocommerce ul.products li.product,
    body.tax-product_cat .woocommerce ul.products li.product,
    body.post-type-archive-product .woocommerce ul.products li.product {{
      contain: content !important;
      content-visibility: auto !important;
      contain-intrinsic-size: 360px 520px !important;
    }}

    /* Hero: sin poster pesado visible al recargar */
    body.page-id-14 .pd-hero,
    body.home .pd-hero {{
      background-color: #111111 !important;
      background-image: none !important;
    }}

    body.page-id-14 .pd-hero video,
    body.home .pd-hero video {{
      transform: translate(-50%, -50%) translateZ(0) !important;
      backface-visibility: hidden !important;
    }}

    @media (max-width: 900px) {{
      body.page-id-547 .woo-listing-top,
      body.tax-product_cat .woo-listing-top,
      body.woocommerce-shop .woo-listing-top,
      body.post-type-archive-product .woo-listing-top {{
        width: min(100% - 28px, 560px) !important;
        grid-template-columns: 1fr !important;
        grid-template-areas:
          "search"
          "count"
          "order" !important;
        justify-items: center !important;
      }}

      body.page-id-547 .woo-listing-top .woocommerce-result-count,
      body.tax-product_cat .woo-listing-top .woocommerce-result-count,
      body.woocommerce-shop .woo-listing-top .woocommerce-result-count,
      body.post-type-archive-product .woo-listing-top .woocommerce-result-count,
      body.page-id-547 .woo-listing-top .woocommerce-ordering,
      body.tax-product_cat .woo-listing-top .woocommerce-ordering,
      body.woocommerce-shop .woo-listing-top .woocommerce-ordering,
      body.post-type-archive-product .woo-listing-top .woocommerce-ordering {{
        justify-self: center !important;
      }}
    }}
    </style>
    <script id="prime-drop-bolsos-search-performance-final-js">
    (function() {{
      function tune() {{
        document.querySelectorAll('.pd-hero video, video.pd-hero-video-bg').forEach(function(video) {{
          video.setAttribute('preload', 'metadata');
          video.removeAttribute('poster');
          video.muted = true;
          video.playsInline = true;
        }});

        document.querySelectorAll('body.page-id-14 ul.products li.product img, body.page-id-547 ul.products li.product img, body.tax-product_cat ul.products li.product img, body.post-type-archive-product ul.products li.product img').forEach(function(img) {{
          img.setAttribute('loading', 'lazy');
          img.setAttribute('decoding', 'async');
          img.style.setProperty('object-fit', 'contain', 'important');
          img.style.setProperty('object-position', 'center center', 'important');
          img.style.setProperty('background', 'transparent', 'important');
          img.style.setProperty('mix-blend-mode', 'normal', 'important');
        }});
      }}

      tune();
      document.addEventListener('DOMContentLoaded', tune);
      window.addEventListener('load', tune);
      window.addEventListener('pageshow', tune);
      setTimeout(tune, 400);

      function warmHeroVideo() {{
        document.querySelectorAll('.pd-hero video, video.pd-hero-video-bg').forEach(function(video) {{
          video.setAttribute('preload', 'auto');
          try {{
            var play = video.play();
            if (play && play.catch) play.catch(function() {{}});
          }} catch (e) {{}}
        }});
      }}

      if ('requestIdleCallback' in window) {{
        requestIdleCallback(warmHeroVideo, {{ timeout: 1800 }});
      }} else {{
        setTimeout(warmHeroVideo, 1400);
      }}
    }})();
    </script>
    <?php
}}, 60);
/* PRIME_DROP_BOLSOS_SEARCH_PERFORMANCE_FINAL_END */
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
    session.headers.update({"User-Agent": "PrimeDropBolsosSearchPerformanceFinal/1.0"})
    login(session)

    editor_url = urljoin(BASE, "/wp-admin/theme-editor.php?file=functions.php&theme=blocksy")
    page = session.get(editor_url, timeout=30)
    page.raise_for_status()

    textarea = re.search(r'<textarea[^>]+name=["\']newcontent["\'][^>]*>(.*?)</textarea>', page.text, re.S)
    if not textarea:
        raise RuntimeError("Could not find functions.php editor textarea")

    current = html.unescape(textarea.group(1))
    Path("wp-backups").mkdir(exist_ok=True)
    backup = Path("wp-backups") / f"functions_before_bolsos_search_perf_{datetime.now():%Y%m%d_%H%M%S}.php"
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
    if resp.status_code >= 400:
        raise RuntimeError(f"Update failed: {resp.status_code}")

    print(f"updated=true backup={backup} purged={purge_cache(session)}")


if __name__ == "__main__":
    main()
