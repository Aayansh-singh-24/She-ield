/**
 * config.js
 * ─────────────────────────────────────────────────────────────
 * Centralised configuration for the Guardian Tracking Page.
 * All tuneable values live here — never scattered through modules.
 */

'use strict';

window.SafeHer = window.SafeHer || {};

window.SafeHer.CONFIG = Object.freeze({

  /* ── WebSocket ─────────────────────────────────────────────
     WS_SCHEME is set to 'wss' when the page is served over HTTPS,
     'ws' otherwise — matches the backend contract exactly.         */
  get WS_SCHEME() {
    return location.protocol === 'https:' ? 'wss' : 'ws';
  },

  /** Backend WebSocket path for the guardian tracking endpoint.
   *  Final URL: ws(s)://<host>/ws/track/<session_id>            */
  WS_PATH: '/ws/track',

  /* ── Reconnect strategy (exponential back-off) ─────────────  */
  /** Initial delay before first reconnect attempt (ms)          */
  RECONNECT_DELAY_INIT:   1_500,
  /** Multiplicative back-off factor per attempt                 */
  RECONNECT_BACKOFF:      1.6,
  /** Maximum delay cap (ms)                                     */
  RECONNECT_DELAY_MAX:    30_000,
  /** Maximum number of reconnect attempts (0 = unlimited)       */
  RECONNECT_MAX_ATTEMPTS: 0,

  /* ── Map defaults ──────────────────────────────────────────  */
  /** Leaflet tile provider                                       */
  MAP_TILE_URL: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
  MAP_TILE_ATTRIBUTION: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
  MAP_DEFAULT_CENTER: [20.5937, 78.9629],   /* India centroid fallback */
  MAP_DEFAULT_ZOOM:   5,
  MAP_TRACKING_ZOOM:  17,

  /* ── Route polyline ────────────────────────────────────────  */
  ROUTE_COLOR:        '#e84393',
  ROUTE_WEIGHT:       3,
  ROUTE_OPACITY:      0.75,
  ROUTE_DASH_ARRAY:   '6 4',

  /* ── Marker smooth animation ───────────────────────────────  */
  /** Duration (ms) of the CSS transition on marker position     */
  MARKER_ANIM_DURATION: 800,

  /* ── Toast ─────────────────────────────────────────────────  */
  TOAST_DURATION:     4_000,   /* ms before auto-dismiss        */

  /* ── Display formatting ────────────────────────────────────  */
  COORD_PRECISION:    6,       /* decimal places for lat/lng     */
  SPEED_UNIT:         'km/h',
  ACCURACY_UNIT:      'm',
});
