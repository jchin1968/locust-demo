from locust import HttpUser, task, between, run_single_user
from bs4 import BeautifulSoup
import string
import random

def random_string(length=8):
  random_string = ''.join(random.choices(string.ascii_letters, k=length))
  return str(random_string)

class RegistrationTest(HttpUser):
  host = "http://umami.lndo.site"

  @task
  def register(self):
    # Visit registration page and get form build id.
    response = self.client.get("/free-cookbook", name="register")
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
    })
    print(resp)
    print(drupal_form_id)
    while True:
      pass

if __name__ == "__main__":
  run_single_user(RegistrationTest)

