
import '../../../core/app_export.dart';
import '../../../widgets/feature_card.dart';

class HomeFeatureGridWidget extends StatelessWidget {
  final int crossAxisCount;

  const HomeFeatureGridWidget({super.key, this.crossAxisCount = 2});

  @override
  Widget build(BuildContext context) {
    final features = _buildFeatureList(context);

    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: crossAxisCount,
        crossAxisSpacing: 12,
        mainAxisSpacing: 12,
        childAspectRatio: 1.05,
      ),
      itemCount: features.length,
      itemBuilder: (context, index) {
        final f = features[index];
        return FeatureCard(
          title: f['title'] as String,
          subtitle: f['subtitle'] as String,
          iconName: f['iconName'] as String,
          iconBgColor: f['iconBgColor'] as Color,
          iconColor: f['iconColor'] as Color,
          onTap: f['onTap'] as VoidCallback?,
          animationDelay: index * 60,
        );
      },
    );
  }

  List<Map<String, dynamic>> _buildFeatureList(BuildContext context) {
    return [
      {
        'title': AppStrings.stressCheck,
        'subtitle': AppStrings.stressCheckSub,
        'iconName': 'favorite',
        'iconBgColor': const Color(0xFFFFE0EC),
        'iconColor': const Color(0xFFF0437A),
        'onTap': () {
          // TODO: Navigate to stress assessment screen
        },
      },
      {
        'title': AppStrings.cycleTracker,
        'subtitle': AppStrings.cycleTrackerSub,
        'iconName': 'water_drop',
        'iconBgColor': const Color(0xFFFFE0EC),
        'iconColor': const Color(0xFFE91E8C),
        'onTap': () {
          // TODO: Navigate to cycle tracker screen
        },
      },
      {
        'title': AppStrings.chatSupport,
        'subtitle': AppStrings.chatSupportSub,
        'iconName': 'chat',
        'iconBgColor': const Color(0xFFFFE8E8),
        'iconColor': const Color(0xFFD32F2F),
        'onTap': () {
          // TODO: Navigate to chat support screen
        },
      },
      {
        'title': AppStrings.wellnessTips,
        'subtitle': AppStrings.wellnessTipsSub,
        'iconName': 'spa',
        'iconBgColor': const Color(0xFFE0F5EC),
        'iconColor': const Color(0xFF2D9E6B),
        'onTap': () {
          // TODO: Navigate to wellness tips screen
        },
      },
      {
        'title': AppStrings.trustedContacts,
        'subtitle': AppStrings.trustedContactsSub,
        'iconName': 'group',
        'iconBgColor': const Color(0xFFEDE0F5),
        'iconColor': const Color(0xFF8B1A52),
        'onTap': () {
          // TODO: Navigate to trusted contacts screen
        },
      },
      {
        'title': AppStrings.emergencyHelp,
        'subtitle': AppStrings.emergencyHelpSub,
        'iconName': 'local_police',
        'iconBgColor': const Color(0xFFDEEBFF),
        'iconColor': const Color(0xFF1565C0),
        'onTap': () {
          // TODO: Navigate to emergency help screen
        },
      },
      {
        'title': AppStrings.alertHistory,
        'subtitle': AppStrings.alertHistorySub,
        'iconName': 'history',
        'iconBgColor': const Color(0xFFFDE8D8),
        'iconColor': const Color(0xFFE07B39),
        'onTap': () {
          // TODO: Navigate to alert history screen
        },
      },
      {
        'title': AppStrings.safetyMap,
        'subtitle': AppStrings.safetyMapSub,
        'iconName': 'map',
        'iconBgColor': const Color(0xFFE0F5EC),
        'iconColor': const Color(0xFF1B7A4F),
        'onTap': () {
          // TODO: Navigate to safety map screen
        },
      },
    ];
  }
}
