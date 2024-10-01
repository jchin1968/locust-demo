from locust import HttpUser, task, between
class SimpleTest(HttpUser):
  wait_time = between(1,3)
    
  @task(9)
  def homepage(self):
    self.client.get("/")

  @task(8)
  def recipes(self):
    self.client.get("/recipes")
    
  @task(3)
  def contact(self):
    self.client.get("/contact")
