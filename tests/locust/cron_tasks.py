from locust import HttpUser, task, constant
from locust.exception import StopUser
from bs4 import BeautifulSoup
import re

class CronTasks(HttpUser):
  """Run cron."""

  # Spawn one user only.
  fixed_count = 1

  # Run cron every minute
  wait_time = constant(60)

  def on_start(self):
    """Login as admin."""

    # Goto user login page and get form build id.
    response = self.client.get("/user/login")
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

    # If login failed, exit.
    if response.status_code != 200:
      raise StopUser()

    # Go to the home page after successful login and get the logout URL with token value.
    response = self.client.get("/")
    soup = BeautifulSoup(response.content, 'html.parser')
    self.logout_link = soup.body.find('a', href=re.compile('user/logout\?token='))['href']

    # Go to the admin cron page and get the external cron URL
    response = self.client.get("/admin/config/system/cron")
    soup = BeautifulSoup(response.content, 'html.parser')
    self.cron_link = soup.body.find('a', href=re.compile('/cron/'))['href']

  @task
  def drupal_cron(self):
    """Run drupal cron"""
    response = self.client.get(self.cron_link)

  def on_stop(self):
    """Logout after test is complete. This ensures the session table doesn't grow too large."""
    self.client.get(self.logout_link)

