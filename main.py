import sys
import os
import tkinter as tk
# Add the 'src' folder to sys.path dynamically
src_path = os.path.join(os.path.dirname(__file__), '.', 'src')
sys.path.append(src_path)
from controller.api_handler import APIHandler
from view.ui_manager import UIManager
from tkinter import messagebox
from utils.config import CA_PATH, JANS_HOSTNAME, FLOW_NAME, CLIENT_ID, ACR_VALUES, AUTH_URL, APP_NAME, WINDOW_SIZE

class AgamaApp:
    def __init__(self, root):
        self.root = root
        root.title(APP_NAME)
        root.geometry(WINDOW_SIZE)
        self.ui = UIManager(root)
        self.api = APIHandler()
        self.auth_session = None  # Store the auth_session for subsequent requests

        # Create Start Authentication Button
        self.start_button = tk.Button(root, text="User Registration", 
                                      command=self.start_authentication_flow, 
                                      font=("Helvetica", 14))
        self.start_button.pack(pady=20)

    def start_authentication_flow(self):
        """
        Initiates the authentication flow by making the initial request.
        """
        print("Main. Start authentication flow...")
        self.ui.show_loading("Starting authentication...")

        # Make the initial request
        response = self.api.start_authentication_flow()

        if response.get("error") == "flow_paused":
            self.auth_session = response.get("auth_session")
            self.handle_flow_paused(response.get("flow_paused"))
        else:
            self.ui.show_message("Unexpected Error! Please try again.")

    def handle_flow_paused(self, flow_paused):
        """
        Handles the flow_paused state by updating the UI and managing user input.
        """
        print("Main. handle_flow_paused starting...")
        template = flow_paused.get("_template")

        if template == "profile.ftlh":
            if not hasattr(self, "form_frame"):  # Check if form already exists
                self.ui.clear_screen()

                # Title
                title_label = tk.Label(self.root, text="Registration Form", font=("Helvetica", 16, "bold"))
                title_label.pack(pady=10)

                # Error Label (Initially Hidden, Appears Below Title)
                self.error_label = tk.Label(self.root, text="", font=("Helvetica", 12), fg="red")
                self.error_label.pack(pady=5)
                self.error_label.place_forget()  # Hide initially

                # Create a frame for better layout
                self.form_frame = tk.Frame(self.root)
                self.form_frame.pack(pady=10)

                # Input fields
                fields = [
                    ("uid", "User name:"),
                    ("sn", "First name:"),
                    ("givenName", "Last name:"),
                    ("displayName", "Given name:"),
                    ("mail", "Mail:"),
                    ("userPassword", "Password:"),
                    ("confirmPassword", "Confirm password:")
                ]
                self.entries = {}

                for row, (field, label_text) in enumerate(fields):
                    field_label = tk.Label(self.form_frame, text=label_text, font=("Helvetica", 12))
                    field_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")  # Align left

                    entry = tk.Entry(self.form_frame, font=("Helvetica", 12), show="*" if "Password" in field else "", width=35)
                    entry.grid(row=row, column=1, padx=10, pady=5)

                    self.entries[field] = entry  # Store entry widget

                # Submit Button
                def submit_registration():
                    print("Main. submit_registration starting...")
                    # Get values
                    form_data = {field: self.entries[field].get() for field, _ in fields}

                    # Password validation
                    if form_data["userPassword"] != form_data["confirmPassword"]:
                        self.show_error_magic("Passwords do not match!")  # Show magic error
                        return

                    # Remove confirmPassword before submitting
                    # del form_data["confirmPassword"]

                    # Send to server
                    self.submit_user_input(form_data)

                submit_button = tk.Button(self.root, text="Submit", font=("Helvetica", 12, "bold"), 
                                        command=submit_registration, bg="green", fg="white")
                submit_button.pack(pady=10)

            else:
                print("Form already exists, reusing it.")

            # Show errors if any
            error_message = flow_paused.get("errorMessage", "")
            if error_message:
                self.show_error_magic(error_message)  # Animate error display

        elif template == "acknowledgement.ftlh":
            self.ui.clear_screen()

            # Success message
            success_label = tk.Label(self.root, text="Registration Successful!", font=("Helvetica", 16, "bold"), fg="green")
            success_label.pack(pady=10)

            # Continue button
            continue_button = tk.Button(self.root, text="Continue", font=("Helvetica", 14, "bold"),
                                        command=lambda: self.submit_user_input({"continue": "continue"}), 
                                        bg="blue", fg="white")
            continue_button.pack(pady=10)

            # Reset button (Appears After Flow Finishes)
            reset_button = tk.Button(self.root, text="Reset", font=("Helvetica", 14, "bold"),
                             command=self.reset_app, bg="red", fg="white")
            reset_button.pack(pady=10)

        else:
            self.ui.show_message("Unknown template! Please contact support.")

    # 🔹 Function to Show Error Message with Fade Effect (Under Title)
    def show_error_magic(self, message):
        self.error_label.config(text=message)  # Update error message
        self.error_label.pack()  # Make it appear under the title

        # Make it disappear after 5 seconds
        self.root.after(5000, lambda: self.error_label.pack_forget())

    # 🔹 Function to Reset Form
    def reset_app(self):
        """
        Completely resets the application by destroying the current window
        and restarting a new instance of the app.
        """
        print("Resetting app...")

        # Destroy the existing Tkinter root window
        self.root.destroy()

        # Create a new root window and start the app again
        new_root = tk.Tk()
        app = AgamaApp(new_root)  # Initialize a new instance of the app
        new_root.mainloop()   

    def submit_user_input(self, data):
        """
        Submits user input to the server for the current RRF step.
        """
        self.ui.show_loading("Processing...")

        # Make a subsequent request with user input
        response = self.api.send_user_input(data)

        if response.get("error") == "flow_paused":
            self.handle_flow_paused(response.get("flow_paused"))

        elif response.get("error") == "flow_finished":
            self.handle_flow_finished(response.get("flow_finished"))

        else:
            self.ui.show_message("Unexpected Error! Please try again.")

    def handle_flow_finished(self, flow_finished):
        """
        Handles the flow_finished state and completes authentication.
        """
        print("Main. handle_flow_finished starting...")
        success = flow_finished.get("success")
        if success:
            self.ui.show_message("Authentication Successful!\nFetching Authorization Code...")

            # Final request to get authorization code
            # auth_code_response = self.api.send_final_request(self.auth_session)
            auth_code_response = self.api.send_user_input({})
            authorization_code = auth_code_response.get("authorization_code")

            if authorization_code:
                self.ui.show_message(f"Authentication Complete!\nAuthorization Code: {authorization_code}")
            else:
                self.ui.show_message("Failed to retrieve authorization code.")
        else:
            self.ui.show_message("Authentication Failed. Please try again.")

if __name__ == "__main__":
    print("Native app starting...")
    root = tk.Tk()
    app = AgamaApp(root)
    root.mainloop()
