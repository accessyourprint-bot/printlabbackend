import io

path = r"static\specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_login = """async function doLogin(){
  const em = document.getElementById('em').value;
  const pw = document.getElementById('pw').value;
  try{
    const r = await fetch(API+'/api/v1/auth/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:em,password:pw})});
    const d = await r.json();
    if(d.access_token){tok=d.access_token;localStorage.setItem('pl_s',tok);if(d.shop_id)localStorage.setItem('pl_shop',d.shop_id);initD();}
    else document.getElementById('lerr').textContent='Invalid credentials';
  }catch(e){document.getElementById('lerr').textContent='Cannot connect to server';}
}"""

new_login = """async function doLogin(){
  let em = document.getElementById('em').value.trim();
  if(em && em.indexOf('@')===-1){ em = em + '@altprint.in'; }
  const pw = document.getElementById('pw').value;
  try{
    const r = await fetch(API+'/api/v1/auth/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:em,password:pw})});
    const d = await r.json();
    if(d.access_token){tok=d.access_token;localStorage.setItem('pl_s',tok);if(d.shop_id)localStorage.setItem('pl_shop',d.shop_id);initD();}
    else document.getElementById('lerr').textContent='Invalid credentials';
  }catch(e){document.getElementById('lerr').textContent='Cannot connect to server';}
}"""

if old_login not in content:
    print("LOGIN FUNCTION NOT FOUND - aborting")
else:
    content = content.replace(old_login, new_login, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("PATCHED SUCCESSFULLY")
