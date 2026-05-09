import 'package:flutter/material.dart';
import '../core/app_export.dart';

class LoadingView extends StatefulWidget {
  final int itemCount;
  final double itemHeight;

  const LoadingView({super.key, this.itemCount = 5, this.itemHeight = 80});

  @override
  State<LoadingView> createState() => _LoadingViewState();
}

class _LoadingViewState extends State<LoadingView>
    with SingleTickerProviderStateMixin {
  late AnimationController _shimmerController;
  late Animation<double> _shimmerAnimation;

  @override
  void initState() {
    super.initState();
    _shimmerController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1200),
    )..repeat();
    _shimmerAnimation = Tween<double>(begin: -1.0, end: 2.0).animate(
      CurvedAnimation(parent: _shimmerController, curve: Curves.easeInOutSine),
    );
  }

  @override
  void dispose() {
    _shimmerController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ListView.separated(
      physics: const NeverScrollableScrollPhysics(),
      shrinkWrap: true,
      itemCount: widget.itemCount,
      separatorBuilder: (context, index) => const SizedBox(height: 12),
      itemBuilder: (context, index) => AnimatedBuilder(
        animation: _shimmerAnimation,
        builder: (context, child) {
          return Container(
            height: widget.itemHeight,
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(16),
              gradient: LinearGradient(
                begin: Alignment.centerLeft,
                end: Alignment.centerRight,
                stops: [
                  (_shimmerAnimation.value - 0.4).clamp(0.0, 1.0),
                  _shimmerAnimation.value.clamp(0.0, 1.0),
                  (_shimmerAnimation.value + 0.4).clamp(0.0, 1.0),
                ],
                colors: const [
                  Color(0xFFFFF0F5),
                  Color(0xFFFFE0EC),
                  Color(0xFFFFF0F5),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
