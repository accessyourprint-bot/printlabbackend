import io

path = r"static\specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """        <div id="sdrop" class="sdrop hidden">
          <div class="sdi" onclick="closeSD();openDT()">&#128666; Logistics</div>
          <div class="sdi" onclick="closeSD();alert(curShop?curShop.name:String(curShop.id))">&#9881;&#65039; Settings</div>
          <div class="sdi red" onclick="doLogout()">&#8594; Logout</div>
        </div>"""

new = """        <div id="sdrop" class="sdrop hidden">
          <div class="sdi-info">
            <div class="sdi-info-row"><b>ID:</b> <span id="sdShopId">-</span></div>
            <div class="sdi-info-row"><b>Email:</b> <span id="sdShopEmail">-</span></div>
            <div class="sdi-info-row"><b>Phone:</b> <span id="sdShopPhone">-</span></div>
          </div>
          <div class="sdi" onclick="closeSD();openDT()">&#128666; Logistics</div>
          <div class="sdi" onclick="closeSD();alert(curShop?curShop.name:String(curShop.id))">&#9881;&#65039; Settings</div>
          <div class="sdi red" onclick="doLogout()">&#8594; Logout</div>
        </div>"""

if old not in content:
    print("OLD BLOCK NOT FOUND - aborting")
else:
    content = content.replace(old, new, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("DROPDOWN HTML PATCHED")
