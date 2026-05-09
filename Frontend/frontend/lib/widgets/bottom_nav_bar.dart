
import '../core/app_export.dart';
import './sos_button.dart';

class SafeHerBottomNavBar extends StatelessWidget {
  final int currentIndex;
  final ValueChanged<int> onTap;

  const SafeHerBottomNavBar({
    super.key,
    required this.currentIndex,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 80 + MediaQuery.of(context).padding.bottom,
      padding: EdgeInsets.only(bottom: MediaQuery.of(context).padding.bottom),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: const Color(0xFFF0437A).withAlpha(26),
            blurRadius: 20,
            offset: const Offset(0, -4),
          ),
        ],
        borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          _NavItem(
            iconName: currentIndex == 0 ? 'home' : 'home_outlined',
            label: 'Home',
            isActive: currentIndex == 0,
            onTap: () => onTap(0),
          ),
          _NavItem(
            iconName: currentIndex == 1 ? 'mic' : 'mic_outlined',
            label: 'Record',
            isActive: currentIndex == 1,
            onTap: () => onTap(1),
          ),
          // Center SOS button — elevated above bar
          Transform.translate(
            offset: const Offset(0, -18),
            child: const SosButton(),
          ),
          _NavItem(
            iconName: currentIndex == 3 ? 'phone' : 'phone_outlined',
            label: 'Fake Call',
            isActive: currentIndex == 3,
            onTap: () => onTap(3),
          ),
          _NavItem(
            iconName: currentIndex == 4 ? 'help' : 'help_outlined',
            label: 'Help',
            isActive: currentIndex == 4,
            onTap: () => onTap(4),
          ),
        ],
      ),
    );
  }
}

class _NavItem extends StatelessWidget {
  final String iconName;
  final String label;
  final bool isActive;
  final VoidCallback onTap;

  const _NavItem({
    required this.iconName,
    required this.label,
    required this.isActive,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(16),
      splashColor: const Color(0xFFF0437A).withAlpha(31),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            AnimatedContainer(
              duration: const Duration(milliseconds: 200),
              curve: Curves.easeOutCubic,
              padding: const EdgeInsets.all(6),
              decoration: BoxDecoration(
                color: isActive
                    ? const Color(0xFFF0437A).withAlpha(31)
                    : Colors.transparent,
                borderRadius: BorderRadius.circular(12),
              ),
              child: CustomIconWidget(
                iconName: iconName,
                color: isActive
                    ? const Color(0xFFF0437A)
                    : const Color(0xFFB08090),
                size: 22,
              ),
            ),
            const SizedBox(height: 2),
            AnimatedDefaultTextStyle(
              duration: const Duration(milliseconds: 200),
              style: GoogleFonts.nunitoSans(
                fontSize: 11,
                fontWeight: isActive ? FontWeight.w700 : FontWeight.w500,
                color: isActive
                    ? const Color(0xFFF0437A)
                    : const Color(0xFFB08090),
              ),
              child: Text(label),
            ),
          ],
        ),
      ),
    );
  }
}
