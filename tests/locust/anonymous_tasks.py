from locust import HttpUser, task, between
from bs4 import BeautifulSoup
from helper import fetch_static_assets, random_string
import random

class AnonymousTasks(HttpUser):
  """General load tests from anonymous users."""

  # Assume user pauses between 1 and 3 seconds between pages
  wait_time = between(1,3)
  
  def on_start(self):
    """Read list of URLs that will be randomly accessed by each user"""
    filename = 'urls.txt'
    try:
      with open(filename, 'r') as file:
        self.urls = [line.strip() for line in file]
        self.count = len(self.urls) 
    except FileNotFoundError:
        print(f"File {filename} does not exist.")

  @task(100)
  def homepage(self):
    """Most users go to the home page"""
    response = self.client.get("/")
    fetch_static_assets(self, response) 

  @task(50)
  def page_2(self):
    """Some users will visit a 2nd random page"""
    index = random.randrange(self.count)
    response = self.client.get(self.urls[index])
    fetch_static_assets(self, response) 

  @task(25)
  def page_3(self):
    """Fewer Users will visit a 3rd random page"""
    index = random.randrange(self.count)
    response = self.client.get(self.urls[index])
    fetch_static_assets(self, response) 

  @task(10)
  def register(self):
    """A few users will register for a free cookbook"""

    # Visit registration page and get form build id.
    response = self.client.get("/free-cookbook")
    fetch_static_assets(self, response) 
    soup = BeautifulSoup(response.text, "html.parser")
    drupal_form_id = soup.select('input[name="form_build_id"]')[0]["value"]

    # Generate random strings
    first_name = random_string()
    last_name = random_string()
    email = f'{first_name}_{last_name}@test.com'
    address = random_string(15)
    city = random_string(10)
    postal_code = random_string(5)

    # Submit form
    resp = self.client.post("/free-cookbook", {
      'form_build_id': drupal_form_id,
      'first_name': first_name,
      'last_name': last_name,
      'email': email,
      'address[address]': address,
      'address[city]': city,
      'address[state_province]': '',
      'address[postal_code]': postal_code,
      'address[country]': 'Singapore',
      'form_id': 'webform_submission_cookbook_registration_add_form',
      'op': 'Submit'
    }, name="(registration)")
    
