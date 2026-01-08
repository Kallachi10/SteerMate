import 'package:flutter/material.dart';
import 'checker_background.dart';
import 'package:http/http.dart' as http;

class SignUpPage extends StatelessWidget {
  final TextEditingController email = TextEditingController();
  final TextEditingController password = TextEditingController();
  final TextEditingController confirmPassword = TextEditingController();

  bool isValidEmail(String value) {
    return RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$').hasMatch(value);
  }

  bool isStrongPassword(String value) {
    return RegExp(r'^(?=.*\d)(?=.*[@$!%*?&]).{8,}$').hasMatch(value);
  }

  void showMessage(BuildContext context, String message, bool success) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: success ? Colors.green : Colors.red,
      ),
    );
  }

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
                  "Create Account",
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
                const SizedBox(height: 16),
                _field(confirmPassword, "Confirm Password", obscure: true),
                const SizedBox(height: 24),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: () async {
                      if (!isValidEmail(email.text)) {
                        showMessage(context, "Enter a valid email address", false);
                        return;
                      }

                      if (!isStrongPassword(password.text)) {
                        showMessage(
                          context,
                          "Password must be 8+ chars with a number and symbol",
                          false,
                        );
                        return;
                      }

                      if (password.text != confirmPassword.text) {
                        showMessage(context, "Passwords do not match", false);
                        return;
                      }

                      final response = await http.post(
                        Uri.parse('http://127.0.0.1:8000/auth/register'),
                        headers: {
                          'Content-Type': 'application/x-www-form-urlencoded',
                        },
                        body: {
                          'username': email.text,
                          'password': password.text,
                        },
                      );

                      if (response.statusCode == 200 ||
                          response.statusCode == 201) {
                        showMessage(context, "Account created successfully", true);
                        Navigator.pop(context);
                      } else {
                        showMessage(context, "Registration failed", false);
                      }
                    },
                    child: const Padding(
                      padding: EdgeInsets.symmetric(vertical: 14),
                      child: Text("Sign Up", style: TextStyle(fontSize: 18)),
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
      style: const TextStyle(color: Colors.black, fontSize: 16),
      decoration: InputDecoration(
        labelText: l,
        filled: true,
        fillColor: Colors.white,
        floatingLabelBehavior: FloatingLabelBehavior.never,
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
      ),
    );
  }
}
