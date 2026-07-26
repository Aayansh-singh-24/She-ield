/**
 * wsManager.js
 * ------------------------------------------------------------
 * Handles WebSocket connection, reconnection and event dispatch.
 */

'use strict';

window.SafeHer = window.SafeHer || {};

window.SafeHer.WsManager = (() => {

    const { CONFIG, Utils } = window.SafeHer;

    let _ws = null;
    let _sessionId = null;

    let _reconnectTimer = null;
    let _reconnectDelay = CONFIG.RECONNECT_DELAY_INIT;
    let _reconnectCount = 0;

    let _stopped = false;

    /* -------------------------------------------------------- */

    function connect(sessionId) {
        _sessionId = sessionId;
        _stopped = false;

        _openSocket();
    }

    function disconnect() {

        _stopped = true;

        _clearReconnectTimer();

        if (_ws) {
            _ws.onclose = null;
            _ws.close(1000, "Session Ended");
            _ws = null;
        }
    }

    /* -------------------------------------------------------- */

    function _openSocket() {

        if (_ws) {
            _ws.onclose = null;
            _ws.onerror = null;
            _ws.close();
            _ws = null;
        }

        const url = Utils.buildWsUrl(_sessionId);

        console.log("==================================");
        console.log("[WS] Connecting");
        console.log(url);

        try {
            _ws = new WebSocket(url);
        }
        catch (err) {

            console.error("[WS] Failed to create websocket", err);

            _emit("safeher:ws:error", {
                message: err.message
            });

            _scheduleReconnect();
            return;
        }

        _ws.onopen = _onOpen;
        _ws.onmessage = _onMessage;
        _ws.onerror = _onError;
        _ws.onclose = _onClose;
    }

    /* -------------------------------------------------------- */

    function _onOpen(event) {

        console.log("[WS] Connected");

        _reconnectDelay = CONFIG.RECONNECT_DELAY_INIT;
        _reconnectCount = 0;

        _emit("safeher:ws:open", {
            event
        });
    }

    /* -------------------------------------------------------- */

    function _onMessage(event) {

        console.log("==================================");
        console.log("[WS] RAW MESSAGE");
        console.log(event.data);

        let payload;

        try {

            payload = JSON.parse(event.data);

        } catch (err) {

            console.error("[WS] JSON Parse Error");
            console.error(err);
            return;
        }

        console.log("[WS] Parsed Payload");
        console.log(payload);

        switch (payload.type) {

            case "location_update":

                console.log("[WS] Dispatch -> location_update");

                _emit(
                    "safeher:ws:location",
                    payload
                );

                break;

            case "latest_location":

                console.log("[WS] Dispatch -> latest_location");

                _emit(
                    "safeher:ws:location",
                    payload
                );

                break;

            case "session_ended":

                console.log("[WS] Dispatch -> session_ended");

                _emit(
                    "safeher:ws:session_ended",
                    payload
                );

                disconnect();

                break;

            default:

                console.warn("[WS] Unknown message type");
                console.log(payload);
        }

    }

    /* -------------------------------------------------------- */

    function _onError(event) {

        console.error("[WS] Error");

        console.error(event);

        _emit(
            "safeher:ws:error",
            {
                event
            }
        );
    }

    /* -------------------------------------------------------- */

    function _onClose(event) {

        console.warn("[WS] Closed");

        console.log(event.code);
        console.log(event.reason);

        _emit(
            "safeher:ws:closed",
            {
                code: event.code,
                reason: event.reason
            }
        );

        if (!_stopped) {
            _scheduleReconnect();
        }
    }

    /* -------------------------------------------------------- */

    function _scheduleReconnect() {

        if (_stopped)
            return;

        if (
            CONFIG.RECONNECT_MAX_ATTEMPTS > 0 &&
            _reconnectCount >= CONFIG.RECONNECT_MAX_ATTEMPTS
        ) {

            console.error("[WS] Maximum reconnect attempts reached");

            _emit(
                "safeher:ws:error",
                {
                    message: "Maximum reconnect attempts reached"
                }
            );

            return;
        }

        _reconnectCount++;

        const delay = Math.min(
            _reconnectDelay,
            CONFIG.RECONNECT_DELAY_MAX
        );

        console.log(`[WS] Reconnecting in ${delay} ms`);

        _emit(
            "safeher:ws:reconnecting",
            {
                attempt: _reconnectCount,
                delayMs: delay
            }
        );

        _reconnectTimer = setTimeout(() => {

            if (!_stopped) {
                _openSocket();
            }

        }, delay);

        _reconnectDelay = Math.min(
            _reconnectDelay * CONFIG.RECONNECT_BACKOFF,
            CONFIG.RECONNECT_DELAY_MAX
        );
    }

    /* -------------------------------------------------------- */

    function _clearReconnectTimer() {

        if (_reconnectTimer !== null) {

            clearTimeout(_reconnectTimer);

            _reconnectTimer = null;
        }
    }

    /* -------------------------------------------------------- */

    function _emit(name, detail = {}) {

        console.log(`[EVENT] ${name}`);

        window.dispatchEvent(
            new CustomEvent(name, {
                detail
            })
        );
    }

    /* -------------------------------------------------------- */

    function getReadyState() {

        if (!_ws)
            return WebSocket.CLOSED;

        return _ws.readyState;
    }

    /* -------------------------------------------------------- */

    return {

        connect,
        disconnect,
        getReadyState

    };

})();