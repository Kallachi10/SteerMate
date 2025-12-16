import 'package:flutter/material.dart';
import 'checker_background.dart';

class HomeDashboard extends StatelessWidget {
  const HomeDashboard({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: CheckerBackground(
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  "Welcome Back!",
                  style: TextStyle(
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),

                SizedBox(height: 16),

                Text(
                  "Your Driving Summary",
                  style: TextStyle(
                    fontSize: 16,
                    color: Colors.white70,
                  ),
                ),

                SizedBox(height: 20),

                // ✅ YOUR ORIGINAL SUMMARY CARD (UNCHANGED)
                Container(
                  width: double.infinity,
                  padding: EdgeInsets.all(20),
                  decoration: BoxDecoration(
                    color: const Color.fromARGB(255, 39, 86, 119),
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: const [
                      Text(
                        "Last Trip Summary",
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                      SizedBox(height: 12),
                      Text("Distance: 12.5 km"),
                      Text("Avg Speed: 42 km/h"),
                      Text("Hard Brakes: 2"),
                      Text("Overspeed Alerts: 1"),
                    ],
                  ),
                ),

                SizedBox(height: 40),

                // ✅ YOUR ORIGINAL BUTTON (UNCHANGED)
                Center(
                  child: SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        padding: EdgeInsets.symmetric(vertical: 14),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                      ),
                      onPressed: () {
                        // TODO: Navigate to Start Trip / Sensor Page
                      },
                      child: Text(
                        "Start Trip",
                        style: TextStyle(fontSize: 18),
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
