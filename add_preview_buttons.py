import io

path = r"static\full_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """<div><div class="form-panel"><h3>&#128248; Live Preview</h3>
<div class="preview-box" style="padding:0;overflow:hidden">
<iframe id="livePreviewFrame" src="http://localhost:5173/?preview=1" style="width:100%;height:640px;border:none;display:block"></iframe>
<p style="text-align:center;color:#aaa;font-size:.76rem;padding:8px 16px 14px">Live app - updates as you type</p>
</div></div></div>"""

new = """<div><div class="form-panel"><h3>&#128248; Live Preview</h3>
<div style="display:flex;gap:8px;margin-bottom:10px">
<button class="btn-sm" id="pvBtnLogin" onclick="setPreviewView('login')" style="flex:1;background:#1a223e;color:#fff;border:none">Login</button>
<button class="btn-sm" id="pvBtnDash" onclick="setPreviewView('dashboard')" style="flex:1;background:#eee;color:#1a223e;border:none">Dashboard</button>
</div>
<div class="preview-box" style="padding:0;overflow:hidden">
<iframe id="livePreviewFrame" src="http://localhost:5173/?preview=1&view=login" style="width:100%;height:640px;border:none;display:block"></iframe>
<p style="text-align:center;color:#aaa;font-size:.76rem;padding:8px 16px 14px">Live app - updates as you type</p>
</div></div></div>"""

if old not in content:
    print("PREVIEW BLOCK NOT FOUND - aborting")
else:
    content = content.replace(old, new, 1)

    # add the JS function right before the closing </script>
    old_close = "</script>"
    new_close = """function setPreviewView(view){
  document.getElementById('livePreviewFrame').src='http://localhost:5173/?preview=1&view='+view;
  document.getElementById('pvBtnLogin').style.background=view==='login'?'#1a223e':'#eee';
  document.getElementById('pvBtnLogin').style.color=view==='login'?'#fff':'#1a223e';
  document.getElementById('pvBtnDash').style.background=view==='dashboard'?'#1a223e':'#eee';
  document.getElementById('pvBtnDash').style.color=view==='dashboard'?'#fff':'#1a223e';
}
</script>"""
    # only replace the LAST </script> occurrence (end of main script block)
    idx = content.rfind(old_close)
    if idx == -1:
        print("CLOSING SCRIPT TAG NOT FOUND - aborting")
    else:
        content = content[:idx] + new_close + content[idx+len(old_close):]
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("PATCHED SUCCESSFULLY")
