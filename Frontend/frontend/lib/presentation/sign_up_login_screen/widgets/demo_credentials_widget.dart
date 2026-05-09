import 'package:flutter/services.dart';

import '../../../core/app_export.dart';
import '../../../core/utils/helpers.dart';

class DemoCredentialsWidget extends StatelessWidget {
  const DemoCredentialsWidget({super.key});

  void _copyToClipboard(BuildContext context, String text, String label) {
    Clipboard.setData(ClipboardData(text: text));
    Helpers.showToast(context, '$label copied to clipboard');
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFFFFF0F5),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: const Color(0xFFFFD6E7), width: 1.5),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: const Color(0xFFF0437A),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  'Demo Account',
                  style: GoogleFonts.nunitoSans(
                    fontSize: 11,
                    fontWeight: FontWeight.w700,
                    color: Colors.white,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          _CredentialRow(
            label: 'Email',
            value: 'aarya@safeher.app',
            onCopy: () =>
                _copyToClipboard(context, 'aarya@safeher.app', 'Email'),
          ),
          const SizedBox(height: 8),
          _CredentialRow(
            label: 'Password',
            value: 'SafeHer@2026',
            onCopy: () => _copyToClipboard(context, 'SafeHer@2026', 'Password'),
          ),
        ],
      ),
    );
  }
}

class _CredentialRow extends StatelessWidget {
  final String label;
  final String value;
  final VoidCallback onCopy;

  const _CredentialRow({
    required this.label,
    required this.value,
    required this.onCopy,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        SizedBox(
          width: 72,
          child: Text(
            label,
            style: GoogleFonts.nunitoSans(
              fontSize: 12,
              fontWeight: FontWeight.w600,
              color: const Color(0xFF6B4A58),
            ),
          ),
        ),
        Expanded(
          child: Text(
            value,
            style: GoogleFonts.nunitoSans(
              fontSize: 13,
              fontWeight: FontWeight.w600,
              color: const Color(0xFF1A0A12),
            ),
          ),
        ),
        InkWell(
          onTap: onCopy,
          borderRadius: BorderRadius.circular(8),
          child: Padding(
            padding: const EdgeInsets.all(4),
            child: CustomIconWidget(
              iconName: 'copy',
              color: const Color(0xFFF0437A),
              size: 18,
            ),
          ),
        ),
      ],
    );
  }
}
