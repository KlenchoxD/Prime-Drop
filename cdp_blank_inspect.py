import asyncio, json, sys, time, urllib.parse
import requests, websockets
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CDP="http://127.0.0.1:9224"
async def call(ws,m,p=None,_id=[0]):
    _id[0]+=1; await ws.send(json.dumps({"id":_id[0],"method":m,"params":p or {}}))
    while True:
        d=json.loads(await ws.recv())
        if d.get("id")==_id[0]: return d
def target(url):
    enc=urllib.parse.quote(url,safe="")
    r=requests.put(f"{CDP}/json/new?{enc}",timeout=10)
    if r.status_code>=400:r=requests.get(f"{CDP}/json/new?{enc}",timeout=10)
    r.raise_for_status(); return r.json()["webSocketDebuggerUrl"]
async def inspect(url, name):
    async with websockets.connect(target(url),max_size=20_000_000) as ws:
        await call(ws,"Page.enable"); await call(ws,"Runtime.enable")
        await call(ws,"Emulation.setDeviceMetricsOverride",{"width":390,"height":844,"deviceScaleFactor":1,"mobile":True})
        await call(ws,"Page.navigate",{"url":url}); await asyncio.sleep(4)
        res=await call(ws,"Runtime.evaluate",{"expression":"""
        (() => {
          const els = Array.from(document.querySelectorAll('body,main,article,section,div,header,.ct-container,.ct-container-full,.entry-content,.site-main,.woocommerce,.product,.woocommerce-notices-wrapper,.woocommerce-breadcrumb,.hero-section,.page-title,.entry-header,.ct-breadcrumbs'));
          return els.map(el => {
            const r=el.getBoundingClientRect(), cs=getComputedStyle(el);
            return {
              tag:el.tagName, id:el.id, cls:String(el.className).slice(0,130),
              text:(el.textContent||'').trim().replace(/\\s+/g,' ').slice(0,70),
              x:Math.round(r.x), y:Math.round(r.y), w:Math.round(r.width), h:Math.round(r.height),
              mt:cs.marginTop, mb:cs.marginBottom, pt:cs.paddingTop, pb:cs.paddingBottom,
              minH:cs.minHeight, display:cs.display
            }
          }).filter(e => e.w>0 && e.h>0 && e.y < 1200).sort((a,b)=>a.y-b.y || b.h-a.h).slice(0,140);
        })()
        ""","returnByValue":True})
        print("====",name,"====")
        print(json.dumps(res["result"]["result"]["value"],ensure_ascii=False,indent=2))
async def main():
    ts=str(int(time.time()))
    await inspect("https://primedropelite.com/product/cheyann-bag-black/?nocache="+ts,"product")
    await inspect("https://primedropelite.com/checkout/?nocache="+ts,"checkout")
asyncio.run(main())
