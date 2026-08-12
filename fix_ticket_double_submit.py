import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """async function subTK(){
  const by=document.getElementById('tBy').value,sj=document.getElementById('tSj').value;
  if(!by||!sj)return alert('Fill Raised By and Subject');
  try{
    const dtVal=(document.getElementById('tDt').value||'').trim();const r = await api('/api/v1/tickets','POST',{subject:sj,description:dtVal.length>=3?dtVal:sj,priority:curTK==='technical'?'high':'normal',category:curTK,raised_by:by,shop_id:curShop?curShop.id:null});
    if(r && (r.id || (r.data && r.data.id))){cMo('tkMo');alert('Ticket raised successfully!');loadTickets && loadTickets();}
    else{alert('Error raising ticket: '+(r&&r.detail?r.detail:'Please try logging in again'));}
  }catch(e){alert('Error raising ticket');}
}"""

new = """let tkSubmitting=false;
async function subTK(){
  if(tkSubmitting)return;
  const by=document.getElementById('tBy').value,sj=document.getElementById('tSj').value;
  if(!by||!sj)return alert('Fill Raised By and Subject');
  tkSubmitting=true;
  const btn=document.querySelector('#tkMo .bsb');
  if(btn){btn.disabled=true;btn.textContent='Raising...';}
  try{
    const dtVal=(document.getElementById('tDt').value||'').trim();const r = await api('/api/v1/tickets','POST',{subject:sj,description:dtVal.length>=3?dtVal:sj,priority:curTK==='technical'?'high':'normal',category:curTK,raised_by:by,shop_id:curShop?curShop.id:null});
    if(r && (r.id || (r.data && r.data.id))){
      document.getElementById('tBy').value='';document.getElementById('tSj').value='';document.getElementById('tDt').value='';
      cMo('tkMo');alert('Ticket raised successfully!');loadTickets && loadTickets();
    }
    else{alert('Error raising ticket: '+(r&&r.detail?r.detail:'Please try logging in again'));}
  }catch(e){alert('Error raising ticket');}
  finally{
    tkSubmitting=false;
    if(btn){btn.disabled=false;btn.textContent='Raise Ticket';}
  }
}"""

c = content.count(old)
print(f"Anchor found {c} time(s)")
if c == 1:
    content = content.replace(old, new)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Double-submit protection added, form now clears after success")
else:
    print("WARNING: anchor not unique - manual fix needed")
