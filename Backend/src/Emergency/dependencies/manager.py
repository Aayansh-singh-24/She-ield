from __future__ import annotations
from typing import Dict, Set
from fastapi import WebSocket
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)

@dataclass
class SessionConnection:
    mobile : WebSocket | None = None
    guardian : Set[WebSocket] = field(default_factory=set)


class ConnectionManager:
    def __init__(self):
        self.active_session : Dict[str, SessionConnection] = {} # Store current runnig session in a form of dict {session_id : websocketConnection}
    

    # Helper functions

    # to fetch active_session from dictionary
    def _get_session_(self, session_id: str):

        if session_id not in self.active_sessions:
            self.active_sessions[session_id] = SessionConnection()

        return self.active_sessions[session_id]
    
    # delete teh non-usable seesion info from active session dictionary
    def _cleanup_(self, session_id:str):
        
        if session_id not in self.active_session:
            return
        
        session = self.active_session[session_id]
        if session.mobile is None and len(session.gurdian) == 0:
            del self.active_session[session_id]
            logger.info("Removed session %s from memory")


    # CONECTION-METHODS:-
    
    async def connect_mobile(self, session_id:str, websocket: WebSocket):
        await websocket.accept()
        session = self._get_session_(session_id)
        session.mobile = websocket
        logger.info("Mobile connected for session %s",session_id)


    async def disconnect_mobile(self, session_id:str):
        if session_id not in self.active_session:
            return
        
        session = self.active_session[session_id]
        session.mobile = None

        logger.info("Mobile disconnect from session %s", session_id)

        self._cleanup_(session_id)


    async def connect_guardian(self,session_id:str, websocket:WebSocket):
        await websocket.accept()
        session = self._get_session_(session_id)
        session.guardian.add(websocket)

        logger.info("Guardian connected to session %s " "(Total Guardian: %d)", session_id, len(session.guardian))

    async def disconnect_guardian(self, session_id : str, websocket: WebSocket):

        if session_id not in self.active_session:
            return
        
        session = self.active_session[session_id]
        session.guardian.discard(websocket)

        logger.info("Guardian disconnected from session %s " "(Remaining Guardians: %d)",session_id, len(session.guardians),)


    async def broadcast(self, session_id: str, message:dict):
        if session_id not in self.active_session:
            return
        
        session = self.active_session[session_id]
        disconnected = []

        for guardian in session.guardian:
            try:
                await guardian.send_json(message)
            except Exception:
                disconnected.append(guardian)
        
        for guardian in disconnected:
            session.guardian.discard(guardian)

        logger.info("Broadcasted location to %d guardian(s) ""for session %s",len(session.guardians),session_id)

        self._cleanup_(session_id)


#object
manager = ConnectionManager()