import io

path = r"static\full_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove the two tab buttons, keep just a header
old_tabs = """<div style="display:flex;justify-content:space-between;align-items:center;margin:20px 0 16px">
<div class="tab-row" style="margin:0">
<button class="tab-btn on" onclick="filterTickets('customer',this)">&#128100; Customer Complaint</button>
<button class="tab-btn" onclick="filterTickets('outlet',this)">&#127970; Outlet Complaint</button>
</div>
<button class="btn-sm btn-orange" onclick="openRaiseTicket()">+ Raise Ticket</button>
</div>
<div class="panel"><div class="panel-hd" id="tkHd">Customer Complaints (<span id="tkCount">0</span>)</div><div id="tkList"><div class="loading">Loading...</div></div></div>"""

new_tabs = """<div style="display:flex;justify-content:space-between;align-items:center;margin:20px 0 16px">
<div></div>
<button class="btn-sm btn-orange" onclick="openRaiseTicket()">+ Raise Ticket</button>
</div>
<div class="panel"><div class="panel-hd" id="tkHd">All Tickets (<span id="tkCount">0</span>)</div><div id="tkList"><div class="loading">Loading...</div></div></div>"""

if old_tabs not in content:
    print("TABS BLOCK NOT FOUND - aborting")
else:
    content = content.replace(old_tabs, new_tabs, 1)

    # 2. Replace loadTickets + filterTickets logic with a single unified render
    old_js = """async function loadTickets(){
  const d=await api('/api/v1/tickets');
  allTickets=Array.isArray(d)?d:(d?.data||[]);
  filterTickets('customer',document.querySelector('#pg-ticket .tab-btn.on'));
}"""
    new_js = """async function loadTickets(){
  const d=await api('/api/v1/tickets');
  allTickets=Array.isArray(d)?d:(d?.data||[]);
  renderAllTickets();
}
function renderAllTickets(){
  const list=allTickets;
  document.getElementById('tkHd').innerHTML='All Tickets (<span id="tkCount">'+list.length+'</span>)';
  document.getElementById('tkList').innerHTML=list.length?list.map(t=>'<div class="ticket-item" style="cursor:pointer" onclick="showTicketDetail(\\''+t.id+'\\')"><div><div class="ticket-title"><b>'+(t.subject||'Issue')+'</b><span class="badge '+(t.status==='resolved'?'b-green':'b-yellow')+'">'+(t.status||'open')+'</span></div><div class="ticket-meta">Raised by: <b>'+(t.raised_by||'Anonymous')+'</b> &bull; '+fmtDate(t.created_at)+', '+fmtTime(t.created_at)+'</div><div class="ticket-desc">'+(t.description||'No details provided.')+'</div></div><button class="btn-sm" onclick="event.stopPropagation();resolveTicket(\\''+t.id+'\\')">&#10003; Resolve</button></div>').join(''):'<div class="empty">No tickets raised yet</div>';
}"""

    if old_js not in content:
        print("JS BLOCK NOT FOUND - aborting (tabs already patched though)")
    else:
        content = content.replace(old_js, new_js, 1)

        # 3. Remove the now-unused filterTickets function entirely
        old_filter = """function filterTickets(type,el){
  document.querySelectorAll('#pg-ticket .tab-row .tab-btn').forEach(t=>t.classList.remove('on'));
  if(el) el.classList.add('on');
  const list=allTickets.filter(t=>type==='customer'?(t.category==='customer'||!t.category):(t.category==='outlet'||t.category==='stock'||t.category==='technical'));
  document.getElementById('tkHd').innerHTML=(type==='customer'?'Customer':'Outlet')+' Complaints (<span id="tkCount">'+list.length+'</span>)';
  document.getElementById('tkList').innerHTML=list.length?list.map(t=>'<div class="ticket-item" style="cursor:pointer" onclick="showTicketDetail(\\''+t.id+'\\')"><div><div class="ticket-title"><b>'+(t.subject||'Issue')+'</b><span class="badge '+(t.status==='resolved'?'b-green':'b-yellow')+'">'+(t.status||'open')+'</span></div><div class="ticket-meta">Raised by: <b>'+(t.raised_by||'Anonymous')+'</b> &bull; '+fmtDate(t.created_at)+', '+fmtTime(t.created_at)+'</div><div class="ticket-desc">'+(t.description||'No details provided.')+'</div></div><button class="btn-sm" onclick="event.stopPropagation();resolveTicket(\\''+t.id+'\\')">&#10003; Resolve</button></div>').join(''):'<div class="empty">No complaints</div>';
}"""
        if old_filter in content:
            content = content.replace(old_filter, "", 1)
            print("FILTER FUNCTION REMOVED TOO")
        else:
            print("filterTickets function not found for removal (not critical, leaving as dead code)")

        with io.open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("PATCHED SUCCESSFULLY")
