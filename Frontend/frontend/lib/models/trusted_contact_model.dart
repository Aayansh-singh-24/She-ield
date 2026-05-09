class TrustedContactModel {
  final String id;
  final String name;
  final String phone;
  final bool isSosContact;
  final String? avatarUrl;

  const TrustedContactModel({
    required this.id,
    required this.name,
    required this.phone,
    this.isSosContact = false,
    this.avatarUrl,
  });

  factory TrustedContactModel.fromMap(Map<String, dynamic> map) {
    return TrustedContactModel(
      id: map['id']?.toString() ?? '',
      name: map['name']?.toString() ?? '',
      phone: map['phone']?.toString() ?? '',
      isSosContact:
          map['isSosContact'] == true || map['isSosContact'] == 'true',
      avatarUrl: map['avatarUrl']?.toString(),
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'name': name,
      'phone': phone,
      'isSosContact': isSosContact,
      if (avatarUrl != null) 'avatarUrl': avatarUrl,
    };
  }
}
