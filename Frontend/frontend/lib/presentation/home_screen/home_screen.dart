import 'package:flutter/services.dart';

import '../../core/app_export.dart';
import '../../presentation/home_screen/widgets/home_drawer_widget.dart';
import '../../presentation/home_screen/widgets/home_feature_grid_widget.dart';
import '../../presentation/home_screen/widgets/home_track_me_widget.dart';
import '../../presentation/home_screen/widgets/home_user_card_widget.dart';
import '../../widgets/app_header.dart';
import '../../widgets/bottom_nav_bar.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  // TODO: Replace setState with Riverpod/Bloc for production
  int _currentNavIndex = 0;
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();
    SystemChrome.setSystemUIOverlayStyle(
      const SystemUiOverlayStyle(
        statusBarColor: Colors.transparent,
        statusBarIconBrightness: Brightness.dark,
      ),
    );
  }

  void _onNavTap(int index) {
    setState(() => _currentNavIndex = index);
    // TODO: Navigate to corresponding screen based on index
    // 0 = Home, 1 = Record, 3 = Fake Call, 4 = Help
  }

  @override
  Widget build(BuildContext context) {
    final isTablet = MediaQuery.of(context).size.width >= 600;

    return Scaffold(
      key: _scaffoldKey,
      backgroundColor: const Color(0xFFFFF8FA),
      drawer: const HomeDrawerWidget(),
      body: Column(
        children: [
          // Custom AppBar
          AppHeader(
            onNotificationTap: () {
              // TODO: Navigate to notifications screen
            },
            onMenuTap: () => _scaffoldKey.currentState?.openDrawer(),
          ),
          // Body
          Expanded(
            child: isTablet ? _buildTabletLayout() : _buildPhoneLayout(),
          ),
        ],
      ),
      bottomNavigationBar: SafeHerBottomNavBar(
        currentIndex: _currentNavIndex,
        onTap: _onNavTap,
      ),
    );
  }

  Widget _buildPhoneLayout() {
    return SingleChildScrollView(
      physics: const BouncingScrollPhysics(),
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const HomeUserCardWidget(),
          const SizedBox(height: 16),
          const HomeTrackMeWidget(),
          const SizedBox(height: 24),
          _buildQuickAccessHeader(),
          const SizedBox(height: 16),
          const HomeFeatureGridWidget(crossAxisCount: 2),
          const SizedBox(height: 32),
        ],
      ),
    );
  }

  Widget _buildTabletLayout() {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Left column
        Expanded(
          flex: 6,
          child: SingleChildScrollView(
            physics: const BouncingScrollPhysics(),
            padding: const EdgeInsets.all(20),
            child: Column(
              children: [
                const HomeUserCardWidget(),
                const SizedBox(height: 16),
                const HomeTrackMeWidget(),
              ],
            ),
          ),
        ),
        // Right column
        Expanded(
          flex: 4,
          child: SingleChildScrollView(
            physics: const BouncingScrollPhysics(),
            padding: const EdgeInsets.fromLTRB(8, 20, 20, 20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _buildQuickAccessHeader(),
                const SizedBox(height: 16),
                const HomeFeatureGridWidget(crossAxisCount: 2),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildQuickAccessHeader() {
    return Text(
      AppStrings.quickAccess,
      style: GoogleFonts.nunitoSans(
        fontSize: 20,
        fontWeight: FontWeight.w800,
        color: const Color(0xFF1A0A12),
      ),
    );
  }
}
