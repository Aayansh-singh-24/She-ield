enum AlertStatus { sent, failed, pending }

class AlertModel {
  final String id;
  final String threatType;
  final DateTime triggeredAt;
  final AlertStatus status;
  final double? lat;
  final double? lng;
  final int contactsNotified;

  const AlertModel({
    required this.id,
    required this.threatType,
    required this.triggeredAt,
    required this.status,
    this.lat,
    this.lng,
    this.contactsNotified = 0,
  });

  static AlertStatus _statusFromString(String v) {
    switch (v) {
      case 'sent':
        return AlertStatus.sent;
      case 'failed':
        return AlertStatus.failed;
      case 'pending':
      default:
        return AlertStatus.pending;
    }
  }

  factory AlertModel.fromMap(Map<String, dynamic> map) {
    return AlertModel(
      id: map['id']?.toString() ?? '',
      threatType: map['threatType']?.toString() ?? 'manual_sos',
      triggeredAt:
          DateTime.tryParse(map['triggeredAt']?.toString() ?? '') ??
          DateTime.now(),
      status: _statusFromString(map['status']?.toString() ?? 'pending'),
      lat: (map['lat'] as num?)?.toDouble(),
      lng: (map['lng'] as num?)?.toDouble(),
      contactsNotified: (map['contactsNotified'] as num?)?.toInt() ?? 0,
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'threatType': threatType,
      'triggeredAt': triggeredAt.toIso8601String(),
      'status': status.name,
      if (lat != null) 'lat': lat,
      if (lng != null) 'lng': lng,
      'contactsNotified': contactsNotified,
    };
  }
}
