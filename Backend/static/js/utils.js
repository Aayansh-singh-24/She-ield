/**
 * utils.js
 * ─────────────────────────────────────────────────────────────
 * Pure utility functions — no side-effects, no DOM access.
 * All functions are stateless and unit-testable.
 */

'use strict';

window.SafeHer = window.SafeHer || {};

window.SafeHer.Utils = (() => {

  /**
   * Extract the session_id from the current page URL.
   * Supports both:
   *   /track/<session_id>        (path-based)
   *   ?session_id=<value>        (query fallback)
   *
   * @returns {string|null}
   */
  function getSessionId() {
    // Primary: path segment  /track/{session_id}
    const pathMatch = location.pathname.match(/\/track\/([^/?#]+)/i);
    if (pathMatch) return decodeURIComponent(pathMatch[1]);

    // Fallback: query string  ?session_id=...
    const params = new URLSearchParams(location.search);
    const qId = params.get('session_id');
    if (qId) return qId;

    return null;
  }

  /**
   * Build the WebSocket URL for a given session_id.
   *
   * @param {string} sessionId
   * @returns {string}  e.g. "wss://example.com/ws/track/abc-123"
   */
  function buildWsUrl(sessionId) {
    const { WS_SCHEME, WS_PATH } = window.SafeHer.CONFIG;
    return `${WS_SCHEME}://${location.host}${WS_PATH}/${encodeURIComponent(sessionId)}`;
  }

  /**
   * Format a coordinate number to a fixed number of decimal places.
   *
   * @param {number} value
   * @param {number} [precision]
   * @returns {string}
   */
  function formatCoord(value, precision) {
    const p = precision ?? window.SafeHer.CONFIG.COORD_PRECISION;
    return Number(value).toFixed(p);
  }

  /**
   * Format speed (m/s from GPS) into km/h display string.
   * Backend may send raw m/s or already-converted km/h —
   * we treat the value as-is and append the unit label.
   *
   * @param {number|null|undefined} speed
   * @returns {string}
   */
  function formatSpeed(speed) {
    if (speed == null || isNaN(speed)) return '—';
    const { SPEED_UNIT } = window.SafeHer.CONFIG;
    return `${Number(speed).toFixed(1)} ${SPEED_UNIT}`;
  }

  /**
   * Format GPS accuracy (metres).
   *
   * @param {number|null|undefined} accuracy
   * @returns {string}
   */
  function formatAccuracy(accuracy) {
    if (accuracy == null || isNaN(accuracy)) return '—';
    const { ACCURACY_UNIT } = window.SafeHer.CONFIG;
    return `±${Number(accuracy).toFixed(0)} ${ACCURACY_UNIT}`;
  }

  /**
   * Format an ISO timestamp into a human-readable local time string.
   *
   * @param {string} isoString
   * @returns {string}
   */
  function formatTimestamp(isoString) {
    if (!isoString) return '—';
    try {
      const d = new Date(isoString);
      return d.toLocaleTimeString(undefined, {
        hour:   '2-digit',
        minute: '2-digit',
        second: '2-digit',
      });
    } catch {
      return isoString;
    }
  }

  /**
   * Compute the Haversine great-circle distance (metres) between two
   * [lat, lng] pairs.
   *
   * @param {[number,number]} a
   * @param {[number,number]} b
   * @returns {number}  metres
   */
  function haversineDistance(a, b) {
    const R = 6_371_000; // Earth radius in metres
    const toRad = (deg) => (deg * Math.PI) / 180;
    const dLat = toRad(b[0] - a[0]);
    const dLng = toRad(b[1] - a[1]);
    const sinDLat = Math.sin(dLat / 2);
    const sinDLng = Math.sin(dLng / 2);
    const c =
      sinDLat * sinDLat +
      Math.cos(toRad(a[0])) * Math.cos(toRad(b[0])) * sinDLng * sinDLng;
    return R * 2 * Math.atan2(Math.sqrt(c), Math.sqrt(1 - c));
  }

  /**
   * Format a distance in metres to a human-readable string.
   *
   * @param {number} metres
   * @returns {string}
   */
  function formatDistance(metres) {
    if (metres < 1000) return `${Math.round(metres)} m`;
    return `${(metres / 1000).toFixed(2)} km`;
  }

  /**
   * Clamp a value between min and max.
   *
   * @param {number} val
   * @param {number} min
   * @param {number} max
   * @returns {number}
   */
  function clamp(val, min, max) {
    return Math.max(min, Math.min(max, val));
  }

  // Public API
  return {
    getSessionId,
    buildWsUrl,
    formatCoord,
    formatSpeed,
    formatAccuracy,
    formatTimestamp,
    haversineDistance,
    formatDistance,
    clamp,
  };

})();
