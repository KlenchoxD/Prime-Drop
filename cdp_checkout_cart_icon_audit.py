import asyncio
import base64
import json
import sys
import time
import urllib.parse
from pathlib import Path

import requests
import websockets

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
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


async def open_page(url, width=390, height=844, mobile=True):
    ws = await websockets.connect(target(url), max_size=20_000_000)
    await call(ws, "Page.enable")
    await call(ws, "Runtime.enable")
    await call(ws, "Emulation.setDeviceMetricsOverride", {
        "width": width,
        "height": height,
        "deviceScaleFactor": 1,
        "mobile": mobile
    })
    await call(ws, "Page.navigate", {"url": url})
    await asyncio.sleep(3)
    return ws


async def main():
    ts = str(int(time.time()))
    results = {}

    ws = await open_page("https://primedropelite.com/product/angel-bag-black/?audit=" + ts, 390, 844, True)
    await call(ws, "Runtime.evaluate", {"expression": "document.querySelector('button.single_add_to_cart_button, .single_add_to_cart_button')?.click()", "returnByValue": True})
    await asyncio.sleep(2)
    await call(ws, "Page.navigate", {"url": "https://primedropelite.com/checkout/?audit=" + ts})
    await asyncio.sleep(4)
    results["checkout_top"] = await screenshot(ws, "audit-checkout-top-current.png")
    checkout_state = await call(ws, "Runtime.evaluate", {"expression": """
      (() => {
        const box = el => { if(!el) return null; const r=el.getBoundingClientRect(); return {x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height)} };
        return {
          url: location.href,
          title: box(document.querySelector('.entry-title,h1')),
          fields: Array.from(document.querySelectorAll('.woocommerce-billing-fields__field-wrapper .form-row')).map(row => ({
            id: row.id,
            label: row.querySelector('label')?.textContent?.trim().replace(/\\s+/g,' '),
            visible: getComputedStyle(row).display !== 'none',
            input: row.querySelector('input,select,textarea')?.id,
            tag: row.querySelector('input,select,textarea')?.tagName,
            select2: !!row.querySelector('.select2-container'),
            rect: box(row)
          })),
          checks: Array.from(document.querySelectorAll('input[type=checkbox],input[type=radio]')).slice(0,12).map(input => ({
            id: input.id, name: input.name, type: input.type, checked: input.checked,
            rect: box(input),
            bg: getComputedStyle(input).backgroundImage || getComputedStyle(input).backgroundColor,
            border: getComputedStyle(input).borderColor,
            label: document.querySelector('label[for="'+input.id+'"]')?.textContent?.trim().replace(/\\s+/g,' ')
          }))
        };
      })()
    """, "returnByValue": True})
    results["checkout_state"] = checkout_state["result"]["value"]
    await call(ws, "Runtime.evaluate", {"expression": "window.scrollTo(0, 850)", "returnByValue": True})
    await asyncio.sleep(.8)
    results["checkout_fields"] = await screenshot(ws, "audit-checkout-fields-current.png")
    await ws.close()

    ws = await open_page("https://primedropelite.com/?iconaudit=" + ts, 1200, 850, False)
    async def icon_state(label):
        state = await call(ws, "Runtime.evaluate", {"expression": """
          (() => {
            const svgs = Array.from(document.querySelectorAll('header [data-id="cart"] svg, .ct-header-cart svg, header a[href*="cart"] svg, .ct-cart-item svg'));
            return svgs.map(svg => ({cls: svg.getAttribute('class'), outer: svg.outerHTML.slice(0,240), opacity: getComputedStyle(svg).opacity}));
          })()
        """, "returnByValue": True})
        results[label] = state["result"]["value"]
    await icon_state("home_icon_after_load")
    await call(ws, "Runtime.evaluate", {"expression": "location.href='/bolsos/?iconaudit=" + ts + "'", "returnByValue": True})
    await asyncio.sleep(.25)
    await icon_state("bolsos_icon_250ms")
    await asyncio.sleep(2)
    await icon_state("bolsos_icon_after_load")
    results["bolsos_header"] = await screenshot(ws, "audit-bolsos-header-icon-current.png")
    await ws.close()

    print(json.dumps(results, ensure_ascii=False, indent=2))


asyncio.run(main())
