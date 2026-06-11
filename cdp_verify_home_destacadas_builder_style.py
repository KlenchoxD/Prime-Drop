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
    ws = await websockets.connect(target("https://primedropelite.com/?destacadasbuilder=" + str(int(time.time()))), max_size=20_000_000)
    await call(ws, "Page.enable")
    await call(ws, "Runtime.enable")
    await call(ws, "Emulation.setDeviceMetricsOverride", {
        "width": 1366,
        "height": 760,
        "deviceScaleFactor": 1,
        "mobile": False,
    })
    await call(ws, "Page.navigate", {"url": "https://primedropelite.com/?destacadasbuilder=" + str(int(time.time()))})
    await asyncio.sleep(5)
    await call(ws, "Runtime.evaluate", {"expression": """
      (() => {
        const heading = Array.from(document.querySelectorAll('h1,h2,h3')).find(h => /DESTACADAS/i.test(h.textContent || ''));
        if (heading) heading.scrollIntoView({block:'start'});
      })()
    """, "returnByValue": True})
    await asyncio.sleep(1.5)
    state = (await call(ws, "Runtime.evaluate", {"expression": r"""
      (() => {
        const heading = Array.from(document.querySelectorAll('h1,h2,h3')).find(h => /DESTACADAS/i.test(h.textContent || ''));
        const img = heading && Array.from(document.querySelectorAll('.woocommerce ul.products li.product img')).find(el => el.getBoundingClientRect().y > heading.getBoundingClientRect().y);
        const r = img && img.getBoundingClientRect();
        const s = img && getComputedStyle(img);
        return {
          heading: heading?.textContent?.trim(),
          img: img ? {x:Math.round(r.x), y:Math.round(r.y), w:Math.round(r.width), h:Math.round(r.height), objectFit:s.objectFit, background:s.backgroundColor, padding:s.padding} : null
        };
      })()
    """, "returnByValue": True}))["result"]["value"]
    OUT.mkdir(exist_ok=True)
    img = await call(ws, "Page.captureScreenshot", {"format": "png", "fromSurface": True})
    p = OUT / "audit-home-destacadas-builder-style.png"
    p.write_bytes(base64.b64decode(img["data"]))
    print(json.dumps({"state": state, "screenshot": str(p.resolve())}, ensure_ascii=False, indent=2))
    await ws.close()


asyncio.run(main())
