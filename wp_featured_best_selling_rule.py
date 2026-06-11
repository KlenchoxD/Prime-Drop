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

OLD = "/wp-json/wc/store/v1/products?per_page=8&orderby=date&order=desc"
NEW = "/wp-json/wc/store/v1/products?per_page=8&orderby=popularity&order=desc"


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


def main():
    session = requests.Session()
    session.headers.update({"User-Agent": "PrimeDropFeaturedBestSellingRule/1.0"})
    login(session)

    editor_url = urljoin(BASE, "/wp-admin/theme-editor.php?file=functions.php&theme=blocksy")
    page = session.get(editor_url, timeout=30)
    page.raise_for_status()

    textarea = re.search(r'<textarea[^>]+name=["\']newcontent["\'][^>]*>(.*?)</textarea>', page.text, re.S)
    if not textarea:
        raise RuntimeError("Could not find functions.php editor textarea")

    current = html.unescape(textarea.group(1))
    Path("wp-backups").mkdir(exist_ok=True)
    backup = Path("wp-backups") / f"functions_before_featured_best_selling_rule_{datetime.now():%Y%m%d_%H%M%S}.php"
    backup.write_text(current, encoding="utf-8")

    if OLD not in current and NEW not in current:
        raise RuntimeError("Featured products fetch URL not found")

    updated = current.replace(OLD, NEW)

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
    if resp.status_code != 200:
        raise RuntimeError(f"Update failed: {resp.status_code}")

    dashboard = session.get(urljoin(BASE, "/wp-admin/"), timeout=30)
    purged = False
    for href in re.findall(r'href=["\']([^"\']+)["\']', dashboard.text):
        raw = html.unescape(href)
        if "litespeed" in raw.lower() and "purge" in raw.lower():
            session.get(urljoin(BASE, raw), timeout=25)
            purged = True
            break

    print(f"updated=true backup={backup} purged={purged}")


if __name__ == "__main__":
    main()
