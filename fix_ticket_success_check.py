import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = "if(r && r.id){cMo('tkMo');alert('Ticket raised successfully!');}\n    else{alert('Error raising ticket: '+(r&&r.detail?r.detail:'Please try logging in again'));}"

new = "if(r && (r.id || (r.data && r.data.id))){cMo('tkMo');alert('Ticket raised successfully!');loadTickets && loadTickets();}\n    else{alert('Error raising ticket: '+(r&&r.detail?r.detail:'Please try logging in again'));}"

c = content.count(old)
print(f"Anchor found {c} time(s)")
if c == 1:
    content = content.replace(old, new)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Success check fixed to match actual APIResponse shape")
else:
    print("WARNING: anchor not unique - manual fix needed")
