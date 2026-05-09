import '../../../core/app_export.dart';
import '../../../core/services/auth_service.dart';

class HomeDrawerWidget extends StatelessWidget {
  const HomeDrawerWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return Drawer(
      backgroundColor: const Color(0xFF1A0A12),
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.horizontal(right: Radius.circular(28)),
      ),
      child: SafeArea(
        child: Column(
          children: [
            // Header
            _buildDrawerHeader(),
            const SizedBox(height: 8),
            // Nav items
            Expanded(
              child: ListView(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                children: [
                  _DrawerNavItem(
                    iconName: 'home',
                    label: 'Home',
                    onTap: () => Navigator.of(context).pop(),
                  ),
                  _DrawerNavItem(
                    iconName: 'person',
                    label: 'Profile',
                    onTap: () {
                      Navigator.of(context).pop();
                      // TODO: Navigate to profile screen
                    },
                  ),
                  _DrawerNavItem(
                    iconName: 'contacts',
                    label: 'Trusted Contacts',
                    onTap: () {
                      Navigator.of(context).pop();
                      // TODO: Navigate to trusted contacts
                    },
                  ),
                  _DrawerNavItem(
                    iconName: 'local_police',
                    label: 'Emergency Help',
                    onTap: () {
                      Navigator.of(context).pop();
                      // TODO: Navigate to emergency help
                    },
                  ),
                  _DrawerNavItem(
                    iconName: 'phone',
                    label: 'Fake Call',
                    onTap: () {
                      Navigator.of(context).pop();
                      // TODO: Navigate to fake call
                    },
                  ),
                  _DrawerNavItem(
                    iconName: 'mic',
                    label: 'Record Evidence',
                    onTap: () {
                      Navigator.of(context).pop();
                      // TODO: Navigate to record screen
                    },
                  ),
                  _DrawerNavItem(
                    iconName: 'location_on',
                    label: 'Live Location',
                    onTap: () {
                      Navigator.of(context).pop();
                      // TODO: Navigate to live location
                    },
                  ),
                  _DrawerNavItem(
                    iconName: 'history',
                    label: 'Alert History',
                    onTap: () {
                      Navigator.of(context).pop();
                      // TODO: Navigate to alert history
                    },
                  ),
                  _DrawerNavItem(
                    iconName: 'settings',
                    label: 'Settings',
                    onTap: () {
                      Navigator.of(context).pop();
                      // TODO: Navigate to settings
                    },
                  ),
                  const SizedBox(height: 8),
                  Divider(color: Colors.white.withAlpha(31), height: 1),
                  const SizedBox(height: 8),
                  // Logout — destructive
                  _DrawerNavItem(
                    iconName: 'logout',
                    label: 'Logout',
                    isDestructive: true,
                    onTap: () async {
                      Navigator.of(context).pop();
                      await AuthService().logout();
                      if (context.mounted) {
                        Navigator.of(context).pushNamedAndRemoveUntil(
                          AppRoutes.signUpLoginScreen,
                          (route) => false,
                        );
                      }
                    },
                  ),
                ],
              ),
            ),
            // Footer
            Padding(
              padding: const EdgeInsets.all(20),
              child: Text(
                '© 2026 SafeHer',
                style: GoogleFonts.nunitoSans(
                  fontSize: 12,
                  color: Colors.white.withAlpha(89),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDrawerHeader() {
    return Container(
      padding: const EdgeInsets.all(24),
      child: Column(
        children: [
          // Logo row
          Row(
            children: [
              Container(
                width: 44,
                height: 44,
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [Color(0xFFF0437A), Color(0xFF8B1A52)],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: const Center(
                  child: CustomIconWidget(
                    iconName: 'shield',
                    color: Colors.white,
                    size: 24,
                  ),
                ),
              ),
              const SizedBox(width: 12),
              Text(
                'SafeHer',
                style: GoogleFonts.nunitoSans(
                  fontSize: 24,
                  fontWeight: FontWeight.w900,
                  color: const Color(0xFFF0437A),
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),
          // User summary
          Row(
            children: [
              Container(
                width: 48,
                height: 48,
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [Color(0xFFF0437A), Color(0xFF8B1A52)],
                  ),
                  shape: BoxShape.circle,
                ),
                child: Center(
                  child: Text(
                    'A',
                    style: GoogleFonts.nunitoSans(
                      fontSize: 20,
                      fontWeight: FontWeight.w800,
                      color: Colors.white,
                    ),
                  ),
                ),
              ),
              const SizedBox(width: 12),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Aarya Sharma',
                    style: GoogleFonts.nunitoSans(
                      fontSize: 15,
                      fontWeight: FontWeight.w700,
                      color: Colors.white,
                    ),
                  ),
                  Text(
                    '+91 91198 92200',
                    style: GoogleFonts.nunitoSans(
                      fontSize: 12,
                      color: Colors.white.withAlpha(153),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _DrawerNavItem extends StatelessWidget {
  final String iconName;
  final String label;
  final VoidCallback onTap;
  final bool isDestructive;

  const _DrawerNavItem({
    required this.iconName,
    required this.label,
    required this.onTap,
    this.isDestructive = false,
  });

  @override
  Widget build(BuildContext context) {
    final color = isDestructive
        ? const Color(0xFFCF6679)
        : Colors.white.withAlpha(217);

    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(14),
      splashColor: const Color(0xFFF0437A).withAlpha(38),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        child: Row(
          children: [
            Container(
              width: 36,
              height: 36,
              decoration: BoxDecoration(
                color: isDestructive
                    ? const Color(0xFFCF6679).withAlpha(38)
                    : Colors.white.withAlpha(20),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Center(
                child: CustomIconWidget(
                  iconName: iconName,
                  color: color,
                  size: 18,
                ),
              ),
            ),
            const SizedBox(width: 14),
            Text(
              label,
              style: GoogleFonts.nunitoSans(
                fontSize: 14,
                fontWeight: FontWeight.w600,
                color: color,
              ),
            ),
            const Spacer(),
            CustomIconWidget(
              iconName: 'chevron_right',
              color: Colors.white.withAlpha(64),
              size: 18,
            ),
          ],
        ),
      ),
    );
  }
}
