from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def index_page(self):
        self.client.get("/")

    @task(3)
    def view_posts(self):
        self.client.get("/")

    @task(2)
    def view_comments(self):
        self.client.get("/comments")

    @task(2)
    def view_albums(self):
        self.client.get("/albums")

    @task(1)
    def view_photos(self):
        self.client.get("/photos")