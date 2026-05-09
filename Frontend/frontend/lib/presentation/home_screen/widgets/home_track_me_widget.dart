
import '../../../core/app_export.dart';
import '../../../core/utils/helpers.dart';
import '../../../widgets/custom_button.dart';

class HomeTrackMeWidget extends StatefulWidget {
  const HomeTrackMeWidget({super.key});

  @override
  State<HomeTrackMeWidget> createState() => _HomeTrackMeWidgetState();
}

class _HomeTrackMeWidgetState extends State<HomeTrackMeWidget> {
  // TODO: Replace setState with Riverpod/Bloc for production
  bool _isSharing = false;

  Future<void> _handleShareLocation() async {
    setState(() => _isSharing = true);
    // TODO: Call LocationService.shareLiveLocation()
    await Future.delayed(const Duration(milliseconds: 800));
    if (mounted) {
      Helpers.showToast(context, '📍 Live location sharing started!');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Title
        Text(
          AppStrings.trackMe,
          style: GoogleFonts.nunitoSans(
            fontSize: 22,
            fontWeight: FontWeight.w800,
            color: const Color(0xFF1A0A12),
          ),
        ),
        const SizedBox(height: 4),
        Text(
          AppStrings.trackMeSubtitle,
          style: GoogleFonts.nunitoSans(
            fontSize: 13,
            fontWeight: FontWeight.w400,
            color: const Color(0xFF6B4A58),
          ),
        ),
        const SizedBox(height: 16),
        // Map placeholder card
        Container(
          height: 200,
          width: double.infinity,
          decoration: BoxDecoration(
            color: const Color(0xFFEEEEEE),
            borderRadius: BorderRadius.circular(20),
          ),
          child: Stack(
            children: [
              // Map grid lines (visual placeholder)
              ClipRRect(
                borderRadius: BorderRadius.circular(20),
                child: CustomPaint(
                  size: const Size(double.infinity, 200),
                  painter: _MapGridPainter(),
                ),
              ),
              // Center content
              Center(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Container(
                      padding: const EdgeInsets.all(14),
                      decoration: BoxDecoration(
                        color: Colors.white.withAlpha(230),
                        shape: BoxShape.circle,
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black.withAlpha(20),
                            blurRadius: 8,
                            offset: const Offset(0, 2),
                          ),
                        ],
                      ),
                      child: const CustomIconWidget(
                        iconName: 'location_off',
                        color: Color(0xFFB08090),
                        size: 28,
                      ),
                    ),
                    const SizedBox(height: 12),
                    Text(
                      AppStrings.enableLocation,
                      style: GoogleFonts.nunitoSans(
                        fontSize: 14,
                        fontWeight: FontWeight.w500,
                        color: const Color(0xFF6B4A58),
                      ),
                    ),
                    const SizedBox(height: 16),
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 32),
                      child: CustomButton(
                        label: AppStrings.shareMyLocation,
                        isLoading: _isSharing,
                        height: 46,
                        onPressed: _isSharing ? null : _handleShareLocation,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 12),
        // No friends card
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(16),
            boxShadow: [
              BoxShadow(
                color: const Color(0xFFF0437A).withAlpha(15),
                blurRadius: 12,
                offset: const Offset(0, 3),
              ),
            ],
          ),
          child: Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      AppStrings.noFriendsYet,
                      style: GoogleFonts.nunitoSans(
                        fontSize: 15,
                        fontWeight: FontWeight.w700,
                        color: const Color(0xFF1A0A12),
                      ),
                    ),
                    const SizedBox(height: 3),
                    Text(
                      AppStrings.addFriendsHint,
                      style: GoogleFonts.nunitoSans(
                        fontSize: 12,
                        fontWeight: FontWeight.w400,
                        color: const Color(0xFF6B4A58),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(width: 12),
              InkWell(
                onTap: () {
                  // TODO: Navigate to trusted contacts screen
                },
                borderRadius: BorderRadius.circular(12),
                child: Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 22,
                    vertical: 12,
                  ),
                  decoration: BoxDecoration(
                    color: const Color(0xFF8B1A52),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Text(
                    AppStrings.add,
                    style: GoogleFonts.nunitoSans(
                      fontSize: 14,
                      fontWeight: FontWeight.w700,
                      color: Colors.white,
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}

class _MapGridPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = const Color(0xFFDDDDDD)
      ..strokeWidth = 1;

    const step = 30.0;
    for (double x = 0; x < size.width; x += step) {
      canvas.drawLine(Offset(x, 0), Offset(x, size.height), paint);
    }
    for (double y = 0; y < size.height; y += step) {
      canvas.drawLine(Offset(0, y), Offset(size.width, y), paint);
    }

    // Road-like horizontal band
    final roadPaint = Paint()
      ..color = const Color(0xFFC8C8C8)
      ..strokeWidth = 12;
    canvas.drawLine(
      Offset(0, size.height * 0.45),
      Offset(size.width, size.height * 0.45),
      roadPaint,
    );
    canvas.drawLine(
      Offset(size.width * 0.55, 0),
      Offset(size.width * 0.55, size.height),
      roadPaint,
    );
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
