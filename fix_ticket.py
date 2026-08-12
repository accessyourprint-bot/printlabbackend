p = "static/specific_control.html"
with open(p, "r", encoding="utf-8") as f:
    s = f.read()

old = """async function subTK(){
  const by=document.getElementById('tBy').value,sj=document.getElementById('tSj').value;
  if(!by||!sj)return alert('Fill Raised By and Subject');
  try{
    await api('/api/v1/tickets','POST',{subject:sj,description:document.getElementById('tDt').value,priority:curTK==='technical'?'high':'medium',category:curTK,raised_by:by,shop_id:curShop?curShop.id:null});
    cMo('tkMo');alert('Ticket raised successfully!');
  }catch(e){alert('Error raising ticket');}
}"""

new = """async function subTK(){
  const by=document.getElementById('tBy').value,sj=document.getElementById('tSj').value;
  if(!by||!sj)return alert('Fill Raised By and Subject');
  try{
    const r = await api('/api/v1/tickets','POST',{subject:sj,description:document.getElementById('tDt').value,priority:curTK==='technical'?'high':'medium',category:curTK,raised_by:by,shop_id:curShop?curShop.id:null});
    if(r && r.id){cMo('tkMo');alert('Ticket raised successfully!');}
    else{alert('Error raising ticket: '+(r&&r.detail?r.detail:'Please try logging in again'));}
  }catch(e){alert('Error raising ticket');}
}"""

if old in s:
    s = s.replace(old, new, 1)
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)
    print("Patched OK")
else:
    print("MATCH NOT FOUND -- check manually")
