/**
 * mapManager.js
 * ─────────────────────────────────────────────────────────────
 * Encapsulates all Leaflet map interactions:
 *   • Map initialisation
 *   • Custom SVG marker with smooth animated movement
 *   • Accuracy circle
 *   • Route polyline
 *   • Re-center / clear helpers
 *
 * Depends on: config.js, utils.js
 * Exposes:    window.SafeHer.MapManager
 */

'use strict';

window.SafeHer = window.SafeHer || {};

window.SafeHer.MapManager = (() => {

  const { CONFIG, Utils } = window.SafeHer;

  /* ── State ────────────────────────────────────────────────── */
  let _map             = null;
  let _marker          = null;
  let _accuracyCircle  = null;
  let _routePolyline   = null;
  let _routeLatLngs    = [];     // array of [lat, lng] pairs
  let _totalDistance   = 0;      // metres
  let _lastLatLng      = null;   // for distance accumulation

  /* ── Custom marker HTML ─────────────────────────────────────
     A pulsing pink location pin built entirely in SVG + CSS.  */
  const MARKER_HTML = `
    <div class="safeher-marker" style="
        position: relative;
        width: 40px;
        height: 40px;
        transform: translate(-50%, -50%);
        cursor: pointer;
      ">
      <!-- Pulse ring -->
      <div style="
          position: absolute; inset: -8px;
          border-radius: 50%;
          background: rgba(232,67,147,0.18);
          animation: markerPulse 2s ease-out infinite;
        "></div>
      <!-- Outer ring -->
      <div style="
          position: absolute; inset: 0;
          border-radius: 50%;
          background: rgba(232,67,147,0.3);
          border: 2.5px solid rgba(232,67,147,0.8);
        "></div>
      <!-- Inner dot -->
      <div style="
          position: absolute; inset: 9px;
          border-radius: 50%;
          background: #e84393;
          box-shadow: 0 0 12px rgba(232,67,147,0.8);
        "></div>
    </div>
  `;

  /* Inject keyframe animation for the marker once */
  (function _injectMarkerStyle() {
    if (document.getElementById('safeher-marker-style')) return;
    const style = document.createElement('style');
    style.id = 'safeher-marker-style';
    style.textContent = `
      @keyframes markerPulse {
        0%   { transform: scale(0.8); opacity: 0.9; }
        70%  { transform: scale(1.9); opacity: 0;   }
        100% { transform: scale(0.8); opacity: 0;   }
      }
    `;
    document.head.appendChild(style);
  })();

  /* ── Public: init ───────────────────────────────────────────  */
  /**
   * Initialise the Leaflet map inside the #map element.
   * Must be called once, after Leaflet is loaded.
   */
  function init() {
    _map = L.map('map', {
      center:  CONFIG.MAP_DEFAULT_CENTER,
      zoom:    CONFIG.MAP_DEFAULT_ZOOM,
      zoomControl: true,
      attributionControl: true,
    });

    L.tileLayer(CONFIG.MAP_TILE_URL, {
      attribution: CONFIG.MAP_TILE_ATTRIBUTION,
      maxZoom: 20,
      subdomains: 'abcd',
    }).addTo(_map);

    // Route polyline (starts empty)
    _routePolyline = L.polyline([], {
      color:     CONFIG.ROUTE_COLOR,
      weight:    CONFIG.ROUTE_WEIGHT,
      opacity:   CONFIG.ROUTE_OPACITY,
      dashArray: CONFIG.ROUTE_DASH_ARRAY,
    }).addTo(_map);

    return _map;
  }

  /* ── Public: updatePosition ─────────────────────────────────  */
  /**
   * Move the marker smoothly to [lat, lng] and update accuracy circle + route.
   *
   * @param {number} lat
   * @param {number} lng
   * @param {number} accuracy  metres
   * @param {boolean} [panMap=true]
   */
  function updatePosition(lat, lng, accuracy, panMap = true) {
    if (!_map) return;

    const latlng = L.latLng(lat, lng);

    /* ── Marker ───────────────────────────────────────────────  */
    if (!_marker) {
      _marker = L.marker(latlng, {
        icon: L.divIcon({
          html:      MARKER_HTML,
          className: '',
          iconSize:  [40, 40],
          iconAnchor:[20, 20],
        }),
        zIndexOffset: 1000,
      }).addTo(_map);

      _marker.bindPopup(_buildPopupContent(lat, lng, accuracy), {
        closeButton: false,
        className:   'safeher-popup',
        maxWidth:    220,
      });
    } else {
      /* Smooth CSS transition via Leaflet's setLatLng */
      _smoothMove(_marker, latlng);
      _marker.setPopupContent(_buildPopupContent(lat, lng, accuracy));
    }

    /* ── Accuracy circle ──────────────────────────────────────  */
    if (_accuracyCircle) {
      _accuracyCircle.setLatLng(latlng).setRadius(accuracy ?? 0);
    } else {
      _accuracyCircle = L.circle(latlng, {
        radius:      accuracy ?? 0,
        color:       '#e84393',
        fillColor:   '#e84393',
        fillOpacity: 0.06,
        weight:      1.5,
        opacity:     0.4,
        dashArray:   '4 4',
      }).addTo(_map);
    }

    /* ── Route accumulation ───────────────────────────────────  */
    const point = [lat, lng];
    if (_lastLatLng) {
      _totalDistance += Utils.haversineDistance(_lastLatLng, point);
    }
    _lastLatLng = point;
    _routeLatLngs.push(latlng);
    _routePolyline.setLatLngs(_routeLatLngs);

    /* ── Pan ──────────────────────────────────────────────────  */
    if (panMap) {
      const currentZoom = _map.getZoom();
      if (currentZoom < CONFIG.MAP_TRACKING_ZOOM) {
        _map.setView(latlng, CONFIG.MAP_TRACKING_ZOOM, { animate: true });
      } else {
        _map.panTo(latlng, { animate: true, duration: 0.8 });
      }
    }

    /* ── Accuracy legend label ────────────────────────────────  */
    const label = document.getElementById('accuracy-ring-label');
    if (label) {
      label.textContent = accuracy
        ? `GPS accuracy: ±${Math.round(accuracy)} m`
        : 'Accuracy data unavailable';
    }
  }

  /* ── Smooth marker movement ─────────────────────────────────
     Leaflet's setLatLng is instant.  We override the marker's
     _icon element with a CSS transition so the pin glides.     */
  function _smoothMove(marker, newLatLng) {
    const icon = marker.getElement();
    if (icon) {
      icon.style.transition = `transform ${CONFIG.MARKER_ANIM_DURATION}ms cubic-bezier(0.22, 1, 0.36, 1)`;
    }
    marker.setLatLng(newLatLng);
  }

  /* ── Popup content ──────────────────────────────────────────  */
  function _buildPopupContent(lat, lng, accuracy) {
    return `
      <div style="font-family:Inter,sans-serif;font-size:12px;color:#f0f0f8;line-height:1.7;">
        <strong style="display:block;margin-bottom:4px;color:#e84393;">📍 Live Position</strong>
        <div>${Utils.formatCoord(lat)}, ${Utils.formatCoord(lng)}</div>
        ${accuracy ? `<div style="color:#9898b8;">Accuracy: ±${Math.round(accuracy)} m</div>` : ''}
      </div>
    `;
  }

  /* ── Public: clearRoute ─────────────────────────────────────  */
  function clearRoute() {
    _routeLatLngs  = [];
    _totalDistance = 0;
    _lastLatLng    = null;
    if (_routePolyline) _routePolyline.setLatLngs([]);
  }

  /* ── Public: centerOnMarker ─────────────────────────────────  */
  function centerOnMarker() {
    if (!_map || !_marker) return;
    _map.setView(_marker.getLatLng(), CONFIG.MAP_TRACKING_ZOOM, { animate: true });
  }

  /* ── Public: getRouteStats ──────────────────────────────────  */
  function getRouteStats() {
    return {
      points:   _routeLatLngs.length,
      distance: _totalDistance,
    };
  }

  /* ── Public: getMap ─────────────────────────────────────────  */
  function getMap() { return _map; }

  return {
    init,
    updatePosition,
    clearRoute,
    centerOnMarker,
    getRouteStats,
    getMap,
  };

})();
