import 'package:flutter/material.dart';
import 'checker_background.dart';
import 'main.dart';

class ProfilePage extends StatelessWidget {
  const ProfilePage({super.key});

  @override
  Widget build(BuildContext context) {
    return CheckerBackground(
      child: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            children: [
              const CircleAvatar(radius: 48, child: Icon(Icons.person, size: 48)),
              const SizedBox(height: 16),
              const Text("Driver Profile",
                  style: TextStyle(fontSize: 22, color: Colors.white)),
              const SizedBox(height: 24),
              SwitchListTile(
                title: const Text("Dark Mode",
                    style: TextStyle(color: Colors.white)),
                value: themeNotifier.value == ThemeMode.dark,
                onChanged: (_) {
                  themeNotifier.value =
                      themeNotifier.value == ThemeMode.dark
                          ? ThemeMode.light
                          : ThemeMode.dark;
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
