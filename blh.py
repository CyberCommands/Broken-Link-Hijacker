#!/usr/bin/env python3
import os
import random
import argparse
import requests
import urllib3
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup


headers = { 'user-agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
 }

# Change it to True if SSL errors are thrown.
to_verify_ssl_cert=False
urllib3.disable_warnings()

social_list=["twitter.com","facebook.com","instagram.com","linkedin.com","youtube.com","twitch.com","twitch.tv","discord.com","slack.com","soundcloud.com","medium.com",
"vimeo.com","skype.com","pinterest.com","ct.pinterest.com","snapchat.com","telegram","t.me","telegram.com","clickcease.com","wistia.com","adjust.com","github.com"

]

inbound_urls = set()
outbound_urls = set()
current_inbound_urls =set()
broken_urls  = set()
social_urls = []
number_of_broken_link=0

total_urls_visited = 0

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    ascii_banner="""
    __________                __                  
    \______   \_______  ____ |  | __ ____   ____  
     |    |  _/\_  __ \/  _ \|  |/ // __ \ /    \ 
     |    |   \ |  | \(  <_> )    <\  ___/|   |  \ 
     |______  / |__|   \____/|__|_ \\___  >___|  /
            \/                    \/     \/    \/ 
              ____     __        __ 
             |    |   |__| ____ |  | __  
             |    |   |  |/    \|  |/ / 
             |    |___|  |   |  \    < 
             |_______ \__|___|  /__|_ \           
                     \/       \/     \/ 
      ___ ___  __     __               __      _ 
     /   |   \|__|   |__|____    ____ |  | __ | | 
    /    ~    \  |   |  \__  \ _/ ___\|  |/ / | | 
    \    Y    /  |   |  |/ __ \\  \___|    <   \| 
     \___|_  /|__/\__|  (____  /\___  >__|_ \  __ 
           \/    \______|    \/     \/     \/  \/ 
    
    """
    
    print(ascii_banner)

def random_ua():
    UAS=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
     "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36",
     "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1",
     "Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36"
     )

    # To generate random User-Agent for deep crawling.
    ua = UAS[random.randrange(len(UAS))]
    ua = str(ua)
    headers['user-agent'] = ua

# Checking For Valid Urls.
def is_valid(url):
    try:
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)
        valid_request=requests.get(url,headers=headers,verify=to_verify_ssl_cert)
        if valid_request != 200:
            print(f"\033[31m[!] Enter Valid Url \033[0m")
            quit()
            
    except:
        print(f"\033[31m[!] ERROR \033[0m")
        quit()

# Returns all URLs from the given Main Website.
def main_webpage_links(url):
    try:
        urls = set()
        random_ua()
        domain_name = urlparse(url).netloc
        soup = BeautifulSoup(requests.get(url,headers=headers,verify=to_verify_ssl_cert).content, "html.parser")
        
        # Check for link in herf tag.
        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                continue
            
            href = urljoin(url, href)
            parsed_href = urlparse(href)
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
            if not is_valid(href):
                continue
            
            if href in inbound_urls:
                continue
            
            if domain_name not in href:
                if href not in outbound_urls:
                    if verbosity:
                        print(f"\033[34m[!] Outbound link: {href} \033[0m")
                    outbound_urls.add(href)
                    social_domain=str(urlparse(href).netloc)
                    if social_domain and social_domain.strip('www.') in social_list:
                        social_urls.append(href)
                continue
            
            if verbosity:
                print(f"\033[32m[*] Inbound link: {href} \033[0m")
            
            urls.add(href)
            inbound_urls.add(href)
        
        # Check for link inside images.    
        for img_tag in soup.findAll('img'):
            href = img_tag.attrs.get('src')
            if href == "" or href is None:
                continue
            href = urljoin(url, href)
            parsed_href = urlparse(href)
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
            if not is_valid(href):
                continue
            if href in inbound_urls:
                continue
            if domain_name not in href:
                if href not in outbound_urls:
                    if verbosity:
                        print(f"\033[37m[!] Outbound Image link: {href} \033[0m")
                    outbound_urls.add(href)
                    social_domain = str(urlparse(href).netloc)
                    if social_domain and social_domain.strip('www.') in social_list:
                        social_urls.append(href)
                continue
            if verbosity:
                print(f"\033[37m[!] Inbound Image link: {href} \033[0m")
            
            inbound_urls.add(href)

        return urls
    except KeyboardInterrupt:
        print(f"\033[31m[!] Keyboard Interrupt detected \033[0m")
        quit()


def crawl(url):
    try:
        global total_urls_visited
        total_urls_visited += 1
        links = main_webpage_links(url)
        for link in links:
            random_ua()
            crawl(link)
    except KeyboardInterrupt:
        print(f"\033[31m[!] Keyboard Interrupt detected \033[0m\n")
        quit()
    except:
        print(f"\033[31m[!] ERROR \033[0m")
        quit()

