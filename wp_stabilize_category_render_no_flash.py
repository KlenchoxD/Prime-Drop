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


def block_pattern(start, end):
    return re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)


def replace_block(content, start, end, callback):
    pattern = block_pattern(start, end)
    match = pattern.search(content)
    if not match:
        return content, False
    return content[: match.start()] + callback(match.group(0)) + content[match.end() :], True


def move_style_block_to_head(block, priority):
    block = block.replace("add_action('wp_footer', function() {", "add_action('wp_head', function() {")
    block = re.sub(r"\},\s*(?:PHP_INT_MAX|\d+)\);\s*/\*", f"}}, {priority});\n/*", block, count=1)
    return block


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
    session.headers.update({"User-Agent": "PrimeDropCategoryNoFlash/1.0"})
    login(session)

    editor_url = urljoin(BASE, "/wp-admin/theme-editor.php?file=functions.php&theme=blocksy")
    page = session.get(editor_url, timeout=30)
    page.raise_for_status()

    textarea = re.search(r'<textarea[^>]+name=["\']newcontent["\'][^>]*>(.*?)</textarea>', page.text, re.S)
    if not textarea:
        raise RuntimeError("Could not find functions.php editor textarea")

    current = html.unescape(textarea.group(1))
    Path("wp-backups").mkdir(exist_ok=True)
    backup = Path("wp-backups") / f"functions_before_category_no_flash_{datetime.now():%Y%m%d_%H%M%S}.php"
    backup.write_text(current, encoding="utf-8")

    updated = current

    old_start = "/* PRIME_DROP_TAX_CATEGORIES_MATCH_BOLSOS_START */"
    old_end = "/* PRIME_DROP_TAX_CATEGORIES_MATCH_BOLSOS_END */"
    updated, removed_old_match = replace_block(updated, old_start, old_end, lambda _: "")

    blocks = [
        (
            "/* PRIME_DROP_MATCH_BUILDER_PRODUCTS_START */",
            "/* PRIME_DROP_MATCH_BUILDER_PRODUCTS_END */",
            18,
        ),
        (
            "/* PRIME_DROP_TAX_CATEGORIES_FORCE_BOLSOS_GRID_START */",
            "/* PRIME_DROP_TAX_CATEGORIES_FORCE_BOLSOS_GRID_END */",
            19,
        ),
        (
            "/* PRIME_DROP_CATEGORY_SEARCH_CART_EMPTY_FIXES_START */",
            "/* PRIME_DROP_CATEGORY_SEARCH_CART_EMPTY_FIXES_END */",
            20,
        ),
    ]

    moved = []
    for start, end, priority in blocks:
        updated, did_move = replace_block(updated, start, end, lambda block, p=priority: move_style_block_to_head(block, p))
        moved.append((start, did_move))

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

    print(
        "updated=true "
        f"backup={backup} "
        f"removed_old_match={removed_old_match} "
        f"moved={moved} "
        f"purged={purge_cache(session)}"
    )


if __name__ == "__main__":
    main()
