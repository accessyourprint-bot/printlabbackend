import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# --- Part 1: save shop_id at login (both normal login and any token-set spots) ---
old1 = "if(d.access_token){tok=d.access_token;localStorage.setItem('pl_s',tok);initD();}"
new1 = "if(d.access_token){tok=d.access_token;localStorage.setItem('pl_s',tok);if(d.shop_id)localStorage.setItem('pl_shop',d.shop_id);initD();}"

c1 = content.count(old1)
print(f"Login save-token line found {c1} time(s)")
if c1 == 1:
    content = content.replace(old1, new1)
else:
    print("WARNING: login anchor not found exactly once, aborting")
    exit()

# --- Part 2: fix initD() to fetch the correct logged-in shop, not s[0] ---
old2 = """async function initD(){
  document.getElementById('lw').classList.add('hidden');
  document.getElementById('dw').classList.remove('hidden');
  try{
    const d = await api('/api/v1/shops');
    const s = Array.isArray(d)?d:(d.data||[]);
    if(s.length){curShop=s[0];document.getElementById('shopName').textContent=curShop.name||'Print Lab';}
  }catch(e){}
  loadJ();
  setInterval(loadJ,15000);
}"""

new2 = """async function initD(){
  document.getElementById('lw').classList.add('hidden');
  document.getElementById('dw').classList.remove('hidden');
  try{
    const myShopId = localStorage.getItem('pl_shop');
    if(myShopId){
      curShop = await api('/api/v1/shops/'+myShopId);
      document.getElementById('shopName').textContent=curShop.name||'Print Lab';
    }else{
      const d = await api('/api/v1/shops');
      const s = Array.isArray(d)?d:(d.data||[]);
      if(s.length){curShop=s[0];document.getElementById('shopName').textContent=curShop.name||'Print Lab';}
    }
  }catch(e){}
  loadJ();
  setInterval(loadJ,15000);
}"""

c2 = content.count(old2)
print(f"initD() found {c2} time(s)")
if c2 == 1:
    content = content.replace(old2, new2)
    print("initD() now loads the correct logged-in shop")
else:
    print("WARNING: initD anchor not found exactly once, aborting")
    exit()

# --- Part 3: clear pl_shop on logout too ---
old3 = "function doLogout(){localStorage.removeItem('pl_s');location.reload();}"
new3 = "function doLogout(){localStorage.removeItem('pl_s');localStorage.removeItem('pl_shop');location.reload();}"

c3 = content.count(old3)
print(f"Logout function found {c3} time(s)")
if c3 == 1:
    content = content.replace(old3, new3)
else:
    print("WARNING: logout anchor not found exactly once, aborting")
    exit()

# --- Part 4: show outlet Login ID in the ticket popup subtitle ---
old4 = "document.getElementById('tkS').textContent=m.s+(curShop?' for '+curShop.name:'');"
new4 = "document.getElementById('tkS').textContent=m.s+(curShop?' for '+curShop.name:'')+(curShop&&curShop.owner_email?' \\u2022 Outlet ID: '+curShop.owner_email.split('@')[0]:'');"

c4 = content.count(old4)
print(f"Popup subtitle line found {c4} time(s)")
if c4 == 1:
    content = content.replace(old4, new4)
    print("Outlet ID now shown in ticket popup")
else:
    print("WARNING: subtitle anchor not found exactly once, aborting")
    exit()

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
