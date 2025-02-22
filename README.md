# Agama Registration Native App

This is a native application for user registration using the Agama flow with the Janssen Authorization Challenge endpoint. The application provides a graphical user interface (GUI) using Tkinter and interacts with a backend API to handle user authentication and registration.

## Project Structure

```
project-root/
│-- src/
│   ├── controller/
│   │   ├── api_handler.py  # Handles API requests
│   ├── view/
│   │   ├── ui_manager.py  # Manages UI components
│   │-- utils/
│   │   ├── config.py  # Stores configuration constants
│-- CA/
│   ├── cert.crt  # CA certificate for secure communication

├── main.py  # Entry point of the application
│-- README.md
```

## Prerequisites

Ensure you have the following dependencies installed:
- Python 3.8+
- Tkinter (GUI library, pre-installed with Python on most systems)
- Requests library

### Install Dependencies
```bash
pip install -r requirements.txt
```

For Linux systems, ensure Tkinter is installed:
```bash
sudo apt install python3-tk -y
```

## Running the Application
To start the application, navigate to the `server` directory and run:
```bash
python main.py
```

## Configuration
Update `utils/config.py` with the appropriate values, such as API URLs and the path to the CA certificate.

Example `config.py`:
```python
CLIENT_ID = "e38bf8cf-822c-4ce7-bad7-xxxxxx"    # Replace with your registered client ID
FLOW_NAME = "org.gluu.agama.registration.main"  # Replace with your Agama flow name
ACR_VALUES = "agama_challenge"
CA_PATH = "CA/cert.crt" 
API_BASE_URL = "https://your-jans-server.com/jans-auth/restv1/authorize-challenge"
```

## Features
- User registration with form validation
- Secure API communication using SSL
- Dynamic UI updates for errors and success messages
- Reset functionality to re-use the registration form


## Troubleshooting
If you encounter `ModuleNotFoundError: No module named 'tkinter'`, install Tkinter:
```bash
sudo apt install python3-tk -y
```
To debug SSL issues related to CA certificates, ensure the correct path is set in `config.py`.



