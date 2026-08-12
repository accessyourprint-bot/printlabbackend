import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """      document.getElementById('tBy').value='';document.getElementById('tSj').value='';document.getElementById('tDt').value='';
      cMo('tkMo');alert('Ticket raised successfully!');loadTickets && loadTickets();"""

new = """      document.getElementById('tBy').value='';document.getElementById('tSj').value='';document.getElementById('tDt').value='';
      cMo('tkMo');alert('Ticket raised successfully!');"""

c = content.count(old)
print(f"Anchor found {c} time(s)")
if c == 1:
    content = content.replace(old, new)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Removed the crashing loadTickets() call - bug fixed")
else:
    print("WARNING: anchor not unique - manual fix needed")
