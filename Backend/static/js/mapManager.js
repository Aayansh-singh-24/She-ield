/**
 * mapManager.js
 * ------------------------------------------------------------
 * Leaflet Map Manager
 */

'use strict';

window.SafeHer = window.SafeHer || {};

window.SafeHer.MapManager = (() => {

    const { CONFIG, Utils } = window.SafeHer;

    let _map = null;
    let _marker = null;
    let _accuracyCircle = null;
    let _routePolyline = null;

    let _routeLatLngs = [];
    let _lastLatLng = null;
    let _totalDistance = 0;

    /* ====================================================== */

    function init() {

        console.log("[MAP] Initializing Map");

        _map = L.map("map", {
            center: CONFIG.MAP_DEFAULT_CENTER,
            zoom: CONFIG.MAP_DEFAULT_ZOOM
        });

        L.tileLayer(CONFIG.MAP_TILE_URL, {
            attribution: CONFIG.MAP_TILE_ATTRIBUTION,
            maxZoom: 20
        }).addTo(_map);

        _routePolyline = L.polyline([], {
            color: CONFIG.ROUTE_COLOR,
            weight: CONFIG.ROUTE_WEIGHT,
            opacity: CONFIG.ROUTE_OPACITY,
            dashArray: CONFIG.ROUTE_DASH_ARRAY
        }).addTo(_map);

        console.log("[MAP] Map Initialized");

        return _map;
    }

    /* ====================================================== */

    function updatePosition(lat, lng, accuracy, panMap = true) {

        console.log("=================================");
        console.log("[MAP] updatePosition()");
        console.log({
            lat,
            lng,
            accuracy
        });

        if (!_map) {

            console.error("[MAP] Map is NULL");

            return;
        }

        const latLng = L.latLng(lat, lng);

        /* ---------------- Marker ---------------- */

        if (!_marker) {

            console.log("[MAP] Creating Marker");

            _marker = L.marker(latLng).addTo(_map);

            console.log("[MAP] Marker Created");

        } else {

            console.log("[MAP] Moving Marker");

            _marker.setLatLng(latLng);
        }

        /* ---------------- Accuracy ---------------- */

        if (_accuracyCircle) {

            _accuracyCircle
                .setLatLng(latLng)
                .setRadius(accuracy);

        } else {

            console.log("[MAP] Creating Accuracy Circle");

            _accuracyCircle = L.circle(latLng, {

                radius: accuracy,

                color: "#ff2d55",

                fillColor: "#ff2d55",

                fillOpacity: 0.15

            }).addTo(_map);

        }

        /* ---------------- Route ---------------- */

        if (_lastLatLng) {

            _totalDistance += Utils.haversineDistance(
                _lastLatLng,
                [lat, lng]
            );

        }

        _lastLatLng = [lat, lng];

        _routeLatLngs.push(latLng);

        _routePolyline.setLatLngs(_routeLatLngs);

        console.log(
            "[MAP] Route Points:",
            _routeLatLngs.length
        );

        /* ---------------- Camera ---------------- */

        if (panMap) {

            _map.setView(
                latLng,
                CONFIG.MAP_TRACKING_ZOOM,
                {
                    animate: true
                }
            );

            console.log("[MAP] Camera Updated");
        }

    }

    /* ====================================================== */

    function clearRoute() {

        console.log("[MAP] Clearing Route");

        _routeLatLngs = [];
        _lastLatLng = null;
        _totalDistance = 0;

        if (_routePolyline)
            _routePolyline.setLatLngs([]);

    }

    /* ====================================================== */

    function centerOnMarker() {

        if (!_marker)
            return;

        console.log("[MAP] Center On Marker");

        _map.setView(
            _marker.getLatLng(),
            CONFIG.MAP_TRACKING_ZOOM
        );

    }

    /* ====================================================== */

    function getRouteStats() {

        return {

            points: _routeLatLngs.length,

            distance: _totalDistance

        };

    }

    /* ====================================================== */

    function getMap() {

        return _map;

    }

    /* ====================================================== */

    return {

        init,

        updatePosition,

        clearRoute,

        centerOnMarker,

        getRouteStats,

        getMap

    };

})();