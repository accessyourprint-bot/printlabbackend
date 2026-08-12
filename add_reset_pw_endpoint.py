import io

path = r"app\api\v1\endpoints\shops.py"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

new_endpoint = '''

@router.patch("/{shop_id}/reset-password", response_model=APIResponse)
async def reset_shop_password(
    shop_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin")),
):
    """Reset the shop owner's login password to a new random password."""
    result = await db.execute(select(Shop).where(Shop.id == shop_id))
    shop = result.scalar_one_or_none()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")

    user_result = await db.execute(select(User).where(User.shop_id == shop_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="No login account found for this shop")

    new_password = secrets.token_urlsafe(9)
    user.hashed_password = hash_password(new_password)
    await db.flush()

    await log_action(db, str(current_user.email), "RESET_SHOP_PASSWORD", shop_id,
                     details=shop.name, role=current_user.role, ip_address=get_client_ip(request))
    return APIResponse(message=f"Password reset for '{shop.name}'", data={"new_password": new_password})
'''

with io.open(path, "a", encoding="utf-8") as f:
    f.write(new_endpoint)

print("APPENDED SUCCESSFULLY")
