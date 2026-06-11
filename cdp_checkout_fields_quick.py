import asyncio, base64, json, sys, time, urllib.parse
from pathlib import Path
import requests, websockets

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

async def main():
    ts = str(int(time.time()))
    ws = await websockets.connect(target("https://primedropelite.com/product/angel-bag-black/?quick=" + ts), max_size=20_000_000)
    await call(ws, "Page.enable")
    await call(ws, "Runtime.enable")
    await call(ws, "Emulation.setDeviceMetricsOverride", {"width": 390, "height": 844, "deviceScaleFactor": 1, "mobile": True})
    await call(ws, "Page.navigate", {"url": "https://primedropelite.com/product/angel-bag-black/?quick=" + ts})
    await asyncio.sleep(4)
    await call(ws, "Runtime.evaluate", {"expression": "document.querySelector('button.single_add_to_cart_button, .single_add_to_cart_button')?.click()", "returnByValue": True})
    await asyncio.sleep(2)
    await call(ws, "Page.navigate", {"url": "https://primedropelite.com/checkout/?quick=" + ts})
    await asyncio.sleep(5)
    await call(ws, "Runtime.evaluate", {"expression": "window.scrollTo(0, 760)", "returnByValue": True})
    await asyncio.sleep(1)
    shot = await screenshot(ws, "audit-checkout-fields-quick.png")
    state = await call(ws, "Runtime.evaluate", {"expression": """
      (() => {
        const box = el => { if(!el) return null; const r=el.getBoundingClientRect(); return {x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height)} };
        const ids = ['billing_state_field','billing_city_field','createaccount','ship-to-different-address-checkbox'];
        return {
          screenshot: null,
          fields: ids.map(id => {
            const el = document.getElementById(id);
            return {id, rect: box(el), text: el?.textContent?.trim().replace(/\\s+/g,' ') || document.querySelector('label[for="'+id+'"]')?.textContent?.trim().replace(/\\s+/g,' '), tag: el?.tagName, checked: el?.checked, bg: el ? (getComputedStyle(el).backgroundImage || getComputedStyle(el).backgroundColor) : null, border: el ? getComputedStyle(el).borderColor : null};
          })
        }
      })()
    """, "returnByValue": True})
    result = state["result"]["value"]
    result["screenshot"] = shot
    print(json.dumps(result, ensure_ascii=False, indent=2))
    await ws.close()

asyncio.run(main())
