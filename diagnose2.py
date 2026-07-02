import re
path = r"C:\Users\Shiva\Downloads\specific_control.html"
html = open(path, encoding="utf-8").read()
print("File size:", len(html))
print("--- id=\"pg-...\" matches ---")
for m in re.finditer(r'id="pg-[a-zA-Z0-9_-]+"', html):
    print(m.group())
print("--- has 'App Control':", "App Control" in html)
print("--- has 'Payment for Day':", "Payment for Day" in html)
print("--- has 'Sub-Admin':", "Sub-Admin" in html or "subadmin" in html.lower())
