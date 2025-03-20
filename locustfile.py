import logging
from locust import HttpUser, task, between, events
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

    @events.quitting.add_listener
    def _(environment, **kw):
        if environment.stats.total.fail_ratio > 0.05:
            logging.error("Test failed due to failure ratio > 5%")
            environment.process_exit_code = 1
        elif environment.stats.total.avg_response_time > 1000:
            logging.error("Test failed due to average response time ratio > 1000 ms")
            environment.process_exit_code = 1
        elif environment.stats.total.get_response_time_percentile(0.95) > 2000:
            logging.error("Test failed due to 95th percentile response time > 2000 ms")
            environment.process_exit_code = 1
        else:
            environment.process_exit_code = 0