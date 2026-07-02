with open("static/full_control.html", "r", encoding="utf-8") as f:
    content = f.read()
content = content.replace(
    'const API = "http://127.0.0.1:8001".replace(" :8000\\,\\:8001\\);',
    'const API = "http://127.0.0.1:8001";'
)
with open("static/full_control.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
