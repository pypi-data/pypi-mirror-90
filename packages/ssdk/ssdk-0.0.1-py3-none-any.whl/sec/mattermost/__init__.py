import requests


def client(webhook_url):
    return MattermostClient(webhook_url)


class MattermostClient:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send(self, data):
        requests.post(self.webhook_url, json=data)
