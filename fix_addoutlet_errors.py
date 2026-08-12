import io

path = r"static\full_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = """  const newShopId=shopResp&&shopResp.data&&shopResp.data.id;
  if(loginId&&password&&newShopId){
    try{
      await api('/api/v1/admin/create-shop-login','POST',{email:loginEmail,password:password,full_name:owner,shop_id:newShopId});
    }catch(e){
      alert('Outlet was created, but the login account could not be set up (the email may already be in use). You can add a login later.');
    }
  }"""

new_block = """  const newShopId=shopResp&&shopResp.data&&shopResp.data.id;
  if(!newShopId){
    alert('Failed to create outlet: '+(shopResp&&shopResp.detail?shopResp.detail:'unknown error'));
    return;
  }
  if(loginId&&password){
    const loginResp=await api('/api/v1/admin/create-shop-login','POST',{email:loginEmail,password:password,full_name:owner,shop_id:newShopId});
    if(!loginResp||loginResp.detail||loginResp.success===false){
      alert('Outlet was created, but the login account could not be set up: '+(loginResp&&loginResp.detail?loginResp.detail:'unknown error')+'\\n\\nYou can add a login later using Reset Password once a login exists, or contact support.');
    }
  }"""

if old_block not in content:
    print("BLOCK NOT FOUND - aborting")
else:
    content = content.replace(old_block, new_block, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("PATCHED SUCCESSFULLY")
