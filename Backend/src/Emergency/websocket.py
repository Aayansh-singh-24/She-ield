from fastapi import APIRouter,  WebSocket
from src.emergency import controller


router = APIRouter(prefix="/ws", tags=["Emergency WebSocket"])


@router.websocket("/live_location/{session_id}")
async def live_location(websocket:WebSocket, session_id:str):
    await controller.live_location(websocket, session_id)

@router.websocket("/track/{session_id}")
async def track(websocket:WebSocket, session_id:str ):
    await controller.track(websocket, session_id)