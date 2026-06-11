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


async def shot(ws, name):
    OUT.mkdir(exist_ok=True)
    img = await call(ws, "Page.captureScreenshot", {"format": "png", "fromSurface": True})
    p = OUT / name
    p.write_bytes(base64.b64decode(img["data"]))
    return str(p.resolve())


async def main():
    ws = await websockets.connect(
        target("https://primedropelite.com/bolsos/?imgcontaincheck=" + str(int(time.time()))),
        max_size=20_000_000,
    )
    await call(ws, "Page.enable")
    await call(ws, "Runtime.enable")
    await call(ws, "Emulation.setDeviceMetricsOverride", {
        "width": 1366,
        "height": 760,
        "deviceScaleFactor": 1,
        "mobile": False,
    })
    await call(ws, "Page.navigate", {"url": "https://primedropelite.com/bolsos/?imgcontaincheck=" + str(int(time.time()))})
    await asyncio.sleep(5)
    state = (await call(ws, "Runtime.evaluate", {"expression": r"""
      (() => {
        const img = document.querySelector('body.page-id-547 .woocommerce ul.products li.product img');
        const card = img && img.closest('li.product');
        const style = img && getComputedStyle(img);
        const rect = img && img.getBoundingClientRect();
        const cardRect = card && card.getBoundingClientRect();
        return {
          imgFound: !!img,
          title: card?.querySelector('.woocommerce-loop-product__title')?.textContent?.trim(),
          src: img?.currentSrc || img?.src,
          imgRect: rect ? {x:Math.round(rect.x), y:Math.round(rect.y), w:Math.round(rect.width), h:Math.round(rect.height)} : null,
          cardRect: cardRect ? {x:Math.round(cardRect.x), y:Math.round(cardRect.y), w:Math.round(cardRect.width), h:Math.round(cardRect.height)} : null,
          objectFit: style?.objectFit,
          background: style?.backgroundColor,
          padding: style?.padding,
          borderRadius: style?.borderRadius
        };
      })()
    """, "returnByValue": True}))["result"]["value"]
    image = await shot(ws, "audit-bolsos-images-complete.png")
    print(json.dumps({"state": state, "screenshot": image}, ensure_ascii=False, indent=2))
    await ws.close()


asyncio.run(main())
