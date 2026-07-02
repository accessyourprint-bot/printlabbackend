from pathlib import Path

import pytest
from pydantic import ValidationError

from app.schemas.schemas import CreateOrderRequest, RegisterRequest
from app.services import storage


def test_create_order_accepts_delivery_distance():
    request = CreateOrderRequest(
        shop_id="shop-001",
        file_ids=[],
        file_customizations={},
        delivery_type="home_delivery",
        delivery_distance_km=3.5,
    )

    assert request.delivery_distance_km == 3.5


def test_register_requires_email_or_phone():
    with pytest.raises(ValidationError):
        RegisterRequest(password="AltPrint2024!", full_name="Test User")


@pytest.mark.asyncio
async def test_local_storage_encrypts_and_decrypts(tmp_path, monkeypatch):
    monkeypatch.setattr(storage.settings, "STORAGE_PROVIDER", "local")
    monkeypatch.setattr(storage.settings, "LOCAL_STORAGE_PATH", str(tmp_path))

    plaintext = b"frontend upload test"
    storage_key, nonce = await storage.upload_encrypted_file(
        plaintext,
        "sample.pdf",
        "application/pdf",
    )

    stored_bytes = (Path(tmp_path) / storage_key).read_bytes()
    assert stored_bytes != plaintext
    assert await storage.download_decrypted_file(storage_key, nonce) == plaintext
    assert await storage.delete_file_from_storage(storage_key) is True
    assert not (Path(tmp_path) / storage_key).exists()
