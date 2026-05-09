class AlertService {
  // TODO: Connect to POST /api/v1/alerts/sos_trigger
  Future<Map<String, dynamic>> triggerSOSAlert({
    double lat = 28.6139,
    double lng = 77.2090,
  }) async {
    try {
      // TODO: Replace with real API call
      // final response = await _client.post(
      //   ApiConstants.triggerSOS,
      //   data: {
      //     "userId": 1,
      //     "threat_type": "manual_sos",
      //     "confidence": 1.0,
      //     "location": {"lat": lat, "lng": lng},
      //   },
      // );
      // return response.data;
      await Future.delayed(const Duration(milliseconds: 500));
      return {
        'success': true,
        'alertId': 'alert_mock_001',
        'message': 'SOS sent to 3 contacts',
      };
    } catch (e) {
      return {'success': false, 'message': e.toString()};
    }
  }

  /// TODO: Connect to GET /api/v1/alerts/history
  Future<List<Map<String, dynamic>>> getAlertHistory() async {
    try {
      await Future.delayed(const Duration(milliseconds: 500));
      return [];
    } catch (e) {
      return [];
    }
  }
}
