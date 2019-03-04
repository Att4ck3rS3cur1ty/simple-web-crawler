# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests

def extract_title(content):
        soup = BeautifulSoup(content, "lxml") # parser
	tag = soup.find("title", text=True)

	if not tag:
		return None

	return tag.string.strip() # "trim" serve para retirar espaços à esquerda e direita da tag

def extract_links(content):
        soup = BeautifulSoup(content, "lxml") 
        links = set() # se houver link duplicado ou +2, mandará apenas o primeiro

        for tag in soup.find_all("a", href=True):
            if tag["href"].startswith("http"): # não pega link relativo, apenas diretos
                links.add(tag["href"])
        return links

def crawl(start_url):
    seen_urls = set([start_url]) # só visitará uma vez cada url
    available_urls = set([start_url]) # as que existem, mas não foram visitadas ainda

    while available_urls:
        url = available_urls.pop()

        try: 
            content = requests.get(url, timeout=3).text
        except Exception:
            continue

        title = extract_title(content)

        if title:
            print(title)
            print(url)
            print()

        for link in extract_links(content):
            if link not in seen_urls:
                seen_urls.add(link)
                available_urls.add(link)
try:
    crawl("http://python.org")
except KeyboardInterrupt:
    print()
    print("Bye!")

page = requests.get("http://www.python.org");

links = extract_links(page.text)

for link in links: 
    print(link)
