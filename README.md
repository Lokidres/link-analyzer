# 📌 Link Analyzer AI 🔍

A Python-based AI tool to analyze the content of a link, including text, images, links, and files.

## ✨ Features
- **Text Analysis**: Extracts and analyzes text (e.g., sentiment analysis).
- **Image Analysis**: Detects images and extracts text using OCR.
- **Link Extraction**: Finds and lists all links on the page.
- **File Detection**: Identifies downloadable files (e.g., PDFs, Word documents).
- **Security Check**: (Optional) Integrates with the VirusTotal API to check for malicious links.

## ⚙️ Installation And Usage
```bash
git clone https://github.com/Lokidres/link-analyzer.git
cd link-analyzer
pip install requests beautifulsoup4 pillow pytesseract whois nltk
python -c "import nltk; nltk.download('vader_lexicon')"
python link-analyzer.py








