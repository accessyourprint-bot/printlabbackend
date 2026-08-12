import re
import io

path = "static/full_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# --- Part 1: replace filterTickets() function using regex (avoids corrupted-byte matching issues) ---
pattern = re.compile(r"function filterTickets\(type,el\)\{.*?\n\}", re.S)
matches = pattern.findall(content)
print(f"filterTickets function found {len(matches)} time(s)")

new_func = """function showTicketDetail(id){
  const t=allTickets.find(x=>x.id===id);
  if(!t)return;
  document.getElementById('tdName').textContent=t.raised_by||'Not provided';
  document.getElementById('tdSubject').textContent=t.subject||'Issue';
  document.getElementById('tdDesc').textContent=t.description||'No details provided.';
  document.getElementById('tdStatus').textContent=t.status||'open';
  document.getElementById('tdStatus').className='badge '+(t.status==='resolved'?'b-green':'b-yellow');
  const rb=document.getElementById('tdResolveBtn');
  rb.style.display=t.status==='resolved'?'none':'inline-block';
  rb.onclick=function(){resolveTicket(t.id);document.getElementById('ticketDetailModal').style.display='none';};
  document.getElementById('ticketDetailModal').style.display='flex';
}
function filterTickets(type,el){
  document.querySelectorAll('#pg-ticket .tab-row .tab-btn').forEach(t=>t.classList.remove('on'));
  if(el) el.classList.add('on');
  const list=allTickets.filter(t=>type==='customer'?(t.category==='customer'||!t.category):(t.category==='outlet'||t.category==='stock'||t.category==='technical'));
  document.getElementById('tkHd').innerHTML=(type==='customer'?'Customer':'Outlet')+' Complaints (<span id="tkCount">'+list.length+'</span>)';
  document.getElementById('tkList').innerHTML=list.length?list.map(t=>'<div class="ticket-item" style="cursor:pointer" onclick="showTicketDetail(\\''+t.id+'\\')"><div><div class="ticket-title"><b>'+(t.subject||'Issue')+'</b><span class="badge '+(t.status==='resolved'?'b-green':'b-yellow')+'">'+(t.status||'open')+'</span></div><div class="ticket-meta">Raised by: <b>'+(t.raised_by||'Anonymous')+'</b> &bull; '+fmtDate(t.created_at)+', '+fmtTime(t.created_at)+'</div><div class="ticket-desc">'+(t.description||'No details provided.')+'</div></div><button class="btn-sm" onclick="event.stopPropagation();resolveTicket(\\''+t.id+'\\')">&#10003; Resolve</button></div>').join(''):'<div class="empty">No complaints</div>';
}"""

if len(matches) == 1:
    content = pattern.sub(lambda m: new_func, content, count=1)
    print("filterTickets replaced, showTicketDetail added")
else:
    print("WARNING: filterTickets not found exactly once, aborting")
    exit()

# --- Part 2: insert the detail modal HTML before </body> ---
old_anchor = """<button class="btn-full" onclick="submitRaiseTicket()">Raise Ticket</button>
</div>
</div></div>

</body>
</html>"""

new_anchor = """<button class="btn-full" onclick="submitRaiseTicket()">Raise Ticket</button>
</div>
</div></div>

<div id="ticketDetailModal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:999;align-items:center;justify-content:center">
<div style="background:#fff;border-radius:14px;width:480px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,.2)">
<div style="padding:20px 24px;border-bottom:1px solid #f0f0f3;display:flex;justify-content:space-between;align-items:center">
<b style="font-size:1rem">Ticket Details</b>
<button onclick="document.getElementById(\\'ticketDetailModal\\').style.display=\\'none\\'" style="background:none;border:none;font-size:1.3rem;cursor:pointer">&#10005;</button>
</div>
<div style="padding:24px">
<div class="fg"><label>Raised By</label><div id="tdName" style="padding:10px 0;font-weight:600"></div></div>
<div class="fg"><label>Subject</label><div id="tdSubject" style="padding:10px 0;font-weight:600"></div></div>
<div class="fg"><label>Status</label><div style="padding:6px 0"><span id="tdStatus" class="badge b-yellow"></span></div></div>
<div class="fg"><label>Description</label><div id="tdDesc" style="padding:10px 0;white-space:pre-wrap"></div></div>
<button id="tdResolveBtn" class="btn-full">&#10003; Resolve Ticket</button>
</div>
</div></div>

</body>
</html>"""

c2 = content.count(old_anchor)
print(f"Modal insert anchor found {c2} time(s)")
if c2 == 1:
    content = content.replace(old_anchor, new_anchor)
    print("ticketDetailModal inserted")
else:
    print("WARNING: anchor not unique, aborting")
    exit()

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
