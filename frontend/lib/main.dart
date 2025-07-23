import 'package:flutter/material.dart';
import 'ui/chat_screen.dart';
import 'config/config_loader.dart'; // <- import your config class

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Load JSON config
  await AppConfig.load();

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'YouTube QnA Bot',
      theme: ThemeData(
        primarySwatch: Colors.indigo,
      ),
      home: const ChatScreen(),
    );
  }
}
