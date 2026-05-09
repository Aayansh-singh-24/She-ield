class ApiConstants {
  static const String baseUrl = 'http://127.0.0.1:8000';

  // Auth
  static const String login = '/api/v1/auth/login';
  static const String register = '/api/v1/auth/register';
  static const String sendOtp = '/api/v1/auth/send-otp';
  static const String verifyOtp = '/api/v1/auth/verify-otp';

  // Trusted Contacts
  static const String trustedContacts = '/trusted-contacts/';
  static const String sosContacts = '/trusted-contacts/sos';

  // Alerts
  static const String triggerSOS = '/api/v1/alerts/sos_trigger';
  static const String alertHistory = '/api/v1/alerts/history';

  // Location
  static const String shareLocation = '/api/v1/location/share';
  static const String stopLocation = '/api/v1/location/stop';

  // Reports
  static const String reportUnsafeArea = '/api/v1/reports/unsafe-area';

  // Recording
  static const String uploadRecording = '/api/v1/recordings/upload';
  static const String recordingHistory = '/api/v1/recordings/history';

  // Profile
  static const String profile = '/api/v1/users/profile';
  static const String updateProfile = '/api/v1/users/profile/update';

  // Google Maps placeholder key
  static const String googleMapsApiKey = 'YOUR_GOOGLE_MAPS_API_KEY_HERE';
}
