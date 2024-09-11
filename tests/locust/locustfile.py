from locust import HttpUser, task, between
from random import randrange
from bs4 import BeautifulSoup

def is_static_file(file):
  matches = ['/sites/default/files', '/themes/']
  if any(x in file for x in matches):
    return True
  else:
    return False

def fetch_static_assets(session, response):
    """Determine if a URL in the web page is a static asset and should be downloaded."""
    resource_urls = set()
    soup = BeautifulSoup(response.text, "html.parser")

    for res in soup.find_all(src=True):
        url = res['src']
        if is_static_file(url):
            resource_urls.add(url)
        else:
            print(f'Skipping: {url}')

    for url in set(resource_urls):
        session.client.get(url, name="(Static File)")


class LoadTest(HttpUser):
  
  def on_start(self):
    """Read list of URLs that will be randomly accessed by each user"""
    filename = 'urls.txt'
    try:
      with open(filename, 'r') as file:
        self.urls = [line.strip() for line in file]
        self.count = len(self.urls) 
    except FileNotFoundError:
        print(f"File {filename} does not exist.")

  @task
  def page_1(self):
    """Assume all users start their browsing from the homepage"""
    response = self.client.get("/")
    fetch_static_assets(self, response) 

  @task
  def page_2(self):
    """User 2nd random page visit"""
    index = randrange(self.count)
    response = self.client.get(self.urls[index])
    fetch_static_assets(self, response) 

  @task
  def page_3(self):
    """User 3rd random page visit"""
    index = randrange(self.count)
    response = self.client.get(self.urls[index])
    fetch_static_assets(self, response) 

  @task
  def page_4(self):
    """User 4th random page visit"""
    index = randrange(self.count)
    response = self.client.get(self.urls[index])
    fetch_static_assets(self, response) 
  
  @task
  def page_5(self):
    """User 5th random page visit"""
    index = randrange(self.count)
    response = self.client.get(self.urls[index])
    fetch_static_assets(self, response) 

  # Assume user pauses between 1 and 3 seconds between pages
  wait_time = between(1,3)

