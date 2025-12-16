import 'package:flutter/material.dart';
import 'login_page.dart';
import 'checker_background.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen>
    with SingleTickerProviderStateMixin {
  late AnimationController controller;

  @override
  void initState() {
    super.initState();
    controller =
        AnimationController(vsync: this, duration: const Duration(seconds: 2))
          ..forward();

    Future.delayed(const Duration(seconds: 3), () {
      if (!mounted) return;
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => LoginPage()),
      );
    });
  }

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: CheckerBackground(
        child: Center(
          child: FadeTransition(
            opacity: controller,
            child: ScaleTransition(
              scale: Tween(begin: 0.85, end: 1.0).animate(controller),
              child: Text(
                "SteerMate",
                style: TextStyle(
                  fontSize: 56,
                  fontWeight: FontWeight.w900,
                  letterSpacing: 2,
                  color: Colors.white,
                  shadows: [
                    Shadow(
                      blurRadius: 30,
                      color: Colors.blueAccent.withOpacity(0.7),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
