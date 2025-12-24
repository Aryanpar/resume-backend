import 'dart:io';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class ResumeUploadScreen extends StatefulWidget {
  const ResumeUploadScreen({super.key});

  @override
  State<ResumeUploadScreen> createState() => _ResumeUploadScreenState();
}

class _ResumeUploadScreenState extends State<ResumeUploadScreen> {
  File? selectedFile;
  String? fileName;
  bool isLoading = false;

  int scanCount = 0;
  List<String> recentScans = [];

  // ================= PICK PDF =================
  Future<void> pickPdf() async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf'],
    );

    if (result == null || result.files.single.path == null) return;

    setState(() {
      selectedFile = File(result.files.single.path!);
      fileName = result.files.single.name;
    });

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text("File selected: $fileName"),
        backgroundColor: Colors.green,
      ),
    );
  }

  // ================= ANALYZE =================
  Future<void> analyzeResume() async {
    if (selectedFile == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Please upload a resume first"),
          backgroundColor: Colors.redAccent,
        ),
      );
      return;
    }

    setState(() => isLoading = true);

    try {
      final result = await ApiService.analyzePdf(selectedFile!);

      final int score =
          int.tryParse(result["score"].toString()) ?? 0;

      final List<String> feedback =
          (result["feedback"] as List).map((e) => e.toString()).toList();

      setState(() {
        scanCount++;
        recentScans.insert(0, fileName!);
      });

      _showResultPopup(score, feedback);
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text("Failed to analyze resume: $e"),
          backgroundColor: Colors.redAccent,
        ),
      );
    } finally {
      setState(() => isLoading = false);
    }
  }

  // ================= RESULT POPUP =================
  void _showResultPopup(int score, List<String> feedback) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.white,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(18)),
      ),
      builder: (_) {
        return Padding(
          padding: const EdgeInsets.all(18),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  const Text(
                    "Resume Score",
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const Spacer(),
                  IconButton(
                    onPressed: () => Navigator.pop(context),
                    icon: const Icon(Icons.close),
                  )
                ],
              ),

              Center(
                child: Text(
                  "$score / 100",
                  style: const TextStyle(
                    fontSize: 34,
                    fontWeight: FontWeight.bold,
                    color: Colors.blueAccent,
                  ),
                ),
              ),

              const SizedBox(height: 18),

              const Text(
                "Suggestions",
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w600,
                ),
              ),

              const SizedBox(height: 10),

              ...feedback.map(
                (f) => Padding(
                  padding: const EdgeInsets.only(bottom: 8),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text("• "),
                      Expanded(child: Text(f)),
                    ],
                  ),
                ),
              ),

              const SizedBox(height: 20),
            ],
          ),
        );
      },
    );
  }

  // ================= UI =================
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(18),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _topBar(),
              const SizedBox(height: 30),
              _uploadBox(),
              if (fileName != null) _selectedFileInfo(),
              const SizedBox(height: 24),
              _analyzeButton(),
              const SizedBox(height: 30),
              _recentScans(),
            ],
          ),
        ),
      ),
    );
  }

  // ================= COMPONENTS =================

  Widget _topBar() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: const [
        Text(
          "AI Resume Analyzer",
          style: TextStyle(
            color: Colors.white,
            fontSize: 20,
            fontWeight: FontWeight.w600,
          ),
        ),
        CircleAvatar(
          backgroundColor: Colors.white12,
          child: Icon(Icons.person, color: Colors.white),
        )
      ],
    );
  }

  Widget _uploadBox() {
    return GestureDetector(
      onTap: pickPdf,
      child: Container(
        height: 160,
        width: double.infinity,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(14),
          border: Border.all(color: Colors.blueAccent, width: 2),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: const [
            Icon(Icons.upload_file, color: Colors.blueAccent, size: 42),
            SizedBox(height: 10),
            Text(
              "Tap to upload resume (PDF)",
              style: TextStyle(color: Colors.blueAccent),
            )
          ],
        ),
      ),
    );
  }

  Widget _selectedFileInfo() {
    return Padding(
      padding: const EdgeInsets.only(top: 12),
      child: Row(
        children: [
          const Icon(Icons.picture_as_pdf, color: Colors.redAccent, size: 18),
          const SizedBox(width: 8),
          Expanded(
            child: Text(
              fileName!,
              style: const TextStyle(
                color: Colors.white70,
                fontSize: 12,
              ),
              overflow: TextOverflow.ellipsis,
            ),
          ),
          IconButton(
            icon: const Icon(Icons.close, color: Colors.white54, size: 18),
            onPressed: () {
              setState(() {
                selectedFile = null;
                fileName = null;
              });
            },
          )
        ],
      ),
    );
  }

  Widget _analyzeButton() {
    return SizedBox(
      width: double.infinity,
      child: OutlinedButton(
        onPressed:
            (selectedFile == null || isLoading) ? null : analyzeResume,
        style: OutlinedButton.styleFrom(
          side: const BorderSide(color: Colors.blueAccent),
          padding: const EdgeInsets.symmetric(vertical: 14),
        ),
        child: isLoading
            ? const SizedBox(
                height: 18,
                width: 18,
                child: CircularProgressIndicator(
                  strokeWidth: 2,
                  color: Colors.blueAccent,
                ),
              )
            : const Text(
                "Analyze Resume",
                style: TextStyle(color: Colors.white),
              ),
      ),
    );
  }

  Widget _recentScans() {
    if (recentScans.isEmpty) return const SizedBox();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          "Recent Scans • $scanCount total",
          style: const TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.w600,
          ),
        ),
        const SizedBox(height: 12),
        ...recentScans.take(3).map(
          (file) => Container(
            margin: const EdgeInsets.only(bottom: 10),
            padding: const EdgeInsets.symmetric(horizontal: 12),
            height: 50,
            decoration: BoxDecoration(
              color: Colors.white12,
              borderRadius: BorderRadius.circular(10),
            ),
            child: Row(
              children: [
                const Icon(Icons.picture_as_pdf,
                    color: Colors.redAccent, size: 20),
                const SizedBox(width: 10),
                Expanded(
                  child: Text(
                    file,
                    style: const TextStyle(color: Colors.white),
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
              ],
            ),
          ),
        )
      ],
    );
  }
}
