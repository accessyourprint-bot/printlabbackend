"""
Alt Print - WebSocket Endpoint
Real-time updates for feature flags, system config, order status
"""
import logging
from typing import Optional

from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect

from app.services.websocket import ws_manager

logger = logging.getLogger(__name__)

router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: Optional[str] = Query(None, description="JWT access token for authenticated updates"),
):
    """
    WebSocket connection endpoint.
    
    Connect with: ws://your-domain/ws?token=YOUR_JWT_TOKEN
    
    Events received from server:
    - connected: Initial connection confirmation
    - SYSTEM_CONFIG_UPDATE: App state changes (app_enabled, maintenance, etc.)
    - FEATURE_FLAG_UPDATE: Feature flag toggles
    - ORDER_STATUS_UPDATE: Order status changes
    
    All events format: {"type": "EVENT_TYPE", "payload": {...}, "timestamp": "ISO8601"}
    """
    client_id = await ws_manager.connect(websocket, token)

    try:
        while True:
            # Keep connection alive; listen for ping/pong
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        await ws_manager.disconnect(client_id)
        logger.info(f"WebSocket client {client_id} disconnected normally")
    except Exception as e:
        logger.error(f"WebSocket error for {client_id}: {e}")
        await ws_manager.disconnect(client_id)
