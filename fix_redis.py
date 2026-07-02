with open("app/services/cache.py", "r", encoding="utf-8") as f:
    content = f.read()

old = 'async def check_rate_limit(key: str, limit: int = 100, window: int = 60) -> tuple[bool, int]:'
new = '''async def check_rate_limit(key: str, limit: int = 100, window: int = 60) -> tuple[bool, int]:
    try:
        import redis.asyncio as _r
        _test = _r.from_url("redis://localhost:6379")
        await _test.ping()
        await _test.aclose()
    except Exception:
        return True, limit'''

content = content.replace(old, new)
with open("app/services/cache.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
