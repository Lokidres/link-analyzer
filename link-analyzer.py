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
import nltk
import json
from tqdm import tqdm

# Ensure NLTK data is available
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    print("NLTK data is missing. Please run the following command to download it:")
    print(">>> import nltk; nltk.download('vader_lexicon')")
    exit()

class AdvancedLinkAnalyzer:
    def __init__(self, url):
        self.url = url
        self.parsed_url = urlparse(url)
        self.soup = None
        self.text_content = ""
        self.images = []
        self.links = []
        self.files = []
        self.results = {}

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
            print(f"❌ Error fetching content: {e}")

    def extract_images(self):
        for img in self.soup.find_all('img'):
            img_url = urljoin(self.url, img.get('src', ''))
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
                    self.results['ssl'] = {
                        "valid": True,
                        "issuer": cert.get('issuer'),
                        "expires": cert.get('notAfter')
                    }
                    print(f"✅ SSL Certificate is valid.")
        except Exception as e:
            self.results['ssl'] = {"valid": False, "error": str(e)}
            print(f"❌ SSL Certificate is invalid or not found: {e}")

    def check_domain_info(self):
        try:
            domain = whois.whois(self.parsed_url.hostname)
            self.results['domain_info'] = {
                "registrar": domain.registrar if domain.registrar else "Unknown",
                "creation_date": str(domain.creation_date) if domain.creation_date else "Unknown",
                "expiration_date": str(domain.expiration_date) if domain.expiration_date else "Unknown"
            }
            print(f"🌐 Domain information fetched successfully.")
        except Exception as e:
            self.results['domain_info'] = {"error": str(e)}
            print(f"❌ Failed to fetch WHOIS information: {e}")

    def check_redirects(self):
        try:
            response = requests.get(self.url, allow_redirects=True)
            if response.history:
                self.results['redirects'] = [resp.url for resp in response.history]
                print(f"🔀 Redirects detected.")
            else:
                self.results['redirects'] = []
                print(f"✅ No redirects detected.")
        except Exception as e:
            self.results['redirects'] = {"error": str(e)}
            print(f"❌ Failed to check redirects: {e}")

    def analyze_text(self):
        try:
            sia = SentimentIntensityAnalyzer()
            sentiment = sia.polarity_scores(self.text_content)
            self.results['text_sentiment'] = sentiment
            print(f"📊 Text Sentiment Analysis: {sentiment}")
        except Exception as e:
            self.results['text_sentiment'] = {"error": str(e)}
            print(f"❌ Error analyzing text sentiment: {e}")

    def analyze_images(self):
        self.results['image_texts'] = []
        for img_url in tqdm(self.images, desc="Analyzing Images"):
            try:
                response = requests.get(img_url, stream=True)
                img = Image.open(response.raw)
                text = pytesseract.image_to_string(img)
                self.results['image_texts'].append({"url": img_url, "text": text})
                print(f"🖼️ Text from Image: {text}")
            except Exception as e:
                print(f"Image analysis error: {e}")

    def analyze_links(self):
        self.results['links'] = self.links
        print(f"🔗 Total {len(self.links)} links found:")
        for link in tqdm(self.links, desc="Analyzing Links"):
            print(f" - {link}")

    def analyze_files(self):
        self.results['files'] = self.files
        print(f"📂 Total {len(self.files)} files found:")
        for file in self.files:
            print(f" - {file}")

    def check_broken_links(self):
        broken_links = []
        for link in tqdm(self.links, desc="Checking Broken Links"):
            try:
                response = requests.head(link, timeout=5)
                if response.status_code >= 400:
                    broken_links.append(link)
            except Exception:
                broken_links.append(link)
        self.results['broken_links'] = broken_links
        print(f"❌ Total {len(broken_links)} broken links found.")

    def save_results(self):
        # Generate a unique filename based on the current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analysis_results_{timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=4)
        print(f"📁 Results saved to '{filename}'.")

    def display_results(self):
        print("\n==================== RESULTS ====================")
        for key, value in self.results.items():
            print(f"{key.upper()}:")
            print(json.dumps(value, indent=4))
        print("=================================================")

    def run_analysis(self):
        print(f"\n==================== ANALYSIS ====================")
        print(f"🚀 Analyzing Link: {self.url}")
        print(f"🔍 Domain Extension: {self.parsed_url.netloc}")

        self.check_ssl()
        self.check_domain_info()
        self.check_redirects()

        self.fetch_content()
        self.analyze_text()
        self.analyze_images()
        self.analyze_links()
        self.analyze_files()
        self.check_broken_links()

        self.save_results()
        self.display_results()

if __name__ == "__main__":
    url = input("Enter the URL to analyze: ")
    if not url.startswith("http"):
        print("❌ Invalid URL. Please include 'http://' or 'https://'.")
    else:
        analyzer = AdvancedLinkAnalyzer(url)
        analyzer.run_analysis()
