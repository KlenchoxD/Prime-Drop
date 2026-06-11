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


async def main():
    url = "https://primedropelite.com/bolsos/?mobilecardoldstyle=" + str(int(time.time()))
    ws = await websockets.connect(target(url), max_size=20_000_000)
    await call(ws, "Page.enable")
    await call(ws, "Runtime.enable")
    await call(ws, "Emulation.setDeviceMetricsOverride", {
        "width": 390,
        "height": 844,
        "deviceScaleFactor": 1,
        "mobile": True,
        "hasTouch": True,
    })
    await call(ws, "Page.navigate", {"url": url})
    await asyncio.sleep(5)
    OUT.mkdir(exist_ok=True)
    img = await call(ws, "Page.captureScreenshot", {"format": "png", "fromSurface": True})
    p = OUT / "audit-bolsos-old-card-mobile.png"
    p.write_bytes(base64.b64decode(img["data"]))
    state = (await call(ws, "Runtime.evaluate", {"expression": r"""
      (() => {
        const card = document.querySelector('body.page-id-547 .woocommerce ul.products li.product');
        const img = card?.querySelector('img');
        const btn = card?.querySelector('.button');
        const title = card?.querySelector('.woocommerce-loop-product__title');
        const price = card?.querySelector('.price');
        const read = el => {
          if (!el) return null;
          const r = el.getBoundingClientRect();
          const s = getComputedStyle(el);
          return {
            text: (el.innerText || el.textContent || '').trim().replace(/\s+/g,' '),
            x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height),
            background: s.backgroundColor,
            border: s.border,
            objectFit: s.objectFit,
            textAlign: s.textAlign,
            borderRadius: s.borderRadius
          };
        };
        return {card:read(card), img:read(img), title:read(title), price:read(price), button:read(btn)};
      })()
    """, "returnByValue": True}))["result"]["value"]
    print(json.dumps({"screenshot": str(p.resolve()), "state": state}, ensure_ascii=False, indent=2))
    await ws.close()


asyncio.run(main())
