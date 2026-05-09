import './token_service.dart';

class AuthService {
  /// TODO: Connect to POST /api/v1/auth/register
  Future<Map<String, dynamic>> registerUser({
    required String mobile,
    required String email,
  }) async {
    try {
      // TODO: Replace with real API call
      // final response = await _client.post(
      //   ApiConstants.register,
      //   data: {'mobile': mobile, 'email': email},
      // );
      // return response.data;
      await Future.delayed(const Duration(milliseconds: 800));
      return {'success': true, 'message': 'OTP sent to $mobile'};
    } catch (e) {
      return {'success': false, 'message': e.toString()};
    }
  }

  /// TODO: Connect to POST /api/v1/auth/send-otp
  Future<Map<String, dynamic>> sendOtp({required String mobile}) async {
    try {
      await Future.delayed(const Duration(milliseconds: 600));
      return {'success': true, 'message': 'OTP sent'};
    } catch (e) {
      return {'success': false, 'message': e.toString()};
    }
  }

  /// TODO: Connect to POST /api/v1/auth/verify-otp
  Future<Map<String, dynamic>> verifyOtp({
    required String mobile,
    required String otp,
  }) async {
    try {
      await Future.delayed(const Duration(milliseconds: 600));
      return {'success': true, 'token': 'mock_token_placeholder'};
    } catch (e) {
      return {'success': false, 'message': e.toString()};
    }
  }

  /// TODO: Connect to POST /api/v1/auth/login
  Future<Map<String, dynamic>> loginUser({
    required String identifier,
    required String password,
  }) async {
    try {
      // TODO: Replace with real API call
      await Future.delayed(const Duration(milliseconds: 800));
      if (identifier.trim() == 'aarya@safeher.app' &&
          password == 'SafeHer@2026') {
        try {
          await TokenService.saveToken('mock_jwt_token_aarya');
          await TokenService.saveUserId('user_001');
        } catch (_) {
          // Token save failed (e.g. storage unavailable) — still allow login
        }
        return {'success': true, 'token': 'mock_jwt_token_aarya'};
      }
      return {
        'success': false,
        'message':
            'Invalid credentials. Use demo: aarya@safeher.app / SafeHer@2026',
      };
    } catch (e) {
      return {'success': false, 'message': 'Login error: ${e.toString()}'};
    }
  }

  Future<void> logout() async {
    await TokenService.clearToken();
  }
}
