import html
import os
import re
from urllib.parse import urljoin

import requests

BASE = "https://primedropelite.com"
USER = os.environ["PD_WP_USER"]
PASS = os.environ["PD_WP_PASS"]


def login(session):
    login_url = urljoin(BASE, "/wp-login.php")
    session.get(login_url, timeout=30).raise_for_status()
    resp = session.post(
        login_url,
        data={
            "log": USER,
            "pwd": PASS,
            "wp-submit": "Acceder",
            "redirect_to": urljoin(BASE, "/wp-admin/"),
            "testcookie": "1",
        },
        timeout=30,
        allow_redirects=True,
    )
    resp.raise_for_status()


def main():
    session = requests.Session()
    session.headers.update({"User-Agent": "PrimeDropPurge/1.0"})
    login(session)
    dashboard = session.get(urljoin(BASE, "/wp-admin/"), timeout=30)
    dashboard.raise_for_status()

    purged = False
    for href in re.findall(r'href=["\']([^"\']+)["\']', dashboard.text):
        raw = html.unescape(href)
        if "litespeed" in raw.lower() and "purge" in raw.lower():
            session.get(urljoin(BASE, raw), timeout=25)
            purged = True
            break

    print(f"purged={purged}")


if __name__ == "__main__":
    main()
