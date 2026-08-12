import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = "<span class=\"ji-file\">&#8595; '+(o.file_name||'document.pdf')+'</span>"
new = "'+((o.files&&o.files.length)?o.files.map(function(f){return '<span class=\"ji-file\" style=\"cursor:pointer;text-decoration:underline\" onclick=\"event.stopPropagation();dlFile(&quot;'+f.id+'&quot;,&quot;'+(f.original_filename||'file').replace(/\"/g,'')+'&quot;)\">&#8595; '+(f.original_filename||'document.pdf')+'</span>';}).join(''):'<span class=\"ji-file\">&#8595; No file</span>')+'"

if old not in content:
    print("MARKER NOT FOUND")
else:
    content = content.replace(old, new)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Patched successfully")
