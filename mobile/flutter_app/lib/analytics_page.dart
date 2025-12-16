import 'package:flutter/material.dart';
import 'checker_background.dart';

class AnalyticsPage extends StatelessWidget {
  const AnalyticsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return CheckerBackground(
      child: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: SingleChildScrollView(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  "Analytics",
                  style: TextStyle(
                    fontSize: 26,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
                const SizedBox(height: 24),

                const Text(
                  "Safety Score Dashboard",
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                    color: Colors.white,
                  ),
                ),
                const SizedBox(height: 16),

                _statCard("Average Weekly Score", "82 / 100"),
                const SizedBox(height: 16),
                _statCard("Hard Braking Trend", "Improving"),
                const SizedBox(height: 16),
                _statCard("Overspeed Heatmap", "3 Hot Zones"),
                const SizedBox(height: 16),
                _statCard("Road Sign Compliance", "92%"),
                const SizedBox(height: 16),
                _statCard("Driving Behavior Comparison", "Better than last week"),

                const SizedBox(height: 32),

                const Text(
                  "Insights & Recommendations",
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                    color: Colors.white,
                  ),
                ),
                const SizedBox(height: 16),

                _insightCard("Brake earlier to reduce hard braking events"),
                const SizedBox(height: 12),
                _insightCard("Reduce cornering speed on sharp turns"),
                const SizedBox(height: 12),
                _insightCard("Follow posted speed limits near signboards"),
                const SizedBox(height: 12),
                _insightCard("Improve compliance at stop and speed-limit signs"),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _statCard(String title, String value) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: const Color.fromARGB(255, 39, 86, 119),
        borderRadius: BorderRadius.circular(16),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title,
              style: const TextStyle(color: Colors.white70, fontSize: 14)),
          const SizedBox(height: 8),
          Text(value,
              style: const TextStyle(
                color: Colors.white,
                fontSize: 22,
                fontWeight: FontWeight.bold,
              )),
        ],
      ),
    );
  }

  Widget _insightCard(String text) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color.fromARGB(255, 28, 66, 94),
        borderRadius: BorderRadius.circular(14),
      ),
      child: Text(
        text,
        style: const TextStyle(
          color: Colors.white,
          fontSize: 15,
        ),
      ),
    );
  }
}
