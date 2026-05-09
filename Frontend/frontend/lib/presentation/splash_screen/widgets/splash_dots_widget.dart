import 'package:flutter/material.dart';

class SplashDotsWidget extends StatefulWidget {
  final AnimationController controller;

  const SplashDotsWidget({super.key, required this.controller});

  @override
  State<SplashDotsWidget> createState() => _SplashDotsWidgetState();
}

class _SplashDotsWidgetState extends State<SplashDotsWidget>
    with TickerProviderStateMixin {
  late List<AnimationController> _dotControllers;
  late List<Animation<double>> _dotAnimations;

  @override
  void initState() {
    super.initState();
    _dotControllers = List.generate(
      3,
      (i) => AnimationController(
        vsync: this,
        duration: const Duration(milliseconds: 600),
      ),
    );
    _dotAnimations = _dotControllers
        .map(
          (c) => Tween<double>(
            begin: 0.5,
            end: 1.0,
          ).animate(CurvedAnimation(parent: c, curve: Curves.easeInOut)),
        )
        .toList();

    _startSequence();
  }

  void _startSequence() async {
    while (mounted) {
      for (int i = 0; i < 3; i++) {
        if (!mounted) return;
        _dotControllers[i].forward().then((_) => _dotControllers[i].reverse());
        await Future.delayed(const Duration(milliseconds: 180));
      }
      await Future.delayed(const Duration(milliseconds: 400));
    }
  }

  @override
  void dispose() {
    for (final c in _dotControllers) {
      c.dispose();
    }
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: List.generate(3, (i) {
        return AnimatedBuilder(
          animation: _dotAnimations[i],
          builder: (context, _) {
            return Container(
              margin: const EdgeInsets.symmetric(horizontal: 5),
              width: 10 * _dotAnimations[i].value,
              height: 10 * _dotAnimations[i].value,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: Colors.white.withValues(
                  alpha: 0.5 + 0.5 * (_dotAnimations[i].value - 0.5) / 0.5,
                ),
              ),
            );
          },
        );
      }),
    );
  }
}
