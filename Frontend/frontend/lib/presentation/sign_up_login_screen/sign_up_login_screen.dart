import 'package:flutter/services.dart';

import '../../core/app_export.dart';
import '../../core/services/auth_service.dart';
import '../../core/utils/helpers.dart';
import '../../presentation/sign_up_login_screen/widgets/auth_footer_widget.dart';
import '../../presentation/sign_up_login_screen/widgets/auth_segmented_tab_widget.dart';
import '../../presentation/sign_up_login_screen/widgets/demo_credentials_widget.dart';
import '../../presentation/sign_up_login_screen/widgets/login_form_widget.dart';
import '../../presentation/sign_up_login_screen/widgets/signup_form_widget.dart';

class SignUpLoginScreen extends StatefulWidget {
  const SignUpLoginScreen({super.key});

  @override
  State<SignUpLoginScreen> createState() => _SignUpLoginScreenState();
}

class _SignUpLoginScreenState extends State<SignUpLoginScreen>
    with SingleTickerProviderStateMixin {
  // TODO: Replace setState with Riverpod/Bloc for production
  int _selectedTab = 0; // 0 = Login, 1 = Signup
  bool _isLoading = false;
  late AnimationController _tabSlideController;

  @override
  void initState() {
    super.initState();
    SystemChrome.setSystemUIOverlayStyle(
      const SystemUiOverlayStyle(
        statusBarColor: Colors.transparent,
        statusBarIconBrightness: Brightness.dark,
      ),
    );
    _tabSlideController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 280),
    );
  }

  @override
  void dispose() {
    _tabSlideController.dispose();
    super.dispose();
  }

  void _switchTab(int index) {
    if (index == _selectedTab) return;
    setState(() => _selectedTab = index);
    if (index == 1) {
      _tabSlideController.forward();
    } else {
      _tabSlideController.reverse();
    }
  }

  Future<void> _handleLogin({
    required String identifier,
    required String password,
  }) async {
    if (!mounted) return;
    setState(() => _isLoading = true);
    try {
      final result = await AuthService().loginUser(
        identifier: identifier,
        password: password,
      );
      if (!mounted) return;
      setState(() => _isLoading = false);
      if (result['success'] == true) {
        Navigator.of(context).pushReplacementNamed(AppRoutes.homeScreen);
      } else {
        Helpers.showToast(
          context,
          result['message']?.toString() ?? 'Login failed. Please try again.',
          isError: true,
        );
      }
    } catch (e) {
      if (!mounted) return;
      setState(() => _isLoading = false);
      Helpers.showToast(
        context,
        'Login failed. Please try again.',
        isError: true,
      );
    }
  }

  Future<void> _handleSendOtp({required String mobile}) async {
    if (!mounted) return;
    setState(() => _isLoading = true);
    try {
      final result = await AuthService().sendOtp(mobile: mobile);
      if (!mounted) return;
      setState(() => _isLoading = false);
      Helpers.showToast(
        context,
        result['success'] == true
            ? 'OTP sent to +91 $mobile'
            : 'Failed to send OTP. Please try again.',
        isError: result['success'] != true,
      );
    } catch (e) {
      if (!mounted) return;
      setState(() => _isLoading = false);
      Helpers.showToast(
        context,
        'Failed to send OTP. Please try again.',
        isError: true,
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final isTablet = size.width >= 600;

    return Scaffold(
      backgroundColor: const Color(0xFFFFF8FA),
      body: SafeArea(
        child: Center(
          child: ConstrainedBox(
            constraints: BoxConstraints(
              maxWidth: isTablet ? 480 : double.infinity,
            ),
            child: SingleChildScrollView(
              physics: const BouncingScrollPhysics(),
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  const SizedBox(height: 16),
                  // Logo
                  _buildLogoSection(),
                  const SizedBox(height: 36),
                  // Segmented tab control
                  AuthSegmentedTabWidget(
                    selectedIndex: _selectedTab,
                    onTabChanged: _switchTab,
                  ),
                  const SizedBox(height: 28),
                  // Form — animates between login/signup
                  AnimatedSwitcher(
                    duration: const Duration(milliseconds: 300),
                    transitionBuilder: (child, animation) {
                      return FadeTransition(
                        opacity: animation,
                        child: SlideTransition(
                          position:
                              Tween<Offset>(
                                begin: const Offset(0.05, 0),
                                end: Offset.zero,
                              ).animate(
                                CurvedAnimation(
                                  parent: animation,
                                  curve: Curves.easeOutCubic,
                                ),
                              ),
                          child: child,
                        ),
                      );
                    },
                    child: _selectedTab == 0
                        ? LoginFormWidget(
                            key: const ValueKey('login'),
                            isLoading: _isLoading,
                            onLogin: _handleLogin,
                          )
                        : SignupFormWidget(
                            key: const ValueKey('signup'),
                            isLoading: _isLoading,
                            onSendOtp: _handleSendOtp,
                            onSwitchToLogin: () => _switchTab(0),
                          ),
                  ),
                  const SizedBox(height: 20),
                  // Demo credentials box (login only)
                  if (_selectedTab == 0) ...[
                    const DemoCredentialsWidget(),
                    const SizedBox(height: 20),
                  ],
                  // Footer
                  const AuthFooterWidget(),
                  const SizedBox(height: 16),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildLogoSection() {
    return Column(
      children: [
        Container(
          width: 80,
          height: 80,
          decoration: BoxDecoration(
            gradient: const LinearGradient(
              colors: [Color(0xFFF0437A), Color(0xFF8B1A52)],
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
            ),
            borderRadius: BorderRadius.circular(22),
            boxShadow: [
              BoxShadow(
                color: const Color(0xFFF0437A).withAlpha(89),
                blurRadius: 20,
                offset: const Offset(0, 8),
              ),
            ],
          ),
          child: Stack(
            alignment: Alignment.center,
            children: [
              const CustomIconWidget(
                iconName: 'shield',
                color: Colors.white,
                size: 50,
              ),
              Positioned(
                top: 14,
                child: CustomIconWidget(
                  iconName: 'person',
                  color: Colors.white.withAlpha(230),
                  size: 28,
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 16),
        Text(
          'SafeHer',
          style: GoogleFonts.nunitoSans(
            fontSize: 32,
            fontWeight: FontWeight.w900,
            color: const Color(0xFFF0437A),
            letterSpacing: -0.5,
          ),
        ),
        const SizedBox(height: 4),
        Text(
          'Your Safety, Our Priority.',
          style: GoogleFonts.nunitoSans(
            fontSize: 14,
            fontWeight: FontWeight.w500,
            color: const Color(0xFF6B4A58),
          ),
        ),
      ],
    );
  }
}
