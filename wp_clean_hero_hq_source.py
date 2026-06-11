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

MARKER_START = "/* PRIME_DROP_FORCE_CLIENT_HERO_SOURCE_START */"
MARKER_END = "/* PRIME_DROP_FORCE_CLIENT_HERO_SOURCE_END */"
HERO_URL = "https://primedropelite.com/wp-content/uploads/2026/06/prime-drop-hero-1080p-24fps-hq.mp4"

BLOCK = f"""
/* PRIME_DROP_FORCE_CLIENT_HERO_SOURCE_START */
add_filter('the_content', function($content) {{
    if (!is_front_page() && !is_page(14)) {{
        return $content;
    }}

    $hero_url = '{HERO_URL}';

    $content = preg_replace_callback('/<video[^>]*class=["\\'][^"\\']*pd-hero-video-bg[^"\\']*["\\'][\\s\\S]*?<\\/video>/i', function($matches) use ($hero_url) {{
        $video = $matches[0];
        $video = preg_replace('/\\s+poster=["\\'][^"\\']*["\\']/i', '', $video);

        if (preg_match('/\\s+preload=["\\'][^"\\']*["\\']/i', $video)) {{
            $video = preg_replace('/\\s+preload=["\\'][^"\\']*["\\']/i', ' preload="metadata"', $video);
        }} else {{
            $video = preg_replace('/<video\\b/i', '<video preload="metadata"', $video, 1);
        }}

        $source = '<source src="' . esc_url($hero_url) . '" type="video/mp4">';

        if (preg_match('/<source\\b[^>]*>/i', $video)) {{
            $video = preg_replace('/<source\\b[^>]*>/i', $source, $video, 1);
        }} else {{
            $video = preg_replace('/(<video\\b[^>]*>)/i', '$1' . $source, $video, 1);
        }}

        return $video;
    }}, $content);

    return $content;
}}, 1300);

add_action('wp_footer', function() {{
    if (!is_front_page() && !is_page(14)) {{
        return;
    }}
    ?>
    <script id="prime-drop-force-client-hero-source-js">
    (function() {{
      var newUrl = "{HERO_URL}";
      function run() {{
        document.querySelectorAll('.pd-hero video, video.pd-hero-video-bg').forEach(function(video) {{
          video.removeAttribute('poster');
          video.setAttribute('preload', 'metadata');
          var source = video.querySelector('source');
          if (source && source.getAttribute('src') !== newUrl) {{
            source.setAttribute('src', newUrl);
          }}
          if (video.getAttribute('src')) {{
            video.removeAttribute('src');
          }}
        }});
      }}
      run();
      document.addEventListener('DOMContentLoaded', run);
      window.addEventListener('pageshow', run);
    }})();
    </script>
    <?php
}}, 120);
/* PRIME_DROP_FORCE_CLIENT_HERO_SOURCE_END */
"""


def login(session):
    session.get(urljoin(BASE, "/wp-login.php"), timeout=30).raise_for_status()
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
    resp.raise_for_status()
    if "/wp-admin/" not in resp.url:
        raise RuntimeError("Login did not reach wp-admin")


def hidden_value(text, name):
    for tag in re.findall(r"<input[^>]+>", text, re.I):
        name_pattern = r"name=[\"']" + re.escape(name) + r"[\"']"
        if not re.search(name_pattern, tag, re.I):
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
    session.headers.update({"User-Agent": "PrimeDropCleanHeroHQSource/1.0"})
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
    backup = Path("wp-backups") / f"functions_before_clean_hero_hq_{datetime.now():%Y%m%d_%H%M%S}.php"
    backup.write_text(current, encoding="utf-8")

    pattern = re.compile(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), re.S)
    if not pattern.search(current):
        raise RuntimeError("Hero source marker block not found")
    updated = pattern.sub(lambda _: BLOCK.strip(), current)

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
