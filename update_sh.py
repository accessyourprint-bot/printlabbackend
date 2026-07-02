import re
import os

path = r'static/specific_control.html'
with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. REMOVE the standalone Sales History button from the topbar
# We look for the button that calls showSalesHistory or openSalesHistory
html = re.sub(r'<button class="btn_top" onclick="(?:showSalesHistory|openSalesHistory)\(\)">.*?</button>', '', html)

# 2. ADD the "Sales History" button and content container INSIDE the Performance Modal
# We insert it after the catBars div (where the print type progress bars are)
sales_history_ui_snippet = """
                <div style="text-align: center; margin-top: 20px;">
                    <button class="btn_top" id="toggleShBtn" onclick="toggleSalesHistoryContent()" style="width: 100%; justify-content: center; background: #fafafa; border-style: dashed;">
                        📈 View Sales History
                    </button>
                </div>

                <div id="shContentInModal" class="hidden" style="margin-top: 25px; border-top: 2px solid #f1f5f9; padding-top: 25px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
                        <h3 style="font-size:1.2rem; font-weight:900;">Sales History Breakdown</h3>
                        <div class="tt_box" style="flex-wrap: wrap; gap: 5px;">
                            <button class="tab_b on" id="shAll" onclick="updateHistory('all', this)">All</button>
                            <button class="tab_b" onclick="updateHistory('Bw', this)">B/W</button>
                            <button class="tab_b" onclick="updateHistory('Colour', this)">Colour</button>
                            <button class="tab_b" onclick="updateHistory('Photo', this)">Photo</button>
                            <button class="tab_b" onclick="updateHistory('Tshirt', this)">T-Shirt</button>
                            <button class="tab_b" onclick="updateHistory('Project', this)">Project</button>
                        </div>
                    </div>
                    <canvas id="pChart" height="150"></canvas>
                    <h4 style="margin:30px 0 15px; font-weight:900; border-bottom:2px solid #f1f5f9; padding-bottom:12px;">Daily History</h4>
                    <div id="hList"></div>
                </div>
"""

# Insert the snippet into the Performance Modal body
html = html.replace('<div id="catBars"></div>', '<div id="catBars"></div>' + sales_history_ui_snippet)

# 3. ADD the toggle logic to the script section
toggle_js = """
        function toggleSalesHistoryContent() {
            const content = document.getElementById('shContentInModal');
            const btn = document.getElementById('toggleShBtn');
            if (content.classList.contains('hidden')) {
                content.classList.remove('hidden');
                btn.innerHTML = '▲ Hide Sales History';
                updateHistory('all', document.getElementById('shAll'));
            } else {
                content.classList.add('hidden');
                btn.innerHTML = '📈 View Sales History';
            }
        }
"""

# 4. ENSURE openPerf() resets the toggle state so it stays clean
html = html.replace("openMo('perfModal');", "openMo('perfModal'); document.getElementById('shContentInModal').classList.add('hidden'); document.getElementById('toggleShBtn').innerHTML = '📈 View Sales History';")

# Inject the toggle function before the closing script tag
html = html.replace('</script>', toggle_js + '\n</script>')

# 5. CLEAN UP: Remove any old Sales History View containers if they still exist in the HTML
html = re.sub(r'<!-- Sales History View.*?</div.*?>\s*</div>', '', html, flags=re.DOTALL)
html = re.sub(r'<div id="salesView".*?</div>\s*</div>', '', html, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print("SUCCESS: Sales History moved inside Performance Status modal!")
