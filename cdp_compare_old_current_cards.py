import asyncio
import base64
import json
import time
import urllib.parse
from pathlib import Path

import requests
import websockets

CDP = "http://127.0.0.1:9224"
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


def target(url):
    enc = urllib.parse.quote(url, safe="")
    r = requests.put(f"{CDP}/json/new?{enc}", timeout=10)
    if r.status_code >= 400:
        r = requests.get(f"{CDP}/json/new?{enc}", timeout=10)
    r.raise_for_status()
    return r.json()["webSocketDebuggerUrl"]


async def screenshot(ws, name):
    OUT.mkdir(exist_ok=True)
    img = await call(ws, "Page.captureScreenshot", {"format": "png", "fromSurface": True})
    p = OUT / name
    p.write_bytes(base64.b64decode(img["data"]))
    return str(p.resolve())


async def inspect(url, name, selector_expr, width=390, height=844, mobile=True):
    ws = await websockets.connect(target(url), max_size=20_000_000)
    await call(ws, "Page.enable")
    await call(ws, "Runtime.enable")
    await call(ws, "Emulation.setDeviceMetricsOverride", {
        "width": width,
        "height": height,
        "deviceScaleFactor": 1,
        "mobile": mobile,
        "hasTouch": mobile,
    })
    await call(ws, "Page.navigate", {"url": url})
    await asyncio.sleep(5)
    state = (await call(ws, "Runtime.evaluate", {"expression": f"""
      (() => {{
        const card = {selector_expr};
        const img = card && card.querySelector('img');
        const title = card && (card.querySelector('h2,h3,.product-title,.woocommerce-loop-product__title,[class*="title"]'));
        const price = card && (card.querySelector('.price,[class*="price"]'));
        const btn = card && (card.querySelector('button,a.button,[class*="button"],a[href*="cart"]'));
        const read = el => {{
          if (!el) return null;
          const r = el.getBoundingClientRect();
          const s = getComputedStyle(el);
          return {{
            tag: el.tagName,
            text: (el.innerText || el.textContent || '').trim().replace(/\\s+/g,' ').slice(0,120),
            x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height),
            display: s.display,
            background: s.backgroundColor,
            border: s.border,
            borderRadius: s.borderRadius,
            padding: s.padding,
            objectFit: s.objectFit,
            fontFamily: s.fontFamily,
            fontSize: s.fontSize,
            fontWeight: s.fontWeight,
            textAlign: s.textAlign,
            color: s.color
          }};
        }};
        return {{
          url: location.href,
          bodyText: document.body.innerText.replace(/\\s+/g,' ').slice(0,300),
          card: read(card),
          img: read(img),
          title: read(title),
          price: read(price),
          button: read(btn)
        }};
      }})()
    """, "returnByValue": True}))["result"]["value"]
    shot = await screenshot(ws, name)
    await ws.close()
    return {"state": state, "screenshot": shot}


async def main():
    ts = int(time.time())
    old = await inspect(
        f"https://prime-drop-builder-asmmz0g1emn5eupe.hostingersite.com/bolsos?oldcard={ts}",
        "old-bolsos-card.png",
        "document.querySelector('[data-qa=\"product-card\"], .store-product-card, .product-card, article, .grid a, a[href*=\"product\"], div')",
    )
    current = await inspect(
        f"https://primedropelite.com/bolsos/?currentcard={ts}",
        "current-bolsos-card-before-exact.png",
        "document.querySelector('body.page-id-547 .woocommerce ul.products li.product')",
    )
    print(json.dumps({"old": old, "current": current}, ensure_ascii=False, indent=2))


asyncio.run(main())
