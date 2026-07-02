import os

path = r'C:\Users\Shiva\Downloads\altprint-backend (6)\altprint\static\specific_control.html'

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PrintLab Outlet</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif; background: #f8f8f8; color: #1a1a1a; min-height: 100vh; }
        .hidden { display: none !important; }
        
        /* Login UI */
        .lw { display: flex; align-items: center; justify-content: center; min-height: 100vh; background: #f5f0eb; }
        .lb { background: #fff; border-radius: 14px; padding: 40px; width: 360px; box-shadow: 0 4px 20px rgba(0,0,0,.08); }
        .lb h2 { font-size: 1.5rem; font-weight: 800; margin-bottom: 8px; color: #1a1a1a; }
        .lb p { color: #666; font-size: .85rem; margin-bottom: 24px; }
        .fi { width: 100%; padding: 12px; border: 1.5px solid #e0e0e0; border-radius: 8px; font-size: .95rem; margin-bottom: 16px; outline: none; }
        .fi:focus { border-color: #e84c1e; }
        .lpb { width: 100%; padding: 14px; background: #e84c1e; color: #fff; border: none; border-radius: 8px; font-size: 1rem; font-weight: 700; cursor: pointer; }
        
        /* Dashboard Header */
        .tb { background: #fff; border-bottom: 1px solid #eee; padding: 0 24px; height: 65px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 100; }
        .tbl { display: flex; align-items: center; gap: 15px; }
        .si { width: 44px; height: 44px; background: #fde8e0; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; cursor: pointer; position: relative; }
        .sn { font-size: 1.1rem; font-weight: 800; }
        .ss { font-size: .8rem; color: #888; }
        .tbr { display: flex; align-items: center; gap: 10px; position: relative; }
        .btn { padding: 10px 18px; border: 1.5px solid #ddd; background: #fff; border-radius: 25px; cursor: pointer; font-size: .85rem; font-weight: 600; display: flex; align-items: center; gap: 8px; color: #333; }
        .tbtn { background: #e84c1e; color: #fff; border-color: #e84c1e; }
        
        /* Dropdowns */
        .sdrop, .tdrop { position: absolute; top: calc(100% + 10px); background: #fff; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.15); width: 200px; overflow: hidden; border: 1px solid #eee; }
        .sdrop { left: 0; } .tdrop { right: 0; }
        .si-item, .ti { padding: 14px 18px; cursor: pointer; font-size: .9rem; font-weight: 700; display: flex; align-items: center; gap: 12px; color: #1a1a1a !important; border-bottom: 1px solid #f9f9f9; }
        .si-item:hover, .ti:hover { background: #f8f8f8; }

        /* Main Content */
        .ct { padding: 25px; max-width: 1200px; margin: 0 auto; }
        .jp { background: #fff; border-radius: 16px; border: 1px solid #eee; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.02); }
        .jh { display: flex; justify-content: space-between; align-items: center; padding: 20px 25px; border-bottom: 1px solid #f0f0f0; }
        .jh h2 { font-size: 1.2rem; font-weight: 800; }
        .tt { display: flex; gap: 8px; }
        .t { padding: 8px 18px; border: 1.5px solid #eee; background: #fff; border-radius: 25px; cursor: pointer; font-size: .85rem; font-weight: 600; color: #666; }
        .t.on { background: #1a1a1a; border-color: #1a1a1a; color: #fff; }
        .jc { padding: 30px; text-align: center; color: #999; font-size: .9rem; }
        
        /* Performance Modal */
        .mo { position: fixed; inset: 0; background: rgba(0,0,0,0.6); display: flex; align-items: center; justify-content: center; z-index: 200; padding: 20px; }
        .mb { background: #fff; border-radius: 20px; width: 100%; max-width: 750px; max-height: 90vh; overflow-y: auto; position: relative; }
        .mh { padding: 25px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; background: #fff; z-index: 10; }
        .mh h3 { font-size: 1.3rem; font-weight: 800; }
        .mbody { padding: 25px; }
        .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 25px; }
        .stat-card { border: 1px solid #eee; padding: 20px; border-radius: 15px; background: #fafafa; }
        .stat-card div:first-child { font-size: .75rem; color: #888; font-weight: 700; text-transform: uppercase; margin-bottom: 5px; }
        .stat-val { font-size: 1.6rem; font-weight: 800; }
        .prog-row { display: flex; align-items: center; gap: 15px; margin-bottom: 12px; }
        .prog-label { width: 80px; font-size: .85rem; font-weight: 700; }
        .prog-bar-bg { flex: 1; height: 10px; background: #eee; border-radius: 5px; overflow: hidden; }
        .prog-bar-fill { height: 100%; border-radius: 5px; }
        .prog-val { width: 60px; text-align: right; font-weight: 800; font-size: .85rem; }
        .dh-row { display: flex; justify-content: space-between; align-items: center; padding: 15px 0; border-bottom: 1px solid #f0f0f0; }
    </style>
</head>
<body>

    <!-- LOGIN SCREEN -->
    <div id="loginPage">
        <div class="lw">
            <div class="lb">
                <h2>PrintLab Outlet</h2>
                <p>Sign in to manage your shop</p>
                <input class="fi" type="email" id="userEmail" placeholder="admin@altprint.in" value="admin@altprint.in">
                <input class="fi" type="password" id="userPass" placeholder="Password" value="AltPrint2024!">
                <button class="lpb" onclick="handleLogin()">Sign In</button>
                <div id="loginError" style="color:#e84c1e; font-size:.8rem; margin-top:15px; text-align:center; font-weight:700;"></div>
            </div>
        </div>
    </div>

    <!-- MAIN DASHBOARD -->
    <div id="mainPage" class="hidden">
        <div class="tb">
            <div class="tbl">
                <div class="si" onclick="toggleMenu('sdrop')">🖨️
                    <div id="sdrop" class="sdrop hidden">
                        <div class="si-item" onclick="openPopup('logMo')">🚚 Logistics</div>
                        <div class="si-item" onclick="openPopup('setMo')">⚙️ Settings</div>
                        <div class="si-item" onclick="handleLogout()" style="color:#e84c1e;">➔ Logout</div>
                    </div>
                </div>
                <div><div class="sn">Print Lab Koramangala</div><div class="ss">Dashboard</div></div>
            </div>
            <div class="tbr">
                <button class="btn" onclick="openPopup('delMo')">👥 Delivery Team</button>
                <button class="btn" onclick="openPerformance()">📊 Performance Status</button>
                <button class="btn tbtn" onclick="toggleMenu('tdrop')">🎫 Ticket Raise ▼
                    <div id="tdrop" class="tdrop hidden">
                        <div class="ti" onclick="alert('Ticket Raised')">👤 Customer Ticket</div>
                        <div class="ti" onclick="alert('Ticket Raised')">📦 Stock Ticket</div>
                        <div class="ti" onclick="alert('Ticket Raised')">🛠️ Technical Issue</div>
                    </div>
                </button>
            </div>
        </div>
        <div class="ct">
            <div class="jp">
                <div class="jh">
                    <h2>Active Jobs</h2>
                    <div class="tt">
                        <button class="t on">All</button>
                        <button class="t">B/W</button>
                        <button class="t">Colour</button>
                    </div>
                </div>
                <div class="jc" id="jobsContainer">No active jobs found.</div>
            </div>
        </div>
    </div>

    <!-- PERFORMANCE MODAL -->
    <div id="perfModal" class="mo hidden">
        <div class="mb">
            <div class="mh">
                <h3>Performance Status</h3>
                <button onclick="closePopup('perfModal')" style="background:none; border:none; font-size:1.5rem; cursor:pointer;">✕</button>
            </div>
            <div class="mbody">
                <div class="stats-grid" id="perfStats"></div>
                <h4 style="margin-bottom:15px; font-size:.9rem;">Earnings by Print Type (Today)</h4>
                <div id="perfBars"></div>
                
                <hr style="margin:25px 0; border:none; border-top:1px solid #eee;">
                
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                    <h3 style="font-size:1.1rem;">Sales History</h3>
                    <select id="graphFilter" onchange="renderGraph()" style="padding:5px; border-radius:5px;">
                        <option value="all">All Types</option>
                        <option value="Bw">B/W</option>
                        <option value="Colour">Colour</option>
                    </select>
                </div>
                <canvas id="salesChart" height="150"></canvas>
                
                <h4 style="margin:25px 0 10px; font-size:.9rem;">Daily History</h4>
                <div id="historyList"></div>
            </div>
        </div>
    </div>

    <!-- SIMPLE MODALS -->
    <div id="logMo" class="mo hidden"><div class="mb"><div class="mh"><h3>Logistics</h3><button onclick="closePopup('logMo')">✕</button></div><div class="mbody">Logistics data coming soon.</div></div></div>
    <div id="setMo" class="mo hidden"><div class="mb"><div class="mh"><h3>Settings</h3><button onclick="closePopup('setMo')">✕</button></div><div class="mbody">Shop Settings coming soon.</div></div></div>
    <div id="delMo" class="mo hidden"><div class="mb"><div class="mh"><h3>Delivery Team</h3><button onclick="closePopup('delMo')">✕</button></div><div class="mbody">Agent list coming soon.</div></div></div>

    <script>
        const API_BASE = window.location.origin;
        let token = localStorage.getItem('pl_s');
        let orderData = [];
        let myChart = null;
        const CAT_COLORS = { Bw: '#3b82f6', Colour: '#f97316', Photo: '#10b981', Tshirt: '#8b5cf6', Project: '#ef4444' };
        const MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

        // Init
        if (token) {
            document.getElementById('loginPage').classList.add('hidden');
            document.getElementById('mainPage').classList.remove('hidden');
            fetchOrders();
        }

        async function handleLogin() {
            const email = document.getElementById('userEmail').value;
            const pass = document.getElementById('userPass').value;
            const err = document.getElementById('loginError');
            err.textContent = "Checking...";

            try {
                const res = await fetch(API_BASE + '/api/v1/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: email, password: pass })
                });
                const data = await res.json();
                if (data.access_token) {
                    localStorage.setItem('pl_s', data.access_token);
                    window.location.reload();
                } else {
                    err.textContent = "Invalid Credentials";
                }
            } catch (e) {
                err.textContent = "Backend Offline";
            }
        }

        async function fetchOrders() {
            try {
                const res = await fetch(API_BASE + '/api/v1/orders', {
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                const data = await res.json();
                orderData = Array.isArray(data) ? data : (data.orders || []);
                renderJobs();
            } catch (e) { console.error("Fetch failed", e); }
        }

        function renderJobs() {
            const container = document.getElementById('jobsContainer');
            if (orderData.length === 0) return;
            
            let html = '<table style="width:100%; border-collapse:collapse;">';
            html += '<tr style="text-align:left; color:#888; font-size:.7rem; text-transform:uppercase;"><th style="padding:15px;">Order</th><th>Customer</th><th>Document</th><th>Status</th></tr>';
            orderData.slice(0,5).forEach(o => {
                html += `<tr style="border-top:1px solid #eee;">
                    <td style="padding:15px; font-weight:800; color:#e84c1e;">#${o.order_number || '000'}</td>
                    <td style="font-weight:700;">${o.user_name || 'Keerthi'}<br><small style="color:#999;">${o.user_phone || '9876...'}</small></td>
                    <td style="font-size:.85rem;">${o.file_name || 'document.pdf'}</td>
                    <td><span style="background:#fff3e0; color:#e65100; padding:4px 10px; border-radius:15px; font-size:.7rem; font-weight:800;">${o.status}</span></td>
                </tr>`;
            });
            container.innerHTML = html + '</table>';
        }

        function openPerformance() {
            openPopup('perfModal');
            
            // Calc stats
            document.getElementById('perfStats').innerHTML = `
                <div class="stat-card"><div>Total Orders</div><div class="stat-val">${orderData.length}</div></div>
                <div class="stat-card"><div>Pending</div><div class="stat-val" style="color:orange;">${orderData.filter(o=>o.status=='pending').length}</div></div>
                <div class="stat-card"><div>Processing</div><div class="stat-val" style="color:blue;">${orderData.filter(o=>o.status=='confirmed').length}</div></div>
                <div class="stat-card"><div>Delivered</div><div class="stat-val" style="color:green;">${orderData.filter(o=>o.status=='delivered').length}</div></div>
            `;

            // Today's bars (Example logic)
            document.getElementById('perfBars').innerHTML = Object.keys(CAT_COLORS).map(k => `
                <div class="prog-row">
                    <div class="prog-label">${k}</div>
                    <div class="prog-bar-bg"><div class="prog-bar-fill" style="width:40%; background:${CAT_COLORS[k]};"></div></div>
                    <div class="prog-val" style="color:${CAT_COLORS[k]};">Rs 500</div>
                </div>
            `).join('');

            renderGraph();
        }

        function renderGraph() {
            const filter = document.getElementById('graphFilter').value;
            const ctx = document.getElementById('salesChart').getContext('2d');
            const labels = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7", "Today"];
            const data = [1200, 1900, 800, 1500, 2200, 3000, 2500, 3850];

            if (myChart) myChart.destroy();
            myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        data: data,
                        backgroundColor: filter == 'all' ? '#1a1a1a' : CAT_COLORS[filter] || '#1a1a1a',
                        borderRadius: 5
                    }]
                },
                options: { plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } }
            });

            // History List
            document.getElementById('historyList').innerHTML = labels.reverse().map((l, i) => `
                <div class="dh-row">
                    <div>
                        <div style="font-weight:800;">${l} <small style="color:#aaa; font-weight:400; margin-left:10px;">16 Jun</small></div>
                        <div style="margin-top:5px; font-size:.7rem; color:#666;">
                            <span style="margin-right:10px;"><span style="color:${CAT_COLORS.Bw}">●</span> Bw Rs200</span>
                            <span style="margin-right:10px;"><span style="color:${CAT_COLORS.Colour}">●</span> Colour Rs500</span>
                        </div>
                    </div>
                    <div style="font-weight:900;">Rs 3,850</div>
                </div>
            `).join('');
        }

        function toggleMenu(id) { document.getElementById(id).classList.toggle('hidden'); }
        function openPopup(id) { document.getElementById(id).classList.remove('hidden'); }
        function closePopup(id) { document.getElementById(id).classList.add('hidden'); }
        function handleLogout() { localStorage.removeItem('pl_s'); window.location.reload(); }
        
        window.onclick = function(event) {
            if (!event.target.closest('.si') && !event.target.closest('.tbtn')) {
                document.getElementById('sdrop').classList.add('hidden');
                document.getElementById('tdrop').classList.add('hidden');
            }
        }
    </script>
</body>
</html>"""

with open(path, 'w', encoding='utf-8') as f:
    f.write(html_content)
print("SUCCESS: Brand-new specific_control.html written!")
