p = "static/specific_control.html"
with open(p, "r", encoding="utf-8") as f:
    s = f.read()

# 1. Replace modal body HTML: wrap "Raised By" and "Subject" so we can toggle them,
# and add a dropdown version of Subject for Technical Issue.
old_html = """    <div class="mbody">
      <div class="fg"><label>Raised By</label><input id="tBy" placeholder="Your name"></div>
      <div class="fg"><label>Subject</label><input id="tSj" placeholder="Brief description"></div>
      <div class="fg"><label>Details (Optional)</label><textarea id="tDt" rows="3" placeholder="More details..."></textarea></div>
    </div>"""

new_html = """    <div class="mbody">
      <div class="fg" id="tByField"><label>Raised By</label><input id="tBy" placeholder="Your name"></div>
      <div class="fg" id="tSjTextField"><label>Subject</label><input id="tSj" placeholder="Brief description"></div>
      <div class="fg hidden" id="tSjSelectField"><label>Subject</label><select id="tSjSelect"><option value="Device Issue">Device Issue</option><option value="Software">Software</option><option value="Equipment">Equipment</option><option value="Electricity Issue">Electricity Issue</option></select></div>
      <div class="fg"><label>Details</label><textarea id="tDt" rows="3" placeholder="Explain the issue..."></textarea></div>
    </div>"""

if old_html in s:
    s = s.replace(old_html, new_html, 1)
    print("HTML patched OK")
else:
    print("HTML MATCH NOT FOUND")

# 2. Update openTK() to show/hide fields based on type
old_open = """function openTK(type){
  curTK=type;closeTD();
  const m=TKM[type];
  document.getElementById('tkT').textContent=m.t;
  document.getElementById('tkS').textContent=m.s+(curShop?' for '+curShop.name:'');
  ['tBy','tSj','tDt'].forEach(id=>document.getElementById(id).value='');
  oMo('tkMo');
}"""

new_open = """function openTK(type){
  curTK=type;closeTD();
  const m=TKM[type];
  document.getElementById('tkT').textContent=m.t;
  document.getElementById('tkS').textContent=m.s+(curShop?' for '+curShop.name:'');
  ['tBy','tSj','tDt'].forEach(id=>document.getElementById(id).value='');
  document.getElementById('tSjSelect').selectedIndex=0;
  if(type==='technical'){
    document.getElementById('tByField').classList.add('hidden');
    document.getElementById('tSjTextField').classList.add('hidden');
    document.getElementById('tSjSelectField').classList.remove('hidden');
  }else{
    document.getElementById('tByField').classList.remove('hidden');
    document.getElementById('tSjTextField').classList.remove('hidden');
    document.getElementById('tSjSelectField').classList.add('hidden');
  }
  oMo('tkMo');
}"""

if old_open in s:
    s = s.replace(old_open, new_open, 1)
    print("openTK patched OK")
else:
    print("openTK MATCH NOT FOUND")

# 3. Update subTK() to read from the right fields depending on type
old_sub_validate = """  const by=document.getElementById('tBy').value,sj=document.getElementById('tSj').value;
  if(!by||!sj)return alert('Fill Raised By and Subject');"""

new_sub_validate = """  const isTech=curTK==='technical';
  const by=isTech?'N/A':document.getElementById('tBy').value;
  const sj=isTech?document.getElementById('tSjSelect').value:document.getElementById('tSj').value;
  const dt=(document.getElementById('tDt').value||'').trim();
  if(isTech){ if(!dt)return alert('Please explain the issue in Details'); }
  else if(!by||!sj)return alert('Fill Raised By and Subject');"""

if old_sub_validate in s:
    s = s.replace(old_sub_validate, new_sub_validate, 1)
    print("subTK validation patched OK")
else:
    print("subTK validation MATCH NOT FOUND")

with open(p, "w", encoding="utf-8") as f:
    f.write(s)
