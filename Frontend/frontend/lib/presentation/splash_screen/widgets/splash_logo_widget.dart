
import '../../../core/app_export.dart';

class SplashLogoWidget extends StatelessWidget {
  final Animation<double> scaleAnimation;
  final Animation<double> fadeAnimation;

  const SplashLogoWidget({
    super.key,
    required this.scaleAnimation,
    required this.fadeAnimation,
  });

  @override
  Widget build(BuildContext context) {
    return FadeTransition(
      opacity: fadeAnimation,
      child: ScaleTransition(
        scale: scaleAnimation,
        child: Container(
          width: 140,
          height: 140,
          decoration: BoxDecoration(
            color: const Color(0xFFFFF8F0),
            borderRadius: BorderRadius.circular(28),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withAlpha(46),
                blurRadius: 32,
                spreadRadius: 4,
                offset: const Offset(0, 8),
              ),
            ],
          ),
          child: Stack(
            alignment: Alignment.center,
            children: [
              // Shield shape via icon
              CustomIconWidget(
                iconName: 'shield',
                color: const Color(0xFF8B1A52),
                size: 90,
              ),
              // Woman silhouette
              Positioned(
                top: 28,
                child: CustomIconWidget(
                  iconName: 'person',
                  color: Colors.white.withAlpha(242),
                  size: 52,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
