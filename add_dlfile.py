import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

marker = "function fj(t,el){"
dlfile_fn = """async function dlFile(fileId, filename){
  try{
    const r = await fetch(API + '/api/v1/files/' + fileId + '/download', {headers:{Authorization:'Bearer '+tok}});
    if(!r.ok){ alert('Download failed'); return; }
    const blob = await r.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename || 'file';
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  }catch(e){ alert('Download failed'); }
}
"""

if marker not in content:
    print("MARKER NOT FOUND")
else:
    content = content.replace(marker, dlfile_fn + marker, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("dlFile function added successfully")
