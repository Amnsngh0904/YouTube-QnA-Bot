import 'dart:convert';
import 'package:flutter/services.dart' show rootBundle;

class AppConfig {
  static late String backendUrl;

  static Future<void> load() async {
    final configString = await rootBundle.loadString('assets/env.json');
    final config = json.decode(configString);
    backendUrl = config['BACKEND_URL'];
  }
}
