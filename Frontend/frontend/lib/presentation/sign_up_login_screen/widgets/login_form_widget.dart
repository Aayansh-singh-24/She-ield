
import '../../../core/app_export.dart';
import '../../../core/utils/validators.dart';
import '../../../widgets/custom_button.dart';
import '../../../widgets/custom_text_field.dart';

class LoginFormWidget extends StatefulWidget {
  final bool isLoading;
  final Future<void> Function({
    required String identifier,
    required String password,
  })
  onLogin;

  const LoginFormWidget({
    super.key,
    required this.isLoading,
    required this.onLogin,
  });

  @override
  State<LoginFormWidget> createState() => _LoginFormWidgetState();
}

class _LoginFormWidgetState extends State<LoginFormWidget> {
  final _formKey = GlobalKey<FormState>();
  final _identifierController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  void dispose() {
    _identifierController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _submit() {
    if (_formKey.currentState?.validate() ?? false) {
      widget.onLogin(
        identifier: _identifierController.text.trim(),
        password: _passwordController.text,
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Mobile / Email field
          CustomTextField(
            label: 'Mobile Number or Email',
            hint: 'Enter your mobile or email',
            controller: _identifierController,
            keyboardType: TextInputType.emailAddress,
            prefixWidget: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 14),
              child: CustomIconWidget(
                iconName: 'phone_android',
                color: const Color(0xFFF0437A),
                size: 20,
              ),
            ),
            validator: (v) {
              if (v == null || v.isEmpty) return 'This field is required';
              return null;
            },
          ),
          const SizedBox(height: 16),
          // Password field
          CustomTextField(
            label: 'Password',
            hint: 'Enter your password',
            controller: _passwordController,
            obscureText: true,
            prefixWidget: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 14),
              child: CustomIconWidget(
                iconName: 'lock',
                color: const Color(0xFFF0437A),
                size: 20,
              ),
            ),
            validator: Validators.validatePassword,
          ),
          const SizedBox(height: 8),
          // Forgot password
          Align(
            alignment: Alignment.centerRight,
            child: TextButton(
              onPressed: () {
                // TODO: Navigate to forgot password screen
              },
              child: Text(
                'Forgot Password?',
                style: GoogleFonts.nunitoSans(
                  fontSize: 13,
                  fontWeight: FontWeight.w600,
                  color: const Color(0xFFF0437A),
                ),
              ),
            ),
          ),
          const SizedBox(height: 16),
          // Login button
          CustomButton(
            label: 'Log In',
            isLoading: widget.isLoading,
            onPressed: widget.isLoading ? null : _submit,
          ),
        ],
      ),
    );
  }
}
