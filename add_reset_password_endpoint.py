import io

path = "app/api/v1/endpoints/admin.py"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# --- Add import for hash_password ---
old_import = "from app.api.v1.deps import get_client_ip, require_role"
new_import = "from app.api.v1.deps import get_client_ip, require_role\nfrom app.core.security import hash_password"

c1 = content.count(old_import)
print(f"Import anchor found {c1} time(s)")
if c1 == 1:
    content = content.replace(old_import, new_import)
else:
    print("WARNING: import anchor not found exactly once, aborting")
    exit()

# --- Add the reset-password endpoint after toggle_user_status ---
anchor = '    return APIResponse(message=f"User {\'enabled\' if enabled else \'disabled\'} successfully")\n\n\n@router.get("/owner/config"'

new_endpoint = '''    return APIResponse(message=f"User {'enabled' if enabled else 'disabled'} successfully")


@router.patch("/users/{user_id}/reset-password", response_model=APIResponse)
async def reset_user_password(
    user_id: str,
    new_password: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin")),
):
    """Reset a specific user's password (admin action)."""
    if len(new_password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = hash_password(new_password)
    await db.flush()

    await log_action(
        db,
        actor=str(current_user.email or current_user.phone),
        action="RESET_USER_PASSWORD",
        target=str(user.id),
        details={},
        role=current_user.role,
        ip_address=get_client_ip(request),
    )

    return APIResponse(message="Password reset successfully")


@router.get("/owner/config"'''

c2 = content.count(anchor)
print(f"Endpoint anchor found {c2} time(s)")
if c2 == 1:
    content = content.replace(anchor, new_endpoint)
    print("reset_user_password endpoint added")
else:
    print("WARNING: endpoint anchor not found exactly once, aborting")
    exit()

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
