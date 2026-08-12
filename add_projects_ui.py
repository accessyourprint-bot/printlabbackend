import io

path = r"static\specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add topbar button
old_btn = """      <button class="tbtn" onclick="openDT()">&#128101; <span>Delivery Team</span></button>
      <button class="tbtn" onclick="openPS()">&#128202; <span>Performance Status</span></button>"""
new_btn = """      <button class="tbtn" onclick="openDT()">&#128101; <span>Delivery Team</span></button>
      <button class="tbtn" onclick="openPJ()">&#128193; <span>Projects</span></button>
      <button class="tbtn" onclick="openPS()">&#128202; <span>Performance Status</span></button>"""

# 2. Add modal HTML right after the dtMo modal closes
old_modal_anchor = """    <div class="mfoot"><button class="bsb" onclick="openAA()">+ Add Person</button></div>
  </div>
</div>"""
new_modal_anchor = """    <div class="mfoot"><button class="bsb" onclick="openAA()">+ Add Person</button></div>
  </div>
</div>

<div id="pjMo" class="mo hidden">
  <div class="mb">
    <div class="mh">
      <div><h3>Projects</h3><p>Upload completed project files. These are visible to all customers in the app.</p></div>
      <button class="mx" onclick="cMo('pjMo')">&#10005;</button>
    </div>
    <div class="mbody">
      <div style="display:flex;gap:8px;margin-bottom:16px">
        <input type="text" id="pjTitle" placeholder="Project title" style="flex:1;padding:10px 12px;border:1px solid #ddd;border-radius:8px;font-size:13px">
        <input type="file" id="pjFile" style="flex:1;font-size:13px">
      </div>
      <button class="bsb" onclick="uploadPJ()" id="pjUploadBtn" style="width:100%;margin-bottom:16px">+ Upload Project</button>
      <div id="pjB"><div class="loading">Loading&#8230;</div></div>
    </div>
  </div>
</div>"""

if old_btn not in content:
    print("BUTTON MARKER NOT FOUND - aborting")
elif old_modal_anchor not in content:
    print("MODAL ANCHOR NOT FOUND - aborting")
else:
    content = content.replace(old_btn, new_btn, 1)
    content = content.replace(old_modal_anchor, new_modal_anchor, 1)

    # 3. Add JS functions right before the DROPDOWNS comment
    old_js_anchor = "/* DROPDOWNS */"
    new_js_anchor = """/* PROJECTS SHOWCASE */
async function openPJ(){
  oMo('pjMo');
  loadPJ();
}
async function loadPJ(){
  const b=document.getElementById('pjB');
  b.innerHTML='<div class="loading">Loading&#8230;</div>';
  try{
    const items = await api('/api/v1/showcase/mine');
    const list = Array.isArray(items)?items:[];
    b.innerHTML = list.length
      ? list.map(function(p){
          return '<div class="ag"><div class="av">&#128196;</div><div style="flex:1"><div class="an">'+p.title+'</div>'
            + '<div class="aa">'+(p.original_filename||'')+'</div></div>'
            + '<div style="display:flex;gap:8px">'
            + '<a href="'+API+'/api/v1/showcase/'+p.id+'/download" target="_blank" style="background:#2563eb;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:12px;text-decoration:none;font-weight:600">Download</a>'
            + '<button onclick="deletePJ(&quot;'+p.id+'&quot;)" style="background:#e74c3c;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:12px;cursor:pointer;font-weight:600">Delete</button>'
            + '</div></div>';
        }).join('')
      : '<div class="empty">No projects uploaded yet</div>';
  }catch(e){b.innerHTML='<div class="empty">Error loading</div>';}
}
async function uploadPJ(){
  const title=document.getElementById('pjTitle').value.trim();
  const fileInput=document.getElementById('pjFile');
  const file=fileInput.files[0];
  if(!title){alert('Please enter a project title');return;}
  if(!file){alert('Please choose a file');return;}
  const btn=document.getElementById('pjUploadBtn');
  btn.disabled=true;btn.textContent='Uploading...';
  try{
    const fd=new FormData();
    fd.append('title',title);
    fd.append('file',file);
    const r=await fetch(API+'/api/v1/showcase/upload',{method:'POST',headers:{'Authorization':'Bearer '+tok},body:fd});
    if(!r.ok){const err=await r.json().catch(()=>({}));alert('Upload failed: '+(err.detail||r.status));return;}
    document.getElementById('pjTitle').value='';
    fileInput.value='';
    loadPJ();
  }catch(e){alert('Upload failed');}
  finally{btn.disabled=false;btn.textContent='+ Upload Project';}
}
async function deletePJ(id){
  if(!confirm('Delete this project? This cannot be undone.'))return;
  try{
    const r=await fetch(API+'/api/v1/showcase/'+id,{method:'DELETE',headers:{'Authorization':'Bearer '+tok}});
    if(!r.ok){alert('Failed to delete');return;}
    loadPJ();
  }catch(e){alert('Failed to delete');}
}

/* DROPDOWNS */"""

    if old_js_anchor not in content:
        print("JS ANCHOR NOT FOUND - aborting (HTML already patched though)")
    else:
        content = content.replace(old_js_anchor, new_js_anchor, 1)
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("PROJECTS UI PATCHED SUCCESSFULLY")
