import 'package:flutter/material.dart';

class EmergencyNumberModel {
  final String number;
  final String label;
  final String iconName;
  final Color iconBgColor;
  final Color iconColor;

  const EmergencyNumberModel({
    required this.number,
    required this.label,
    required this.iconName,
    required this.iconBgColor,
    required this.iconColor,
  });

  factory EmergencyNumberModel.fromMap(Map<String, dynamic> map) {
    return EmergencyNumberModel(
      number: map['number']?.toString() ?? '',
      label: map['label']?.toString() ?? '',
      iconName: map['iconName']?.toString() ?? 'phone',
      iconBgColor: Color(map['iconBgColor'] as int? ?? 0xFFFFE0EC),
      iconColor: Color(map['iconColor'] as int? ?? 0xFFF0437A),
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'number': number,
      'label': label,
      'iconName': iconName,
      'iconBgColor': iconBgColor.toARGB32,
      'iconColor': iconColor.toARGB32,
    };
  }
}
