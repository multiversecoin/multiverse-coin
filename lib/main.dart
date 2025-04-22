import 'package:flutter/material.dart';

void main() {
  runApp(MoedaMultiversoApp());
}

class MoedaMultiversoApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Moeda Multiverso',
      theme: ThemeData(
        primarySwatch: Colors.deepPurple,
      ),
      home: PaginaInicial(),
    );
  }
}

class PaginaInicial extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Moeda Multiverso'),
      ),
      body: Center(
        child: Text(
          'Bem-vindo à moeda digital de Moema!',
          style: TextStyle(fontSize: 20),
        ),
      ),
    );
  }
}
