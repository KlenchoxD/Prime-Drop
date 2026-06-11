import asyncio
import base64
import json
import shutil
import subprocess
import tempfile
import time
import urllib.parse
from pathlib import Path

import requests
import websockets


CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PORT = 9231
CDP = f"http://127.0.0.1:{PORT}"
OUT = Path("audit-screens")


async def call(ws, method, params=None, _id=[0]):
    _id[0] += 1
    await ws.send(json.dumps({"id": _id[0], "method": method, "params": params or {}}))
    while True:
        data = json.loads(await ws.recv())
        if data.get("id") == _id[0]:
            if "error" in data:
                raise RuntimeError(data["error"])
            return data.get("result", {})


def wait_for_cdp():
    for _ in range(80):
        try:
            requests.get(f"{CDP}/json/version", timeout=0.25).raise_for_status()
            return
        except Exception:
            time.sleep(0.15)
    raise RuntimeError("Chrome CDP did not start")


def target(url):
    enc = urllib.parse.quote(url, safe="")
    resp = requests.put(f"{CDP}/json/new?{enc}", timeout=10)
    if resp.status_code >= 400:
        resp = requests.get(f"{CDP}/json/new?{enc}", timeout=10)
    resp.raise_for_status()
    return resp.json()["webSocketDebuggerUrl"]


async def open_page(url, width, height, mobile=False):
    ws = await websockets.connect(target(url), max_size=30_000_000)
    await call(ws, "Page.enable")
    await call(ws, "Runtime.enable")
    await call(
        ws,
        "Emulation.setDeviceMetricsOverride",
        {"width": width, "height": height, "deviceScaleFactor": 1, "mobile": mobile},
    )
    await call(ws, "Page.navigate", {"url": url})
    await asyncio.sleep(4.2)
    await call(ws, "Runtime.evaluate", {"expression": "document.querySelector('.ct-cookies-accept-button')?.click()", "returnByValue": True})
    await asyncio.sleep(0.8)
    return ws


async def screenshot(ws, name):
    OUT.mkdir(exist_ok=True)
    img = await call(ws, "Page.captureScreenshot", {"format": "png", "fromSurface": True})
    path = OUT / name
    path.write_bytes(base64.b64decode(img["data"]))
    return str(path.resolve())


async def inspect(ws):
    expression = r"""
    (() => {
      const box = el => {
        if (!el) return null;
        const r = el.getBoundingClientRect();
        return {x:Math.round(r.x), y:Math.round(r.y), w:Math.round(r.width), h:Math.round(r.height)};
      };
      const css = (el, prop) => el ? getComputedStyle(el)[prop] : null;
      const cards = [...document.querySelectorAll('body:not(.single-product) .woocommerce ul.products li.product')].slice(0,4).map(card => ({
        card: box(card),
        figure: box(card.querySelector('figure, .ct-media-container')),
        img: box(card.querySelector('img')),
        title: box(card.querySelector('.woocommerce-loop-product__title')),
        titleText: (card.querySelector('.woocommerce-loop-product__title')?.textContent || '').trim(),
        titleAlign: css(card.querySelector('.woocommerce-loop-product__title'), 'textAlign'),
        price: (card.querySelector('.price')?.textContent || '').replace(/\s+/g, ' ').trim(),
        priceBox: box(card.querySelector('.price')),
        button: box(card.querySelector('.button')),
        buttonOpacity: css(card.querySelector('.button'), 'opacity'),
        buttonVisibility: css(card.querySelector('.button'), 'visibility')
      }));
      return {
        viewport: {w: innerWidth, h: innerHeight},
        top: box(document.querySelector('.woo-listing-top')),
        count: box(document.querySelector('.woocommerce-result-count')),
        search: box(document.querySelector('.pd-professional-shop-search')),
        order: box(document.querySelector('.woocommerce-ordering')),
        oldBrandRail: !!document.querySelector('.pd-listing-brand-rail'),
        oldBrandFilter: !!document.querySelector('.pd-brand-filter'),
        sidebarFilterDisplay: css(document.querySelector('.pd-shop-filters'), 'display'),
        menuTexts: [...document.querySelectorAll('#header [data-device="desktop"] .pd-bolsos-submenu a')].map(a => a.textContent.trim()),
        menuVisible: css(document.querySelector('#header [data-device="desktop"] .pd-bolsos-submenu'), 'visibility'),
        cards
      };
    })()
    """
    return (await call(ws, "Runtime.evaluate", {"expression": expression, "returnByValue": True}))["result"]["value"]


async def hover_menu(ws):
    await call(ws, "Runtime.evaluate", {
        "expression": """
        (() => {
          const link = document.querySelector('#header [data-device="desktop"] .pd-bolsos-menu-parent > a');
          if (!link) return false;
          link.dispatchEvent(new MouseEvent('mouseenter', {bubbles:true, view:window}));
          link.parentElement.dispatchEvent(new MouseEvent('mouseenter', {bubbles:true, view:window}));
          link.parentElement.classList.add('pd-submenu-open');
          return true;
        })()
        """,
        "returnByValue": True,
    })
    await asyncio.sleep(0.3)
    return (await call(ws, "Runtime.evaluate", {
        "expression": """
        (() => {
          const sub = document.querySelector('#header [data-device="desktop"] .pd-bolsos-menu-parent > .pd-bolsos-submenu');
          const r = sub?.getBoundingClientRect();
          return {
            visible: sub ? getComputedStyle(sub).visibility : null,
            opacity: sub ? getComputedStyle(sub).opacity : null,
            box: sub ? {x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height)} : null,
            texts: sub ? [...sub.querySelectorAll('a')].map(a=>a.textContent.trim()) : []
          };
        })()
        """,
        "returnByValue": True,
    }))["result"]["value"]


async def main():
    tmp = tempfile.mkdtemp(prefix="prime-drop-cdp-")
    proc = subprocess.Popen([
        CHROME,
        "--headless=new",
        f"--remote-debugging-port={PORT}",
        f"--user-data-dir={tmp}",
        "--disable-gpu",
        "--hide-scrollbars",
        "about:blank",
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        wait_for_cdp()
        ts = int(time.time())
        results = {}
        pages = [
            ("bolsos_desktop", f"https://primedropelite.com/bolsos/?visual_verify={ts}", 1366, 768, False),
            ("karl_desktop", f"https://primedropelite.com/product-category/karl-lagerfeld/?visual_verify={ts}", 1366, 768, False),
            ("home_desktop", f"https://primedropelite.com/?visual_verify={ts}", 1366, 768, False),
            ("bolsos_mobile", f"https://primedropelite.com/bolsos/?visual_verify={ts}", 390, 844, True),
            ("bolsos_tablet", f"https://primedropelite.com/bolsos/?visual_verify={ts}", 768, 1024, True),
        ]

        for name, url, width, height, mobile in pages:
            ws = await open_page(url, width, height, mobile)
            results[name] = await inspect(ws)
            if name == "bolsos_desktop":
                results["menu_hover"] = await hover_menu(ws)
            results[name + "_png"] = await screenshot(ws, f"{name}.png")
            await ws.close()

        print(json.dumps(results, ensure_ascii=False, indent=2))
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        shutil.rmtree(tmp, ignore_errors=True)


asyncio.run(main())
