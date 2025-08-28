
# relative urls will have https 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options



chrome_options = Options()
chrome_options.add_argument("--headless=new")  # modern headless mode
chrome_options.add_argument("--disable-gpu")   # recommended on Windows
chrome_options.add_argument("--no-sandbox")    # useful for Linux/CI
chrome_options.add_argument("--disable-dev-shm-usage")  # avoid memory issues
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()) , options=chrome_options)

import time
from bs4 import BeautifulSoup

import json 
import time
import os 
from datetime import  datetime
from urllib.parse import urlparse,urlunparse ,urljoin



from collections import deque


# global variables
links_queue = deque()
visited_urls = set()
target_domain = ""
crawler_state = "initializing" 
#state initializing -> loading_state -> runing -> saving_state -> stopped

import signal 
import sys


class worker:
    
    def load_state():
        """
        load state.json file
        
        """
        
        global links_queue, visited_urls
        
        file_name = 'state.json'
        
        if os.path.exists(file_name):
            
            with open("state.json",'r+') as f:
                previous_state = json.load(f)
                links_queue = deque(previous_state['links_queue'])
                visited_urls = set(previous_state['visited_urls'])
            
    
    def save_state():
        """
        save links_queue , visited_urls to state.json
        """
        
        global links_queue, visited_urls
        
        with open("state.json",'w') as f:
            state = {"links_queue": list(links_queue) , "visited_urls":list(visited_urls)}
            json.dump( state, f ,indent=4,sort_keys=True) 
    
    def gracefull_shutdown(sig, frame):
        """
        handle the kill the process via system kill , ctl+c 
        """
        
        global crawler_state
    
        crawler_state =  "saving_state"
        print('saving state')
        # save state
        worker.save_state()
        crawler_state =  "stopped"
        print('crawler is stopped')
        sys.exit(0)
    
    
    
     
    def fetch(url):
        
        if url in visited_urls:
            print(url , 'already visited')
            return 
        
        print(url,'fetching ')
        driver.implicitly_wait(5)
        time.sleep(6)
        driver.get(url)
        
        
        visited_urls.add(url)
        return {"url":driver.current_url,"title":driver.title , "content-html":driver.page_source}
    
    def process_url(soup):
        all_links = []
        for link in soup.find_all("a"):
            href = link.get("href")
            if href and worker.is_valid_url(href):
                parsed = urlparse(href)
                if not parsed.scheme and not parsed.netloc:
                    # relative → join with domain
                    full_url = urljoin(f"https://{target_domain}", href)
                else:
                    # absolute → keep as is
                    full_url = href

                full_url = worker.remove_params(full_url)  # apply param removal
                all_links.append(full_url)
        return all_links


    def is_valid_url(url: str) -> bool:
        """
        Allow both absolute (http/https) and relative URLs
        but only from the target domain.
        """
        # resolve against https://domain (instead of http only)
        absolute_url = urljoin(f"https://{target_domain}", url)
        parsed = urlparse(absolute_url)
        return all([
            parsed.scheme in ["http", "https"],
            parsed.netloc == target_domain
        ])


    def remove_params(url: str) -> str:
        """Strip query params and fragments from URL"""
        parsed = urlparse(url)
        return urlunparse(parsed._replace(query="", fragment=""))

    def parse(task ):
        
        
   
        soup = BeautifulSoup(task.get('content-html'),'html.parser')
        
        print(task['url'], 'parsing')


        all_valid_urls = worker.process_url(soup)
       
        links_queue.extend(all_valid_urls)
       
        return {"url":task.get("url"),"title": task.get('title') , "content":soup.getText() , "allLink":list(all_valid_urls)}
    
    def save(task, folder= 'output'):
        
        
        os.makedirs(folder, exist_ok=True)
        
        print(task['url'],'saving ')
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(folder, f"{timestamp}.json")

        with open(file_path,'w') as f:
            json.dump(task, f ,  indent=4,sort_keys=True,)
            
   
   
    def crawl(seedurl):
        
        global target_domain
        target_domain = urlparse(seedurl).netloc
        
        worker.load_state()
        
        
        if len(links_queue) == 0  : 
             links_queue.append(seedurl)
             
             
        while True :
                    
            if len(links_queue) == 0 : 
                print('queue is empty')
                worker.save_state()
                break 
            url = links_queue.pop()
            try:
                
                worker.save(worker.parse(worker.fetch(url)))
            except  Exception as e:
                print(url, 'failed to process',e)
        
        
        
        
        
        
signal.signal(signal.SIGINT, worker.gracefull_shutdown)
signal.signal(signal.SIGTERM, worker.gracefull_shutdown)
