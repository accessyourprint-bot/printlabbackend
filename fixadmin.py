with open("static/full_control.html", "r", encoding="utf-8") as f:
    content = f.read()

# Fix admin button to show dropdown instead of logout
old = '<button class="admin-btn" onclick="doLogout()">⚙ Admin</button>'
new = '''<div style="position:relative;display:inline-block">
  <button class="admin-btn" onclick="toggleAdminMenu()">⚙ Admin</button>
  <div id="adminMenu" style="display:none;position:absolute;right:0;top:38px;background:#fff;border:1.5px solid #ebebee;border-radius:10px;box-shadow:0 4px 16px rgba(0,0,0,.1);min-width:160px;z-index:999">
    <div style="padding:10px 16px;font-size:.8rem;color:#888;border-bottom:1px solid #f0f0f0">Logged in as<br><b style="color:#1a223e">admin@altprint.in</b></div>
    <div onclick="doLogout()" style="padding:10px 16px;font-size:.85rem;cursor:pointer;color:#e53935;font-weight:600">⏻ Logout</div>
  </div>
</div>'''
content = content.replace(old, new)

# Add toggleAdminMenu function after doLogout
old2 = 'function doLogout(){localStorage.removeItem(\'pl_full\');location.reload();}'
new2 = '''function doLogout(){localStorage.removeItem('pl_full');location.reload();}
function toggleAdminMenu(){const m=document.getElementById('adminMenu');m.style.display=m.style.display==='none'?'block':'none';}
document.addEventListener('click',function(e){const m=document.getElementById('adminMenu');if(m&&!e.target.closest('#adminMenu')&&!e.target.closest('.admin-btn'))m.style.display='none';});'''
content = content.replace(old2, new2)

with open("static/full_control.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
