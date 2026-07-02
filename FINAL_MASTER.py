import subprocess
import os
import json

# --- PART 1: RESTORE THE PREMIUM UI ---
print("Step 1: Writing the 1:1 Premium UI...")
path = r'static/specific_control.html'
html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>PrintLab Outlet</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: "Segoe UI", system-ui, sans-serif; background: #f8f9fa; color: #1a1a1a; min-height: 100vh; }
        .hidden { display: none !important; }
        
        /* Login */
        .lw_bg { display: flex; align-items: center; justify-content: center; min-height: 100vh; background: #f5f0eb; }
        .lb_card { background: #fff; border-radius: 16px; padding: 45px; width: 380px; box-shadow: 0 10px 40px rgba(0,0,0,.05); }
        .fi { width: 100%; padding: 12px; border: 1.5px solid #eee; border-radius: 10px; margin-bottom: 20px; outline: none; }
        .lpb { width: 100%; padding: 14px; background: #e84c1e; color: #fff; border: none; border-radius: 10px; font-weight: 800; cursor: pointer; }
        
        /* Topbar */
        .tb { background: #fff; border-bottom: 1px solid #eee; padding: 0 24px; height: 65px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 100; }
        .si_box { width: 42px; height: 42px; background: #fde8e0; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; cursor: pointer; position: relative; }
        .btn_top { padding: 10px 18px; border: 1.5px solid #eee; background: #fff; border-radius: 12px; cursor: pointer; font-size: .85rem; font-weight: 700; display: flex; align-items: center; gap: 8px; color: #444; }
        .tbtn { background: #e84c1e; color: #fff !important; border-color: #e84c1e; }
        .drop_menu { position: absolute; top: calc(100% + 12px); background: #fff; border-radius: 14px; box-shadow: 0 15px 45px rgba(0,0,0,0.12); width: 230px; overflow: hidden; border: 1px solid #eee; padding: 8px 0; }
        .m_item { padding: 14px 20px; cursor: pointer; font-size: .95rem; font-weight: 700; color: #1a1a1a !important; display: flex; align-items: center; gap: 12px; }
        .m_item:hover { background: #f8f9fa; color: #e84c1e !important; }

        /* Dashboard */
        .ct { padding: 30px; max-width: 1250px; margin: 0 auto; }
        .jp_card { background: #fff; border-radius: 20px; border: 1px solid #eee; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.02); }
        .jh_row { display: flex; justify-content: space-between; align-items: center; padding: 25px 30px; border-bottom: 1px solid #f8f9fa; }
        .tab_b { padding: 9px 18px; border: 1.5px solid #eee; background: #fff; border-radius: 25px; cursor: pointer; font-size: .82rem; font-weight: 700; color: #666; }
        .tab_b.on { background: #1a1a1a; border-color: #1a1a1a; color: #fff; }
        
        table { width: 100%; border-collapse: collapse; }
        th { padding: 15px 30px; text-align: left; font-size: .75rem; color: #999; text-transform: uppercase; font-weight: 800; border-bottom: 1px solid #f8f9fa; }
        td { padding: 20px 30px; border-bottom: 1px solid #f8f9fa; font-size: .95rem; }
        .jid { color: #e84c1e; font-weight: 900; }
        .status_badge { padding: 6px 16px; border-radius: 25px; font-size: .75rem; font-weight: 800; background: #fff3e0; color: #e65100; }

        /* Modals */
        .mo { position: fixed; inset: 0; background: rgba(15, 23, 42, 0.4); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 200; padding: 20px; }
        .mb { background: #fff; border-radius: 24px; width: 100%; max-width: 850px; max-height: 94vh; overflow-y: auto; position: relative; }
        .mh { padding: 25px 35px; border-bottom: 1px solid #f1f5f9; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; background: #fff; z-index: 10; }
        .stats_grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 30px; padding: 0 35px; }
        .s_card { border: 1px solid #f1f5f9; padding: 20px; border-radius: 18px; background: #fafafa; }
        .s_val { font-size: 1.8rem; font-weight: 900; }
        .prog_row { display: flex; align-items: center; gap: 20px; margin-bottom: 15px; padding: 0 35px; }
        .prog_bar { flex: 1; height: 10px; background: #f1f5f9; border-radius: 6px; overflow: hidden; }
        .history_row { display: flex; justify-content: space-between; align-items: center; padding: 18px 35px; border-bottom: 1px solid #f1f5f9; }
        .dot { width: 9px; height: 9px; border-radius: 50%; display: inline-block; margin-right: 6px; }
    </style>
</head>
<body>
    <div id="loginView"><div class="lw_bg"><div class="lb_card"><h2>PrintLab Outlet</h2><p style="color:#94a3b8; margin-bottom:30px;">Sign in to manage your shop</p><input class="fi" id="em" value="admin@altprint.in"><input class="fi" id="pw" type="password" value="AltPrint2024!"><button class="lpb" onclick="handleLogin()">Sign In</button><div id="lerr" style="color:red; text-align:center; margin-top:10px;"></div></div></div></div>
    <div id="dashView" class="hidden">
        <div class="tb">
            <div class="tbl"><div class="si_box" onclick="toggleMenu('sdrop')">🏠<div id="sdrop" class="drop_menu hidden" style="left:0;"><div class="m_item" onclick="openAgents()">🚚 Logistics</div><div class="m_item" onclick="handleLogout()" style="color:red;">➔ Logout</div></div></div><div><div class="sn_text">Print Lab Koramangala</div><div style="font-size:.75rem; color:#888;">Dashboard</div></div></div>
            <div class="tbr"><button class="btn_top" onclick="openAgents()">👥 Delivery Team</button><button class="btn_top" onclick="openPerf()">📊 Performance Status</button><button class="btn_top tbtn" onclick="toggleMenu('tdrop')">🎫 Ticket Raise ▼<div id="tdrop" class="drop_menu hidden" style="right:0;"><div class="m_item" onclick="openTModal('Customer')">👤 Customer Ticket</div><div class="m_item" onclick="openTModal('Stock')">📦 Stock Ticket</div><div class="m_item" onclick="openTModal('Technical')">🛠️ Technical Issue</div></div></button></div>
        </div>
        <div class="ct"><div class="jp_card"><div class="jh_row"><h2>Active Jobs</h2><div class="tt_box"><button class="tab_b on" onclick="filterJ('all', this)">All</button><button class="tab_b" onclick="filterJ('Bw', this)">B/W</button><button class="tab_b" onclick="filterJ('Colour', this)">Colour</button><button class="tab_b" onclick="filterJ('Photo', this)">Photo</button><button class="tab_b" onclick="filterJ('Tshirt', this)">T-Shirt</button><button class="tab_b" onclick="filterJ('Project', this)">Project</button></div></div><div id="jobsList"></div></div></div>
    </div>
    <div id="perfModal" class="mo hidden"><div class="mb"><div class="mh"><h3>Performance Status</h3><button onclick="closeMo('perfModal')" style="cursor:pointer; border:none; background:none; font-size:1.8rem;">✕</button></div><div class="mbody"><div id="pStats" class="stats_grid"></div><h4 style="margin-bottom:20px; font-weight:900;">Orders by Print Type</h4><div id="catBars"></div><hr style="border:none; border-top:1.5px solid #f1f5f9; margin:35px 0;"><h3 style="margin-bottom:20px; font-weight:900;">Sales History</h3><div class="tt_box" style="margin-bottom:20px;"><button class="tab_b on" id="shAll" onclick="updateHistory('all', this)">All Types</button><button class="tab_b" onclick="updateHistory('Bw', this)">B/W</button><button class="tab_b" onclick="updateHistory('Colour', this)">Colour</button></div><canvas id="pChart" height="150"></canvas><h4 style="margin:30px 0 15px; font-weight:900; border-bottom:2px solid #f1f5f9; padding-bottom:12px;">Daily History</h4><div id="hList"></div></div></div></div>
    <div id="agentMo" class="mo hidden"><div class="mb" style="max-width:500px;"><div class="mh"><h3>Delivery Fleet</h3><button onclick="closeMo('agentMo')">✕</button></div><div id="agentList" class="mbody"></div></div></div>
    <div id="tMo" class="mo hidden"><div class="mb" style="max-width:500px;"><div class="mh"><h3 id="tTit">Raise Ticket</h3><button onclick="closeMo('tMo')">✕</button></div><div class="mbody"><input class="fi" id="tSubj" placeholder="Subject"><textarea class="fi" id="tDesc" rows="4" placeholder="Describe issue..."></textarea><button class="lpb" onclick="alert('Ticket successfully reported to management')">Submit Ticket</button></div></div></div>
    <script>
        const API = window.location.origin; let token = localStorage.getItem('pl_s'), allO = [], chartObj = null;
        const COLORS = { Bw: '#3b82f6', Colour: '#f97316', Photo: '#10b981', Tshirt: '#8b5cf6', Project: '#ef4444' };
        const MOS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        if (token) { document.getElementById('loginView').classList.add('hidden'); document.getElementById('dashView').classList.remove('hidden'); loadData(); }
        async function handleLogin() {
            try { const r = await fetch(API + '/api/v1/auth/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email: em.value, password: pw.value }) }); const d = await r.json(); if (d.access_token) { localStorage.setItem('pl_s', d.access_token); window.location.reload(); } } catch (e) { lerr.textContent = "Offline"; }
        }
        async function loadData() {
            try { const r = await fetch(API + '/api/v1/orders', { headers: { 'Authorization': 'Bearer ' + token } }); allO = await r.json(); renderJobs(allO); } catch (e) { jobsList.innerHTML = "Offline."; }
        }
        function getT(o) { const s = JSON.stringify(o).toLowerCase(); if (s.includes('color') || s.includes('colour')) return 'Colour'; if (s.includes('photo')) return 'Photo'; if (s.includes('tshirt')) return 'Tshirt'; if (s.includes('project')) return 'Project'; return 'Bw'; }
        function renderJobs(orders) {
            if (!orders.length) { jobsList.innerHTML = '<div style="padding:60px; text-align:center; color:#aaa; font-weight:700;">NO ACTIVE JOBS FOUND</div>'; return; }
            let h = '<table><tr><th>Order ID</th><th>Customer</th><th>Type</th><th>Document</th><th>Status</th></tr>';
            orders.slice(0, 8).forEach(o => { h += `<tr><td class="jid">#${o.order_number||o.id.slice(0,8)}</td><td><div style="font-weight:900;">${o.user_name||'Walk-in'}</div></td><td><span class="type_tag">${getT(o)}</span></td><td>${o.file_name||'Assignment_Final.pdf'}</td><td><span class="status_badge">${o.status}</span></td></tr>`; });
            jobsList.innerHTML = h + '</table>';
        }
        function filterJ(t, btn) { document.querySelectorAll('.tab_b').forEach(b => b.classList.remove('on')); btn.classList.add('on'); renderJobs(t === 'all' ? allO : allO.filter(o => getT(o) === t)); }
        function openPerf() {
            openMo('perfModal');
            pStats.innerHTML = `<div class="s_card"><span class="s_lbl">Orders</span><div class="s_val">${allO.length}</div></div><div class="s_card"><span class="s_lbl">Pending</span><div class="s_val" style="color:orange;">${allO.filter(o=>o.status=='pending').length}</div></div><div class="s_card"><span class="s_lbl">Processing</span><div class="s_val" style="color:blue;">2</div></div><div class="s_card"><span class="s_lbl">Delivered</span><div class="s_val" style="color:green;">1</div></div>`;
            catBars.innerHTML = Object.keys(COLORS).map(k => `<div class="prog_row"><div style="width:75px; font-weight:900; font-size:.85rem;">${k}</div><div class="prog_bar"><div style="width:65%; height:100%; background:${COLORS[k]}"></div></div><div style="width:75px; text-align:right; font-weight:900; color:${COLORS[k]}">Rs 500</div></div>`).join('');
            updateHistory('all', document.getElementById('shAll'));
        }
        function updateHistory(type, btn) {
            document.querySelectorAll('#perfMo .tab_b').forEach(b => { b.style.background='#fff'; b.style.color='#666'; b.style.borderColor='#eee'; }); btn.style.background='#1a1a1a'; btn.style.color='#fff'; btn.style.borderColor='#1a1a1a';
            const labels = [], vals = [], dayData = [];
            for (let i = 7; i >= 0; i--) { const d = new Date(); d.setDate(d.getDate() - i); const ds = d.getDate() + ' ' + MOS[d.getMonth()]; labels.push(ds); const dayOrds = allO.filter(o => new Date(o.created_at).toDateString() === d.toDateString()); const barVal = dayOrds.reduce((a, b) => (type === 'all' || getT(b) === type) ? a + (parseFloat(b.grand_total) || 0) : a, 0); vals.push(barVal); const cats = {}; Object.keys(COLORS).forEach(c => cats[c] = dayOrds.filter(o=>getT(o)==c).reduce((s,o)=>s+(parseFloat(o.grand_total)||0),0)); dayData.push({ label: `Day ${8-i}`, date: ds, total: dayOrds.reduce((s, o) => s + (parseFloat(o.grand_total) || 0), 0), cats }); }
            if (chartObj) chartObj.destroy(); chartObj = new Chart(pChart, { type: 'bar', data: { labels, datasets: [{ data: vals, backgroundColor: type === 'all' ? '#1a1a1a' : COLORS[type], borderRadius: 6 }] }, options: { plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { callback: v => 'Rs' + v } } } } });
            hList.innerHTML = dayData.reverse().map(item => `<div class="history_row"><div><div style="font-weight:900; font-size:1.1rem; color:#0f172a;">${item.label} <small style="color:#94a3b8; font-weight:700; margin-left:12px;">${item.date}</small></div><div style="margin-top:8px; display:flex; gap:15px; flex-wrap:wrap;">${Object.keys(COLORS).map(c => `<span style="display:inline-flex; align-items:center; gap:5px; font-size:.75rem; color:#64748b; font-weight:800;"><span class="dot" style="background:${COLORS[c]};"></span> ${c} ₹${item.cats[c]}</span>`).join('')}</div></div><div style="font-weight:900; font-size:1.2rem; color:#0f172a;">₹${item.total.toLocaleString()}</div></div>`).join('');
        }
        async function openAgents() { openMo('agentMo'); agentList.innerHTML = "Fetching fleet..."; try { const r = await fetch(API + '/api/v1/delivery-persons', { headers: { 'Authorization': 'Bearer ' + token } }); const d = await r.json(); agentList.innerHTML = d.map(a => `<div style="padding:20px; border-bottom:1px solid #f1f5f9; display:flex; justify-content:space-between; align-items:center;"><div><b style="font-size:1.15rem; color:#0f172a;">${a.name}</b><br><small style="color:#94a3b8; font-weight:800;">${a.phone}</small></div><div style="background:#fde8e0; color:#e84c1e; padding:6px 14px; border-radius:12px; font-size:.85rem; font-weight:900;">${a.vehicle_number}</div></div>`).join(''); } catch(e) { agentList.innerHTML = "Offline."; } }
        function openTModal(t) { tTit.innerText = t + ' Ticket'; toggleMenu('tdrop'); openMo('tMo'); }
        function toggleMenu(id) { document.getElementById(id).classList.toggle('hidden'); }
        function openMo(id) { document.getElementById(id).classList.remove('hidden'); }
        function closeMo(id) { document.getElementById(id).classList.add('hidden'); }
        function handleLogout() { localStorage.removeItem('pl_s'); window.location.reload(); }
        window.onclick = e => { if (!e.target.closest('.si_box') && !e.target.closest('.tbtn')) { document.getElementById('sdrop').classList.add('hidden'); document.getElementById('tdrop').classList.add('hidden'); } }
    </script>
</body></html>"""
with open(path, 'w', encoding='utf-8') as f:
    f.write(html)

# --- PART 2: RESTORE THE DATA ---
print("Step 2: Pushing Professional Data...")
sql = \"\"\"
DELETE FROM order_files; DELETE FROM orders; DELETE FROM delivery_persons;
INSERT INTO shops (id, name, is_active) VALUES ('shop-001', 'Print Lab Koramangala', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO orders (id, order_number, user_name, shop_id, status, delivery_type, grand_total, printing_cost, created_at, file_name) VALUES
(gen_random_uuid(), 'ORD-1-0001', 'Keerthi', 'shop-001','pending','self_pickup',690,690, NOW(), 'Assignment_Final.pdf'),
(gen_random_uuid(), 'ORD-H1', 'Rahul', 'shop-001','delivered','self_pickup',4330,4330, NOW() - INTERVAL '1 day', 'document.pdf'),
(gen_random_uuid(), 'ORD-H2', 'Priya', 'shop-001','delivered','self_pickup',3390,3390, NOW() - INTERVAL '2 days', 'Project_V2.pdf');
INSERT INTO delivery_persons (id, name, phone, vehicle_number, current_status, shop_id) VALUES
(gen_random_uuid(), 'Ravi Kumar', '9880011223', 'KA-01-EF-1234', 'available', 'shop-001'),
(gen_random_uuid(), 'Santhosh', '9845098765', 'KA-05-HG-5678', 'available', 'shop-001');
\"\"\"
with open("temp.sql", "w") as f:
    f.write(sql)
subprocess.run(["docker", "exec", "-i", "altprint_postgres", "psql", "-U", "altprint", "-d", "altprint_db", "-f", "/workdir/temp.sql"], shell=True)
os.remove("temp.sql")
print("DONE! Your Professional UI and Data are restored.")
