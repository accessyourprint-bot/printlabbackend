import io

path = r"static\specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add CSS
old_css = """.sdi.red{color:#e84c1e;}"""
new_css = """.sdi.red{color:#e84c1e;}
.sdi-info{padding:12px 16px;border-bottom:1px solid #eee;background:#fafafa;}
.sdi-info-row{font-size:.78rem;color:#555;padding:2px 0;word-break:break-all;}
.sdi-info-row b{color:#222;font-weight:600;margin-right:4px;}"""

if old_css not in content:
    print("CSS BLOCK NOT FOUND - aborting")
else:
    content = content.replace(old_css, new_css, 1)

    # 2. Wire up JS to populate the spans in initD()
    old_js = """      curShop = await api('/api/v1/shops/'+myShopId);
      document.getElementById('shopName').textContent=curShop.name||'Print Lab';
    }else{
      const d = await api('/api/v1/shops');
      const s = Array.isArray(d)?d:(d.data||[]);
      if(s.length){curShop=s[0];document.getElementById('shopName').textContent=curShop.name||'Print Lab';}
    }"""

    new_js = """      curShop = await api('/api/v1/shops/'+myShopId);
      document.getElementById('shopName').textContent=curShop.name||'Print Lab';
    }else{
      const d = await api('/api/v1/shops');
      const s = Array.isArray(d)?d:(d.data||[]);
      if(s.length){curShop=s[0];document.getElementById('shopName').textContent=curShop.name||'Print Lab';}
    }
    if(curShop){
      document.getElementById('sdShopId').textContent=curShop.id||'-';
      document.getElementById('sdShopEmail').textContent=curShop.owner_email||'-';
      document.getElementById('sdShopPhone').textContent=curShop.owner_phone||'-';
    }"""

    if old_js not in content:
        print("JS BLOCK NOT FOUND - aborting (CSS already patched though)")
    else:
        content = content.replace(old_js, new_js, 1)
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("CSS AND JS PATCHED SUCCESSFULLY")
