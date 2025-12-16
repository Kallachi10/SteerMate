import 'package:flutter/material.dart';

class CheckerBackground extends StatelessWidget {
  final Widget child;
  const CheckerBackground({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
        gradient: LinearGradient(
          colors: [Color(0xFF0B1220), Color(0xFF0F172A)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
      ),
      child: CustomPaint(
        painter: _CheckerPainter(),
        child: child,
      ),
    );
  }
}

class _CheckerPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    const double s = 40;
    final paint = Paint()..color = Colors.white.withOpacity(0.035);

    for (double x = 0; x < size.width; x += s) {
      for (double y = 0; y < size.height; y += s) {
        if (((x + y) ~/ s) % 2 == 0) {
          canvas.drawRect(Rect.fromLTWH(x, y, s, s), paint);
        }
      }
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) {
    return false;
  }
}
