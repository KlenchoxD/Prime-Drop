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

MARKER_START = "/* PRIME_DROP_HEADER_INSTAGRAM_REFERENCE_FIX_START */"
MARKER_END = "/* PRIME_DROP_HEADER_INSTAGRAM_REFERENCE_FIX_END */"

BLOCK = r"""
/* PRIME_DROP_HEADER_INSTAGRAM_REFERENCE_FIX_START */
add_action('wp_footer', function() {
    ?>
    <style id="prime-drop-header-instagram-reference-fix-css">
    /* Header desktop como referencia anterior */
    @media (min-width: 1000px) {
      #header,
      #header.ct-header,
      #header [data-device="desktop"],
      #header .ct-sticky-container,
      #header [data-sticky],
      #header [data-device="desktop"] [data-row="middle"] {
        height: 104px !important;
        min-height: 104px !important;
        max-height: 104px !important;
        background: #ffffff !important;
        position: relative !important;
        top: auto !important;
        transform: none !important;
      }

      #header [data-device="desktop"] .ct-container {
        height: 104px !important;
        min-height: 104px !important;
        max-height: 104px !important;
        display: grid !important;
        grid-template-columns: 1fr auto 1fr !important;
        grid-template-rows: 52px 42px !important;
        align-items: center !important;
        padding: 0 16px !important;
        position: relative !important;
      }

      #header [data-device="desktop"] [data-column="start"],
      #header [data-device="desktop"] [data-id="logo"] {
        grid-column: 2 !important;
        grid-row: 1 !important;
        align-self: center !important;
        justify-self: center !important;
        position: relative !important;
        top: auto !important;
        left: auto !important;
        transform: none !important;
        width: auto !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
      }

      #header [data-device="desktop"] [data-column="middle"],
      #header [data-device="desktop"] [data-id="menu"],
      #header [data-device="desktop"] .header-menu-1 {
        grid-column: 1 / 4 !important;
        grid-row: 2 !important;
        align-self: center !important;
        justify-self: center !important;
        position: relative !important;
        top: auto !important;
        left: auto !important;
        transform: none !important;
        width: auto !important;
        height: auto !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 0 !important;
      }

      #header [data-device="desktop"] [data-column="end"] {
        grid-column: 3 !important;
        grid-row: 2 !important;
        align-self: center !important;
        justify-self: end !important;
        position: relative !important;
        top: auto !important;
        right: auto !important;
        bottom: auto !important;
        transform: none !important;
        display: flex !important;
        align-items: center !important;
        gap: 18px !important;
      }

      #header [data-device="desktop"] .header-menu-1 > ul,
      #header [data-device="desktop"] .header-menu-1 .menu {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 32px !important;
        width: auto !important;
        margin: 0 !important;
        padding: 0 !important;
      }

      #header [data-device="desktop"] .header-menu-1 .menu > li,
      #header [data-device="desktop"] .header-menu-1 > ul > li {
        margin: 0 !important;
      }

      #header [data-device="desktop"] .header-menu-1 .ct-menu-link {
        font-size: 13px !important;
        font-weight: 500 !important;
        line-height: 1 !important;
        padding: 0 !important;
        color: #0d141a !important;
        text-transform: uppercase !important;
      }
    }

    /* Instagram sin titulo, con franja negra como referencia */
    body.page-id-14 .pd-instagram-feed,
    body.home .pd-instagram-feed {
      width: 100vw !important;
      max-width: none !important;
      margin-left: calc(50% - 50vw) !important;
      margin-right: calc(50% - 50vw) !important;
      margin-bottom: 0 !important;
      padding: clamp(54px, 6vw, 78px) 0 !important;
      background: #101010 !important;
      overflow: hidden !important;
    }

    body.page-id-14 .pd-instagram-feed h2,
    body.home .pd-instagram-feed h2 {
      display: none !important;
    }

    body.page-id-14 .pd-instagram-grid,
    body.home .pd-instagram-grid {
      width: min(1224px, calc(100vw - 64px)) !important;
      max-width: 1224px !important;
      margin: 0 auto !important;
    }

    @media (max-width: 900px) {
      body.page-id-14 .pd-instagram-grid,
      body.home .pd-instagram-grid {
        width: min(100%, calc(100vw - 28px)) !important;
      }
    }
    </style>
    <script id="prime-drop-header-instagram-reference-fix-js">
    (function() {
      function tuneReferenceHeader() {
        if (window.innerWidth < 1000) return;
        document.querySelectorAll(
          '#header, #header.ct-header, #header [data-device="desktop"], #header .ct-sticky-container, #header [data-sticky], #header [data-device="desktop"] [data-row="middle"]'
        ).forEach(function(el) {
          el.style.setProperty('height', '104px', 'important');
          el.style.setProperty('min-height', '104px', 'important');
          el.style.setProperty('max-height', '104px', 'important');
          el.style.setProperty('position', 'relative', 'important');
          el.style.setProperty('top', 'auto', 'important');
          el.style.setProperty('transform', 'none', 'important');
        });
        document.querySelectorAll('#header [data-device="desktop"] .ct-container').forEach(function(el) {
          el.style.setProperty('height', '104px', 'important');
          el.style.setProperty('min-height', '104px', 'important');
          el.style.setProperty('max-height', '104px', 'important');
          el.style.setProperty('display', 'grid', 'important');
          el.style.setProperty('grid-template-columns', '1fr auto 1fr', 'important');
          el.style.setProperty('grid-template-rows', '52px 42px', 'important');
          el.style.setProperty('align-items', 'center', 'important');
          el.style.setProperty('padding', '0 16px', 'important');
        });
      }

      function run() {
        tuneReferenceHeader();
        document.querySelectorAll('body.page-id-14 .pd-instagram-feed h2, body.home .pd-instagram-feed h2').forEach(function(el) {
          el.style.setProperty('display', 'none', 'important');
        });
      }

      run();
      document.addEventListener('DOMContentLoaded', run);
      window.addEventListener('pageshow', run);
      window.addEventListener('scroll', tuneReferenceHeader, { passive: true });
      setTimeout(run, 400);
      setTimeout(run, 1400);
      setTimeout(run, 2800);
    })();
    </script>
    <?php
}, 100020);
/* PRIME_DROP_HEADER_INSTAGRAM_REFERENCE_FIX_END */
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
    session.headers.update({"User-Agent": "PrimeDropHeaderInstagramReferenceFix/1.0"})
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
    backup = Path("wp-backups") / f"functions_before_header_instagram_reference_fix_{datetime.now():%Y%m%d_%H%M%S}.php"
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
