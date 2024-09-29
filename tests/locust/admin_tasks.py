from locust import HttpUser, task
from locust.exception import StopUser
from bs4 import BeautifulSoup
from helper import fetch_static_assets, random_string
from time import sleep
import re

class AdminTasks(HttpUser):
  """General tasks by an admin user."""
  fixed_count = 1

  def on_start(self):
    """Login as admin before running tasks."""
 
    # Goto user login page and get form build id.
    response = self.client.get("/user/login")
    fetch_static_assets(self, response)
    content = BeautifulSoup(response.content, 'html.parser')
    form_build_id = content.body.find('input', {'name': 'form_build_id'})['value']
    
    # Login submission
    response = self.client.post("/user/login", {
        "name": "admin",
        "pass": "test",
        "form_id": "user_login_form",
        "form_build_id": form_build_id,
        "op": "Log in"
    })

    # Redirect to homepage after successful login
    response = self.client.get("/")
    fetch_static_assets(self, response)
    content = BeautifulSoup(response.content, 'html.parser')
    self.logout_link = content.body.find('a', href=re.compile('user/logout\?token='))['href']

  @task
  def admin_page(self):
    sleep(30)
    response = self.client.get("/admin")
    fetch_static_assets(self, response)
    raise StopUser()

  def on_stop(self):
    """Logout after test is complete"""
    self.client.get(self.logout_link) 

