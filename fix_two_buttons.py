import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """(curStabFilter==='completed'?'<button onclick="markOutForDelivery(&quot;'+o.id+'&quot;)" style="background:#2563eb;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:12px;cursor:pointer;font-weight:600">&#10003; Completed</button>':"""

count = content.count(old)
print(f"Target found {count} time(s)")

new = """(curStabFilter==='completed'?('<div style="display:flex;gap:6px;flex-wrap:wrap">'+((o.files&&o.files.length)?'<button onclick="downloadAllZip(&quot;'+o.id+'&quot;,&quot;'+(o.order_number||o.id)+'&quot;)" style="background:#ea580c;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:12px;cursor:pointer;font-weight:600">&#8595; Download</button>':'')+'<button onclick="markOutForDelivery(&quot;'+o.id+'&quot;)" style="background:#2563eb;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:12px;cursor:pointer;font-weight:600">&#128666; Out for Delivery</button>'+'</div>'):"""

if count == 1:
    content = content.replace(old, new, 1)
    print("Replaced: Completed tab now shows Download + Out for Delivery buttons")
else:
    print("WARNING: expected exactly 1 match, found", count, "- no changes made")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
