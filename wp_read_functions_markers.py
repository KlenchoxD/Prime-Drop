import html
import os
import re
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


def main():
    session = requests.Session()
    session.trust_env = False
    session.headers.update({"User-Agent": "PrimeDropReadFunctionsMarkers/1.0"})
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
    snapshot = Path("wp-backups") / "functions_current_snapshot.php"
    snapshot.write_text(current, encoding="utf-8")

    markers = sorted(set(re.findall(r"/\*\s*(PRIME_DROP_[A-Z0-9_]+)_START\s*\*/", current)))
    print(f"bytes={len(current.encode('utf-8'))}")
    print(f"snapshot={snapshot}")
    print("markers:")
    for marker in markers:
        print(f"- {marker}")

    hero_hits = re.findall(r"https?://[^\"'\s<>]+(?:mp4|MOV|mov)", current)
    print("video_urls:")
    for url in sorted(set(hero_hits)):
        print(f"- {url}")


if __name__ == "__main__":
    main()
