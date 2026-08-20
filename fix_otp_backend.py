path = r"app\core\security.py"
with open(path, "r", encoding="utf-8") as f:
    src = f.read()

old = '''def generate_otp() -> str:
    """Generate a 6-digit OTP"""
    return str(secrets.randbelow(900000) + 100000)'''

new = '''def generate_otp() -> str:
    """Generate a 4-digit OTP"""
    return str(secrets.randbelow(9000) + 1000)'''

if src.count(old) != 1:
    raise SystemExit(f"FAILED: found {src.count(old)} matches, expected 1.")

src = src.replace(old, new, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(src)

print("SUCCESS: generate_otp() now returns a 4-digit OTP.")
