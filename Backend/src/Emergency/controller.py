from fastapi import WebSocket, WebSocketDisconnect, status
from src.emergency.dependencies. manager import manager
from src.emergency.dependencies.service import EmergencyService
from src.emergency.schema import LiveLocationSchema
from src.user.models import UserModel

from sqlalchemy.orm import Session
from src.utils.db import SessionLocal
from src.user.controller import websocket_authenticate


async def live_location(websocket:WebSocket, session_id:str, current_user:UserModel):
    
    db = SessionLocal()
    current_user = await websocket_authenticate(websocket, db)

    service = EmergencyService(db)

    service.validate_user_owner(session_id, current_user)

    await manager.connect_mobile(session_id, websocket)

    try:

        while True:

            data = await websocket.receive_json()

            payload = LiveLocationSchema(**data)

            location = service.save_location(session_id, payload, current_user)

            await manager.broadcast(
                session_id=session_id,
                message={
                    "type": "location_update",
                    "session_id": session_id,
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "speed": location.speed,
                    "accuracy": location.accuracy,
                    "timestamp": location.timestamp.isoformat(),
                },
            )

    except WebSocketDisconnect:
        await manager.disconnect_mobile(session_id)

    except Exception as e:
        await manager.disconnect_mobile(session_id)

        await websocket.close(code=1011,reason=str(e))


async def track(websocket:WebSocket, session_id:str, db:Session):

    db = SessionLocal()
    
    service = EmergencyService(db)

    try:
        service.validate_active_session(session_id)

         # Validate that session exists and is active
        service.validate_active_session(session_id)

        # Accept guardian connection
        await manager.connect_guardian(
            session_id=session_id,
            websocket=websocket,
        )

        # Send last known location immediately
        latest = service.get_latest_location(session_id)

        if latest:
            await websocket.send_json(
                {
                    "type": "latest_location",
                    "session_id": session_id,
                    "latitude": latest.latitude,
                    "longitude": latest.longitude,
                    "speed": latest.speed,
                    "accuracy": latest.accuracy,
                    "timestamp": latest.timestamp.isoformat(),
                }
            )

        # Keep connection alive
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:

        await manager.disconnect_guardian(
            session_id=session_id,
            websocket=websocket,
        )

    except Exception:

        await manager.disconnect_guardian(
            session_id=session_id,
            websocket=websocket,
        )

        try:
            await websocket.close(
                code=1011,
                reason="Internal Server Error",
            )
        except Exception:
            pass