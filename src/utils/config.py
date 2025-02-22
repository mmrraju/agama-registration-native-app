import os

# Configuration
JANS_HOSTNAME = "mmrraju-obliging-reindeer.gluu.info"  # Replace with your Jans Server hostname
CLIENT_ID = "e38bf8cf-822c-4ce7-bad7-7885d4e8d1d1"    # Replace with your registered client ID
FLOW_NAME = "org.gluu.agama.registration.main"  # Replace with your Agama flow name
ACR_VALUES = "agama_challenge"
CA_PATH = "./CA/httpd.crt"
AUTH_URL = url = f"https://{JANS_HOSTNAME}/jans-auth/restv1/authorize-challenge"


APP_NAME = "Agama Native App" #
WINDOW_SIZE = "800x750"