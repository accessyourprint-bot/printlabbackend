html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PrintLab Admin</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"Segoe UI",system-ui,-apple-system,sans-serif;background:#f5f6f8;color:#1a223e;min-height:100vh}
.lw{display:flex;align-items:center;justify-content:center;min-height:100vh;background:#1a223e}
.lb{background:#fff;border-radius:16px;padding:40px;width:360px;box-shadow:0 20px 60px rgba(0,0,0,.3)}
.lb h2{font-size:1.35rem;font-weight:800;color:#1a223e;margin-bottom:4px}
.lb p{color:#666;font-size:.9rem;margin-bottom:28px}
.fil{display:block;font-size:.82rem;font-weight:600;color:#444;margin-bottom:6px}
.fi{width:100%;padding:12px 14px;border:1.5px solid #e0e0e0;border-radius:10px;font-size:.95rem;margin-bottom:16px;font-family:inherit}
.fi:focus{outline:none;border-color:#ff5722}
.lpb{width:100%;padding:13px;background:#ff5722;color:#fff;border:none;border-radius:10px;font-size:1rem;font-weight:700;cursor:pointer}
.lerr{color:#ff5722;font-size:.85rem;margin-top:10px;text-align:center}
.topbar{background:#fff;border-bottom:1.5px solid #e8e8ec;padding:0 28px;height:58px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100}
.tb-left{display:flex;align-items:center;gap:12px}
.logo{display:flex;align-items:center;gap:8px}
.logo-box{width:34px;height:34px;background:#ff5722;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:.9rem}
.logo-text{font-weight:800;font-size:1.05rem;color:#1a223e}
.sep{color:#ccc;margin:0 4px}
.crumb-link{color:#999;font-size:.88rem;cursor:pointer}
.crumb-link:hover{color:#ff5722}
.crumb-cur{font-weight:700;font-size:.95rem;color:#1a223e}
.admin-btn{background:#1a223e;color:#fff;border:none;border-radius:8px;padding:7px 16px;font-size:.82rem;font-weight:600;cursor:pointer;display:flex;align-items:center;gap:6px}
.content{padding:28px;max-width:1200px;margin:0 auto}
.live-banner{background:#1a223e;border-radius:12px;padding:18px 24px;display:flex;justify-content:space-between;align-items:center;margin-bottom:28px;cursor:pointer;transition:.15s}
.live-banner:hover{background:#222d44}
.live-left{display:flex;align-items:center;gap:14px}
.live-dot{display:flex;align-items:center;gap:5px;color:#ff5252;font-size:.78rem;font-weight:800;letter-spacing:.6px;flex-shrink:0}
.live-dot::before{content:'';width:8px;height:8px;background:#ff5252;border-radius:50%;display:inline-block;animation:pulse 1.5s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
.live-info h3{color:#fff;font-size:1rem;font-weight:700;margin-bottom:3px}
.live-info p{color:#aab2c5;font-size:.8rem}
.live-link{color:#ff7043;font-size:.88rem;font-weight:600}
.sec-label{font-size:.72rem;font-weight:800;color:#999;letter-spacing:.8px;margin-bottom:14px;margin-top:24px;text-transform:uppercase}
.sec-label:first-child{margin-top:0}
.card-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:0}
.card{background:#fff;border:1.5px solid #ebebee;border-radius:12px;padding:22px;cursor:pointer;transition:.15s}
.card:hover{border-color:#ff5722;box-shadow:0 4px 16px rgba(255,87,34,.08);transform:translateY(-1px)}
.card-icon{width:40px;height:40px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.15rem;margin-bottom:14px;color:#fff}
.card h3{font-size:1rem;font-weight:800;margin-bottom:5px;color:#1a223e}
.card p{font-size:.8rem;color:#888;line-height:1.4;margin-bottom:14px;min-height:34px}
.card-open{font-size:.82rem;font-weight:700;color:#ff5722}
.card-warn{background:#fff4f0;border:1.5px solid #ffccc0}
.panel{background:#fff;border-radius:12px;border:1.5px solid #ebebee;overflow:hidden;margin-bottom:16px}
.panel-hd{padding:16px 20px;border-bottom:1px solid #f0f0f3;font-weight:800;font-size:.95rem;display:flex;align-items:center;gap:8px;justify-content:space-between}
table{width:100%;border-collapse:collapse}
th{padding:12px 20px;text-align:left;font-size:.74rem;font-weight:700;color:#999;text-transform:uppercase;letter-spacing:.4px;border-bottom:1.5px solid #f0f0f3}
td{padding:14px 20px;border-bottom:1px solid #f5f5f8;font-size:.88rem}
tr:last-child td{border-bottom:none}
tr:hover td{background:#fafafc}
.uid{color:#ff5722;font-size:.82rem;font-weight:600}
.badge{display:inline-block;padding:4px 12px;border-radius:6px;font-size:.74rem;font-weight:700}
.b-dark{background:#1a223e;color:#fff}
.b-orange{background:#fff3e0;color:#e65100}
.b-green{background:#e8f5e9;color:#2e7d32}
.b-red{background:#ffebee;color:#c62828}
.b-blue{background:#e3f2fd;color:#1565c0}
.b-purple{background:#f3e5f5;color:#7b1fa2}
.b-yellow{background:#fffde7;color:#f9a825}
.btn-sm{padding:8px 16px;border-radius:8px;font-size:.82rem;font-weight:700;cursor:pointer;border:1.5px solid #e0e0e0;background:#fff;font-family:inherit}
.btn-orange{background:#ff5722;color:#fff;border:none}
.btn-red{background:#e74c3c;color:#fff;border:none}
.btn-green{background:#27ae60;color:#fff;border:none}
.btn-full{width:100%;padding:13px;background:#ff5722;color:#fff;border:none;border-radius:10px;font-size:.95rem;font-weight:700;cursor:pointer;font-family:inherit}
.icon-del{background:#e74c3c;color:#fff;border:none;border-radius:6px;width:32px;height:32px;cursor:pointer;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:1rem}
.stat-row{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:20px;margin-top:20px}
.stat-box{background:#fff;border:1.5px solid #ebebee;border-radius:12px;padding:24px;text-align:center}
.stat-num{font-size:2.4rem;font-weight:800;margin-bottom:4px}
.stat-lbl{font-size:.85rem;color:#888;font-weight:600}
.stat-num.green{color:#1b7a3d}
.stat-num.orange{color:#ff5722}
.stat-num.dark{color:#1a223e}
.total-box{background:#1a223e;border-radius:12px;padding:24px 28px;display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;margin-top:20px}
.total-box .lbl{color:#9aa3b8;font-size:.78rem;font-weight:700;letter-spacing:.5px;margin-bottom:6px}
.total-box .val{color:#fff;font-size:2.2rem;font-weight:800}
.total-box .sub{color:#9aa3b8;font-size:.85rem;margin-top:4px}
.total-icon{width:50px;height:50px;background:rgba(255,255,255,.1);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.4rem;color:#ff7043}
.form-panel{background:#fff;border-radius:12px;border:1.5px solid #ebebee;padding:24px}
.form-panel h3{font-size:1rem;font-weight:800;margin-bottom:20px;color:#1a223e;display:flex;align-items:center;gap:8px}
.fg{margin-bottom:16px}
.fg label{display:block;font-size:.82rem;font-weight:700;color:#444;margin-bottom:6px}
.fg input,.fg select,.fg textarea{width:100%;padding:12px 14px;border:1.5px solid #e0e0e0;border-radius:10px;font-size:.9rem;font-family:inherit}
.fg input:focus,.fg select:focus,.fg textarea:focus{outline:none;border-color:#ff5722}
.two-col{display:grid;grid-template-columns:380px 1fr;gap:20px;align-items:start}
.tab-row{display:flex;gap:8px;margin-bottom:18px}
.tab-btn{padding:10px 20px;border:1.5px solid #e0e0e0;background:#fff;border-radius:8px;cursor:pointer;font-size:.88rem;font-weight:700;font-family:inherit;color:#555;display:flex;align-items:center;gap:6px}
.tab-btn.on{background:#ff5722;color:#fff;border-color:#ff5722}
.dp-card{border:1.5px solid #ebebee;border-radius:10px;padding:16px 20px;margin-bottom:10px;display:flex;justify-content:space-between;align-items:flex-start}
.dp-name{font-weight:800;font-size:.95rem;margin-bottom:3px}
.dp-meta{font-size:.82rem;color:#888;margin-bottom:3px}
.dp-docs{font-size:.78rem;color:#aaa}
.ticket-item{display:flex;justify-content:space-between;align-items:flex-start;padding:16px 20px;border-bottom:1px solid #f5f5f8}
.ticket-title{display:flex;align-items:center;gap:8px;margin-bottom:4px;font-weight:700;font-size:.92rem}
.ticket-meta{font-size:.78rem;color:#aaa;margin-bottom:6px}
.ticket-desc{font-size:.85rem;color:#555}
.appctrl-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.color-row{display:flex;align-items:center;gap:10px}
.color-swatch{width:42px;height:42px;border-radius:8px;flex-shrink:0;border:1.5px solid #e0e0e0}
.font-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.font-btn{padding:10px;border:1.5px solid #e0e0e0;background:#fff;border-radius:7px;cursor:pointer;font-size:.82rem;font-weight:600;text-align:center;font-family:inherit;color:#555}
.font-btn.on{background:#ff5722;color:#fff;border-color:#ff5722}
.preview-box{background:#fff;border-radius:12px;border:1.5px solid #ebebee;overflow:hidden}
.preview-top{background:#1a223e;color:#fff;padding:12px 16px;display:flex;align-items:center;justify-content:space-between}
.preview-top-logo{display:flex;align-items:center;gap:7px;font-weight:800}
.plogo{width:28px;height:28px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:.8rem;font-weight:800;color:#fff}
.preview-admin{border:1px solid #555;border-radius:5px;padding:2px 10px;font-size:.76rem}
.preview-banner{padding:10px 16px;color:#fff;font-weight:700;font-size:.9rem}
.preview-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;padding:16px}
.preview-card{border:1px solid #eee;border-radius:8px;padding:14px 8px;text-align:center}
.picon{width:28px;height:28px;border-radius:6px;margin:0 auto 8px;display:block}
.preview-card span{font-size:.76rem;color:#666}
.warn-box{background:#fff4f0;border:1.5px solid #ffd9cc;border-radius:10px;padding:14px 18px;margin:20px 0;font-size:.88rem;color:#a14a1f;display:flex;align-items:center;gap:10px}
.empty{text-align:center;padding:40px;color:#aaa;font-size:.9rem}
.loading{text-align:center;padding:36px;color:#ff5722}
.hidden{display:none!important}
canvas{width:100%!important}
@media(max-width:900px){
.card-grid{grid-template-columns:1fr 1fr}
.two-col{grid-template-columns:1fr}
.appctrl-grid{grid-template-columns:1fr}
.stat-row{grid-template-columns:1fr}
}
@media(max-width:600px){
.card-grid{grid-template-columns:1fr}
}
</style>
</head>
<body>
<div id="lw"><div class="lw"><div class="lb">
<h2>PrintLab Admin</h2>
<p>Owner Access — Command Center</p>
<label class="fil">Email</label>
<input class="fi" type="email" id="em" value="admin@altprint.in">
<label class="fil">Password</label>
<input class="fi" type="password" id="pw" value="AltPrint2024!">
<button class="lpb" onclick="doLogin()">Sign In</button>
<div class="lerr" id="lerr"></div>
</div></div></div>
<div id="appWrap" class="hidden">
<div class="topbar">
<div class="tb-left">
<div class="logo"><div class="logo-box">PL</div><span class="logo-text">PrintLab</span></div>
<span class="sep" id="cSep" style="display:none">|</span>
<span class="crumb-link" id="cDash" style="display:none" onclick="goDash()">&larr; Dashboard</span>
<span class="crumb-cur" id="cTitle"></span>
</div>
<button class="admin-btn" onclick="doLogout()">&#9881; Admin</button>
</div>
<div class="content">
<div id="pg-dash">
<div class="live-banner" onclick="openPage('liveprint')">
<div class="live-left">
<span class="live-dot">LIVE</span>
<div class="live-info"><h3>Live Print Update</h3><p id="liveSub">Loading...</p></div>
</div>
<span class="live-link">View All &rarr;</span>
</div>
<div class="sec-label">Print &amp; Payments</div>
<div class="card-grid">
<div class="card" onclick="openPage('printdone')"><div class="card-icon" style="background:#22b573">&#10003;</div><h3>Print Done</h3><p>View all completed print jobs and product updates.</p><div class="card-open">Open &rarr;</div></div>
<div class="card" onclick="openPage('paymentday')"><div class="card-icon" style="background:#ff5722">&#128179;</div><h3>Payment for Day</h3><p>Today's sales and payment records.</p><div class="card-open">Open &rarr;</div></div>
<div class="card" onclick="openPage('paymenthist')"><div class="card-icon" style="background:#2979ff">&#128200;</div><h3>Payment History</h3><p>Weekly/daily revenue graph and user-wise breakdown.</p><div class="card-open">Open &rarr;</div></div>
</div>
<div class="sec-label">Operations</div>
<div class="card-grid">
<div class="card" onclick="openPage('delivery')"><div class="card-icon" style="background:#ff7043">&#128666;</div><h3>Delivery Person</h3><p>Manage delivery staff — name, photo, Aadhar, PAN, vehicle.</p><div class="card-open">Open &rarr;</div></div>
<div class="card" onclick="openPage('customer')"><div class="card-icon" style="background:#8e44ad">&#128100;</div><h3>Customer Account</h3><p>View and manage customer IDs and phone numbers.</p><div class="card-open">Open &rarr;</div></div>
<div class="card" onclick="openPage('outlet')"><div class="card-icon" style="background:#16a085">&#127970;</div><h3>Outlet Account</h3><p>Zone-wise outlet map with own and franchise filters.</p><div class="card-open">Open &rarr;</div></div>
</div>
<div class="sec-label">Management</div>
<div class="card-grid">
<div class="card" onclick="openPage('subadmin')"><div class="card-icon" style="background:#3f51b5">&#128101;</div><h3>Sub-Admin Management</h3><p>Create and manage sub-admin accounts with roles.</p><div class="card-open">Open &rarr;</div></div>
<div class="card" onclick="openPage('accountmgmt')"><div class="card-icon" style="background:#607d8b">&#128275;</div><h3>Account Management</h3><p>Securely suspend or reinstate customer accounts.</p><div class="card-open">Open &rarr;</div></div>
<div class="card" onclick="openPage('ticket')"><div class="card-icon" style="background:#e91e63">&#127991;</div><h3>Ticket</h3><p>Customer and outlet complaint management system.</p><div class="card-open">Open &rarr;</div></div>
<div class="card" onclick="openPage('stock')"><div class="card-icon" style="background:#d4a017">&#128230;</div><h3>Stock Management</h3><p>View stock levels and track related complaint tickets.</p><div class="card-open">Open &rarr;</div></div>
</div>
<div class="sec-label">&nbsp;</div>
<div class="card card-warn" style="display:flex;align-items:center;justify-content:space-between;cursor:pointer" onclick="openPage('appcontrol')">
<div style="display:flex;align-items:center;gap:14px">
<div class="card-icon" style="background:#ff5722;margin-bottom:0">&#128295;</div>
<div><h3 style="margin-bottom:2px">App Control</h3><p style="min-height:0;margin-bottom:0">Manage colors, fonts, images / frontend settings</p></div>
</div>
<div class="card-open">Configure &rarr;</div>
</div>
</div>
<div id="pg-liveprint" class="hidden">
<div style="display:flex;align-items:center;gap:20px;margin:20px 0 16px">
<span class="live-dot">LIVE</span>
<span style="font-weight:700"><b id="lpInProg">0</b> In Progress</span>
<span style="font-weight:700"><b id="lpDone">0</b> Done Today</span>
</div>
<div class="panel"><div class="panel-hd">&#9889; Currently In Progress (<span id="lpCount">0</span>)</div><div id="lpTable"><div class="loading">Loading...</div></div></div>
</div>
<div id="pg-printdone" class="hidden">
<div class="stat-row">
<div class="stat-box"><div class="stat-num green" id="pdTotal">0</div><div class="stat-lbl">Total Done</div></div>
<div class="stat-box"><div class="stat-num orange" id="pdInProg">0</div><div class="stat-lbl">In Progress</div></div>
<div class="stat-box"><div class="stat-num dark" id="pdToday">0</div><div class="stat-lbl">Total Today</div></div>
</div>
<div class="panel"><div class="panel-hd">&#10003; Completed Jobs (<span id="pdCount">0</span>)</div><div id="pdTable"><div class="loading">Loading...</div></div></div>
</div>
<div id="pg-paymentday" class="hidden">
<div class="total-box" style="margin-top:20px">
<div><div class="lbl">TODAY'S TOTAL</div><div class="val">&#8377; <span id="pdayTotal">0.00</span></div><div class="sub" id="pdayCount">0 transactions</div></div>
<div class="total-icon">&#128179;</div>
</div>
<div class="panel"><div class="panel-hd">Transaction Log</div><div id="pdayTable"><div class="loading">Loading...</div></div></div>
</div>
<div id="pg-paymenthist" class="hidden">
<div class="panel" style="margin-top:20px;padding:20px"><div style="font-weight:800;font-size:1rem;margin-bottom:14px">Revenue Overview</div><canvas id="revChart" height="100"></canvas></div>
<div id="phWeeks" style="margin-top:16px"></div>
</div>
<div id="pg-delivery" class="hidden">
<div class="two-col" style="margin-top:20px">
<div class="form-panel"><h3>&#128666; Add Delivery Person</h3>
<div class="fg"><label>Name</label><input id="dpName" placeholder="Full name"></div>
<div class="fg"><label>Age</label><input id="dpAge" type="number" placeholder="Age"></div>
<div class="fg"><label>Phone Number</label><input id="dpPhone" placeholder="+91 XXXXX XXXXX"></div>
<div class="fg"><label>Aadhar Number</label><input id="dpAadhar" placeholder="XXXX XXXX XXXX"></div>
<div class="fg"><label>PAN Number</label><input id="dpPan" placeholder="ABCDE1234F"></div>
<div class="fg"><label>Vehicle Number</label><input id="dpVehicle" placeholder="TN XX XX XXXX"></div>
<button class="btn-full" onclick="addDelivery()">+ Add Person</button>
</div>
<div class="panel"><div class="panel-hd">Delivery Staff (<span id="dpCount">0</span>)</div><div id="dpList" style="padding:16px"><div class="loading">Loading...</div></div></div>
</div>
</div>
<div id="pg-customer" class="hidden">
<div class="two-col" style="margin-top:20px">
<div class="form-panel"><h3>&#128100; Add Customer</h3>
<div class="fg"><label>User ID</label><input id="cuId" placeholder="e.g. CUS001"></div>
<div class="fg"><label>Name</label><input id="cuName" placeholder="Full name"></div>
<div class="fg"><label>Phone Number</label><input id="cuPhone" placeholder="+91 XXXXX XXXXX"></div>
<button class="btn-full" onclick="addCustomer()">+ Add Customer</button>
</div>
<div class="panel"><div class="panel-hd">All Customers (<span id="cuCount">0</span>)</div><div id="cuTable"><div class="loading">Loading...</div></div></div>
</div>
</div>
<div id="pg-outlet" class="hidden">
<div class="tab-row" style="margin:20px 0 16px">
<button class="tab-btn on" onclick="filterOutlets('all',this)">&#127970; All Outlets</button>
<button class="tab-btn" onclick="filterOutlets('own',this)">&#128274; Own Outlet</button>
<button class="tab-btn" onclick="filterOutlets('franchise',this)">&#127942; Franchise Outlet</button>
</div>
<div class="two-col">
<div class="form-panel"><h3>&#127970; Add Outlet</h3>
<div class="fg"><label>Zone</label><input id="otZone" placeholder="e.g. North Chennai"></div>
<div class="fg"><label>Pincode</label><input id="otPin" placeholder="600001"></div>
<div class="fg"><label>Owner Name</label><input id="otOwner" placeholder="Owner's name"></div>
<div class="fg"><label>User ID</label><input id="otId" placeholder="e.g. OUT001"></div>
<div class="fg"><label>Type</label><div style="display:flex;gap:8px"><button class="tab-btn on" id="otTypeOwn" onclick="setOtType('own')" style="flex:1">Own</button><button class="tab-btn" id="otTypeFr" onclick="setOtType('franchise')" style="flex:1">Franchise</button></div></div>
<button class="btn-full" onclick="addOutlet()">+ Add Outlet</button>
</div>
<div class="panel"><div class="panel-hd">Outlets (<span id="otCount">0</span>)</div><div id="otTable"><div class="loading">Loading...</div></div></div>
</div>
</div>
<div id="pg-subadmin" class="hidden">
<div class="two-col" style="margin-top:20px">
<div class="form-panel"><h3>&#128101; Add Sub-Admin</h3>
<div class="fg"><label>User ID</label><input id="saId" placeholder="e.g. SA001"></div>
<div class="fg"><label>Name</label><input id="saName" placeholder="Full name"></div>
<div class="fg"><label>Password</label><input id="saPass" type="password" placeholder="Set password"></div>
<div class="fg"><label>Role</label><input id="saRole" value="sub-admin"></div>
<button class="btn-full" onclick="addSubAdmin()">+ Add Sub-Admin</button>
</div>
<div class="panel"><div class="panel-hd">Sub-Admins (<span id="saCount">0</span>)</div><div id="saTable"><div class="loading">Loading...</div></div></div>
</div>
</div>
<div id="pg-accountmgmt" class="hidden">
<div class="warn-box" style="margin-top:20px">&#9888; Manage customer accounts securely. Suspend or reactivate access from here.</div>
<div class="panel"><div class="panel-hd">Customer Accounts (<span id="amCount">0</span>)</div><div id="amTable"><div class="loading">Loading...</div></div></div>
</div>
<div id="pg-ticket" class="hidden">
<div style="display:flex;justify-content:space-between;align-items:center;margin:20px 0 16px">
<div class="tab-row" style="margin:0">
<button class="tab-btn on" onclick="filterTickets('customer',this)">&#128100; Customer Complaint</button>
<button class="tab-btn" onclick="filterTickets('outlet',this)">&#127970; Outlet Complaint</button>
</div>
<button class="btn-sm btn-orange" onclick="alert('Raise Ticket - POST /api/v1/tickets')">+ Raise Ticket</button>
</div>
<div class="panel"><div class="panel-hd" id="tkHd">Customer Complaints (<span id="tkCount">0</span>)</div><div id="tkList"><div class="loading">Loading...</div></div></div>
</div>
<div id="pg-stock" class="hidden">
<div class="two-col" style="margin-top:20px">
<div class="panel"><div class="panel-hd">&#128230; Stock Inventory (<span id="skCount">0</span> items)</div><div id="skTable"><div class="loading">Loading...</div></div></div>
<div class="panel"><div class="panel-hd">&#9888; Open Tickets (<span id="skTkCount">0</span>)</div><div id="skTickets" style="padding:14px"><div class="loading">Loading...</div></div></div>
</div>
</div>
<div id="pg-appcontrol" class="hidden">
<div class="appctrl-grid" style="margin-top:20px">
<div class="form-panel"><h3>&#128736; Frontend Settings</h3>
<div class="fg"><label>Primary Color</label><div class="color-row"><div class="color-swatch" id="acPrimSw" style="background:#ff5722"></div><input id="acPrim" value="#ff5722" oninput="updatePreview()"></div></div>
<div class="fg"><label>Secondary Color</label><div class="color-row"><div class="color-swatch" id="acSecSw" style="background:#1a223e"></div><input id="acSec" value="#1a223e" oninput="updatePreview()"></div></div>
<div class="fg"><label>Font Family</label><div class="font-grid" id="acFonts">
<button class="font-btn on" onclick="setFont('Inter',this)">Inter</button>
<button class="font-btn" onclick="setFont('Roboto',this)">Roboto</button>
<button class="font-btn" onclick="setFont('Poppins',this)">Poppins</button>
<button class="font-btn" onclick="setFont('Montserrat',this)">Montserrat</button>
<button class="font-btn" onclick="setFont('Open Sans',this)">Open Sans</button>
<button class="font-btn" onclick="setFont('Lato',this)">Lato</button>
</div></div>
<div class="fg"><label>Logo URL</label><input id="acLogo" placeholder="https://example.com/logo.png" oninput="updatePreview()"></div>
<div class="fg"><label>Banner Text</label><input id="acBanner" value="PrintLab Admin" oninput="updatePreview()"></div>
<button class="btn-full" onclick="saveAppSettings()">&#128190; Save Settings</button>
</div>
<div><div class="form-panel"><h3>&#128248; Live Preview</h3>
<div class="preview-box">
<div class="preview-top"><div class="preview-top-logo"><div class="plogo" id="prevLogo" style="background:#ff5722">PL</div>PrintLab</div><span class="preview-admin">Admin</span></div>
<div class="preview-banner" id="prevBanner" style="background:#ff5722">PrintLab Admin</div>
<div class="preview-cards">
<div class="preview-card"><div class="picon" id="prevIc1" style="background:#ff5722"></div><span>Print Done</span></div>
<div class="preview-card"><div class="picon" id="prevIc2" style="background:#ff5722"></div><span>Payments</span></div>
<div class="preview-card"><div class="picon" id="prevIc3" style="background:#ff5722"></div><span>Delivery</span></div>
</div>
<p style="text-align:center;color:#aaa;font-size:.76rem;padding:8px 16px 14px">Preview updates as you type</p>
</div></div></div>
</div>
</div>
</div></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script>
const API='http://127.0.0.1:8001';
let tok=localStorage.getItem('pl_full');
let revChartObj=null;
let allOutlets=[],allTickets=[],allCustomers=[],allSubAdmins=[],allStock=[];
let curOtType='own',curTkFilter='customer';
if(tok) initApp();
async function doLogin(){
  try{
    const r=await fetch(API+'/api/v1/auth/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:document.getElementById('em').value,password:document.getElementById('pw').value})});
    const d=await r.json();
    if(d.access_token){tok=d.access_token;localStorage.setItem('pl_full',tok);initApp();}
    else document.getElementById('lerr').textContent='Invalid credentials';
  }catch(e){document.getElementById('lerr').textContent='Cannot connect';}
}
function doLogout(){localStorage.removeItem('pl_full');location.reload();}
function initApp(){
  document.getElementById('lw').classList.add('hidden');
  document.getElementById('appWrap').classList.remove('hidden');
  loadDashSummary();
}
async function api(u,m,b){
  const o={method:m||'GET',headers:{Authorization:'Bearer '+tok}};
  if(b){o.headers['Content-Type']='application/json';o.body=JSON.stringify(b);}
  try{const r=await fetch(API+u,o);return await r.json();}catch(e){return null;}
}
function fmtDate(d){try{return new Date(d).toLocaleDateString('en-GB');}catch(e){return'—';}}
function fmtTime(d){try{return new Date(d).toLocaleString('en-GB',{hour:'2-digit',minute:'2-digit',hour12:true});}catch(e){return'—';}}
const PAGE_TITLES={
  liveprint:'Live Print Update',printdone:'Print Done',paymentday:'Payment for Day',
  paymenthist:'Payment History',delivery:'Delivery Person',customer:'Customer Account',
  outlet:'Outlet Account',subadmin:'Sub-Admin Management',accountmgmt:'Account Management',
  ticket:'Ticket Management',stock:'Stock Management',appcontrol:'App Control'
};
function openPage(id){
  document.querySelectorAll('[id^="pg-"]').forEach(p=>p.classList.add('hidden'));
  document.getElementById('pg-'+id).classList.remove('hidden');
  document.getElementById('cSep').style.display='inline';
  document.getElementById('cDash').style.display='inline';
  document.getElementById('cTitle').textContent=PAGE_TITLES[id]||'';
  const loaders={liveprint:loadLivePrint,printdone:loadPrintDone,paymentday:loadPaymentDay,
    paymenthist:loadPaymentHist,delivery:loadDelivery,customer:loadCustomers,
    outlet:loadOutlets,subadmin:loadSubAdmins,accountmgmt:loadAccountMgmt,
    ticket:loadTickets,stock:loadStock,appcontrol:loadAppControl};
  if(loaders[id]) loaders[id]();
}
function goDash(){
  document.querySelectorAll('[id^="pg-"]').forEach(p=>p.classList.add('hidden'));
  document.getElementById('pg-dash').classList.remove('hidden');
  document.getElementById('cSep').style.display='none';
  document.getElementById('cDash').style.display='none';
  document.getElementById('cTitle').textContent='';
  loadDashSummary();
}
async function loadDashSummary(){
  const d=await api('/api/v1/orders');
  const orders=Array.isArray(d)?d:(d?.data||d?.orders||[]);
  const today=new Date().toDateString();
  const inProg=orders.filter(o=>o.status==='confirmed'||o.status==='printing').length;
  const doneToday=orders.filter(o=>['completed','delivered'].includes(o.status)&&new Date(o.created_at).toDateString()===today).length;
  document.getElementById('liveSub').textContent=inProg+' jobs in progress · '+doneToday+' completed today';
}
async function loadLivePrint(){
  const d=await api('/api/v1/orders');
  const orders=Array.isArray(d)?d:(d?.data||d?.orders||[]);
  const inProg=orders.filter(o=>o.status==='confirmed'||o.status==='printing');
  const today=new Date().toDateString();
  const doneToday=orders.filter(o=>['completed','delivered'].includes(o.status)&&new Date(o.created_at).toDateString()===today);
  document.getElementById('lpInProg').textContent=inProg.length;
  document.getElementById('lpDone').textContent=doneToday.length;
  document.getElementById('lpCount').textContent=inProg.length;
  document.getElementById('lpTable').innerHTML=inProg.length?
    <table><tr><th>#</th><th>User ID</th><th>Product</th><th>Qty</th><th>Status</th><th>Started</th></tr>+
    inProg.map((o,i)=><tr><td></td><td class="uid"></td><td></td><td></td><td><span class="badge b-orange">in progress</span></td><td>, </td></tr>).join('')+'</table>':
    '<div class="empty">No jobs currently in progress</div>';
}
async function loadPrintDone(){
  const d=await api('/api/v1/orders');
  const orders=Array.isArray(d)?d:(d?.data||d?.orders||[]);
  const done=orders.filter(o=>['completed','delivered'].includes(o.status));
  const inProg=orders.filter(o=>['confirmed','printing'].includes(o.status));
  const today=new Date().toDateString();
  const doneToday=done.filter(o=>new Date(o.created_at).toDateString()===today);
  document.getElementById('pdTotal').textContent=done.length;
  document.getElementById('pdInProg').textContent=inProg.length;
  document.getElementById('pdToday').textContent=doneToday.length;
  document.getElementById('pdCount').textContent=done.length;
  document.getElementById('pdTable').innerHTML=done.length?
    <table><tr><th>User ID</th><th>Product</th><th>Qty</th><th>Status</th><th>Completed</th></tr>+
    done.map((o,i)=><tr><td class="uid"></td><td></td><td></td><td><span class="badge b-green">done</span></td><td>, </td></tr>).join('')+'</table>':
    '<div class="empty">No completed jobs yet</div>';
}
async function loadPaymentDay(){
  const d=await api('/api/v1/orders');
  const orders=Array.isArray(d)?d:(d?.data||d?.orders||[]);
  const today=new Date().toDateString();
  const todays=orders.filter(o=>new Date(o.created_at).toDateString()===today);
  const total=todays.reduce((s,o)=>s+(parseFloat(o.grand_total)||0),0);
  document.getElementById('pdayTotal').textContent=total.toLocaleString('en-IN',{minimumFractionDigits:2,maximumFractionDigits:2});
  document.getElementById('pdayCount').textContent=todays.length+' transactions';
  document.getElementById('pdayTable').innerHTML=todays.length?
    <table><tr><th>User ID</th><th>Customer</th><th>Amount</th><th>Method</th><th>Time</th></tr>+
    todays.map((o,i)=><tr><td class="uid"></td><td></td><td style="color:#1b7a3d;font-weight:700">&#8377;</td><td><span class="badge b-dark"></span></td><td></td></tr>).join('')+'</table>':
    '<div class="empty">No payments today yet</div>';
}
async function loadPaymentHist(){
  const d=await api('/api/v1/orders');
  const orders=Array.isArray(d)?d:(d?.data||d?.orders||[]);
  const today=new Date();today.setHours(0,0,0,0);
  const days=Array.from({length:8},(_,i)=>{const dt=new Date(today);dt.setDate(dt.getDate()-(7-i));return dt;});
  const byDay=days.map(dt=>{const ds=dt.toDateString();const dayOrders=orders.filter(o=>new Date(o.created_at).toDateString()===ds);return{date:dt,total:dayOrders.reduce((s,o)=>s+(parseFloat(o.grand_total)||0),0),orders:dayOrders};});
  const ctx=document.getElementById('revChart').getContext('2d');
  if(revChartObj) revChartObj.destroy();
  revChartObj=new Chart(ctx,{type:'bar',data:{labels:byDay.map(d=>d.date.getDate()+' '+['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][d.date.getMonth()]),datasets:[{data:byDay.map(d=>d.total),backgroundColor:'#ff5722',borderRadius:4}]},options:{responsive:true,plugins:{legend:{display:false}},scales:{y:{ticks:{callback:v=>'&#8377;'+v},grid:{color:'#f0f0f3'}},x:{grid:{display:false}}}}}});
  let html='';let weekNum=1;
  for(let w=0;w<byDay.length;w+=3){
    const chunk=byDay.slice(w,w+3).filter(d=>d.orders.length);
    if(!chunk.length) continue;
    html+=<div class="panel" style="margin-bottom:14px"><div class="panel-hd">Week </div><table><tr><th>Day</th><th>User Name</th><th>User ID</th><th>Amount</th></tr>;
    chunk.forEach(d=>{d.orders.forEach(o=>{html+=<tr><td> </td><td></td><td class="uid"></td><td style="color:#1b7a3d;font-weight:700">&#8377;</td></tr>;});});
    html+='</table></div>';weekNum++;
  }
  document.getElementById('phWeeks').innerHTML=html||'<div class="empty">No payment history yet</div>';
}
async function loadDelivery(){
  const d=await api('/api/v1/delivery-persons');
  const agents=Array.isArray(d)?d:(d?.data||[]);
  document.getElementById('dpCount').textContent=agents.length;
  document.getElementById('dpList').innerHTML=agents.length?agents.map(a=>
    <div class="dp-card"><div><div class="dp-name"></div>
    <div class="dp-meta">Age:  &bull; +91 </div>
    <div class="dp-docs">Aadhar:  &bull; PAN: </div>
    <span class="badge b-blue" style="margin-top:6px;display:inline-block"></span></div>
    <button class="icon-del" onclick="delAgent('')">&#128465;</button></div>).join(''):'<div class="empty">No delivery persons yet</div>';
}
async function addDelivery(){
  const name=document.getElementById('dpName').value,phone=document.getElementById('dpPhone').value;
  if(!name||!phone) return alert('Name and phone required');
  await api('/api/v1/delivery-persons?shop_id=shop-001','POST',{
    name,phone,age:parseInt(document.getElementById('dpAge').value)||null,
    vehicle_number:document.getElementById('dpVehicle').value,
    aadhar:document.getElementById('dpAadhar').value,
    pan:document.getElementById('dpPan').value
  });
  ['dpName','dpAge','dpPhone','dpAadhar','dpPan','dpVehicle'].forEach(id=>document.getElementById(id).value='');
  loadDelivery();
}
async function delAgent(id){if(confirm('Remove this delivery person?')){await api('/api/v1/delivery-persons/'+id,'DELETE');loadDelivery();}}
async function loadCustomers(){
  const d=await api('/api/v1/admin/users');
  allCustomers=(Array.isArray(d)?d:(d?.data||[])).filter(u=>u.role==='customer'||!u.role);
  document.getElementById('cuCount').textContent=allCustomers.length;
  document.getElementById('cuTable').innerHTML=allCustomers.length?
    <table><tr><th>User ID</th><th>Name</th><th>Phone</th><th>Status</th><th></th></tr>+
    allCustomers.map((u,i)=><tr><td class="uid">CUS</td><td></td><td>+91 </td><td><span class="badge "></span></td><td><button class="icon-del" onclick="delCustomer('')">&#128465;</button></td></tr>).join('')+'</table>':
    '<div class="empty">No customers yet</div>';
}
async function addCustomer(){
  const id=document.getElementById('cuId').value,name=document.getElementById('cuName').value,phone=document.getElementById('cuPhone').value;
  if(!name||!phone) return alert('Name and phone required');
  await api('/api/v1/auth/register','POST',{email:(id||'cus').toLowerCase()+'@altprint.in',password:'Temp@1234',full_name:name,phone});
  ['cuId','cuName','cuPhone'].forEach(i=>document.getElementById(i).value='');
  loadCustomers();
}
async function delCustomer(id){if(confirm('Delete this customer?')){await api('/api/v1/admin/users/'+id,'DELETE');loadCustomers();}}
async function loadOutlets(){allOutlets=(await api('/api/v1/shops'))||[];filterOutlets('all',document.querySelector('#pg-outlet .tab-btn.on'));}
function filterOutlets(type,el){
  document.querySelectorAll('#pg-outlet .tab-row .tab-btn').forEach(t=>t.classList.remove('on'));
  if(el) el.classList.add('on');
  const list=type==='all'?allOutlets:allOutlets.filter(o=>(o.type||'own')===type);
  document.getElementById('otCount').textContent=list.length;
  document.getElementById('otTable').innerHTML=list.length?
    <table><tr><th>Zone</th><th>Pincode</th><th>Owner</th><th>User ID</th><th>Type</th><th></th></tr>+
    list.map((o,i)=><tr><td></td><td></td><td></td><td class="uid">OUT</td><td><span class="badge "></span></td><td><button class="icon-del" onclick="delOutlet('')">&#128465;</button></td></tr>).join('')+'</table>':
    '<div class="empty">No outlets yet</div>';
}
function setOtType(type){curOtType=type;document.getElementById('otTypeOwn').classList.toggle('on',type==='own');document.getElementById('otTypeFr').classList.toggle('on',type==='franchise');}
async function addOutlet(){
  const zone=document.getElementById('otZone').value,owner=document.getElementById('otOwner').value;
  if(!zone||!owner) return alert('Zone and owner required');
  await api('/api/v1/shops','POST',{name:zone+' Outlet',address:zone,pincode:document.getElementById('otPin').value,owner_name:owner,type:curOtType,is_active:true});
  ['otZone','otPin','otOwner','otId'].forEach(i=>document.getElementById(i).value='');
  loadOutlets();
}
async function delOutlet(id){if(confirm('Delete this outlet?')){await api('/api/v1/shops/'+id,'DELETE');loadOutlets();}}
async function loadSubAdmins(){
  const d=await api('/api/v1/admin/users');
  allSubAdmins=(Array.isArray(d)?d:(d?.data||[])).filter(u=>u.role==='sub-admin'||u.role==='admin');
  document.getElementById('saCount').textContent=allSubAdmins.length;
  document.getElementById('saTable').innerHTML=allSubAdmins.length?
    <table><tr><th>User ID</th><th>Name</th><th>Role</th><th>Created</th><th></th></tr>+
    allSubAdmins.map((u,i)=><tr><td class="uid">SA</td><td></td><td><span class="badge b-dark"></span></td><td></td><td><button class="icon-del" onclick="delSubAdmin('')">&#128465;</button></td></tr>).join('')+'</table>':
    '<div class="empty">No sub-admins yet</div>';
}
async function addSubAdmin(){
  const id=document.getElementById('saId').value,name=document.getElementById('saName').value,pass=document.getElementById('saPass').value,role=document.getElementById('saRole').value;
  if(!name||!pass) return alert('Name and password required');
  await api('/api/v1/auth/register','POST',{email:(id||'sa').toLowerCase()+'@altprint.in',password:pass,full_name:name,role:role||'sub-admin'});
  ['saId','saName','saPass'].forEach(i=>document.getElementById(i).value='');
  loadSubAdmins();
}
async function delSubAdmin(id){if(confirm('Remove this sub-admin?')){await api('/api/v1/admin/users/'+id,'DELETE');loadSubAdmins();}}
async function loadAccountMgmt(){
  const d=await api('/api/v1/admin/users');
  const users=(Array.isArray(d)?d:(d?.data||[])).filter(u=>u.role==='customer'||!u.role);
  document.getElementById('amCount').textContent=users.length;
  document.getElementById('amTable').innerHTML=users.length?
    <table><tr><th>User ID</th><th>Name</th><th>Phone</th><th>Status</th><th>Action</th></tr>+
    users.map((u,i)=>{const active=u.is_active!==false;return<tr><td class="uid">CUS</td><td></td><td>+91 </td><td><span class="badge "></span></td><td><button class="btn-sm " onclick="toggleUserStatus('',)"></button></td></tr>;}).join('')+'</table>':
    '<div class="empty">No customer accounts</div>';
}
async function toggleUserStatus(id,active){await api('/api/v1/admin/users/'+id+'/status?is_active='+active,'PATCH');loadAccountMgmt();}
async function loadTickets(){
  const d=await api('/api/v1/tickets');
  allTickets=Array.isArray(d)?d:(d?.data||[]);
  filterTickets('customer',document.querySelector('#pg-ticket .tab-btn.on'));
}
function filterTickets(type,el){
  document.querySelectorAll('#pg-ticket .tab-row .tab-btn').forEach(t=>t.classList.remove('on'));
  if(el) el.classList.add('on');
  const list=allTickets.filter(t=>(t.category==='customer'?'customer':'outlet')===type||(!t.category&&type==='customer'));
  document.getElementById('tkHd').innerHTML=(type==='customer'?'Customer':'Outlet')+' Complaints (<span id="tkCount">'+list.length+'</span>)';
  document.getElementById('tkList').innerHTML=list.length?list.map(t=>
    <div class="ticket-item"><div><div class="ticket-title"><b></b><span class="badge "></span></div>
    <div class="ticket-meta">User: <span class="uid"></span> &bull; , </div>
    <div class="ticket-desc"></div></div>
    <button class="btn-sm" onclick="resolveTicket('')">&#10003; Resolve</button></div>).join(''):'<div class="empty">No complaints</div>';
}
async function resolveTicket(id){await api('/api/v1/tickets/'+id,'PATCH',{status:'resolved'});loadTickets();}
async function loadStock(){
  const d=await api('/api/v1/stock');
  allStock=Array.isArray(d)?d:(d?.data||[]);
  document.getElementById('skCount').textContent=allStock.length;
  document.getElementById('skTable').innerHTML=allStock.length?
    <table><tr><th>Item Name</th><th>Quantity</th><th>Unit</th><th>Last Updated</th></tr>+
    allStock.map(i=><tr><td><b></b></td><td style="color:;font-weight:700"></td><td></td><td></td></tr>).join('')+'</table>':
    '<div class="empty">No stock items yet</div>';
  const td=await api('/api/v1/tickets');
  const tickets=(Array.isArray(td)?td:(td?.data||[])).filter(t=>t.status==='open'||!t.status);
  document.getElementById('skTkCount').textContent=tickets.length;
  document.getElementById('skTickets').innerHTML=tickets.length?tickets.map(t=>
    <div style="border:1px solid #f0f0f3;border-radius:8px;padding:10px 12px;margin-bottom:8px">
    <div style="display:flex;justify-content:space-between"><span class="badge b-yellow"></span><span style="font-size:.76rem;color:#aaa"></span></div>
    <div style="font-weight:700;font-size:.88rem;margin-top:6px"></div>
    <div style="font-size:.78rem;color:#aaa"></div></div>).join(''):'<div class="empty">No open tickets</div>';
}
function loadAppControl(){updatePreview();}
function setFont(font,el){
  document.querySelectorAll('#acFonts .font-btn').forEach(b=>b.classList.remove('on'));
  el.classList.add('on');
}
function updatePreview(){
  const prim=document.getElementById('acPrim').value||'#ff5722';
  document.getElementById('acPrimSw').style.background=prim;
  document.getElementById('acSecSw').style.background=document.getElementById('acSec').value||'#1a223e';
  document.getElementById('prevBanner').style.background=prim;
  document.getElementById('prevBanner').textContent=document.getElementById('acBanner').value||'PrintLab Admin';
  document.getElementById('prevLogo').style.background=prim;
  ['prevIc1','prevIc2','prevIc3'].forEach(id=>document.getElementById(id).style.background=prim);
}
async function saveAppSettings(){
  const settings={primary_color:document.getElementById('acPrim').value,secondary_color:document.getElementById('acSec').value,logo_url:document.getElementById('acLogo').value,banner_text:document.getElementById('acBanner').value};
  try{await api('/api/v1/admin/app-settings','POST',settings);alert('App settings saved!');}
  catch(e){alert('Saved locally - connect /api/v1/admin/app-settings endpoint');}
}
</script>
</body>
</html>'''

with open(r'static\full_control.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Done! Written', len(html), 'bytes')
