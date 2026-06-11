import html
import json
import mimetypes
import os
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import requests

BASE = "https://primedropelite.com"
USER = os.environ["PD_WP_USER"]
PASS = os.environ["PD_WP_PASS"]
VIDEO_PATH = Path(r"C:\Users\Kleiner\Downloads\ABDM\IMG_1435.MOV")

OLD_VIDEO_URL = "https://videos.pexels.com/video-files/6649983/6649983-uhd_2732_1440_25fps.mp4"
MARKER_START = "/* PRIME_DROP_HOME_HERO_LOCAL_VIDEO_START */"
MARKER_END = "/* PRIME_DROP_HOME_HERO_LOCAL_VIDEO_END */"


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


def extract_rest_nonce(text):
    patterns = [
        r'wpApiSettings\s*=\s*[^;]*"nonce"\s*:\s*"([^"]+)"',
        r'"nonce"\s*:\s*"([a-f0-9]{10,})"',
        r'wp-api-fetch.*?nonce"\s*:\s*"([^"]+)"',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.S | re.I)
        if match:
            return html.unescape(match.group(1))
    return ""


def get_rest_nonce(session):
    page = session.get(urljoin(BASE, "/wp-admin/upload.php"), timeout=35)
    page.raise_for_status()
    nonce = extract_rest_nonce(page.text)
    if not nonce:
        page = session.get(urljoin(BASE, "/wp-admin/post.php?post=14&action=edit"), timeout=35)
        page.raise_for_status()
        nonce = extract_rest_nonce(page.text)
    if not nonce:
        raise RuntimeError("Could not find REST nonce")
    return nonce


def find_existing_media(session, nonce):
    resp = session.get(
        urljoin(BASE, "/wp-json/wp/v2/media?search=IMG_1435&per_page=20&context=edit"),
        headers={"X-WP-Nonce": nonce},
        timeout=35,
    )
    if resp.status_code != 200:
        return None
    for item in resp.json():
        source = item.get("source_url", "")
        title = item.get("title", {}).get("raw", "") or item.get("title", {}).get("rendered", "")
        if "IMG_1435" in source or "IMG_1435" in title or "Prime Drop Hero IMG 1435" in title:
            return item
    return None


def upload_video(session, nonce):
    if not VIDEO_PATH.exists():
        raise FileNotFoundError(str(VIDEO_PATH))

    existing = find_existing_media(session, nonce)
    if existing:
        return existing, False

    mime = mimetypes.guess_type(str(VIDEO_PATH))[0] or "video/quicktime"
    if VIDEO_PATH.suffix.lower() == ".mov":
        mime = "video/quicktime"

    data = VIDEO_PATH.read_bytes()
    resp = session.post(
        urljoin(BASE, "/wp-json/wp/v2/media"),
        headers={
            "X-WP-Nonce": nonce,
            "Content-Disposition": 'attachment; filename="IMG_1435.MOV"',
            "Content-Type": mime,
        },
        data=data,
        timeout=180,
    )
    if resp.status_code not in (200, 201):
        raise RuntimeError(f"Media upload failed: {resp.status_code} {resp.text[:500]}")

    item = resp.json()
    media_id = item["id"]
    session.post(
        urljoin(BASE, f"/wp-json/wp/v2/media/{media_id}"),
        headers={"X-WP-Nonce": nonce, "Content-Type": "application/json"},
        data=json.dumps({
            "title": "Prime Drop Hero IMG 1435",
            "alt_text": "Prime Drop hero video",
            "caption": "",
            "description": "",
        }),
        timeout=35,
    )
    return item, True


def update_functions(session, video_url):
    video_type = "video/mp4" if video_url.lower().split("?")[0].endswith(".mp4") else "video/quicktime"
    block = f"""
/* PRIME_DROP_HOME_HERO_LOCAL_VIDEO_START */
add_filter('the_content', function($content) {{
    if (!is_front_page() && !is_page(14)) {{
        return $content;
    }}

    $old_source = '<source src="{OLD_VIDEO_URL}" type="video/mp4">';
    $new_source = '<source src="' . esc_url('{video_url}') . '" type="{video_type}">';
    $content = str_replace($old_source, $new_source, $content);
    $content = str_replace('{OLD_VIDEO_URL}', esc_url('{video_url}'), $content);
    return $content;
}}, 999);

add_action('wp_footer', function() {{
    if (!is_front_page() && !is_page(14)) {{
        return;
    }}
    ?>
    <style id="prime-drop-home-hero-local-video-css">
    .pd-hero,
    .pd-hero-video.hero-section,
    .hero-video-section {{
      position: relative !important;
      overflow: hidden !important;
    }}

    .pd-hero .pd-hero-video-bg,
    .pd-hero video,
    .hero-video-section video {{
      position: absolute !important;
      top: 50% !important;
      left: 50% !important;
      transform: translate(-50%, -50%) !important;
      min-width: 100% !important;
      min-height: 100% !important;
      width: auto !important;
      height: auto !important;
      object-fit: cover !important;
      object-position: center center !important;
      z-index: 0 !important;
    }}
    </style>
    <?php
}}, 10320);
/* PRIME_DROP_HOME_HERO_LOCAL_VIDEO_END */
""".strip()

    editor_url = urljoin(BASE, "/wp-admin/theme-editor.php?file=functions.php&theme=blocksy")
    page = session.get(editor_url, timeout=30)
    page.raise_for_status()

    textarea = re.search(r'<textarea[^>]+name=["\']newcontent["\'][^>]*>(.*?)</textarea>', page.text, re.S)
    if not textarea:
        raise RuntimeError("Could not find functions.php editor textarea")

    current = html.unescape(textarea.group(1))
    Path("wp-backups").mkdir(exist_ok=True)
    backup = Path("wp-backups") / f"functions_before_home_hero_video_{datetime.now():%Y%m%d_%H%M%S}.php"
    backup.write_text(current, encoding="utf-8")

    pattern = re.compile(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), re.S)
    if pattern.search(current):
        updated = pattern.sub(lambda _: block, current)
    else:
        updated = current.rstrip() + "\n\n" + block + "\n"

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
        raise RuntimeError(f"functions.php update failed: {resp.status_code}")
    return str(backup)


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
    session.headers.update({"User-Agent": "PrimeDropReplaceHomeHeroVideo/1.0"})
    login(session)
    rest_nonce = get_rest_nonce(session)
    media, uploaded = upload_video(session, rest_nonce)
    video_url = media["source_url"]
    backup = update_functions(session, video_url)
    purged = purge_cache(session)
    print(json.dumps({
        "updated": True,
        "uploaded": uploaded,
        "media_id": media.get("id"),
        "video_url": video_url,
        "functions_backup": backup,
        "purged": purged,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
