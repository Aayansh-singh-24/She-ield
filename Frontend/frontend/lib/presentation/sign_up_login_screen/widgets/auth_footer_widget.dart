import '../../../core/app_export.dart';

class AuthFooterWidget extends StatelessWidget {
  const AuthFooterWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextButton(
              onPressed: () {
                // TODO: Navigate to Terms & Conditions
              },
              style: TextButton.styleFrom(
                padding: const EdgeInsets.symmetric(horizontal: 8),
                minimumSize: Size.zero,
                tapTargetSize: MaterialTapTargetSize.shrinkWrap,
              ),
              child: Text(
                'T&Cs',
                style: GoogleFonts.nunitoSans(
                  fontSize: 12,
                  fontWeight: FontWeight.w600,
                  color: const Color(0xFF8B1A52),
                ),
              ),
            ),
            Text(
              '•',
              style: GoogleFonts.nunitoSans(
                color: const Color(0xFFB08090),
                fontSize: 12,
              ),
            ),
            TextButton(
              onPressed: () {
                // TODO: Navigate to Privacy Policy
              },
              style: TextButton.styleFrom(
                padding: const EdgeInsets.symmetric(horizontal: 8),
                minimumSize: Size.zero,
                tapTargetSize: MaterialTapTargetSize.shrinkWrap,
              ),
              child: Text(
                'Privacy Policy',
                style: GoogleFonts.nunitoSans(
                  fontSize: 12,
                  fontWeight: FontWeight.w600,
                  color: const Color(0xFF8B1A52),
                ),
              ),
            ),
          ],
        ),
        const SizedBox(height: 4),
        Text(
          '© 2026 SafeHer. All rights reserved.',
          style: GoogleFonts.nunitoSans(
            fontSize: 11,
            fontWeight: FontWeight.w400,
            color: const Color(0xFFB08090),
          ),
          textAlign: TextAlign.center,
        ),
      ],
    );
  }
}
