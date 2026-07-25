/**
 * wsManager.js
 * ─────────────────────────────────────────────────────────────
 * WebSocket lifecycle manager with automatic exponential-back-off
 * reconnection.  Emits typed events the rest of the app listens to.
 *
 * Event contract (via window.dispatchEvent):
 *   'safeher:ws:open'         — connection established
 *   'safeher:ws:location'     — location_update received  (detail = payload)
 *   'safeher:ws:session_ended'— session_ended received    (detail = payload)
 *   'safeher:ws:error'        — websocket error
 *   'safeher:ws:closed'       — connection closed
 *   'safeher:ws:reconnecting' — about to attempt reconnect
 *                               (detail = { attempt, delayMs })
 *
 * Depends on: config.js, utils.js
 * Exposes:    window.SafeHer.WsManager
 */

'use strict';

window.SafeHer = window.SafeHer || {};

window.SafeHer.WsManager = (() => {

  const { CONFIG, Utils } = window.SafeHer;

  /* ── State ────────────────────────────────────────────────── */
  let _ws              = null;
  let _sessionId       = null;
  let _reconnectTimer  = null;
  let _reconnectDelay  = CONFIG.RECONNECT_DELAY_INIT;
  let _reconnectCount  = 0;
  let _stopped         = false;   // set true when session ends — no more reconnect

  /* ── Public: connect ────────────────────────────────────────  */
  /**
   * Open the WebSocket connection for the given session.
   * Safe to call multiple times — will close any existing socket first.
   *
   * @param {string} sessionId
   */
  function connect(sessionId) {
    _sessionId = sessionId;
    _stopped   = false;
    _openSocket();
  }

  /* ── Public: disconnect ─────────────────────────────────────  */
  /**
   * Permanently close the connection and suppress all further reconnects.
   * Call this when the session has ended.
   */
  function disconnect() {
    _stopped = true;
    _clearReconnectTimer();
    if (_ws) {
      _ws.onclose = null;   // prevent reconnect logic inside onclose
      _ws.close(1000, 'Session ended');
      _ws = null;
    }
  }

  /* ── Internal: open socket ──────────────────────────────────  */
  function _openSocket() {
    if (_ws) {
      _ws.onclose = null;
      _ws.onerror = null;
      _ws.close();
      _ws = null;
    }

    const url = Utils.buildWsUrl(_sessionId);
    console.info(`[WsManager] Connecting → ${url}`);

    try {
      _ws = new WebSocket(url);
    } catch (err) {
      console.error('[WsManager] WebSocket construction failed:', err);
      _emit('safeher:ws:error', { message: err.message });
      _scheduleReconnect();
      return;
    }

    _ws.onopen    = _onOpen;
    _ws.onmessage = _onMessage;
    _ws.onerror   = _onError;
    _ws.onclose   = _onClose;
  }

  /* ── Handlers ───────────────────────────────────────────────  */
  function _onOpen(event) {
    console.info('[WsManager] Connected');
    _reconnectDelay  = CONFIG.RECONNECT_DELAY_INIT;
    _reconnectCount  = 0;
    _emit('safeher:ws:open', { event });
  }

  function _onMessage(event) {
    let payload;
    try {
      payload = JSON.parse(event.data);
    } catch (err) {
      console.warn('[WsManager] Could not parse message:', event.data);
      return;
    }

    const { type } = payload;

    switch (type) {
      case 'location_update':
        _emit('safeher:ws:location', payload);
        break;

      case 'session_ended':
        console.info('[WsManager] Session ended signal received');
        _emit('safeher:ws:session_ended', payload);
        disconnect();   // stop reconnecting
        break;

      default:
        console.debug('[WsManager] Unhandled message type:', type, payload);
    }
  }

  function _onError(event) {
    console.warn('[WsManager] WebSocket error', event);
    _emit('safeher:ws:error', { event });
    // onclose fires automatically after onerror — reconnect logic lives there
  }

  function _onClose(event) {
    console.info(`[WsManager] Connection closed — code=${event.code} reason="${event.reason}"`);
    _emit('safeher:ws:closed', { code: event.code, reason: event.reason });

    if (!_stopped) {
      _scheduleReconnect();
    }
  }

  /* ── Reconnect ──────────────────────────────────────────────  */
  function _scheduleReconnect() {
    if (_stopped) return;

    const maxAttempts = CONFIG.RECONNECT_MAX_ATTEMPTS;
    if (maxAttempts > 0 && _reconnectCount >= maxAttempts) {
      console.warn('[WsManager] Max reconnect attempts reached — giving up');
      _emit('safeher:ws:error', { message: 'Max reconnect attempts reached' });
      return;
    }

    _reconnectCount++;
    const delay = Math.min(_reconnectDelay, CONFIG.RECONNECT_DELAY_MAX);

    console.info(`[WsManager] Reconnecting in ${delay}ms (attempt #${_reconnectCount})…`);
    _emit('safeher:ws:reconnecting', { attempt: _reconnectCount, delayMs: delay });

    _reconnectTimer = setTimeout(() => {
      if (!_stopped) _openSocket();
    }, delay);

    // Exponential back-off
    _reconnectDelay = Math.min(
      _reconnectDelay * CONFIG.RECONNECT_BACKOFF,
      CONFIG.RECONNECT_DELAY_MAX,
    );
  }

  function _clearReconnectTimer() {
    if (_reconnectTimer !== null) {
      clearTimeout(_reconnectTimer);
      _reconnectTimer = null;
    }
  }

  /* ── Event emitter helper ───────────────────────────────────  */
  function _emit(name, detail = {}) {
    window.dispatchEvent(new CustomEvent(name, { detail }));
  }

  /* ── Public: getReadyState ──────────────────────────────────  */
  function getReadyState() {
    if (!_ws) return WebSocket.CLOSED;
    return _ws.readyState;
  }

  return {
    connect,
    disconnect,
    getReadyState,
  };

})();
