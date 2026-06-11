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

BAD_START = "/* PRIME_DROP_REMOVE_HOME_DEMO_SECTIONS_START */"
BAD_END = "/* PRIME_DROP_REMOVE_HOME_DEMO_SECTIONS_END */"
MARKER_START = "/* PRIME_DROP_EMERGENCY_SAFE_HOME_FOOTER_START */"
MARKER_END = "/* PRIME_DROP_EMERGENCY_SAFE_HOME_FOOTER_END */"

BLOCK = r"""
/* PRIME_DROP_EMERGENCY_SAFE_HOME_FOOTER_START */
add_action('wp_head', function() {
    ?>
    <style id="prime-drop-emergency-safe-home-footer-css">
    /* Ocultar sin romper HTML */
    body.page-id-14 .pd-kicker,
    body.page-id-14 .elementor-element-6f27344,
    body.page-id-14 .elementor-element-9855adf,
    body.page-id-14 .elementor-element-f9e1dae,
    body.page-id-14 .pd-about,
    body.page-id-14 .about-section,
    body.page-id-14 .quienes-somos-section,
    body.page-id-14 .pd-cta {
      display: none !important;
    }

    footer.ct-footer,
    #footer.ct-footer,
    .ct-footer {
      display: none !important;
      visibility: hidden !important;
      height: 0 !important;
      min-height: 0 !important;
      overflow: hidden !important;
      padding: 0 !important;
      margin: 0 !important;
    }

    footer.pd-footer {
      display: block !important;
      visibility: visible !important;
      height: auto !important;
      min-height: 0 !important;
      overflow: visible !important;
      background: #000000 !important;
      color: #ffffff !important;
      padding: clamp(52px, 6vw, 84px) 0 24px !important;
      margin: 0 !important;
      font-family: 'Roboto Serif', Georgia, serif !important;
    }

    .pd-footer,
    .pd-footer * {
      color: #ffffff !important;
      font-family: 'Roboto Serif', Georgia, serif !important;
      box-sizing: border-box !important;
    }

    .pd-footer-grid {
      width: min(980px, calc(100vw - 48px)) !important;
      margin: 0 auto !important;
      display: grid !important;
      grid-template-columns: minmax(240px, 1.2fr) minmax(180px, .8fr) minmax(190px, .8fr) minmax(190px, .8fr) !important;
      gap: clamp(34px, 5vw, 74px) !important;
      align-items: start !important;
    }

    .pd-footer h3,
    .pd-footer h4 {
      margin: 0 0 18px !important;
      color: #ffffff !important;
      font-weight: 800 !important;
      letter-spacing: .5px !important;
      text-transform: uppercase !important;
      line-height: 1.15 !important;
    }

    .pd-footer h3 {
      font-size: 24px !important;
    }

    .pd-footer h4 {
      font-size: 14px !important;
    }

    .pd-footer p,
    .pd-footer li,
    .pd-footer a {
      font-size: 13px !important;
      line-height: 1.65 !important;
      text-decoration: none !important;
    }

    .pd-footer ul {
      list-style: none !important;
      margin: 0 !important;
      padding: 0 !important;
      display: grid !important;
      gap: 8px !important;
    }

    .pd-footer-brand p {
      max-width: 320px !important;
      margin: 0 0 22px !important;
    }

    .pd-social-icons {
      display: flex !important;
      align-items: center !important;
      gap: 10px !important;
      flex-wrap: wrap !important;
    }

    .pd-social-icons a {
      width: 34px !important;
      height: 34px !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      border: 1px solid rgba(255,255,255,.38) !important;
      border-radius: 50% !important;
      background: transparent !important;
    }

    .pd-social-icons svg,
    .pd-social-icons img {
      width: 16px !important;
      height: 16px !important;
      fill: #ffffff !important;
      stroke: #ffffff !important;
      filter: brightness(0) invert(1) !important;
    }

    .pd-footer .pd-footer-contact {
      display: grid !important;
      gap: 8px !important;
    }

    .pd-footer-bottom {
      width: min(980px, calc(100vw - 48px)) !important;
      margin: 42px auto 0 !important;
      padding-top: 22px !important;
      border-top: 1px solid rgba(255,255,255,.18) !important;
      text-align: center !important;
      font-size: 12px !important;
      justify-content: center !important;
    }

    @media (max-width: 900px) {
      .pd-footer-grid {
        grid-template-columns: 1fr 1fr !important;
        gap: 34px 24px !important;
      }
    }

    @media (max-width: 560px) {
      .pd-footer-grid {
        grid-template-columns: 1fr !important;
      }
    }
    </style>
    <?php
}, 10000);

add_action('wp_footer', function() {
    ?>
    <script id="prime-drop-remove-blocksy-demo-footer-js">
    (function() {
      var defaultFooter = document.querySelector('#footer.ct-footer');
      if (defaultFooter) {
        defaultFooter.remove();
      }
    })();
    </script>
    <?php
}, 10000);
/* PRIME_DROP_EMERGENCY_SAFE_HOME_FOOTER_END */
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
    session.headers.update({"User-Agent": "PrimeDropEmergencyRestoreFooterSafe/1.0"})
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
    backup = Path("wp-backups") / f"functions_before_emergency_restore_footer_{datetime.now():%Y%m%d_%H%M%S}.php"
    backup.write_text(current, encoding="utf-8")

    bad_pattern = re.compile(re.escape(BAD_START) + r".*?" + re.escape(BAD_END), re.S)
    updated = bad_pattern.sub("", current)

    pattern = re.compile(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), re.S)
    if pattern.search(updated):
        updated = pattern.sub(lambda _: BLOCK.strip(), updated)
    else:
        updated = updated.rstrip() + "\n\n" + BLOCK.strip() + "\n"

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
