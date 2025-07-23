import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter_dotenv/flutter_dotenv.dart';

class ApiService {
  // Load base URL from .env file, fallback to localhost if not found
  static final String baseUrl = dotenv.env['BACKEND_URL'] ?? 'http://127.0.0.1:8000';

  static Future<String> askQuestion(String question) async {
    final response = await http.post(
      Uri.parse('$baseUrl/qna'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'question': question}),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body)['answer'];
    } else {
      throw Exception('Failed to get response from backend: ${response.statusCode}');
    }
  }
}
