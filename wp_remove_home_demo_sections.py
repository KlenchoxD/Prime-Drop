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

MARKER_START = "/* PRIME_DROP_REMOVE_HOME_DEMO_SECTIONS_START */"
MARKER_END = "/* PRIME_DROP_REMOVE_HOME_DEMO_SECTIONS_END */"

BLOCK = r"""
/* PRIME_DROP_REMOVE_HOME_DEMO_SECTIONS_START */
add_action('template_redirect', function() {
    if (is_admin()) {
        return;
    }

    ob_start(function($html) {
        if (is_front_page() || is_page(14)) {
            $html = preg_replace('/<p\s+class=["\']pd-kicker["\'][^>]*>[\s\S]*?<\/p>/i', '', $html);
            $html = str_replace('&iexcl;DROP LIMITADO. ESTILO ILIMITADO!', '', $html);
            $html = str_replace('¡DROP LIMITADO. ESTILO ILIMITADO!', '', $html);
            $html = str_replace('NO SOMOS SOLO UNA TIENDA', '', $html);

            foreach (array('6f27344', '9855adf', 'f9e1dae') as $element_id) {
                $html = preg_replace(
                    '/\s*<section\b(?=[^>]*\belementor-top-section\b)(?=[^>]*\belementor-element-' . preg_quote($element_id, '/') . '\b)[\s\S]*?(?=<section\b[^>]*\belementor-top-section\b|<\/div><\/main>|<footer\b)/i',
                    '',
                    $html,
                    1
                );
            }

            $html = preg_replace('/\s*<section\b[^>]*>\s*<div[^>]*>\s*<div[^>]*>\s*<div[^>]*>\s*<div[^>]*>\s*<section\s+class=["\']pd-cta["\'][\s\S]*?(?=<\/div><\/main>|<footer\b)/i', '', $html, 1);
            $html = preg_replace('/\s*<section\s+class=["\']pd-cta["\'][\s\S]*?<\/section>/i', '', $html);
        }

        if (
            strpos($html, 'widget-title">About Us') !== false ||
            strpos($html, 'Our Clients') !== false ||
            strpos($html, 'widget-title">Quick Links') !== false ||
            strpos($html, 'Organisation Team') !== false ||
            strpos($html, '578-393-4937') !== false
        ) {
            $html = preg_replace(
                '/<div\s+data-row=["\']middle["\'][\s\S]*?(?=<div\s+data-row=["\']bottom["\']|<\/footer>)/i',
                '',
                $html,
                1
            );
        }

        return $html;
    });
}, 0);

add_action('wp_head', function() {
    ?>
    <style id="prime-drop-remove-home-demo-sections-css">
    body.page-id-14 .pd-kicker,
    body.page-id-14 .elementor-element-6f27344,
    body.page-id-14 .elementor-element-9855adf,
    body.page-id-14 .elementor-element-f9e1dae,
    body.page-id-14 .pd-about,
    body.page-id-14 .pd-cta {
      display: none !important;
    }
    </style>
    <?php
}, 9999);
/* PRIME_DROP_REMOVE_HOME_DEMO_SECTIONS_END */
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
    session.headers.update({"User-Agent": "PrimeDropRemoveHomeDemoSections/1.0"})
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
    backup = Path("wp-backups") / f"functions_before_remove_home_demo_sections_{datetime.now():%Y%m%d_%H%M%S}.php"
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
