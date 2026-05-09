
import '../core/app_export.dart';
import '../models/emergency_number_model.dart';

class EmergencyCard extends StatelessWidget {
  final EmergencyNumberModel emergency;
  final VoidCallback? onCallTap;

  const EmergencyCard({super.key, required this.emergency, this.onCallTap});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
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
          Container(
            width: 52,
            height: 52,
            decoration: BoxDecoration(
              color: emergency.iconBgColor,
              borderRadius: BorderRadius.circular(14),
            ),
            child: Center(
              child: CustomIconWidget(
                iconName: emergency.iconName,
                color: emergency.iconColor,
                size: 26,
              ),
            ),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  emergency.number,
                  style: GoogleFonts.nunitoSans(
                    fontSize: 20,
                    fontWeight: FontWeight.w800,
                    color: const Color(0xFF1A0A12),
                  ),
                ),
                Text(
                  emergency.label,
                  style: GoogleFonts.nunitoSans(
                    fontSize: 13,
                    fontWeight: FontWeight.w500,
                    color: const Color(0xFF6B4A58),
                  ),
                ),
              ],
            ),
          ),
          InkWell(
            onTap: onCallTap,
            borderRadius: BorderRadius.circular(50),
            child: Container(
              width: 48,
              height: 48,
              decoration: const BoxDecoration(
                gradient: LinearGradient(
                  colors: [Color(0xFFF0437A), Color(0xFFE91E8C)],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                shape: BoxShape.circle,
              ),
              child: const Center(
                child: CustomIconWidget(
                  iconName: 'call',
                  color: Colors.white,
                  size: 22,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
