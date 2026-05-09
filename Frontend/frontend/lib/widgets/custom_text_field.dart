import 'package:flutter/services.dart';

import '../core/app_export.dart';

class CustomTextField extends StatefulWidget {
  final String label;
  final String? hint;
  final TextEditingController? controller;
  final String? Function(String?)? validator;
  final TextInputType keyboardType;
  final bool obscureText;
  final Widget? prefixWidget;
  final Widget? suffixWidget;
  final int? maxLines;
  final List<TextInputFormatter>? inputFormatters;
  final void Function(String)? onChanged;
  final bool readOnly;
  final VoidCallback? onTap;

  const CustomTextField({
    super.key,
    required this.label,
    this.hint,
    this.controller,
    this.validator,
    this.keyboardType = TextInputType.text,
    this.obscureText = false,
    this.prefixWidget,
    this.suffixWidget,
    this.maxLines = 1,
    this.inputFormatters,
    this.onChanged,
    this.readOnly = false,
    this.onTap,
  });

  @override
  State<CustomTextField> createState() => _CustomTextFieldState();
}

class _CustomTextFieldState extends State<CustomTextField> {
  bool _isFocused = false;
  bool _obscure = true;

  @override
  void initState() {
    super.initState();
    _obscure = widget.obscureText;
  }

  @override
  Widget build(BuildContext context) {
    return Focus(
      onFocusChange: (focused) => setState(() => _isFocused = focused),
      child: TextFormField(
        controller: widget.controller,
        validator: widget.validator,
        keyboardType: widget.keyboardType,
        obscureText: widget.obscureText ? _obscure : false,
        maxLines: widget.obscureText ? 1 : widget.maxLines,
        inputFormatters: widget.inputFormatters,
        onChanged: widget.onChanged,
        readOnly: widget.readOnly,
        onTap: widget.onTap,
        style: GoogleFonts.nunitoSans(
          fontSize: 15,
          fontWeight: FontWeight.w500,
          color: const Color(0xFF1A0A12),
        ),
        decoration: InputDecoration(
          labelText: widget.label,
          hintText: widget.hint,
          filled: true,
          fillColor: Colors.white,
          prefixIcon: widget.prefixWidget,
          suffixIcon: widget.obscureText
              ? IconButton(
                  onPressed: () => setState(() => _obscure = !_obscure),
                  icon: CustomIconWidget(
                    iconName: _obscure ? 'visibility' : 'visibility_off',
                    color: const Color(0xFFB08090),
                    size: 20,
                  ),
                )
              : widget.suffixWidget,
          contentPadding: const EdgeInsets.symmetric(
            horizontal: 20,
            vertical: 16,
          ),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(16),
            borderSide: const BorderSide(color: Color(0xFFE8D0DA), width: 1.5),
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(16),
            borderSide: const BorderSide(color: Color(0xFFE8D0DA), width: 1.5),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(16),
            borderSide: const BorderSide(color: Color(0xFFF0437A), width: 2),
          ),
          errorBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(16),
            borderSide: const BorderSide(color: Color(0xFFD32F2F), width: 1.5),
          ),
          focusedErrorBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(16),
            borderSide: const BorderSide(color: Color(0xFFD32F2F), width: 2),
          ),
          labelStyle: GoogleFonts.nunitoSans(
            fontSize: 14,
            fontWeight: FontWeight.w600,
            color: _isFocused
                ? const Color(0xFFF0437A)
                : const Color(0xFF6B4A58),
          ),
          hintStyle: GoogleFonts.nunitoSans(
            fontSize: 14,
            fontWeight: FontWeight.w400,
            color: const Color(0xFFB08090),
          ),
          errorStyle: GoogleFonts.nunitoSans(
            fontSize: 12,
            fontWeight: FontWeight.w500,
            color: const Color(0xFFD32F2F),
          ),
        ),
      ),
    );
  }
}
