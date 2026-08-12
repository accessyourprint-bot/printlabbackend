import io

path = "static/full_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """async function addOutlet(){
  const name=document.getElementById('otName').value;
  const owner=document.getElementById('otOwner').value;
  const loginId=document.getElementById('otLoginId').value;
  const password=document.getElementById('otPassword').value;
  if(!name||!owner) return alert('Outlet name and owner required');
  if(loginId&&password){
    await api('/api/v1/auth/register','POST',{email:loginId+'@altprint.in',password:password,full_name:owner,role:'shop'});
  }
  const lat=document.getElementById('otLat').value;
  const lng=document.getElementById('otLng').value;
  await api('/api/v1/shops','POST',{
    name:name,
    owner_name:owner,
    owner_phone:document.getElementById('otPhone').value,
    owner_email:document.getElementById('otEmail').value||loginId+'@altprint.in',
    city:document.getElementById('otCity').value,
    state:document.getElementById('otState').value,
    pincode:document.getElementById('otPin').value,
    address:document.getElementById('otAddr').value,
    latitude:lat?parseFloat(lat):null,
    longitude:lng?parseFloat(lng):null,
    delivery_radius_km:parseFloat(document.getElementById('otRadius').value)||5,
    permission_type:curOtPerm,
    is_active:true
  });"""

new = """async function addOutlet(){
  const name=document.getElementById('otName').value;
  const owner=document.getElementById('otOwner').value;
  const loginId=document.getElementById('otLoginId').value;
  const password=document.getElementById('otPassword').value;
  if(!name||!owner) return alert('Outlet name and owner required');
  const loginEmail=loginId?loginId+'@altprint.in':null;
  if(loginId&&password&&password.length<6) return alert('Password must be at least 6 characters');
  const lat=document.getElementById('otLat').value;
  const lng=document.getElementById('otLng').value;
  const shopResp=await api('/api/v1/shops','POST',{
    name:name,
    owner_name:owner,
    owner_phone:document.getElementById('otPhone').value,
    owner_email:document.getElementById('otEmail').value||loginEmail||('outlet'+Date.now()+'@altprint.in'),
    city:document.getElementById('otCity').value,
    state:document.getElementById('otState').value,
    pincode:document.getElementById('otPin').value,
    address:document.getElementById('otAddr').value,
    latitude:lat?parseFloat(lat):null,
    longitude:lng?parseFloat(lng):null,
    delivery_radius_km:parseFloat(document.getElementById('otRadius').value)||5,
    permission_type:curOtPerm,
    is_active:true
  });
  const newShopId=shopResp&&shopResp.data&&shopResp.data.id;
  if(loginId&&password&&newShopId){
    try{
      await api('/api/v1/admin/create-shop-login','POST',{email:loginEmail,password:password,full_name:owner,shop_id:newShopId});
    }catch(e){
      alert('Outlet was created, but the login account could not be set up (the email may already be in use). You can add a login later.');
    }
  }"""

c = content.count(old)
print(f"addOutlet() found {c} time(s)")
if c == 1:
    content = content.replace(old, new)
    print("addOutlet() fixed to properly link login to shop_id")
else:
    print("WARNING: addOutlet anchor not found exactly once, aborting")
    exit()

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
