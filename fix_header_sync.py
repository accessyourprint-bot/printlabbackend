import io, re

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

marker = "// header-sync-injected"
if marker in content:
    print("Header sync already injected, skipping")
else:
    pattern = re.compile(r'(function rJ\([^)]*\)\s*\{)')
    matches = pattern.findall(content)
    print(f"rJ() function anchor found {len(matches)} time(s)")
    if len(matches) == 1:
        inject = r"""\1
  // header-sync-injected
  (function(){
    const actHead = document.getElementById('actHead');
    if(actHead){
      if(curStabFilter==='all') actHead.innerText = 'Download';
      else if(curStabFilter==='downloaded') actHead.innerText = 'Download';
      else if(curStabFilter==='completed') actHead.innerText = 'Out for Delivery';
      else if(curStabFilter==='out_for_delivery') actHead.innerText = 'Out for Delivery';
    }
  })();"""
        content = pattern.sub(inject, content, count=1)
        print("Header sync injected into rJ()")
    else:
        print("WARNING: rJ() anchor not found or ambiguous, no changes made")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
