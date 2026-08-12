import io

path = r"static\full_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_btns = """      '<div style="display:flex;gap:6px">'+
      '<button id="tog_'+o.id+'" onclick="toggleOutlet(this.id.slice(4))" style="padding:5px 12px;background:'+(o.is_active?'#e74c3c':'#22b573')+';color:#fff;border:none;border-radius:6px;font-size:.78rem;cursor:pointer">'+(o.is_active?'Deactivate':'Activate')+'</button>'+
      '<button id="del_'+o.id+'" onclick="delOutlet(this.id.slice(4))" style="padding:5px 12px;background:#e74c3c;color:#fff;border:none;border-radius:6px;font-size:.78rem;cursor:pointer">Delete</button>'+
      '</div></div></div>';"""

new_btns = """      '<div style="display:flex;gap:6px">'+
      '<button id="rst_'+o.id+'" onclick="resetOutletPassword(this.id.slice(4))" style="padding:5px 12px;background:#1a223e;color:#fff;border:none;border-radius:6px;font-size:.78rem;cursor:pointer">Reset Password</button>'+
      '<button id="tog_'+o.id+'" onclick="toggleOutlet(this.id.slice(4))" style="padding:5px 12px;background:'+(o.is_active?'#e74c3c':'#22b573')+';color:#fff;border:none;border-radius:6px;font-size:.78rem;cursor:pointer">'+(o.is_active?'Deactivate':'Activate')+'</button>'+
      '<button id="del_'+o.id+'" onclick="delOutlet(this.id.slice(4))" style="padding:5px 12px;background:#e74c3c;color:#fff;border:none;border-radius:6px;font-size:.78rem;cursor:pointer">Delete</button>'+
      '</div></div></div>';"""

if old_btns not in content:
    print("BUTTON BLOCK NOT FOUND - aborting")
else:
    content = content.replace(old_btns, new_btns, 1)

    old_after = """async function loadOutlets(){"""
    new_after = """async function resetOutletPassword(id){
  if(!confirm('Reset password for this outlet?')) return;
  try{
    const r=await api('/api/v1/shops/'+id+'/reset-password','PATCH');
    if(r && r.data && r.data.new_password){
      alert('New password: '+r.data.new_password+'\\n\\nCopy this now, it will not be shown again.');
    }else{
      alert('Password reset, but no password was returned.');
    }
  }catch(e){alert('Failed to reset password');}
}
async function loadOutlets(){"""

    if old_after not in content:
        print("loadOutlets NOT FOUND - aborting (button already added though)")
    else:
        content = content.replace(old_after, new_after, 1)
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("PATCHED SUCCESSFULLY")
