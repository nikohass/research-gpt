import json
import requests

KEY_FILE = "key.json"

class GPT:
    def __init__(self, model="gpt-4-32k"):
        self.model = model
        with open(KEY_FILE, "r") as key_file:
            svc_key = json.load(key_file)
        self.svc_key = svc_key
        self.svc_url = svc_key["url"]
        self.client_id = svc_key["uaa"]["clientid"]
        self.client_secret = svc_key["uaa"]["clientsecret"]
        self._get_token()

    def _get_token(self):
        uaa_url = self.svc_key["uaa"]["url"]
        params = {"grant_type": "client_credentials" }
        resp = requests.post(
            f"{uaa_url}/oauth/token",
            auth=(self.client_id, self.client_secret),
            params=params
        )
        self.token = resp.json()["access_token"]
        self.headers = {
            "Authorization":  f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def get_response(self, prompt):
        data = {
            "deployment_id": self.model,
            # "messages": prompt + "\n<|im_start|>assistant",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2000,
            "temperature": 1.0,
            "n": 1,
            "stop": ["<|im_end|>"]
        }
        response = requests.post(
            f"{self.svc_url}/api/v1/completions",
            headers=self.headers,
            json=data
        )
        try:
            response = str(response.json()['choices'][0]['message']['content'])
        except:
            self._get_token()
            response = requests.post(
                f"{self.svc_url}/api/v1/completions",
                headers=self.headers,
                json=data
            )
            response = str(response.json()['choices'][0]['message']['content'])
        return response