from fastapi import APIRouter,  WebSocket, Depends
from sqlalchemy.orm import Session
from src.emergency import controller
from src.utils.db import get_db


router = APIRouter(prefix="/ws", tags=["Emergency WebSocket"])


@router.websocket("/live_location/{session_id}")
async def live_location(websocket:WebSocket, session_id:str, db:Session  = Depends(get_db)):
    await controller.live_location(websocket, session_id, db)


@router.websocket("/track/{session_id}")
async def track(websocket:WebSocket, session_id:str, db:Session = Depends(get_db)):
    await controller.track(websocket, session_id, db)