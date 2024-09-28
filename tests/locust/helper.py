from bs4 import BeautifulSoup
import random
import string

def fetch_static_assets(session, response):
  """Fetch static assets within the main html page"""
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

def is_static_file(file):
  """Determine if a URL in the web page is a static asset and should be downloaded."""
  matches = ['/sites/default/files', '/themes/']
  if any(x in file for x in matches):
    return True
  else:
    return False

def random_string(length=8):
  """Generate a random string"""
  random_string = ''.join(random.choices(string.ascii_letters, k=length))
  return str(random_string)

