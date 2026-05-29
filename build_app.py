"""Builds index.html for the DimeBuy order-image app.

Embeds Designer.png as a base64 data URI so the page works (including the
PNG download) by simply double-clicking the file in a browser on Windows.
Run:  python build_app.py
"""
import base64
import pathlib

HERE = pathlib.Path(__file__).parent
img_b64 = base64.b64encode((HERE / "Designer.png").read_bytes()).decode("ascii")

HTML = """<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DimeBuy – สร้างรูปคำสั่งซื้อ</title>
<style>
  body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
       background:#0d0d10;color:#eee;display:flex;gap:28px;padding:24px;
       flex-wrap:wrap;justify-content:center;align-items:flex-start}
  .panel{width:320px}
  h1{font-size:18px;margin:0 0 6px}
  p.sub{margin:0 0 18px;color:#888;font-size:13px}
  label{display:block;font-size:13px;margin:16px 0 5px;color:#bbb}
  input{width:100%;box-sizing:border-box;padding:12px;border-radius:10px;
        border:1px solid #333;background:#1c1c1e;color:#fff;font-size:16px}
  button{margin-top:24px;width:100%;padding:14px;border:0;border-radius:12px;
         background:#0a84ff;color:#fff;font-size:16px;font-weight:600;cursor:pointer}
  button:active{opacity:.85}
  canvas{width:300px;height:auto;border-radius:26px;
         box-shadow:0 10px 50px rgba(0,0,0,.6)}
  small{display:block;margin-top:10px;color:#777}
</style>
</head>
<body>
  <div class="panel">
    <h1>DimeBuy – กรอกข้อมูลคำสั่งซื้อ</h1>
    <p class="sub">รูปจะอัปเดตอัตโนมัติเมื่อพิมพ์</p>

    <label for="sym">1. Symbol</label>
    <input id="sym" value="AAPL" autocomplete="off">

    <label for="val">2. มูลค่าที่ต้องการซื้อ (USD)</label>
    <input id="val" value="0.00" autocomplete="off">

    <label for="price">3. ราคาหุ้น (USD)</label>
    <input id="price" value="310.66" autocomplete="off">

    <button id="dl">ดาวน์โหลดรูปภาพ (PNG)</button>
    <button id="copy" style="margin-top:10px;background:#2c2c2e">คัดลอก URL สำหรับแชร์</button>
    <small id="copied" style="color:#30d158;display:none">คัดลอกแล้ว!</small>
    <small>ไฟล์ที่ได้: DimeBuy_order.png</small>
  </div>

  <canvas id="c"></canvas>

<script>
const IMG = "data:image/png;base64,__IMG__";
const FONT = '-apple-system,"Helvetica Neue",Arial,sans-serif';

// Geometry measured from Designer.png (1179 x 3000). Backgrounds are flat,
// so each old value is covered with a solid rect, then redrawn.
const THB_RATE = 10139.94 / 310.66;  // implied rate from mockup (~32.64 THB/USD)

const SPEC = {
  sym:      {mask:[60,270,330,349],  bg:'rgb(16,16,17)', x:70,  base:339,  color:'rgb(247,249,252)', font:'700 80px'},
  price:    {mask:[60,378,356,449],  bg:'rgb(16,16,17)', x:70,  base:439,  color:'rgb(247,249,252)', font:'700 54px'},
  thb:      {mask:[350,385,700,442], bg:'rgb(16,16,17)', x:355, base:432,  color:'rgb(152,156,159)', font:'40px'},
  val:      {mask:[55,1558,305,1670],bg:'rgb(37,37,37)', x:65,  base:1656, color:'rgb(124,127,129)', font:'700 132px'},
  ordprice: {mask:[60,2095,500,2175],bg:'rgb(37,37,37)', x:65,  base:2158, color:'rgb(247,249,252)', font:'700 90px'}
};

const c = document.getElementById('c');
const ctx = c.getContext('2d');
const F = {sym:sym, val:val, price:price};   // ids are global
const img = new Image();

function draw(){
  if(!img.naturalWidth) return;
  c.width = img.naturalWidth;
  c.height = img.naturalHeight;
  ctx.drawImage(img, 0, 0);
  const priceNum = parseFloat(F.price.value) || 0;
  const thbStr = '≈ ' + (priceNum * THB_RATE).toLocaleString('en-US',
    {minimumFractionDigits:2, maximumFractionDigits:2}) + ' THB';
  const vals = {
    sym:      F.sym.value,
    price:    F.price.value + ' USD',
    thb:      thbStr,
    val:      F.val.value,
    ordprice: F.price.value
  };
  ctx.textAlign = 'left';
  ctx.textBaseline = 'alphabetic';
  for(const k in SPEC){
    const s = SPEC[k], m = s.mask;
    ctx.fillStyle = s.bg;
    ctx.fillRect(m[0], m[1], m[2]-m[0], m[3]-m[1]);
    ctx.fillStyle = s.color;
    ctx.font = s.font + ' ' + FONT;
    ctx.fillText(vals[k] || '', s.x, s.base);
  }
}

// Pre-fill from URL query params on load
const params = new URLSearchParams(location.search);
if(params.get('sym'))   F.sym.value   = params.get('sym');
if(params.get('val'))   F.val.value   = params.get('val');
if(params.get('price')) F.price.value = params.get('price');

for(const k in F) F[k].addEventListener('input', draw);
img.onload = draw;
img.src = IMG;

document.getElementById('copy').addEventListener('click', () => {
  const u = new URL(location.href);
  u.searchParams.set('sym',   F.sym.value);
  u.searchParams.set('val',   F.val.value);
  u.searchParams.set('price', F.price.value);
  navigator.clipboard.writeText(u.toString()).then(() => {
    const el = document.getElementById('copied');
    el.style.display = 'block';
    setTimeout(() => el.style.display = 'none', 2000);
  });
});

document.getElementById('dl').addEventListener('click', () => {
  c.toBlob(b => {
    const a = document.createElement('a');
    a.download = 'DimeBuy_order.png';
    a.href = URL.createObjectURL(b);
    a.click();
    URL.revokeObjectURL(a.href);
  }, 'image/png');
});
</script>
</body>
</html>
"""

out = HTML.replace("__IMG__", img_b64)
(HERE / "index.html").write_text(out, encoding="utf-8")
print("wrote index.html", round(len(out) / 1024 / 1024, 2), "MB")
