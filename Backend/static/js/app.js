/**
 * app.js
 * ------------------------------------------------------------
 * Main application entry point
 */

'use strict';

(function () {

    const {
        Utils,
        MapManager,
        WsManager,
        UiManager,
        Toast
    } = window.SafeHer;

    /* ---------------------------------------------------- */

    const sessionId = Utils.getSessionId();

    console.log("==================================");
    console.log("[APP] Session ID:", sessionId);

    /* ---------------------------------------------------- */

    MapManager.init();
    UiManager.init(sessionId);

    if (!sessionId) {

        console.error("[APP] Session ID Missing");

        UiManager.showInvalidSession();

        UiManager.setConnectionState(
            "error",
            {
                label: "No Session ID"
            }
        );

        return;
    }

    /* ==================================================== */
    /*                  WebSocket Events                    */
    /* ==================================================== */

    window.addEventListener(
        "safeher:ws:open",
        () => {

            console.log("[APP] WebSocket Connected");

            UiManager.setConnectionState("live");

            Toast.show(
                "Connected Successfully",
                "success"
            );
        }
    );

    /* ---------------------------------------------------- */

    window.addEventListener(
        "safeher:ws:location",
        (event) => {

            console.log("==================================");
            console.log("[APP] LOCATION EVENT RECEIVED");

            console.log(event.detail);

            const payload = event.detail;

            const latitude = Number(payload.latitude);
            const longitude = Number(payload.longitude);
            const accuracy = Number(payload.accuracy ?? 0);

            console.log("Latitude :", latitude);
            console.log("Longitude:", longitude);
            console.log("Accuracy :", accuracy);

            if (
                Number.isNaN(latitude) ||
                Number.isNaN(longitude)
            ) {

                console.error("[APP] Invalid Coordinates");

                return;
            }

            console.log("[APP] Calling MapManager.updatePosition()");

            MapManager.updatePosition(
                latitude,
                longitude,
                accuracy,
                true
            );

            console.log("[APP] Updating Side Panel");

            UiManager.updateLocation(payload);

            const stats = MapManager.getRouteStats();

            UiManager.updateRouteStats(
                stats.points,
                stats.distance
            );

            console.log("[APP] Location Updated Successfully");
        }
    );

    /* ---------------------------------------------------- */

    window.addEventListener(
        "safeher:ws:session_ended",
        (event) => {

            console.log("[APP] Session Ended");

            UiManager.showSessionEnded(
                event.detail
            );

            Toast.show(
                "Emergency Session Ended",
                "info",
                0
            );

            disableButtons();
        }
    );

    /* ---------------------------------------------------- */

    window.addEventListener(
        "safeher:ws:reconnecting",
        (event) => {

            console.log("[APP] Reconnecting...");

            const {
                attempt,
                delayMs
            } = event.detail;

            UiManager.setConnectionState(
                "reconnecting",
                {
                    label: `Reconnect #${attempt}`
                }
            );

            console.log(
                "Reconnect in",
                delayMs,
                "ms"
            );
        }
    );

    /* ---------------------------------------------------- */

    window.addEventListener(
        "safeher:ws:error",
        (event) => {

            console.error("[APP] WebSocket Error");

            console.error(event.detail);

            UiManager.setConnectionState(
                "error"
            );
        }
    );

    /* ---------------------------------------------------- */

    window.addEventListener(
        "safeher:ws:closed",
        () => {

            console.warn("[APP] WebSocket Closed");

        }
    );

    /* ==================================================== */

    console.log("[APP] Starting WebSocket");

    WsManager.connect(sessionId);

    /* ==================================================== */

    const btnClearRoute =
        document.getElementById("btn-clear-route");

    const btnCenterMap =
        document.getElementById("btn-center-map");

    const btnShare =
        document.getElementById("btn-share-location");

    /* ---------------------------------------------------- */

    if (btnClearRoute) {

        btnClearRoute.addEventListener(
            "click",
            () => {

                MapManager.clearRoute();

                UiManager.updateRouteStats(
                    0,
                    0
                );

                Toast.show(
                    "Route Cleared",
                    "info"
                );

            }
        );
    }

    /* ---------------------------------------------------- */

    if (btnCenterMap) {

        btnCenterMap.addEventListener(
            "click",
            () => {

                MapManager.centerOnMarker();

            }
        );
    }

    /* ---------------------------------------------------- */

    if (btnShare) {

        btnShare.addEventListener(
            "click",
            async () => {

                const url = location.href;

                if (navigator.share) {

                    try {

                        await navigator.share({

                            title: "SafeHer Live Tracking",

                            text: "Live Tracking",

                            url

                        });

                    }

                    catch (err) {

                        console.error(err);

                    }

                }

            }
        );
    }

    /* ==================================================== */

    function disableButtons() {

        [
            btnClearRoute,
            btnCenterMap,
            btnShare

        ].forEach(btn => {

            if (btn)
                btn.disabled = true;

        });

    }

})();