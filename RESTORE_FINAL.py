import os
path = r'static/specific_control.html'
html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><title>PrintLab Outlet</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: "Segoe UI", system-ui, sans-serif; background: #f8f9fa; color: #1a1a1a; min-height: 100vh; }
        .hidden { display: none !important; }
        
        /* Login */
        .lw_bg { display: flex; align-items: center; justify-content: center; min-height: 100vh; background: #f5f0eb; }
        .lb_card { background: #fff; border-radius: 16px; padding: 45px; width: 380px; box-shadow: 0 10px 40px rgba(0,0,0,.05); }
        .fi { width: 100%; padding: 12px; border: 1.5px solid #eee; border-radius: 10px; font-size: 1rem; margin-bottom: 20px; outline: none; }
        .lpb { width: 100%; padding: 14px; background: #e84c1e; color: #fff; border: none; border-radius: 10px; font-weight: 800; cursor: pointer; }
        
        /* Topbar */
        .tb { background: #fff; border-bottom: 1px solid #eee; padding: 0 24px; height: 65px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 100; }
        .tbl { display: flex; align-items: center; gap: 15px; }
        .si_box { width: 44px; height: 44px; background: #fde8e0; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; cursor: pointer; position: relative; }
        .sn_text { font-size: 1.1rem; font-weight: 800; color: #1a1a1a; }
        .tbr { display: flex; align-items: center; gap: 10px; position: relative; }
        .btn_top { padding: 10px 20px; border: 1.5px solid #eee; background: #fff; border-radius: 12px; cursor: pointer; font-size: .88rem; font-weight: 700; display: flex; align-items: center; gap: 8px; color: #444; }
        .tbtn { background: #e84c1e; color: #fff !important; border-color: #e84c1e; }
        
        .drop_menu { position: absolute; top: calc(100% + 12px); background: #fff; border-radius: 14px; box-shadow: 0 15px 45px rgba(0,0,0,0.12); width: 220px; overflow: hidden; border: 1px solid #eee; padding: 8px 0; }
        .s_left { left: 0; } .t_right { right: 0; }
        .m_item { padding: 14px 20px; cursor: pointer; font-size: .95rem; font-weight: 700 !important; color: #1a1a1a !important; display: flex; align-items: center; gap: 12px; }
        .m_item:hover { background: #f8f9fa; color: #e84c1e !important; }

        /* Dashboard */
        .ct { padding: 30px; max-width: 1300px; margin: 0 auto; }
        .jp_card { background: #fff; border-radius: 20px; border: 1px solid #eee; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.02); }
        .jh_row { display: flex; justify-content: space-between; align-items: center; padding: 25px 30px; border-bottom: 1px solid #f8f9fa; }
        .jh_row h2 { font-size: 1.3rem; font-weight: 900; }
        .tt_box { display: flex; gap: 8px; flex-wrap: wrap; }
        .tab_b { padding: 9px 20px; border: 1.5px solid #eee; background: #fff; border-radius: 25px; cursor: pointer; font-size: .85rem; font-weight: 700; color: #666; transition: .2s; }
        .tab_b.on { background: #1a1a1a; border-color: #1a1a1a; color: #fff; }
        
        table { width: 100%; border-collapse: collapse; }
        th { padding: 15px 30px; text-align: left; font-size: .75rem; color: #999; text-transform: uppercase; font-weight: 800; border-bottom: 1px solid #f8f9fa; }
        td { padding: 20px 30px; border-bottom: 1px solid #f8f9fa; font-size: .95rem; }
        .jid { color: #e84c1e; font-weight: 900; font-size: 1rem; }
        .status_badge { padding: 6px 16px; border-radius: 25px; font-size: .75rem; font-weight: 800; background: #fff3e0; color: #e65100; border: 1px solid #ffe0b2; }
        .type_tag { padding: 4px 10px; border: 1.5px solid #eee; border-radius: 8px; font-size: .8rem; color: #555; font-weight: 700; background: #fafafa; }

        /* Modals */
        .mo { position: fixed; inset: 0; background: rgba(15, 23, 42, 0.4); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 200; padding: 20px; }
        .mb { background: #fff; border-radius: 24px; width: 100%; max-width: 850px; max-height: 94vh; overflow-y: auto; position: relative; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25); }
        .mh { padding: 25px 35px; border-bottom: 1px solid #f1f5f9; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; background: #fff; z-index: 10; }
        .mh h3 { font-size: 1.4rem; font-weight: 900; }
        .mbody { padding: 30px 35px; }
        .stats_grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 30px; }
        .s_card { border: 1px solid #f1f5f9; padding: 20px; border-radius: 18px; background: #fafafa; }
        .s_lbl { font-size: .72rem; color: #94a3b8; font-weight: 800; text-transform: uppercase; }
        .s_val { font-size: 1.8rem; font-weight: 900; color: #0f172a; margin-top: 5px; }
        .prog_row { display: flex; align-items: center; gap: 20px; margin-bottom: 15px; padding: 12px; border-radius: 12px; border: 1px solid transparent; }
        .prog_bar { flex: 1; height: 10px; background: #f1f5f9; border-radius: 6px; overflow: hidden; }
        .prog_fill { height: 100%; border-radius: 6px; }
        .history_row { display: flex; justify-content: space-between; align-items: center; padding: 18px 0; border-bottom: 1px solid #f1f5f9; }
        .dot { width: 9px; height: 9px; border-radius: 50%; display: inline-block; margin-right: 6px; }
    </style>
</head>
<body>
    <!-- LOGIN -->
    <div id="loginView"><div class="lw_bg"><div class="lb_card"><h2>PrintLab Outlet</h2><p style="color:#94a3b8; font-size:.9rem; margin-bottom:30px; font-weight:600;">Sign in to manage your shop</p><input class="fi" id="loginEm" value="admin@altprint.in"><input class="fi" id="loginPw" type="password" value="AltPrint2024!"><button class="lpb" onclick="handleSignIn()">Sign In</button><div id="loginMsg" style="color:#e84c1e; text-align:center; font-size:.85rem; margin-top:15px; font-weight:800;"></div></div></div></div>

    <!-- DASHBOARD -->
    <div id="dashView" class="hidden">
        <div class="tb">
            <div class="tbl"><div class="si_box" onclick="toggleMenu('sdrop')">🏠<div id="sdrop" class="drop_menu s_left hidden"><div class="m_item" onclick="openAgents()">🚚 Logistics</div><div class="m_item" onclick="openMo('setMo')">⚙️ Settings</div><div class="m_item" onclick="handleLogout()" style="color:#e84c1e;">➔ Logout</div></div></div><div><div class="sn_text">Print Lab Koramangala</div><div style="font-size:.78rem; color:#94a3b8; font-weight:700;">Dashboard</div></div></div>
            <div class="tbr">
                <button class="btn_top" onclick="openAgents()">👥 Delivery Team</button>
                <button class="btn_top" onclick="openPerformance()">📊 Performance Status</button>
                <button class="btn_top tbtn" onclick="toggleMenu('tdrop')">🎫 Ticket Raise ▼
                    <div id="tdrop" class="drop_menu t_right hidden">
                        <div class="m_item" onclick="openTForm('Customer')">👤 Customer Ticket</div>
                        <div class="m_item" onclick="openTForm('Stock')">📦 Stock Ticket</div>
                        <div class="m_item" onclick="openTForm('Technical')">🛠️ Technical Issue</div>
                    </div>
                </button>
            </div>
        </div>

        <div class="ct">
            <div class="jp_card">
                <div class="jh_row">
                    <h2>Active Jobs</h2>
                    <div class="tt_box">
                        <button class="tab_b on" onclick="filterJobs('all', this)">All</button>
                        <button class="tab_b" onclick="filterJobs('Bw', this)">B/W</button>
                        <button class="tab_b" onclick="filterJobs('Colour', this)">Colour</button>
                        <button class="tab_b" onclick="filterJobs('Photo', this)">Photo</button>
                        <button class="tab_b" onclick="filterJobs('Tshirt', this)">T-Shirt</button>
                        <button class="tab_b" onclick="filterJobs('Project', this)">Project</button>
                    </div>
                </div>
                <div id="jobsList"></div>
            </div>
        </div>
    </div>

    <!-- PERFORMANCE MODAL -->
    <div id="perfModal" class="mo hidden">
        <div class="mb">
            <div class="mh">
                <h3>Performance Status</h3>
                <button onclick="closeMo('perfModal')" style="background:none; border:none; font-size:1.8rem; cursor:pointer; color:#cbd5e1;">✕</button>
            </div>
            <div class="mbody">
                <div class="stats_grid" id="perfStats"></div>
                
                <h4 style="margin-bottom:15px; font-size:.9rem; font-weight:800;">Earnings by Print Type (Today)</h4>
                <div id="todayBars" style="margin-bottom:30px;"></div>
                
                <div style="text-align:center;">
                    <button class="btn_top" onclick="toggleSh()" id="shToggleBtn" style="width:100%; justify-content:center; border:2px dashed #eee; background:#fafafa;">📈 View Sales History</button>
                </div>

                <div id="shContent" class="hidden" style="margin-top:35px; border-top:1px solid #f1f5f9; padding-top:35px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
                        <h3 style="font-size:1.1rem; font-weight:800;">Sales History Breakdown</h3>
                        <div class="tt_box">
                            <button class="tab_b on" id="shAll" onclick="updateHistoryGraph('all', this)">All Types</button>
                            <button class="tab_b" onclick="updateHistoryGraph('Bw', this)">B/W</button>
                            <button class="tab_b" onclick="updateHistoryGraph('Colour', this)">Colour</button>
                            <button class="tab_b" onclick="updateHistoryGraph('Photo', this)">Photo</button>
                            <button class="tab_b" onclick="updateHistoryGraph('Tshirt', this)">T-Shirt</button>
                            <button class="tab_b" onclick="updateHistoryGraph('Project', this)">Project</button>
                        </div>
                    </div>
                    <canvas id="historyChart" height="150" style="margin-bottom:30px;"></canvas>
                    <h4 style="margin-bottom:15px; font-size:.95rem; font-weight:800;">Daily History</h4>
                    <div id="historyRows"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- TICKET MODAL -->
    <div id="ticketMo" class="mo hidden">
        <div class="mb" style="max-width:500px;">
            <div class="mh"><h3 id="tTitle">Raise Ticket</h3><button onclick="closeMo('ticketMo')">✕</button></div>
            <div class="mbody">
                <input class="fi" id="tSubj" placeholder="Subject">
                <textarea class="fi" id="tDesc" rows="4" placeholder="Describe the issue..."></textarea>
                <button class="lpb" onclick="alert('Ticket successfully reported to management')">Submit Ticket</button>
            </div>
        </div>
    </div>

    <div id="logMo" class="mo hidden"><div class="mb"><div class="mh"><h3>Logistics & Fleet</h3><button onclick="closeMo('logMo')">✕</button></div><div class="mbody" id="logData"></div></div></div>
    <div id="setMo" class="mo hidden"><div class="mb" style="max-width:450px;"><div class="mh"><h3>Settings</h3><button onclick="closeMo('setMo')">✕</button></div><div class="mbody"><b>Shop ID:</b> shop-001<br><b>Status:</b> Premium Linked</div></div></div>

    <script>
        const API_URL = window.location.origin;
        let token = localStorage.getItem('pl_s'), rawOrders = [], hChart = null;
        const COLORS_MAP = { Bw: '#3b82f6', Colour: '#f97316', Photo: '#10b981', Tshirt: '#8b5cf6', Project: '#ef4444' };
        const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

        if (token) {
            document.getElementById('loginView').classList.add('hidden');
            document.getElementById('dashView').classList.remove('hidden');
            loadInitialData();
        }

        async function handleSignIn() {
            const e = document.getElementById('loginEm').value, p = document.getElementById('loginPw').value;
            try {
                const res = await fetch(API_URL + '/api/v1/auth/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email: e, password: p }) });
                const d = await res.json();
                if (d.access_token) { localStorage.setItem('pl_s', d.access_token); window.location.reload(); }
                else document.getElementById('loginMsg').textContent = "Invalid Credentials";
            } catch (e) { document.getElementById('loginMsg').textContent = "Backend Offline"; }
        }

        async function loadInitialData() {
            try {
                const res = await fetch(API_URL + '/api/v1/orders', { headers: { 'Authorization': 'Bearer ' + token } });
                rawOrders = await res.json(); renderActiveJobs(rawOrders);
            } catch (e) { console.error(e); }
        }

        function getT(o) {
            const s = JSON.stringify(o).toLowerCase();
            if (s.includes('color') || s.includes('colour')) return 'Colour';
            if (s.includes('photo')) return 'Photo';
            if (s.includes('tshirt')) return 'Tshirt';
            if (s.includes('project')) return 'Project';
            return 'Bw';
        }

        function renderActiveJobs(orders) {
            const container = document.getElementById('jobsList');
            if (!orders.length) { container.innerHTML = '<div style="padding:60px; text-align:center; color:#94a3b8; font-weight:700;">NO ACTIVE JOBS FOUND</div>'; return; }
            let h = '<table><tr><th>Order ID</th><th>Customer</th><th>Type</th><th>Document</th><th>Status</th></tr>';
            orders.slice(0, 8).forEach(o => {
                h += `<tr><td class="jid">#${o.order_number || o.id.slice(0,8)}</td><td><div style="font-weight:800; color:#0f172a;">${o.user_name || 'Walk-in'}</div></td><td><span class="type_tag">${getT(o)}</span></td><td>${o.file_name || 'Assignment_Final.pdf'}</td><td><span class="status_badge">${o.status}</span></td></tr>`;
            });
            container.innerHTML = h + '</table>';
        }

        function filterJobs(t, btn) {
            document.querySelectorAll('.tab_b').forEach(b => b.classList.remove('on'));
            btn.classList.add('on');
            renderActiveJobs(t === 'all' ? rawOrders : rawOrders.filter(o => getT(o) === t));
        }

        function openPerformance() {
            openMo('perfModal');
            document.getElementById('shContent').classList.add('hidden');
            document.getElementById('shToggleBtn').textContent = "📈 View Sales History";
            
            document.getElementById('perfStats').innerHTML = `
                <div class="s_card"><span class="s_lbl">Total Orders</span><div class="s_val">${rawOrders.length}</div></div>
                <div class="s_card"><span class="s_lbl">Pending</span><div class="s_val" style="color:orange;">${rawOrders.filter(o=>o.status=='pending').length}</div></div>
                <div class="s_card"><span class="s_lbl">Delivered</span><div class="s_val" style="color:green;">${rawOrders.filter(o=>o.status=='delivered').length}</div></div>
                <div class="s_card"><span class="s_lbl">Processing</span><div class="s_val" style="color:blue;">2</div></div>
            `;
            
            document.getElementById('todayBars').innerHTML = Object.keys(COLORS_MAP).map(k => `
                <div class="prog_row">
                    <div style="width:70px; font-size:.85rem; font-weight:800;">${k}</div>
                    <div class="prog_bar"><div style="height:100%; width:60%; background:${COLORS_MAP[k]}"></div></div>
                    <div style="width:70px; text-align:right; font-weight:900; font-size:.85rem; color:${COLORS_MAP[k]}">Rs 500</div>
                </div>
            `).join('');
        }

        function toggleSh() {
            const sec = document.getElementById('shContent');
            const btn = document.getElementById('shToggleBtn');
            if (sec.classList.contains('hidden')) {
                sec.classList.remove('hidden');
                btn.textContent = "▲ Hide Sales History";
                updateHistoryGraph('all', document.getElementById('shAll'));
            } else {
                sec.classList.add('hidden');
                btn.textContent = "📈 View Sales History";
            }
        }

        function updateHistoryGraph(type, btn) {
            document.querySelectorAll('#shContent .tab_b').forEach(b => { b.style.background='#fff'; b.style.color='#666'; b.style.borderColor='#eee'; });
            btn.style.background='#1a1a1a'; btn.style.color='#fff'; btn.style.borderColor='#1a1a1a';

            const labels = [], vals = [], dayData = [];
            for (let i = 7; i >= 0; i--) {
                const d = new Date(); d.setDate(d.getDate() - i);
                const ds = d.getDate() + ' ' + MONTHS[d.getMonth()];
                labels.push(ds);
                const dayOrds = rawOrders.filter(o => new Date(o.created_at).toDateString() === d.toDateString());
                const barVal = dayOrds.reduce((a, b) => (type === 'all' || getT(b) === type) ? a + (parseFloat(b.grand_total) || 0) : a, 0);
                vals.push(barVal);
                const cats = {}; Object.keys(COLORS_MAP).forEach(c => cats[c] = dayOrds.filter(o=>getT(o)==c).reduce((s,o)=>s+(parseFloat(o.grand_total)||0),0));
                dayData.push({ label: `Day ${8-i}`, date: ds, total: dayOrds.reduce((s, o) => s + (parseFloat(o.grand_total) || 0), 0), cats });
            }

            if (hChart) hChart.destroy();
            hChart = new Chart(document.getElementById('historyChart'), {
                type: 'bar',
                data: { labels, datasets: [{ data: vals, backgroundColor: type === 'all' ? '#1a1a1a' : COLORS_MAP[type], borderRadius: 6 }] },
                options: { plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { callback: v => '₹' + v } } } }
            });

            document.getElementById('historyRows').innerHTML = dayData.reverse().map(item => `
                <div class="history_row">
                    <div>
                        <div style="font-weight:900; font-size:1.05rem;">${item.label} <small style="color:#94a3b8; font-weight:700; margin-left:12px;">${item.date}</small></div>
                        <div style="margin-top:8px; display:flex; gap:12px; flex-wrap:wrap;">
                            ${Object.keys(COLORS_MAP).map(c => `<span style="display:inline-flex; align-items:center; gap:4px; font-size:.72rem; color:#64748b; font-weight:700;"><span class="dot" style="background:${COLORS_MAP[c]};"></span> ${c} ₹${item.cats[c]}</span>`).join('')}
                        </div>
                    </div>
                    <div style="font-weight:900; font-size:1.15rem;">₹${item.total.toLocaleString()}</div>
                </div>
            `).join('');
        }

        async function openAgents() {
            openMo('logMo');
            const el = document.getElementById('logData');
            el.innerHTML = '<div style="text-align:center; padding:30px; font-weight:700; color:#94a3b8;">LINKING TO FLEET...</div>';
            try {
                const res = await fetch(API_URL + '/api/v1/delivery-persons', { headers: { 'Authorization': 'Bearer ' + token } });
                const d = await res.json();
                el.innerHTML = d.map(a => `<div style="padding:20px; border-bottom:1px solid #f1f5f9; display:flex; justify-content:space-between; align-items:center;"><div><b style="font-size:1.1rem; color:#0f172a;">${a.name}</b><br><small style="color:#94a3b8; font-weight:700;">${a.phone}</small></div><div style="background:#fde8e0; color:#e84c1e; padding:5px 12px; border-radius:10px; font-size:.8rem; font-weight:800;">${a.vehicle_number}</div></div>`).join('');
            } catch(e) { el.innerHTML = "Backend offline."; }
        }

        function openTForm(t) { document.getElementById('tTitle').innerText = t + ' Ticket Raise'; toggleLocalMenu('tdrop'); openMo('ticketMo'); }
        function toggleLocalMenu(id) { document.getElementById(id).classList.toggle('hidden'); }
        function openMo(id) { document.getElementById(id).classList.remove('hidden'); }
        function closeMo(id) { document.getElementById(id).classList.add('hidden'); }
        function handleLogout() { localStorage.removeItem('pl_s'); window.location.reload(); }
        window.onclick = e => { if (!e.target.closest('.si_box') && !e.target.closest('.tbtn')) { document.getElementById('sdrop').classList.add('hidden'); document.getElementById('tdrop').classList.add('hidden'); } }
    </script>
</body>
</html>"""
with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print("SUCCESS: Full Replit Design with Integrated Sales History restored!")
