from locust import HttpUser, task, between
from requests.auth import HTTPBasicAuth

class User(HttpUser):
    wait_time = between(1, 5)

    basic = HTTPBasicAuth('presto','T5uUk7cNEiaqDb0ady7E')

    @task
    def devx_builds(self):
        self.client.get("/api/devx-builds", auth=("presto", "T5uUk7cNEiaqDb0ady7E"))

    @task
    def presto_clusters(self):
        self.client.get("/api/presto-clusters", auth=("presto", "T5uUk7cNEiaqDb0ady7E"))