import 'package:flutter/material.dart';
import 'splash_screen.dart';

void main() {
  runApp(const MyApp());
}

final ValueNotifier<ThemeMode> themeNotifier =
    ValueNotifier(ThemeMode.dark);

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder(
      valueListenable: themeNotifier,
      builder: (_, ThemeMode mode, __) {
        return MaterialApp(
          debugShowCheckedModeBanner: false,
          themeMode: mode,
          theme: ThemeData.light(useMaterial3: true),
          darkTheme: ThemeData.dark(useMaterial3: true),
          home: const SplashScreen(),
        );
      },
    );
  }
}
