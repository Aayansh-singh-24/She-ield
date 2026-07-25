from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, status, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


router = APIRouter(tags=["Tracking"])

templates = Jinja2Templates(directory="templates")

@router.get("/track/{session_id}", response_class=HTMLResponse)
async def tracking_page(
    request: Request,
    session_id: str,
):
    return templates.TemplateResponse(
        "tracking/track.html",
        {
            "request": request,
            "session_id": session_id,
        },
    )