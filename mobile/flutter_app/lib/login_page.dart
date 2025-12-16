import 'package:flutter/material.dart';
import 'main_navigation.dart';
import 'checker_background.dart';

class LoginPage extends StatelessWidget {
  final TextEditingController email = TextEditingController();
  final TextEditingController password = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: CheckerBackground(
        child: Center(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Text(
                  "Welcome Back",
                  style: TextStyle(
                    fontSize: 26,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
                const SizedBox(height: 32),
                _field(email, "Email"),
                const SizedBox(height: 16),
                _field(password, "Password", obscure: true),
                const SizedBox(height: 24),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: () {
                      Navigator.pushReplacement(
                        context,
                        MaterialPageRoute(
                          builder: (_) => const MainNavigation(),
                        ),
                      );
                    },
                    child: const Padding(
                      padding: EdgeInsets.symmetric(vertical: 14),
                      child: Text("Login", style: TextStyle(fontSize: 18)),
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

  Widget _field(TextEditingController c, String l, {bool obscure = false}) {
    return TextField(
      controller: c,
      obscureText: obscure,
      decoration: InputDecoration(
        labelText: l,
        filled: true,
        fillColor: Colors.white,
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
      ),
    );
  }
}
