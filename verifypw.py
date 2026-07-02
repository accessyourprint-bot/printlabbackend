import bcrypt
stored = b"$2b$12$ChO6dCG9fTDHXg74k7lVK.D9nghyviulmFwQrEMVFxoIbLAHI17kK"
pw = b"AltPrint2024!"
print("Match:", bcrypt.checkpw(pw, stored))
