/**
 * app.js
 * ─────────────────────────────────────────────────────────────
 * Application entry-point.
 * Wires together MapManager, WsManager, UiManager, and Toast.
 *
 * Responsibilities:
 *  1. Extract session_id from URL
 *  2. Show invalid-session overlay if missing
 *  3. Initialise map + UI
 *  4. Subscribe to WsManager events
 *  5. Handle location updates → map + UI
 *  6. Handle session_ended → overlay + disable
 *  7. Handle reconnect states → badge
 *  8. Wire button actions (clear route, re-center, share)
 *
 * Depends on: config.js, utils.js, toast.js,
 *             mapManager.js, wsManager.js, uiManager.js
 */

'use strict';

(function SafeHerApp() {

  const { CONFIG, Utils, MapManager, WsManager, UiManager, Toast } = window.SafeHer;

  /* ── 1. Extract session_id ──────────────────────────────────  */
  const sessionId = Utils.getSessionId();

  /* ── 2. Initialise Leaflet map ──────────────────────────────  */
  MapManager.init();

  /* ── 3. Initialise UI ───────────────────────────────────────  */
  UiManager.init(sessionId);

  if (!sessionId) {
    /* No session_id found — show error overlay and bail */
    UiManager.showInvalidSession();
    UiManager.setConnectionState('error', { label: 'No session ID' });
    console.error('[App] No session_id in URL — tracking disabled');
    return;
  }

  /* ── 4. Subscribe to WebSocket events ───────────────────────  */

  window.addEventListener('safeher:ws:open', () => {
    UiManager.setConnectionState('live');
    Toast.show('Connected — receiving live location', 'success');
  });

  window.addEventListener('safeher:ws:location', (e) => {
    const payload = e.detail;
    const { latitude, longitude, accuracy } = payload;

    /* Validate payload fields */
    if (typeof latitude !== 'number' || typeof longitude !== 'number') {
      console.warn('[App] location_update missing lat/lng:', payload);
      return;
    }

    /* Update map */
    MapManager.updatePosition(latitude, longitude, accuracy ?? 0, true);

    /* Update side-panel fields */
    UiManager.updateLocation(payload);

    /* Update route stats */
    const stats = MapManager.getRouteStats();
    UiManager.updateRouteStats(stats.points, stats.distance);
  });

  window.addEventListener('safeher:ws:session_ended', (e) => {
    /* Show the "Emergency has ended" overlay */
    UiManager.showSessionEnded(e.detail);
    Toast.show('Emergency has ended — tracking stopped', 'info', 0 /* sticky */);
    _disableButtons();
  });

  window.addEventListener('safeher:ws:reconnecting', (e) => {
    const { attempt, delayMs } = e.detail;
    UiManager.setConnectionState('reconnecting', {
      label: `Reconnecting… (#${attempt})`,
    });
    if (attempt === 1) {
      Toast.show('Connection lost — reconnecting automatically…', 'warn');
    }
    console.info(`[App] Reconnect attempt ${attempt} in ${delayMs}ms`);
  });

  window.addEventListener('safeher:ws:error', (e) => {
    console.error('[App] WebSocket error:', e.detail);
    UiManager.setConnectionState('error');
  });

  window.addEventListener('safeher:ws:closed', () => {
    /* If not stopped (session ended), UiManager badge is updated
       by the reconnecting event. If it is stopped that was handled
       by session_ended.  Nothing extra needed here.               */
  });

  /* ── 5. Start WebSocket ─────────────────────────────────────  */
  WsManager.connect(sessionId);

  /* ── 6. Button: clear route ─────────────────────────────────  */
  const btnClearRoute = document.getElementById('btn-clear-route');
  if (btnClearRoute) {
    btnClearRoute.addEventListener('click', () => {
      MapManager.clearRoute();
      UiManager.updateRouteStats(0, 0);
      Toast.show('Route cleared', 'info');
    });
  }

  /* ── 7. Button: re-center map ───────────────────────────────  */
  const btnCenterMap = document.getElementById('btn-center-map');
  if (btnCenterMap) {
    btnCenterMap.addEventListener('click', () => {
      MapManager.centerOnMarker();
    });
  }

  /* ── 8. Button: share link ──────────────────────────────────  */
  const btnShare = document.getElementById('btn-share-location');
  if (btnShare) {
    btnShare.addEventListener('click', async () => {
      const url = location.href;
      if (navigator.share) {
        try {
          await navigator.share({
            title: 'SafeHer — Live Tracking',
            text:  'Track this person\'s location in real time',
            url,
          });
        } catch (err) {
          if (err.name !== 'AbortError') {
            _copyToClipboard(url);
          }
        }
      } else {
        _copyToClipboard(url);
      }
    });
  }

  /* ── Helpers ────────────────────────────────────────────────  */
  function _copyToClipboard(text) {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text)
        .then(() => Toast.show('Tracking link copied to clipboard!', 'success'))
        .catch(() => _fallbackCopy(text));
    } else {
      _fallbackCopy(text);
    }
  }

  function _fallbackCopy(text) {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity  = '0';
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    Toast.show('Tracking link copied!', 'success');
  }

  function _disableButtons() {
    [btnClearRoute, btnCenterMap, btnShare].forEach(btn => {
      if (btn) btn.disabled = true;
    });
  }

})();
