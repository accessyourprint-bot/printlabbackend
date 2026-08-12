import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """        +'<td style="padding:16px 20px;border-bottom:1px solid #eee">'
        +(hasFiles?'<button onclick="downloadAllZip(&quot;'+o.id+'&quot;,&quot;'+(o.order_number||o.id)+'&quot;)" style="background:#ea580c;color:#fff;border:none;border-radius:8px;padding:8px 18px;font-size:13px;cursor:pointer;font-weight:600">&#8595; Download</button>':'<span style="color:#999;font-size:12px">No files</span>')
        +'</td>'
        +'</tr>';
    }).join('');
    jl.innerHTML = '<table style="width:100%;border-collapse:separate;border-spacing:0;font-size:14px;background:#fff;border:1px solid #e5e7eb;border-radius:10px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.06)">'
      +'<thead><tr style="background:#f8f8fa;text-align:left">'
      +'<th style="padding:14px 20px;border-bottom:2px solid #ddd;font-size:15px;font-weight:700">Order ID</th>'
      +'<th style="padding:14px 20px;border-bottom:2px solid #ddd;font-size:15px;font-weight:700">Customer Name</th>'
      +'<th style="padding:14px 20px;border-bottom:2px solid #ddd;font-size:15px;font-weight:700">Phone Number</th>'
      +'<th style="padding:14px 20px;border-bottom:2px solid #ddd;font-size:15px;font-weight:700">Download</th>'
      +'</tr></thead><tbody>'+rows+'</tbody></table>';
    return;
  }"""

new = """        +'<td style="padding:16px 20px;border-bottom:1px solid #eee">'
        +(hasFiles?'<button onclick="downloadAllZip(&quot;'+o.id+'&quot;,&quot;'+(o.order_number||o.id)+'&quot;)" style="background:#ea580c;color:#fff;border:none;border-radius:8px;padding:8px 18px;font-size:13px;cursor:pointer;font-weight:600">&#8595; Download</button>':'<span style="color:#999;font-size:12px">No files</span>')
        +'</td>'
        +'<td style="padding:16px 20px;border-bottom:1px solid #eee">'
        +'<span style="background:#f0fdf4;color:#16a34a;font-weight:700;border-radius:20px;padding:4px 12px;font-size:.8rem">&#10003; Completed</span>'
        +'</td>'
        +'</tr>';
    }).join('');
    jl.innerHTML = '<table style="width:100%;border-collapse:separate;border-spacing:0;font-size:14px;background:#fff;border:1px solid #e5e7eb;border-radius:10px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.06)">'
      +'<thead><tr style="background:#f8f8fa;text-align:left">'
      +'<th style="padding:14px 20px;border-bottom:2px solid #ddd;font-size:15px;font-weight:700">Order ID</th>'
      +'<th style="padding:14px 20px;border-bottom:2px solid #ddd;font-size:15px;font-weight:700">Customer Name</th>'
      +'<th style="padding:14px 20px;border-bottom:2px solid #ddd;font-size:15px;font-weight:700">Phone Number</th>'
      +'<th style="padding:14px 20px;border-bottom:2px solid #ddd;font-size:15px;font-weight:700">Download</th>'
      +'<th style="padding:14px 20px;border-bottom:2px solid #ddd;font-size:15px;font-weight:700">Status</th>'
      +'</tr></thead><tbody>'+rows+'</tbody></table>';
    return;
  }"""

c = content.count(old)
print(f"Completed-tab block found {c} time(s)")
if c == 1:
    content = content.replace(old, new)
    print("Completed tab now shows Download + Completed status badge")
else:
    print("WARNING: block not found exactly once, aborting")
    exit()

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
