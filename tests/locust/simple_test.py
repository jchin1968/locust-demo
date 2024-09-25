from locust import HttpUser, task, between
class SimpleTest(HttpUser):
  wait_time = between(1,3)
    
  @task
  def homepage(self):
    self.client.get("/")

  @task
  def contact(self):
    self.client.get("/contact")
    
