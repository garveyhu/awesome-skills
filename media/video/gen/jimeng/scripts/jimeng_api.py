#!/usr/bin/env python3
"""即梦图像/视频生成 · 火山 visual API(visual.volcengineapi.com) · V4 签名 · 同步/异步统一入口。
关键:AK/SK 直连,【不需要 maestro vip】(区别 dreamina CLI——CLI 普通账号被拦)。
读 ~/.agents/resources.json 的 media_generation.volcengine.personal 取 AK/SK。

== model 速查 ==
 绘图:
   t2i-4.0   文生图4.0(主力·4K·异步)        --model t2i-4.0 --prompt "..." --out o.png [--width 2048 --height 2048]
   t2i-2.1   文生图2.1(手绘温度好·同步)
   i2i-3.0   图生图3.0(喂基准图保一致·同步)   --model i2i-3.0 --prompt "..." --ref base.png [--scale 0.45]
 P图(图像编辑):
   edit-4.6  4.6 Seedream P图(改背景/重绘·异步)  --model edit-4.6 --prompt "背景换白色" --img-urls https://图
   inpaint   局部重绘/消除笔(异步)               --model inpaint --prompt "删除" --img-urls "原图URL,maskURL"
 视频(都→video_url;文生视频按性价比选):
   video-1080p  文生视频1080P(0.63元/秒·性价比)  --model video-1080p --prompt "..." --out o.mp4 [--frames 121=5s|241=10s --aspect 16:9]
   video-3.0pro 文生+**图生视频**1080P(1元/秒·能图生:加 --ref first.png)
                (720P 0.28元/秒 最省,但 req_key 待确认——拿到 720P 文档的 req_key 再加进 MODELS)
   actor        动作模仿2.0【IP动画神器】(actor-m1=1.0备选):角色图+模板视频→驱动角色按动作/表情/口型动
                --model actor --img-urls https://角色图 --video-url https://模板动作视频 --out o.mp4
 高清放大:
   upscale   智能超清→4K/8K(异步)   --model upscale --ref low.png --out hi.png [--resolution 4k|8k --scale 50]

⚠️ prompt 禁版权 IP 名(吉卜力/魔女宅急便/吉吉)→ 50413 风控,改纯特征描述。
⚠️ edit-4.6/inpaint/actor 输入图走**公网 URL**(本地图先传 个人CDN/火山TOS);t2i/i2i/视频首帧 可本地 --ref(自动 base64)。
画风:手绘软萌温度用 2.1/3.0;干净矢量用 4.0。
错误码:50400 没开通该模型 · 50200 req_key 名错 · 50413 版权词 · 50500/50429 可重试。
官方 SDK 备选:pip install volcengine → VisualService().cv_sync2async_submit_task(form)(不用自写签名),见 SKILL.md。
"""
import json, hashlib, hmac, datetime, base64, urllib.request, urllib.error, time, argparse, sys

RES = "/Users/links/.agents/resources.json"
d = json.load(open(RES))["media_generation"]["volcengine"]["personal"]
AK, SK = d["access_key_id"], d["secret_access_key"]
HOST, REGION, SERVICE, VER = "visual.volcengineapi.com", "cn-north-1", "cv", "2022-08-31"

# model → req_key / 输出 image|video / sync同步异步async / 输入需求
MODELS = {
    "t2i-2.1":      {"rk": "jimeng_high_aes_general_v21_L",      "kind": "image", "mode": "sync",  "need": "text"},
    "i2i-3.0":      {"rk": "jimeng_i2i_v30",                     "kind": "image", "mode": "sync",  "need": "ref"},
    "t2i-4.0":      {"rk": "jimeng_t2i_v40",                     "kind": "image", "mode": "async", "need": "text"},
    "edit-4.6":     {"rk": "jimeng_seedream46_cvtob",           "kind": "image", "mode": "async", "need": "urls"},
    "inpaint":      {"rk": "jimeng_image2image_dream_inpaint",  "kind": "image", "mode": "async", "need": "urls"},
    "video-3.0pro": {"rk": "jimeng_ti2v_v30_pro",               "kind": "video", "mode": "async", "need": "text_or_ref"},
    "actor":        {"rk": "jimeng_dreamactor_m20_gen_video",   "kind": "video", "mode": "async", "need": "actor"},   # 2.0 优先
    "actor-m1":     {"rk": "jimeng_dream_actor_m1_gen_video_cv","kind": "video", "mode": "async", "need": "actor1"},  # 1.0 备选
    # "video-720p": 720P 最省(0.28元/秒)但 req_key 待确认(推测 jimeng_t2v_v30_720p 不对,720P文档未给);拿到再启用
    "video-1080p":  {"rk": "jimeng_t2v_v30_1080p",             "kind": "video", "mode": "async", "need": "text"},    # 文生视频1080P(0.63/秒·性价比)
    "upscale":      {"rk": "jimeng_i2i_seed3_tilesr_cvtob",    "kind": "image", "mode": "async", "need": "upscale"}, # 智能超清放大→4K/8K
}

def _sign(k, m): return hmac.new(k, m.encode(), hashlib.sha256).digest()

