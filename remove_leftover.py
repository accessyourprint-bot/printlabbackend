import io

path = r"static\specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

leftover = """  try{
    const r=await fetch(API+'/api/v1/showcase/'+id,{method:'DELETE',headers:{'Authorization':'Bearer '+tok}});
    if(!r.ok){alert('Failed to delete');return;}
    loadPJ();
  }catch(e){alert('Failed to delete');}
}
"""

if leftover in content:
    content = content.replace(leftover, "", 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("LEFTOVER REMOVED")
else:
    print("LEFTOVER NOT FOUND EXACTLY")
