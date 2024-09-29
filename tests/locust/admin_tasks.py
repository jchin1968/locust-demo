from locust import HttpUser, task, constant
from locust.exception import StopUser
from bs4 import BeautifulSoup
from helper import fetch_static_assets, random_string
from time import sleep
import re

class AdminTasks(HttpUser):
  """General tasks by an admin user."""

  # Spawn one user only.
  fixed_count = 1

  # Wait time between tasks
  wait_time = constant(60)

  def on_start(self):
    """Login as admin before running tasks."""

    # Goto user login page and get form build id.
    response = self.client.get("/user/login")
    fetch_static_assets(self, response)
    soup = BeautifulSoup(response.content, 'html.parser')
    form_build_id = soup.body.find('input', {'name': 'form_build_id'})['value']

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

    # Fetch the unique logout token value which is required to logout.
    soup = BeautifulSoup(response.content, 'html.parser')
    self.logout_link = soup.body.find('a', href=re.compile('user/logout\?token='))['href']

  @task(99)
  def create_article(self):
    # Goto the performance page.
    response = self.client.get("/node/add/article")
    fetch_static_assets(self, response)
    soup = BeautifulSoup(response.content, 'html.parser')

    form_elements = soup.find('form', attrs={'id': 'node-article-form'})
    form_build_id = form_elements.find('input', {'name': 'form_build_id'})['value']

    # Login submission
    response = self.client.post("/node/add/article", {
        "edit-title-0-value": random_string(30),
        "edit-moderation-state-0-state": 'Published',
        "form_id": "node_article_form",
        "form_build_id": form_build_id,
        "op": "Save"
    })


  @task(1)
  def clear_cache(self):
    """Clear Drupal cache"""

    # Goto the performance page.
    response = self.client.get("/admin/config/development/performance")
    fetch_static_assets(self, response)
    soup = BeautifulSoup(response.content, 'html.parser')

    form_elements = soup.find('form', attrs={'id': 'system-clear-cache'})
    form_token = form_elements.find('input', {'name': 'form_token'})['value']
    form_build_id = form_elements.find('input', {'name': 'form_build_id'})['value']

    # Simulate clicking on the clear all caches button.
    response = self.client.post("/admin/config/development/performance", {
        "form_id": "system_clear_cache",
        "form_build_id": form_build_id,
        "form_token": form_token,
        "op": "Clear all caches"
    })

  def on_stop(self):
    """Logout after test is complete. This ensures the session table doesn't grow too large."""

    # Use the logout link with the logout token acquired in on_start().
    self.client.get(self.logout_link)

