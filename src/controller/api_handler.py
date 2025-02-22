import json
import requests
from urllib.parse import urlencode
from utils.config import CA_PATH, JANS_HOSTNAME, FLOW_NAME, CLIENT_ID, ACR_VALUES, AUTH_URL

class APIHandler:
    def __init__(self):
        self.base_url = JANS_HOSTNAME
        self.client_id = CLIENT_ID
        self.flow_name = FLOW_NAME
        self.auth_url = AUTH_URL
        self.auth_session = None  # Store session token

    def start_authentication_flow(self):
        """
        Initiates the Agama authentication flow.
        """
        print("APIHandler. start authentication flow...")
        payload = {
            "acr_values": ACR_VALUES,
            "use_auth_session": True,
            "client_id": self.client_id,
            "flow_name": self.flow_name
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",  # Ensure this matches API expectations
        }
        print("Making request...")
        response = requests.post(self.auth_url, data=payload, headers=headers, verify=CA_PATH)
        print("Response is... : ", response.text)
        return self._process_response(response)

    def send_user_input(self, user_data):
        """
        Sends user input to the authorization challenge endpoint.
        """
        print("APIHandler. send_user_input starting...")
        if not self.auth_session:
            raise ValueError("No active authentication session!")

        payload = {
            "auth_session": self.auth_session,
            "use_auth_session": True,
            "data": json.dumps(user_data)
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",  # Ensure this matches API expectations

        }
        print("APIHandler. send_user_input Payload...:", payload)
        response = requests.post(self.auth_url, data=payload, headers=headers, verify=CA_PATH)
        print("APIHandler. send_user_input response is...: ", response.text)
        return self._process_response(response)
    
    def _process_response(self, response):
        """
        Processes API responses and extracts necessary data.
        """
        print("APIHandler. Process Response start...")
        if response.status_code == 200:
            return response.json()  # Final response with authorization code

        elif response.status_code == 401:
            data = response.json()

            # Store auth session for continued requests
            if "auth_session" in data:
                self.auth_session = data["auth_session"]
            print("Auth session ...:", data["auth_session"])
            return data  # Return paused flow data

        else:
            raise Exception(f"Unexpected response: {response.status_code} - {response.text}")