def _req(action, body):
    bj = json.dumps(body); now = datetime.datetime.now(datetime.timezone.utc)
    xd = now.strftime("%Y%m%dT%H%M%SZ"); ds = now.strftime("%Y%m%d")
    ph = hashlib.sha256(bj.encode()).hexdigest(); q = f"Action={action}&Version={VER}"
    ch = f"content-type:application/json\nhost:{HOST}\nx-content-sha256:{ph}\nx-date:{xd}\n"
    sh = "content-type;host;x-content-sha256;x-date"
    creq = f"POST\n/\n{q}\n{ch}\n{sh}\n{ph}"; sc = f"{ds}/{REGION}/{SERVICE}/request"
    sts = f"HMAC-SHA256\n{xd}\n{sc}\n{hashlib.sha256(creq.encode()).hexdigest()}"
    ks = _sign(_sign(_sign(_sign(SK.encode(), ds), REGION), SERVICE), "request")
    sig = hmac.new(ks, sts.encode(), hashlib.sha256).hexdigest()
    auth = f"HMAC-SHA256 Credential={AK}/{sc}, SignedHeaders={sh}, Signature={sig}"
    r = urllib.request.Request(f"https://{HOST}/?{q}", data=bj.encode(),
        headers={"Content-Type": "application/json", "Host": HOST, "X-Date": xd,
                 "X-Content-Sha256": ph, "Authorization": auth}, method="POST")
    try: return json.loads(urllib.request.urlopen(r, timeout=120).read())
    except urllib.error.HTTPError as e: return json.loads(e.read())

def _save_image(res, out):
    b64 = ((res.get("data") or {}).get("binary_data_base64") or [None])[0]
    if b64: open(out, "wb").write(base64.b64decode(b64)); print(f"✓ {out}")
    else: print(f"✗ {res.get('code')} {res.get('message')}")

def _save_video(res, out):
    url = (res.get("data") or {}).get("video_url")
    if url: urllib.request.urlretrieve(url, out); print(f"✓ {out}  (源 video_url 1h 有效)")
    else: print(f"✗ 无 video_url: {json.dumps(res, ensure_ascii=False)[:300]}")

def run(a):
    m = MODELS[a.model]; rk = m["rk"]
    if m["need"] in ("actor", "actor1"):          # 动作模仿:角色图URL + 模板视频URL(公网)
        if not (a.img_urls and a.video_url): sys.exit("actor 需 --img-urls <角色图URL> --video-url <模板视频URL>")
        img = a.img_urls.split(",")[0].strip()
        body = {"req_key": rk, "video_url": a.video_url, "return_url": True}
        body["image_urls"] = [img] if m["need"] == "actor" else None
        if m["need"] == "actor1": body["image_url"] = img; del body["image_urls"]  # m1 用单数
    elif m["need"] == "upscale":                   # 智能超清:1张图(本地ref或URL) + resolution + scale(0-100细节)
        body = {"req_key": rk, "resolution": a.resolution, "scale": int(a.scale) if a.scale >= 1 else 50, "return_url": False}
        if a.ref: body["binary_data_base64"] = [base64.b64encode(open(a.ref, "rb").read()).decode()]
        elif a.img_urls: body["image_urls"] = [a.img_urls.split(",")[0].strip()]
        else: sys.exit("upscale 需 --ref 或 --img-urls")
    else:
        if not a.prompt: sys.exit("需 --prompt")
        body = {"req_key": rk, "prompt": a.prompt}
        if a.img_urls: body["image_urls"] = [u.strip() for u in a.img_urls.split(",") if u.strip()]
        if a.ref:      body["binary_data_base64"] = [base64.b64encode(open(a.ref, "rb").read()).decode()]
        if m["kind"] == "image":
            body.update({"width": a.width, "height": a.height})
            if m["mode"] == "async": body["force_single"] = True
            if a.ref: body["scale"] = a.scale
        else:
            body.update({"frames": a.frames, "aspect_ratio": a.aspect, "seed": -1})
        body["return_url"] = (m["kind"] == "video")

    if m["mode"] == "sync":
        return _save_image(_req("CVProcess", body), a.out)
    s = _req("CVSync2AsyncSubmitTask", body); tid = (s.get("data") or {}).get("task_id")
    if not tid: sys.exit(f"✗ submit: {s.get('code')} {s.get('message')}")
    print(f"  task_id={tid} 轮询中…")
    for i in range(45):
        time.sleep(4); res = _req("CVSync2AsyncGetResult", {"req_key": rk, "task_id": tid}); code = res.get("code")
        if code in (50500, 50501, 50429, 50430): print(f"  [{i}] {code} 可重试…"); continue
        st = (res.get("data") or {}).get("status")
        if st == "done": return _save_video(res, a.out) if m["kind"] == "video" else _save_image(res, a.out)
        if code != 10000: sys.exit(f"✗ {code} {res.get('message')}")
        print(f"  [{i}] status={st}")
    sys.exit("✗ 轮询超时")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="t2i-4.0", choices=list(MODELS))
    ap.add_argument("--prompt", help="提示词(actor 不需要)")
    ap.add_argument("--ref", help="本地参考图→base64:i2i/视频首帧")
    ap.add_argument("--img-urls", dest="img_urls", help="公网图URL,逗号分隔:edit-4.6/inpaint(原图,mask)/actor(角色图)")
    ap.add_argument("--video-url", dest="video_url", help="actor 模板视频URL(公网)")
    ap.add_argument("--out", default="out.png")
    ap.add_argument("--width", type=int, default=1024); ap.add_argument("--height", type=int, default=1024)
    ap.add_argument("--scale", type=float, default=0.45, help="i2i:0-1(越大越偏prompt);upscale:0-100细节(默认50)")
    ap.add_argument("--resolution", default="4k", help="upscale:4k|8k")
    ap.add_argument("--frames", type=int, default=121, help="视频:121=5s,241=10s")
    ap.add_argument("--aspect", default="16:9")
    run(ap.parse_args())
