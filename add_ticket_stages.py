import io

path = r"static\full_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_header = """<div style="display:flex;justify-content:space-between;align-items:center;margin:20px 0 16px">
<div></div>
<button class="btn-sm btn-orange" onclick="openRaiseTicket()">+ Raise Ticket</button>
</div>
<div class="panel"><div class="panel-hd" id="tkHd">All Tickets (<span id="tkCount">0</span>)</div><div id="tkList"><div class="loading">Loading...</div></div></div>"""

new_header = """<div style="display:flex;justify-content:space-between;align-items:center;margin:20px 0 16px">
<div class="tab-row" style="margin:0">
<button class="tab-btn on" onclick="filterTicketsByStatus('all',this)">All Tickets</button>
<button class="tab-btn" onclick="filterTicketsByStatus('open',this)">&#128308; Open</button>
<button class="tab-btn" onclick="filterTicketsByStatus('in_progress',this)">&#128993; Under Process</button>
<button class="tab-btn" onclick="filterTicketsByStatus('closed',this)">&#128994; Closed</button>
</div>
<button class="btn-sm btn-orange" onclick="openRaiseTicket()">+ Raise Ticket</button>
</div>
<div class="panel"><div class="panel-hd" id="tkHd">All Tickets (<span id="tkCount">0</span>)</div><div id="tkList"><div class="loading">Loading...</div></div></div>"""

if old_header not in content:
    print("HEADER NOT FOUND - aborting")
else:
    content = content.replace(old_header, new_header, 1)

    old_load = """async function loadTickets(){
  const d=await api('/api/v1/tickets');
  allTickets=Array.isArray(d)?d:(d?.data||[]);
  renderAllTickets();
}
function renderAllTickets(){
  const list=allTickets;
  document.getElementById('tkHd').innerHTML='All Tickets (<span id="tkCount">'+list.length+'</span>)';
  document.getElementById('tkList').innerHTML=list.length?list.map(t=>'<div class="ticket-item" style="cursor:pointer" onclick="showTicketDetail(\\''+t.id+'\\')"><div><div class="ticket-title"><b>'+(t.subject||'Issue')+'</b><span class="badge '+(t.status==='resolved'?'b-green':'b-yellow')+'">'+(t.status||'open')+'</span></div><div class="ticket-meta">Raised by: <b>'+(t.raised_by||'Anonymous')+'</b> &bull; '+fmtDate(t.created_at)+', '+fmtTime(t.created_at)+'</div><div class="ticket-desc">'+(t.description||'No details provided.')+'</div></div><button class="btn-sm" onclick="event.stopPropagation();resolveTicket(\\''+t.id+'\\')">&#10003; Resolve</button></div>').join(''):'<div class="empty">No tickets raised yet</div>';
}"""

    new_load = """let ticketStatusFilter='all';
async function loadTickets(){
  const d=await api('/api/v1/tickets');
  allTickets=Array.isArray(d)?d:(d?.data||[]);
  renderAllTickets();
}
function filterTicketsByStatus(status,el){
  ticketStatusFilter=status;
  document.querySelectorAll('#pg-ticket .tab-row .tab-btn').forEach(t=>t.classList.remove('on'));
  if(el) el.classList.add('on');
  renderAllTickets();
}
function ticketBadgeClass(s){
  if(s==='closed'||s==='resolved')return 'b-green';
  if(s==='in_progress')return 'b-yellow';
  return 'b-red';
}
function ticketBadgeLabel(s){
  if(s==='closed'||s==='resolved')return 'Closed';
  if(s==='in_progress')return 'Under Process';
  return 'Open';
}
function ticketNextAction(t){
  const s=t.status||'open';
  if(s==='open'||s==='in_progress'===false&&s!=='in_progress'&&s!=='closed'&&s!=='resolved'){}
  if(s==='closed'||s==='resolved')return '';
  if(s==='in_progress')return '<button class="btn-sm" onclick="event.stopPropagation();updateTicketStatus(\\''+t.id+'\\',\\'closed\\')">&#10003; Close Ticket</button>';
  return '<button class="btn-sm" onclick="event.stopPropagation();updateTicketStatus(\\''+t.id+'\\',\\'in_progress\\')">&#8594; Move to Under Process</button>';
}
function renderAllTickets(){
  const list = ticketStatusFilter==='all' ? allTickets : allTickets.filter(t=>{
    const s=t.status||'open';
    if(ticketStatusFilter==='closed') return s==='closed'||s==='resolved';
    return s===ticketStatusFilter;
  });
  const label = ticketStatusFilter==='all'?'All Tickets':(ticketStatusFilter==='open'?'Open Tickets':(ticketStatusFilter==='in_progress'?'Under Process':'Closed Tickets'));
  document.getElementById('tkHd').innerHTML=label+' (<span id="tkCount">'+list.length+'</span>)';
  document.getElementById('tkList').innerHTML=list.length?list.map(t=>'<div class="ticket-item" style="cursor:pointer" onclick="showTicketDetail(\\''+t.id+'\\')"><div><div class="ticket-title"><b>'+(t.subject||'Issue')+'</b><span class="badge '+ticketBadgeClass(t.status)+'">'+ticketBadgeLabel(t.status)+'</span></div><div class="ticket-meta">Raised by: <b>'+(t.raised_by||'Anonymous')+'</b> &bull; '+fmtDate(t.created_at)+', '+fmtTime(t.created_at)+'</div><div class="ticket-desc">'+(t.description||'No details provided.')+'</div></div>'+ticketNextAction(t)+'</div>').join(''):'<div class="empty">No tickets in this category</div>';
}
async function updateTicketStatus(id,status){
  await api('/api/v1/tickets/'+id,'PATCH',{status:status});
  loadTickets();
}"""

    if old_load not in content:
        print("LOAD/RENDER FUNCTION NOT FOUND - aborting (header already patched though)")
    else:
        content = content.replace(old_load, new_load, 1)
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("PATCHED SUCCESSFULLY")