def status_check(url):
    try:
        r = requests.get(url,headers=headers,verify=to_verify_ssl_cert)
        if r.status_code == 404:
            number_of_broken_link += 1
            print(f"\033[91m[!] Broken link: {url} \033[0m")
        
        if r.status_code == 301 or r.status_code == 302 or r.status_code == 401 or r.status_code == 403 or r.status_code == 429 or r.status_code == 500 or r.status_code == 503:
            print(f"\033[91m[!] HTTP error: {url}{r.status_code} \033[0m")
    
    except KeyboardInterrupt:
        print(f"\033[31m[!] Keyboard Interrupt detected \033[0m\n")
        quit()
    
    except:
         print(f"\033[91m[-] Unable to connect: {url} \033[0m")

def main_proc(deep):
        if deep > 3 or deep <= 0:
                print(f"\033[91m[-] Incorrect Value for Deepness: \033[0m",deep)
                print(f"\033[33m[*] Deepness Level Varies from 1-3 \033[0m\n")
        
        if deep == 1:
            links = main_webpage_links(url)
            print("")
            search_msg()
            for link in outbound_urls:
                link = str(link)
                status_check(link)
            status_check_msg()
        elif deep == 2:
            links = main_webpage_links(url)
            for link in links:
                main_webpage_links(link)
            print("")
            search_msg()
            for link in outbound_urls:
                link = str(link)
                status_check(link)
            status_check_msg()
            
        elif deep == 3:
            crawl(url)
            search_msg()
            for link in outbound_urls:
                link = str(link)
                status_check(link)
            status_check_msg()


def info():
        print(f"\n\033[34mDomain Name ➤ \033[0m",domain_name)
        print(f"\033[34mDeepness ➤ \033[0m",deep)
        print(f"\033[34mOutput To a File ➤ \033[0m",output)
        print(f"\033[34mOutput File ➤ \033[0m",output_location,"(Default)")
        print(f"\033[34mVerbosity ➤ \033[0m",verbosity)
        print(f"\033[34mTO verify SSL Certificate ➤ \033[0m",to_verify_ssl_cert)
        print("")

def print_output():
    print(f"\033[34mPrinting Output To File ➤ ",output_location)
    with open(f"{domain_name}_links.txt", "a") as f:
                print("Domain Name ➤ ",domain_name, file=f)
                print("Deepness ➤ ",deep, file=f)
                print("Output File ➤ ",output_location,"(Default)", file=f)
                print("Verbosity ➤ ",verbosity, file=f)
                print("Output To a File ➤ ",output, file=f)
                print("", file=f)
                print("========== Inbound Urls ==========", file=f)
                print("", file=f)
                
                for internal_link in inbound_urls:
                    print(internal_link.strip(), file=f)
                print("", file=f)
                print("========== Outbound Urls ==========", file=f)
                print("", file=f)
                
                for external_link in outbound_urls:
                    print(external_link.strip(), file=f)
                print("", file=f)
                print("========== Social URL's ==========", file=f)
                print("", file=f)   
                
                for social_links in social_urls:
                    print(social_links.strip(), file=f)
                print("", file=f)
                print("[+] Total Inbound links: ", len(inbound_urls), file=f)
                print("[+] Total Outbound links: ", len(outbound_urls), file=f)
                print("[+] Total Urls: ", len(outbound_urls) + len(inbound_urls), file=f)
                print("", file=f)
    f.close()


def stats():
        print("\n[+] Total Inbound links: ", len(inbound_urls))
        print("[+] Total Outbound links: ", len(outbound_urls))
        print("[+] Total Urls: ", len(outbound_urls) + len(inbound_urls))
        print("")

def status_check_msg():
    try:
        if number_of_broken_link == 0:
                    print(f"\n\033[91m[-] Broken Links Not Found \033[0m\n")
    
    except KeyboardInterrupt:
        print(f"\033[31m[!] Keyboard Interrupt detected \033[0m\n")
        quit()

def search_msg():
    print("\033[5m==================== Searching Broken Links... ==================== \033[0m\n")

def show_social():
    for i in social_urls:
        print(f"\033[92m[*] Social Urls: {i} \033[0m")


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        parser = argparse.ArgumentParser(description="Broken Link Finder Tool")
        parser.add_argument("url", help="The URL to extract links from.")
        parser.add_argument("-d", "--deepness", help="Level of deepness to search.(Default=1)", default=1, type=int)
        parser.add_argument("-o", "--output", help="Weather to save the output in a file. Default is False(Filename=domain-name_links.txt)")
        parser.add_argument("-v", "--verbosity", help="Set the Verbosity of Program(Default=True)")
        args = parser.parse_args()
        
        url = args.url
        deep = args.deepness
        verbosity = args.verbosity
        domain_name = urlparse(url).netloc
        output_location = domain_name+"_links.txt"
        
        banner()
        
        if args.verbosity == False or args.verbosity == "F":
            verbosity = False
        else:
            verbosity = True
        
        if args.output == True or args.output == "T":
            output = True
        else:
            output = False
        
        is_valid(url)
        info()
        main_proc(deep)
        for i in social_urls:
            print(f"\033[92m[*] Social Urls: {i} \033[0m")
        
        stats()
        if output:
            print_output()

    except KeyboardInterrupt:
        print(f"\033[31m[!] Keyboard Interrupt detected \033[0m\n")
        quit()
