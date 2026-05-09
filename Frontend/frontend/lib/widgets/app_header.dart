
import '../core/app_export.dart';

class AppHeader extends StatelessWidget implements PreferredSizeWidget {
  final bool showBackButton;
  final VoidCallback? onNotificationTap;
  final VoidCallback? onMenuTap;
  final List<Widget>? extraActions;

  const AppHeader({
    super.key,
    this.showBackButton = false,
    this.onNotificationTap,
    this.onMenuTap,
    this.extraActions,
  });

  @override
  Size get preferredSize => const Size.fromHeight(64);

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 64 + MediaQuery.of(context).padding.top,
      padding: EdgeInsets.only(top: MediaQuery.of(context).padding.top),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: const Color(0xFFF0437A).withAlpha(20),
            blurRadius: 12,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16),
        child: Row(
          children: [
            if (showBackButton) ...[
              InkWell(
                onTap: () => Navigator.of(context).pop(),
                borderRadius: BorderRadius.circular(50),
                child: Container(
                  width: 40,
                  height: 40,
                  decoration: BoxDecoration(
                    color: const Color(0xFFFFF0F5),
                    borderRadius: BorderRadius.circular(50),
                  ),
                  child: CustomIconWidget(
                    iconName: 'arrow_back',
                    color: const Color(0xFFF0437A),
                    size: 20,
                  ),
                ),
              ),
              const SizedBox(width: 12),
            ],
            // Logo + brand name
            Container(
              width: 36,
              height: 36,
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  colors: [Color(0xFFF0437A), Color(0xFF8B1A52)],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                borderRadius: BorderRadius.circular(10),
              ),
              child: const Center(
                child: CustomIconWidget(
                  iconName: 'shield',
                  color: Colors.white,
                  size: 20,
                ),
              ),
            ),
            const SizedBox(width: 10),
            Text(
              'SafeHer',
              style: GoogleFonts.nunitoSans(
                fontSize: 22,
                fontWeight: FontWeight.w800,
                color: const Color(0xFFF0437A),
              ),
            ),
            const Spacer(),
            if (extraActions != null) ...extraActions!,
            // Notification icon
            InkWell(
              onTap: onNotificationTap,
              borderRadius: BorderRadius.circular(50),
              child: Container(
                width: 40,
                height: 40,
                decoration: BoxDecoration(
                  color: const Color(0xFFFFF0F5),
                  borderRadius: BorderRadius.circular(50),
                ),
                child: CustomIconWidget(
                  iconName: 'notifications_outlined',
                  color: const Color(0xFFF0437A),
                  size: 22,
                ),
              ),
            ),
            const SizedBox(width: 8),
            // Menu icon
            InkWell(
              onTap: onMenuTap,
              borderRadius: BorderRadius.circular(50),
              child: Container(
                width: 40,
                height: 40,
                decoration: BoxDecoration(
                  color: const Color(0xFFFFF0F5),
                  borderRadius: BorderRadius.circular(50),
                ),
                child: CustomIconWidget(
                  iconName: 'menu',
                  color: const Color(0xFF1A0A12),
                  size: 22,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
