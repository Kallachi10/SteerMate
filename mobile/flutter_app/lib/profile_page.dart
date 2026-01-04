import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'checker_background.dart';
import 'main.dart';

class ProfilePage extends StatefulWidget {
  const ProfilePage({super.key});

  @override
  State<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  bool _loading = false;
  String? _error;
  Map<String, dynamic>? _profile;

  // TODO: Replace this with secure storage (SharedPreferences / secure_storage)
  // You can also expose a way to set this token in debug builds.
  static const String _token =
      'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxNzY4MDMyODY4fQ.lnNf6MyDHZjcpKKmsc7zJ-mxYPJoVJQv2Sn26vHWp60';

  @override
  void initState() {
    super.initState();
    _fetchProfile();
  }

  Future<void> _fetchProfile() async {
    setState(() {
      _loading = true;
      _error = null;
    });

    try {
      final res = await http.get(
        Uri.parse('http://127.0.0.1:8000/user/profile'),
        headers: {
          'accept': 'application/json',
          'Authorization': 'Bearer $_token',
        },
      );

      if (res.statusCode == 200) {
        final data = json.decode(res.body);
        setState(() {
          if (data is Map<String, dynamic>) {
            _profile = data;
          } else if (data is List) {
            _profile = {'items': data};
          } else {
            _profile = {'value': data.toString()};
          }
        });
      } else {
        setState(() {
          _error = 'Error ${res.statusCode}: ${res.body}';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Request failed: $e';
      });
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  Widget _buildProfileView() {
    if (_loading) return const Center(child: CircularProgressIndicator());

    if (_error != null) {
      return Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(_error!, style: const TextStyle(color: Colors.white)),
            const SizedBox(height: 12),
            ElevatedButton.icon(
              onPressed: _fetchProfile,
              icon: const Icon(Icons.refresh),
              label: const Text('Retry'),
            ),
          ],
        ),
      );
    }

    if (_profile == null) {
      return Center(
        child: ElevatedButton.icon(
          onPressed: _fetchProfile,
          icon: const Icon(Icons.download),
          label: const Text('Load profile'),
        ),
      );
    }

    final name = _profile!['name'] ?? _profile!['username'] ?? 'Unknown';
    final email = _profile!['email'] ?? '';

    // Header
    final header = Column(
      children: [
        CircleAvatar(
          radius: 48,
          backgroundColor: Colors.white.withOpacity(0.12),
          child: Text(
            _initials(name),
            style: const TextStyle(fontSize: 28, color: Colors.white, fontWeight: FontWeight.bold),
          ),
        ),
        const SizedBox(height: 12),
        Text(name, style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.white)),
        if (email.isNotEmpty) ...[
          const SizedBox(height: 6),
          Text(email, style: TextStyle(color: Colors.white.withOpacity(0.85))),
        ],
        const SizedBox(height: 16),
      ],
    );

    // Build list of info cards, skipping obvious header fields
    final excluded = {'name', 'username', 'email'};
    final keys = _profile!.keys.where((k) => !excluded.contains(k)).toList();

    final List<Widget> infoCards = keys.map((k) {
      final v = _profile![k];
      final String value = v == null ? '' : (v is List ? v.join(', ') : (v is Map ? json.encode(v) : v.toString()));

      return Card(
        elevation: 2,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        margin: const EdgeInsets.symmetric(vertical: 8),
        child: ListTile(
          leading: CircleAvatar(
            backgroundColor: Theme.of(context).colorScheme.primary,
            child: Icon(_iconForKey(k), color: Colors.white, size: 20),
          ),
          title: Text(_prettyKey(k), style: const TextStyle(fontWeight: FontWeight.w600)),
          subtitle: Text(value),
          trailing: IconButton(
            icon: const Icon(Icons.copy),
            onPressed: () {
              Clipboard.setData(ClipboardData(text: value));
              ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Copied')));
            },
          ),
        ),
      );
    }).toList();

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.only(bottom: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          header,
          if (infoCards.isEmpty)
            Card(
              elevation: 2,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              child: const Padding(
                padding: EdgeInsets.all(16.0),
                child: Text('No profile details available'),
              ),
            )
          else
            ...infoCards,
        ],
      ),
    );
  }

  IconData _iconForKey(String key) {
    final k = key.toLowerCase();
    if (k.contains('email')) return Icons.email;
    if (k.contains('phone') || k.contains('mobile')) return Icons.phone;
    if (k.contains('car') || k.contains('vehicle')) return Icons.directions_car;
    if (k.contains('address') || k.contains('city') || k.contains('country')) return Icons.location_on;
    if (k.contains('license') || k.contains('plate')) return Icons.badge;
    if (k.contains('role') || k.contains('type')) return Icons.person_outline;
    return Icons.info_outline;
  }

  String _prettyKey(String key) {
    return key.replaceAllMapped(RegExp(r'[_-]'), (m) => ' ').split(' ').map((w) => w.isEmpty ? '' : '${w[0].toUpperCase()}${w.substring(1)}').join(' ');
  }

  String _initials(String name) {
    final parts = name.split(RegExp(r'\s+')).where((p) => p.isNotEmpty).toList();
    if (parts.isEmpty) return '';
    if (parts.length == 1) return parts.first.substring(0, 1).toUpperCase();
    return (parts[0][0] + parts[1][0]).toUpperCase();
  }

  @override
  Widget build(BuildContext context) {
    return CheckerBackground(
      child: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const CircleAvatar(radius: 48, child: Icon(Icons.person, size: 48)),
              const SizedBox(height: 16),
              const Text("Driver Profile",
                  style: TextStyle(fontSize: 22, color: Colors.white)),
              const SizedBox(height: 24),
              // Make the profile content scrollable to avoid overflow on small screens
              Expanded(
                child: SingleChildScrollView(
                  child: _buildProfileView(),
                ),
              ),
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
