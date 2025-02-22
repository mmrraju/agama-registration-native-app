import tkinter as tk

class UIManager:
    def __init__(self, root):
        self.root = root
        self.current_widgets = []

    def clear_screen(self):
        """
        Clears all widgets from the screen.
        """
        for widget in self.current_widgets:
            widget.destroy()
        self.current_widgets = []

    def show_loading(self, message):
        """
        Displays a loading message to the user.
        """
        self.clear_screen()
        loading_label = tk.Label(self.root, text=message, font=("Helvetica", 14), fg="blue")
        loading_label.pack(pady=20)
        self.current_widgets.append(loading_label)

    def show_message(self, message):
        """
        Displays a message on the screen (e.g., flow_paused template or error message).
        """
        self.clear_screen()
        message_label = tk.Label(self.root, text=message, font=("Helvetica", 14), fg="green")
        message_label.pack(pady=20)
        self.current_widgets.append(message_label)
