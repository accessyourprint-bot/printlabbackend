"""
Alt Print - WebSocket Manager
Real-time updates for feature flag changes, system config, and order status
"""
import json
import logging
import uuid
from datetime import datetime, timezone
from typing import Dict, Optional, Set

from fastapi import WebSocket, WebSocketDisconnect

from app.core.security import decode_token
from app.services.cache import deregister_ws_client, register_ws_client

logger = logging.getLogger(__name__)


class ConnectionManager:
    """
    Manages all active WebSocket connections.
    Supports broadcasting to all clients or filtered by role/shop.
    """

    def __init__(self):
        # All active connections: {client_id: {"ws": WebSocket, "user_id": ..., "role": ...}}
        self.active_connections: Dict[str, Dict] = {}

    async def connect(
        self,
        websocket: WebSocket,
        token: Optional[str] = None,
    ) -> str:
        """Accept a WebSocket connection and register it"""
        await websocket.accept()
        client_id = str(uuid.uuid4())

        user_id = None
        role = "anonymous"
        shop_id = None

        # Authenticate via token if provided
        if token:
            try:
                payload = decode_token(token)
                user_id = payload.get("sub")
                role = payload.get("role", "user")
                shop_id = payload.get("shop_id")
            except Exception:
                # Allow anonymous connections for read-only updates
                pass

        self.active_connections[client_id] = {
            "ws": websocket,
            "user_id": user_id,
            "role": role,
            "shop_id": shop_id,
            "connected_at": datetime.now(timezone.utc).isoformat(),
        }

        await register_ws_client(client_id, user_id, role)
        logger.info(f"WebSocket connected: {client_id} (role={role})")

        # Send current state on connect
        await self._send_welcome(client_id)
        return client_id

    async def disconnect(self, client_id: str) -> None:
        """Remove a WebSocket connection"""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        await deregister_ws_client(client_id)
        logger.info(f"WebSocket disconnected: {client_id}")

    async def send_to_client(self, client_id: str, message: Dict) -> None:
        """Send a message to a specific client"""
        if client_id in self.active_connections:
            ws = self.active_connections[client_id]["ws"]
            try:
                await ws.send_text(json.dumps(message, default=str))
            except Exception as e:
                logger.warning(f"Failed to send to {client_id}: {e}")
                await self.disconnect(client_id)

    async def broadcast(self, message: Dict, role_filter: Optional[str] = None) -> None:
        """
        Broadcast a message to all connected clients.
        Optionally filter by role.
        """
        dead_clients = []
        for client_id, conn_info in self.active_connections.items():
            if role_filter and conn_info["role"] != role_filter:
                continue
            ws = conn_info["ws"]
            try:
                await ws.send_text(json.dumps(message, default=str))
            except Exception:
                dead_clients.append(client_id)

        for cid in dead_clients:
            await self.disconnect(cid)

    async def broadcast_to_shop(self, shop_id: str, message: Dict) -> None:
        """Broadcast to all clients associated with a specific shop"""
        dead_clients = []
        for client_id, conn_info in self.active_connections.items():
            if conn_info.get("shop_id") == shop_id:
                try:
                    await conn_info["ws"].send_text(json.dumps(message, default=str))
                except Exception:
                    dead_clients.append(client_id)

        for cid in dead_clients:
            await self.disconnect(cid)

    async def _send_welcome(self, client_id: str) -> None:
        """Send a welcome message with connection info"""
        await self.send_to_client(client_id, {
            "type": "connected",
            "payload": {
                "client_id": client_id,
                "message": "Connected to Alt Print real-time service",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def get_connection_count(self) -> int:
        return len(self.active_connections)


# Singleton instance
ws_manager = ConnectionManager()


# ============================================================
# EVENT BROADCASTING HELPERS
# ============================================================
async def broadcast_system_config_update(config_data: Dict) -> None:
    """Broadcast system config change to all clients"""
    await ws_manager.broadcast({
        "type": "SYSTEM_CONFIG_UPDATE",
        "payload": config_data,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


async def broadcast_feature_flag_update(feature_data: Dict, shop_id: Optional[str] = None) -> None:
    """Broadcast feature flag change"""
    message = {
        "type": "FEATURE_FLAG_UPDATE",
        "payload": feature_data,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    if shop_id:
        await ws_manager.broadcast_to_shop(shop_id, message)
        # Also broadcast to super_admins
        await ws_manager.broadcast(message, role_filter="super_admin")
    else:
        await ws_manager.broadcast(message)


async def broadcast_order_update(order_id: str, status: str, user_id: str) -> None:
    """Broadcast order status change to relevant clients"""
    message = {
        "type": "ORDER_STATUS_UPDATE",
        "payload": {"order_id": order_id, "status": status},
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    # Find the specific user's connection
    for client_id, conn_info in ws_manager.active_connections.items():
        if conn_info.get("user_id") == user_id:
            await ws_manager.send_to_client(client_id, message)
