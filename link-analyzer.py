import argparse
import logging
import requests
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract
from urllib.parse import urlparse, urljoin
import ssl
import whois
import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    logging.error("NLTK dataset is missing. Please run 'nltk.download(\"vader_lexicon\")'")
    exit()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AdvancedLinkAnalyzer:
    """
    Advanced Link Analyzer.
    Analyzes content, SSL, WHOIS info, redirects, text, images, and file links from a URL.
    """
    def __init__(self, url, timeout=10):
        self.url = url
        self.timeout = timeout
        self.parsed_url = urlparse(url)
        self.soup = None
        self.text_content = ""
        self.images = []
        self.links = []
        self.files = []
        self.headers = {
            "User-Agent": "Mozilla/5.0 (compatible; AdvancedLinkAnalyzer/1.0; +https://example.com/)"
        }

    def fetch_content(self):
        try:
            response = requests.get(self.url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.text, 'html.parser')
            self.text_content = self.soup.get_text(separator=' ', strip=True)
            self.extract_images()
            self.extract_links()
            self.extract_files()
        except Exception as e:
            logging.error(f"Content fetch error: {e}")

    def extract_images(self):
        if self.soup:
            for img in self.soup.find_all('img'):
                src = img.get('src')
                if src:
                    img_url = urljoin(self.url, src)
                    self.images.append(img_url)
            logging.info(f"{len(self.images)} images found.")

    def extract_links(self):
        if self.soup:
            for link in self.soup.find_all('a'):
                href = link.get('href')
                if href:
                    full_url = urljoin(self.url, href)
                    self.links.append(full_url)
            logging.info(f"{len(self.links)} links found.")

    def extract_files(self):
        if self.soup:
            for link in self.soup.find_all('a'):
                href = link.get('href')
                if href and any(href.lower().endswith(ext) for ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx']):
                    full_url = urljoin(self.url, href)
                    self.files.append(full_url)
            logging.info(f"{len(self.files)} file links found.")

    def check_ssl(self):
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.parsed_url.hostname, 443), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=self.parsed_url.hostname) as ssock:
                    cert = ssock.getpeercert()
                    logging.info("SSL certificate valid.")
                    logging.info(f"Issuer: {cert.get('issuer')}")
                    logging.info(f"Expires: {cert.get('notAfter')}")
        except Exception as e:
            logging.error(f"SSL error: {e}")

    def check_domain_info(self):
        try:
            domain = whois.whois(self.parsed_url.hostname)
            logging.info("Domain info:")
            logging.info(f"Registrar: {domain.registrar}")
            logging.info(f"Creation Date: {domain.creation_date}")
            logging.info(f"Expiration Date: {domain.expiration_date}")
        except Exception as e:
            logging.error(f"WHOIS error: {e}")

    def check_redirects(self):
        try:
            response = requests.get(self.url, headers=self.headers, timeout=self.timeout, allow_redirects=True)
            if response.history:
                logging.info("Redirects detected:")
                for resp in response.history:
                    logging.info(f"{resp.url} -> {resp.status_code}")
            else:
                logging.info("No redirects.")
        except Exception as e:
            logging.error(f"Redirect error: {e}")

    def analyze_text(self):
        try:
            sia = SentimentIntensityAnalyzer()
            sentiment = sia.polarity_scores(self.text_content)
            logging.info(f"Text sentiment analysis: {sentiment}")
        except Exception as e:
            logging.error(f"Text analysis error: {e}")

    def analyze_image(self, img_url):
        try:
            response = requests.get(img_url, headers=self.headers, stream=True, timeout=self.timeout)
            img = Image.open(response.raw)
            text = pytesseract.image_to_string(img)
            return img_url, text.strip()
        except Exception as e:
            logging.error(f"Image analysis error ({img_url}): {e}")
            return img_url, ""

    def analyze_images(self):
        results = {}
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(self.analyze_image, url): url for url in self.images}
            for future in as_completed(future_to_url):
                img_url, text = future.result()
                results[img_url] = text
                if text:
                    logging.info(f"{img_url} -> {text}")
                else:
                    logging.info(f"{img_url} -> No text extracted.")
        return results

    def analyze_links(self):
        logging.info(f"Total links found: {len(self.links)}")
        for link in self.links:
            logging.debug(f"{link}")

    def analyze_files(self):
        logging.info(f"Total file links found: {len(self.files)}")
        for file in self.files:
            logging.debug(f"{file}")

    def run_analysis(self):
        logging.info(f"Starting analysis for: {self.url}")
        logging.info(f"Domain: {self.parsed_url.netloc}")
        self.check_ssl()
        self.check_domain_info()
        self.check_redirects()
        self.fetch_content()
        self.analyze_text()
        self.analyze_images()
        self.analyze_links()
        self.analyze_files()

def main():
    parser = argparse.ArgumentParser(description="Advanced Link Analyzer")
    parser.add_argument("-u", "--url", required=True, help="URL to analyze")
    args = parser.parse_args()
    analyzer = AdvancedLinkAnalyzer(args.url)
    analyzer.run_analysis()

if __name__ == "__main__":
    main()


