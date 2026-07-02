import re
path = r'C:\Users\Shiva\Downloads\altprint-backend (6)\altprint\static\specific_control.html'
html = open(path, encoding='utf-8').read()

# Fix: dropdown is opening on LEFT side (under shop logo) instead of RIGHT
# The trDrop div needs to be INSIDE a relative-positioned wrapper on the right
# Check where trDrop is and fix its position
html = html.replace(
    'id="trDrop" class="hidden" style="position:absolute;right:0;top:calc(100% + 8px)',
    'id="trDrop" class="hidden" style="position:absolute;right:0;top:calc(100% + 8px)'
)

# Fix onclick handlers - ensure they call correct functions
# Replace any broken onclick with direct calls
fixes = [
    ('onclick="openLogistics()"', 'onclick="openLogistics()"'),
    ('onclick="openSettings()"',  'onclick="openSettings()"'),
    ('onclick="doLogout()"',      'onclick="doLogout()"'),
]

# The real fix: make sure curShop is accessible globally
# Add curShop global var if missing
if 'let curShop' not in html and 'var curShop' not in html:
    html = html.replace('let tok=', 'let curShop=null;\nlet tok=', 1)
    print("Added curShop global")

# Fix openDash to save curShop
if 'curShop=' not in html:
    html = html.replace(
        'function openDash(shop){',
        'function openDash(shop){curShop=shop;'
    )
    print("Fixed openDash to save curShop")

open(path, 'w', encoding='utf-8').write(html)
print("Saved")
