import 'package:flutter/services.dart';

import '../../../core/app_export.dart';
import '../../../core/utils/validators.dart';
import '../../../widgets/custom_button.dart';
import '../../../widgets/custom_text_field.dart';

class SignupFormWidget extends StatefulWidget {
  final bool isLoading;
  final Future<void> Function({required String mobile}) onSendOtp;
  final VoidCallback onSwitchToLogin;

  const SignupFormWidget({
    super.key,
    required this.isLoading,
    required this.onSendOtp,
    required this.onSwitchToLogin,
  });

  @override
  State<SignupFormWidget> createState() => _SignupFormWidgetState();
}

class _SignupFormWidgetState extends State<SignupFormWidget> {
  final _formKey = GlobalKey<FormState>();
  final _mobileController = TextEditingController();
  final _emailController = TextEditingController();

  @override
  void dispose() {
    _mobileController.dispose();
    _emailController.dispose();
    super.dispose();
  }

  void _submit() {
    if (_formKey.currentState?.validate() ?? false) {
      widget.onSendOtp(mobile: _mobileController.text.trim());
    }
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Mobile number with India prefix
          CustomTextField(
            label: 'Mobile Number',
            hint: '98765 43210',
            controller: _mobileController,
            keyboardType: TextInputType.phone,
            inputFormatters: [
              FilteringTextInputFormatter.digitsOnly,
              LengthLimitingTextInputFormatter(10),
            ],
            prefixWidget: Container(
              margin: const EdgeInsets.only(left: 12, right: 0),
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 14),
              decoration: BoxDecoration(
                border: Border(
                  right: BorderSide(color: const Color(0xFFE8D0DA), width: 1),
                ),
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  // India flag emoji
                  const Text('🇮🇳', style: TextStyle(fontSize: 16)),
                  const SizedBox(width: 6),
                  Text(
                    '+91',
                    style: GoogleFonts.nunitoSans(
                      fontSize: 14,
                      fontWeight: FontWeight.w600,
                      color: const Color(0xFF1A0A12),
                    ),
                  ),
                ],
              ),
            ),
            validator: Validators.validateMobile,
          ),
          const SizedBox(height: 16),
          // Email
          CustomTextField(
            label: 'Email Address',
            hint: 'you@example.com',
            controller: _emailController,
            keyboardType: TextInputType.emailAddress,
            prefixWidget: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 14),
              child: CustomIconWidget(
                iconName: 'email',
                color: const Color(0xFFF0437A),
                size: 20,
              ),
            ),
            validator: Validators.validateEmail,
          ),
          const SizedBox(height: 24),
          // Send OTP button
          CustomButton(
            label: 'Send Verification OTP',
            isLoading: widget.isLoading,
            onPressed: widget.isLoading ? null : _submit,
            prefixIcon: Icons.verified_user_rounded,
          ),
          const SizedBox(height: 20),
          // Already have account
          GestureDetector(
            onTap: widget.onSwitchToLogin,
            child: RichText(
              textAlign: TextAlign.center,
              text: TextSpan(
                style: GoogleFonts.nunitoSans(
                  fontSize: 14,
                  color: const Color(0xFF6B4A58),
                ),
                children: [
                  const TextSpan(text: 'Already have an account? '),
                  TextSpan(
                    text: 'Log In',
                    style: GoogleFonts.nunitoSans(
                      fontSize: 14,
                      fontWeight: FontWeight.w700,
                      color: const Color(0xFFF0437A),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
