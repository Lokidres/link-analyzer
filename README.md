# Advanced Link Analyzer

## Overview

The **Advanced Link Analyzer** is a Python-based tool designed to analyze web pages comprehensively. It extracts and evaluates various elements such as links, images, files, SSL certificates, domain information, and more. The tool also performs sentiment analysis on the text content to provide insights into the webpage's tone.

This project is ideal for developers, researchers, and SEO analysts who need to gather insights about a webpage's structure, content, and security.

---

## Features

- **SSL Certificate Validation**: Checks if the website has a valid SSL certificate and retrieves its issuer and expiration date.
- **Domain Information**: Fetches WHOIS data, including registrar, creation date, and expiration date.
- **Redirect Detection**: Identifies and lists all redirects for the given URL.
- **Text Sentiment Analysis**: Analyzes the sentiment of the webpage's text content using NLTK's VADER sentiment analyzer.
- **Link Analysis**: Extracts and lists all hyperlinks on the webpage.
- **File Detection**: Identifies downloadable files (e.g., PDFs, Word documents, Excel files) linked on the webpage.
- **Broken Link Checker**: Detects and lists broken links on the webpage.
- **Results Export**: Saves the analysis results to a JSON file for further use.

---

## Installation

### Prerequisites
Ensure you have Python 3.7 or higher installed. You can download it from [python.org](https://www.python.org/).

### Clone the Repository
1. Clone the repository:
   ```bash
   git clone https://github.com/Lokidres/link-analyzer.git
   cd link-analyzer
   ```

### Install Required Modules
Install the required Python modules using `pip`:

```bash
pip install requests beautifulsoup4 pillow nltk tqdm whois
```

### NLTK Data Setup
Download the VADER sentiment analysis lexicon:
```python
import nltk
nltk.download('vader_lexicon')
```

---

## Usage

1. Run the script:
   ```bash
   python link-analyzer.py
   ```

2. Enter the URL to analyze when prompted:
   ```
   Enter the URL to analyze: https://example.com
   ```

3. The tool will perform the analysis and display the results in the terminal. A JSON file containing the results will also be saved in the current directory.

---

## Example Output

### Terminal Output
```
==================== ANALYSIS ====================
🚀 Analyzing Link: https://example.com
✅ SSL Certificate is valid.
🌐 Domain information fetched successfully.
🔀 Redirects detected.
📊 Text Sentiment Analysis: {'neg': 0.0, 'neu': 0.9, 'pos': 0.1, 'compound': 0.5}
🔗 Total 10 links found:
 - https://example.com/page1
 - https://example.com/page2
📂 Total 2 files found:
 - https://example.com/file1.pdf
 - https://example.com/file2.docx
❌ Total 1 broken link found.
📁 Results saved to 'analysis_results_20231010_123456.json'.
```

### JSON Output
```json
{
    "ssl": {
        "valid": true,
        "issuer": "Let's Encrypt",
        "expires": "2023-12-31"
    },
    "domain_info": {
        "registrar": "NameCheap",
        "creation_date": "2020-01-01",
        "expiration_date": "2025-01-01"
    },
    "redirects": [
        "https://example.com",
        "https://www.example.com"
    ],
    "text_sentiment": {
        "neg": 0.0,
        "neu": 0.9,
        "pos": 0.1,
        "compound": 0.5
    },
    "links": [
        "https://example.com/page1",
        "https://example.com/page2"
    ],
    "files": [
        "https://example.com/file1.pdf",
        "https://example.com/file2.docx"
    ],
    "broken_links": [
        "https://example.com/broken-link"
    ]
}
```

---

## Notes

- Ensure the URL includes `http://` or `https://` to avoid errors.
- The tool may take longer to analyze pages with many links or files.

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the tool.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.



