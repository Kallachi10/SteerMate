import 'package:flutter/material.dart';
import 'home_dashboard.dart';
//import 'checker_background.dart';
//import 'main.dart';

import 'trips_page.dart';
import 'analytics_page.dart';
import 'profile_page.dart';


class MainNavigation extends StatefulWidget {
  const MainNavigation({super.key});

  @override
  State<MainNavigation> createState() => _MainNavigationState();
}

class _MainNavigationState extends State<MainNavigation> {
  int index = 0;

  final pages = const [
    HomeDashboard(),
    TripsPage(),
    AnalyticsPage(),
    ProfilePage(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: pages[index],
      bottomNavigationBar: NavigationBar(
        selectedIndex: index,
        onDestinationSelected: (i) => setState(() => index = i),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home), label: "Home"),
          NavigationDestination(icon: Icon(Icons.map), label: "Trips"),
          NavigationDestination(icon: Icon(Icons.show_chart), label: "Analytics"),
          NavigationDestination(icon: Icon(Icons.person), label: "Profile"),
        ],
      ),
    );
  }
}

// class TripsPage extends StatelessWidget {
//   const TripsPage({super.key});
//   @override
//   Widget build(BuildContext context) =>
//       const CheckerBackground(child: Center(child: Text("Trips Page", style: TextStyle(color: Colors.white, fontSize: 24))));
// }

// class AnalyticsPage extends StatelessWidget {
//   const AnalyticsPage({super.key});
//   @override
//   Widget build(BuildContext context) =>
//       const CheckerBackground(child: Center(child: Text("Analytics Page", style: TextStyle(color: Colors.white, fontSize: 24))));
// }

// class ProfilePage extends StatelessWidget {
//   const ProfilePage({super.key});

//   @override
//   Widget build(BuildContext context) {
//     return CheckerBackground(
//       child: SafeArea(
//         child: Padding(
//           padding: const EdgeInsets.all(24),
//           child: Column(
//             children: [
//               const CircleAvatar(
//                 radius: 48,
//                 child: Icon(Icons.person, size: 48),
//               ),
//               const SizedBox(height: 16),
//               const Text("Driver Profile",
//                   style: TextStyle(fontSize: 22, color: Colors.white)),
//               const SizedBox(height: 24),
//               SwitchListTile(
//                 title: const Text("Dark Mode",
//                     style: TextStyle(color: Colors.white)),
//                 value: themeNotifier.value == ThemeMode.dark,
//                 onChanged: (_) => themeNotifier.value =
//                     themeNotifier.value == ThemeMode.dark
//                         ? ThemeMode.light
//                         : ThemeMode.dark,
//               ),
//             ],
//           ),
//         ),
//       ),
//     );
//   }
// }
