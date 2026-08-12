import io

path = r"static\specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

pj_js = """/* PROJECTS SHOWCASE */
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
"""

# Step 1: remove the misplaced block from the CSS area (it sits right before the real "/* DROPDOWNS */" CSS comment)
misplaced = pj_js + "/* DROPDOWNS */"
if misplaced not in content:
    print("MISPLACED BLOCK NOT FOUND EXACTLY - aborting, need manual check")
else:
    content = content.replace(misplaced, "/* DROPDOWNS */", 1)

    # Step 2: insert the JS properly before function toggleSD()
    anchor = "function toggleSD(){document.getElementById('sdrop').classList.toggle('hidden');}"
    if anchor not in content:
        print("TOGGLESD ANCHOR NOT FOUND - aborting (CSS cleanup already done though)")
    else:
        content = content.replace(anchor, pj_js + "\n" + anchor, 1)
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("FIXED SUCCESSFULLY - JS MOVED TO SCRIPT BLOCK")
