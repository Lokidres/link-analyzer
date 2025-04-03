import subprocess
import sys

# Gerekli modüller
required_modules = [
    "requests",
    "beautifulsoup4",
    "pillow",
    "pytesseract",
    "whois",
    "nltk"
]

# Modülleri kontrol et ve yükle
for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        print(f"{module} modülü eksik, yükleniyor...")
        subprocess.call([sys.executable, "-m", "pip", "install", module])

# NLTK için özel indirme işlemi
import nltk
nltk.download('vader_lexicon')

import requests
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract
from urllib.parse import urlparse, urljoin
import ssl
import whois
from datetime import datetime
import socket
from nltk.sentiment import SentimentIntensityAnalyzer

class AdvancedLinkAnalyzer:
    def __init__(self, url):
        self.url = url
        self.parsed_url = urlparse(url)
        self.soup = None
        self.text_content = ""
        self.images = []
        self.links = []
        self.files = []

    def fetch_content(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.text, 'html.parser')
            self.text_content = self.soup.get_text()
            self.extract_images()
            self.extract_links()
            self.extract_files()
        except Exception as e:
            print(f"Error: {e}")

    def extract_images(self):
        for img in self.soup.find_all('img'):
            img_url = urljoin(self.url, img['src'])
            self.images.append(img_url)

    def extract_links(self):
        for link in self.soup.find_all('a'):
            href = link.get('href')
            if href:
                full_url = urljoin(self.url, href)
                self.links.append(full_url)

    def extract_files(self):
        for link in self.soup.find_all('a'):
            href = link.get('href')
            if href and any(href.endswith(ext) for ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx']):
                full_url = urljoin(self.url, href)
                self.files.append(full_url)

    def check_ssl(self):
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.parsed_url.hostname, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=self.parsed_url.hostname) as ssock:
                    cert = ssock.getpeercert()
                    print(f"✅ SSL Certificate is valid.")
                    print(f"   Issuer: {cert['issuer']}")
                    print(f"   Expires: {cert['notAfter']}")
        except Exception as e:
            print(f"❌ SSL Certificate is invalid or not found: {e}")

    def check_domain_info(self):
        try:
            domain = whois.whois(self.parsed_url.hostname)
            print(f"🌐 Domain Information:")
            print(f"   Registrar: {domain.registrar}")
            print(f"   Creation Date: {domain.creation_date}")
            print(f"   Expiration Date: {domain.expiration_date}")
        except Exception as e:
            print(f"❌ Failed to fetch WHOIS information: {e}")

    def check_redirects(self):
        try:
            response = requests.get(self.url, allow_redirects=True)
            if response.history:
                print(f"🔀 Redirects detected:")
                for resp in response.history:
                    print(f"   - {resp.url} → {resp.status_code}")
            else:
                print(f"✅ No redirects detected.")
        except Exception as e:
            print(f"❌ Failed to check redirects: {e}")

    def analyze_text(self):
        sia = SentimentIntensityAnalyzer()
        sentiment = sia.polarity_scores(self.text_content)
        print(f"📊 Text Sentiment Analysis: {sentiment}")

    def analyze_images(self):
        for img_url in self.images:
            try:
                response = requests.get(img_url, stream=True)
                img = Image.open(response.raw)
                text = pytesseract.image_to_string(img)
                print(f"🖼️ Text from Image: {text}")
            except Exception as e:
                print(f"Image analysis error: {e}")

    def analyze_links(self):
        print(f"🔗 Total {len(self.links)} links found:")
        for link in self.links:
            print(f" - {link}")

    def analyze_files(self):
        print(f"📂 Total {len(self.files)} files found:")
        for file in self.files:
            print(f" - {file}")

    def run_analysis(self):
        print(f"\n🚀 Analyzing Link: {self.url}")
        print(f"🔍 Domain Extension: {self.parsed_url.netloc}")

        self.check_ssl()
        self.check_domain_info()
        self.check_redirects()

        self.fetch_content()
        self.analyze_text()
        self.analyze_images()
        self.analyze_links()
        self.analyze_files()

if __name__ == "__main__":
    url = input("Enter the URL to analyze: ")
    analyzer = AdvancedLinkAnalyzer(url)
    analyzer.run_analysis()
