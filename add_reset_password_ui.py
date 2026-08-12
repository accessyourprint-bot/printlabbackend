import io

path = "static/full_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# --- Part 1: add Reset Password button next to Deactivate/Delete on outlet card ---
old_buttons = """      '<button id="tog_'+o.id+'" onclick="toggleOutlet(this.id.slice(4))" style="padding:5px 12px;background:'+(o.is_active?'#e74c3c':'#22b573')+';color:#fff;border:none;border-radius:6px;font-size:.78rem;cursor:pointer">'+(o.is_active?'Deactivate':'Activate')+'</button>'+
      '<button id="del_'+o.id+'" onclick="delOutlet(this.id.slice(4))" style="padding:5px 12px;background:#e74c3c;color:#fff;border:none;border-radius:6px;font-size:.78rem;cursor:pointer">Delete</button>'+
      '</div></div></div>';"""

new_buttons = """      '<button onclick="openResetPassword(\\''+o.id+'\\',\\''+o.name.replace(/'/g,"")+'\\')" style="padding:5px 12px;background:#3b5bfd;color:#fff;border:none;border-radius:6px;font-size:.78rem;cursor:pointer">Reset Password</button>'+
      '<button id="tog_'+o.id+'" onclick="toggleOutlet(this.id.slice(4))" style="padding:5px 12px;background:'+(o.is_active?'#e74c3c':'#22b573')+';color:#fff;border:none;border-radius:6px;font-size:.78rem;cursor:pointer">'+(o.is_active?'Deactivate':'Activate')+'</button>'+
      '<button id="del_'+o.id+'" onclick="delOutlet(this.id.slice(4))" style="padding:5px 12px;background:#e74c3c;color:#fff;border:none;border-radius:6px;font-size:.78rem;cursor:pointer">Delete</button>'+
      '</div></div></div>';"""

c1 = content.count(old_buttons)
print(f"Button block found {c1} time(s)")
if c1 == 1:
    content = content.replace(old_buttons, new_buttons)
    print("Reset Password button added to outlet card")
else:
    print("WARNING: button block not found exactly once, aborting")
    exit()

# --- Part 2: add the JS functions (openResetPassword, submitResetPassword) right after filterOutlets ---
anchor2 = "  }).join('')+'</div>';\n}\nasync function addOutlet(){"

new_js = """  }).join('')+'</div>';
}
let _resetPwUserId=null;
async function openResetPassword(shopId,shopName){
  const d=await api('/api/v1/admin/users?shop_id='+shopId);
  const users=(Array.isArray(d)?d:(d?.data||[])).filter(u=>u.role==='shop_admin');
  if(!users.length){alert('No login account is linked to this outlet yet. Add one from Sub-Admin Management or when creating the outlet.');return;}
  _resetPwUserId=users[0].id;
  document.getElementById('rpShopName').textContent=shopName;
  document.getElementById('rpNewPass').value='';
  document.getElementById('resetPasswordModal').style.display='flex';
}
async function submitResetPassword(){
  const pass=document.getElementById('rpNewPass').value;
  if(!pass||pass.length<6){alert('Password must be at least 6 characters');return;}
  await api('/api/v1/admin/users/'+_resetPwUserId+'/reset-password?new_password='+encodeURIComponent(pass),'PATCH');
  document.getElementById('resetPasswordModal').style.display='none';
  alert('Password reset successfully. Share the new password with the outlet.');
}
async function addOutlet(){"""

c2 = content.count(anchor2)
print(f"JS insertion anchor found {c2} time(s)")
if c2 == 1:
    content = content.replace(anchor2, new_js)
    print("Reset password JS functions added")
else:
    print("WARNING: JS anchor not found exactly once, aborting")
    exit()

# --- Part 3: add the modal HTML before </body> ---
old_anchor = """<button class="btn-full" onclick="submitRaiseTicket()">Raise Ticket</button>
</div>
</div></div>

</body>
</html>"""

new_anchor = """<button class="btn-full" onclick="submitRaiseTicket()">Raise Ticket</button>
</div>
</div></div>

<div id="resetPasswordModal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:999;align-items:center;justify-content:center">
<div style="background:#fff;border-radius:14px;width:380px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,.2)">
<div style="padding:20px 24px;border-bottom:1px solid #f0f0f3;display:flex;justify-content:space-between;align-items:center">
<b style="font-size:1rem">Reset Password</b>
<button onclick="document.getElementById(\\'resetPasswordModal\\').style.display=\\'none\\'" style="background:none;border:none;font-size:1.3rem;cursor:pointer">&#10005;</button>
</div>
<div style="padding:24px">
<div class="fg"><label>Outlet</label><div id="rpShopName" style="padding:6px 0;font-weight:600"></div></div>
<div class="fg"><label>New Password</label><input id="rpNewPass" type="text" placeholder="Set new password (min 6 chars)"></div>
<button class="btn-full" onclick="submitResetPassword()" style="margin-top:6px">Reset Password</button>
</div>
</div></div>

</body>
</html>"""

c3 = content.count(old_anchor)
print(f"Modal insert anchor found {c3} time(s)")
if c3 == 1:
    content = content.replace(old_anchor, new_anchor)
    print("resetPasswordModal inserted")
else:
    print("WARNING: modal anchor not found exactly once, aborting")
    exit()

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
