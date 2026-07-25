/**
 * uiManager.js
 * ─────────────────────────────────────────────────────────────
 * Owns every DOM write on the tracking page:
 *   • Connection status badge
 *   • Live-info fields (lat, lng, speed, accuracy, timestamp)
 *   • Session card
 *   • Route stats
 *   • Session-ended overlay
 *   • Invalid-session overlay
 *   • "Updated" highlight flash on value fields
 *
 * Depends on: config.js, utils.js
 * Exposes:    window.SafeHer.UiManager
 */

'use strict';

window.SafeHer = window.SafeHer || {};

window.SafeHer.UiManager = (() => {

  const { Utils } = window.SafeHer;

  /* ── Element refs (resolved once on init) ───────────────────  */
  let _els = {};

  /* ── Connection badge state machine ─────────────────────────  */
  const BADGE_STATES = {
    connecting:   { cls: 'status-connecting',   label: 'Connecting…' },
    live:         { cls: 'status-live',          label: 'Live' },
    reconnecting: { cls: 'status-reconnecting',  label: 'Reconnecting…' },
    error:        { cls: 'status-error',         label: 'Connection error' },
    ended:        { cls: 'status-ended',         label: 'Session ended' },
  };

  const ALL_BADGE_CLASSES = Object.values(BADGE_STATES).map(s => s.cls);

  /* ── Public: init ───────────────────────────────────────────  */
  function init(sessionId) {
    _els = {
      badge:          document.getElementById('connection-badge'),
      badgeLabel:     document.querySelector('#connection-badge .status-label'),
      lat:            document.getElementById('display-lat'),
      lng:            document.getElementById('display-lng'),
      speed:          document.getElementById('display-speed'),
      accuracy:       document.getElementById('display-accuracy'),
      timestamp:      document.getElementById('display-timestamp'),
      sessionId:      document.getElementById('display-session-id'),
      sessionStatus:  document.getElementById('display-session-status'),
      routePoints:    document.getElementById('route-points'),
      routeDistance:  document.getElementById('route-distance'),
      sessionEndedOverlay: document.getElementById('session-ended-overlay'),
      sessionEndedMeta:    document.getElementById('session-ended-meta'),
      invalidOverlay:      document.getElementById('invalid-session-overlay'),
    };

    // Render session ID immediately
    if (_els.sessionId && sessionId) {
      _els.sessionId.textContent = sessionId;
    }

    setConnectionState('connecting');
  }

  /* ── Public: setConnectionState ─────────────────────────────  */
  function setConnectionState(state, meta) {
    const cfg = BADGE_STATES[state];
    if (!cfg || !_els.badge) return;

    _els.badge.classList.remove(...ALL_BADGE_CLASSES);
    _els.badge.classList.add(cfg.cls);

    if (_els.badgeLabel) {
      _els.badgeLabel.textContent =
        meta?.label ?? cfg.label;
    }

    // Session status card
    if (_els.sessionStatus) {
      const statusMap = {
        connecting:   'Connecting…',
        live:         '🟢 Active',
        reconnecting: '⏳ Reconnecting…',
        error:        '🔴 Connection Error',
        ended:        '⬛ Ended',
      };
      _els.sessionStatus.textContent = statusMap[state] ?? state;
    }
  }

  /* ── Public: updateLocation ─────────────────────────────────  */
  /**
   * Push a location_update payload to all display fields.
   *
   * @param {{ latitude, longitude, speed, accuracy, timestamp }} data
   */
  function updateLocation(data) {
    const { latitude, longitude, speed, accuracy, timestamp } = data;

    _setValue(_els.lat,       Utils.formatCoord(latitude));
    _setValue(_els.lng,       Utils.formatCoord(longitude));
    _setValue(_els.speed,     Utils.formatSpeed(speed));
    _setValue(_els.accuracy,  Utils.formatAccuracy(accuracy));
    _setValue(_els.timestamp, Utils.formatTimestamp(timestamp));
  }

  /* ── Public: updateRouteStats ───────────────────────────────  */
  function updateRouteStats(points, distanceMetres) {
    if (_els.routePoints)   _els.routePoints.textContent   = points;
    if (_els.routeDistance) _els.routeDistance.textContent = Utils.formatDistance(distanceMetres);
  }

  /* ── Public: showSessionEnded ───────────────────────────────  */
  function showSessionEnded(payload) {
    if (_els.sessionEndedOverlay) {
      _els.sessionEndedOverlay.classList.remove('hidden');
    }
    if (_els.sessionEndedMeta && payload?.timestamp) {
      _els.sessionEndedMeta.textContent =
        `Session closed at ${Utils.formatTimestamp(payload.timestamp)}`;
    }
    setConnectionState('ended');
  }

  /* ── Public: showInvalidSession ─────────────────────────────  */
  function showInvalidSession() {
    if (_els.invalidOverlay) {
      _els.invalidOverlay.classList.remove('hidden');
    }
  }

  /* ── Internal: set value with flash highlight ───────────────  */
  function _setValue(el, value) {
    if (!el || el.textContent === value) return;
    el.textContent = value;
    // Flash the accent colour briefly
    el.classList.remove('updated');
    // Force reflow so the animation restarts
    void el.offsetWidth;
    el.classList.add('updated');
    setTimeout(() => el.classList.remove('updated'), 800);
  }

  return {
    init,
    setConnectionState,
    updateLocation,
    updateRouteStats,
    showSessionEnded,
    showInvalidSession,
  };

})();
