import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import win32clipboard
import pickle

class ClipboardManager:
    def __init__(self):
        self.history = []
        self.load_history()

        # Create the main window
        self.root = tk.Tk()
        self.root.title("Clipboard Manager")
        self.root.geometry("400x350")
        self.root.resizable(False, False)

        # Apply a theme to the GUI
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Create the clipboard history listbox
        self.history_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, font=("Helvetica", 12))
        self.history_listbox.pack(fill=tk.BOTH, expand=True)
        self.history_listbox.bind("<<ListboxSelect>>", self.on_history_select)

        # Create the Copy button
        copy_button = ttk.Button(self.root, text="Copy", command=self.copy_selected)
        copy_button.pack(pady=10)

        # Create the clear history button
        clear_button = ttk.Button(self.root, text="Clear History", command=self.clear_history)
        clear_button.pack(pady=5)

        # Create the developer label with a hyperlink
        developer_label = tk.Label(self.root, text="Developed by BaptistSec", fg="blue", cursor="hand2")
        developer_label.pack(pady=5)
        developer_label.bind("<Button-1>", lambda event: self.open_link("https://github.com/BaptistSec"))

        # Initialize the clipboard listener
        self.check_clipboard()

    def on_history_select(self, event):
        selected_item = self.history_listbox.get(self.history_listbox.curselection())
        self.selected_item = selected_item

    def copy_selected(self):
        if hasattr(self, 'selected_item'):
            self.set_clipboard(self.selected_item)

    def clear_history(self):
        self.history = []
        self.update_listbox(self.history)
        self.save_history()

    def update_listbox(self, items):
        self.history_listbox.delete(0, tk.END)
        for item in items:
            self.history_listbox.insert(tk.END, item)

    def set_clipboard(self, content):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(content)
        win32clipboard.CloseClipboard()

    def get_clipboard(self):
        win32clipboard.OpenClipboard()
        content = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        return content

    def check_clipboard(self):
        current_clipboard = self.get_clipboard()
        if current_clipboard and (not self.history or current_clipboard != self.history[-1]):
            self.history.append(current_clipboard)
            self.update_listbox(self.history)
            self.save_history()

        self.root.after(1000, self.check_clipboard)

    def save_history(self):
        try:
            with open('clipboard_history.pkl', 'wb') as f:
                pickle.dump(self.history, f)
        except Exception as e:
            messagebox.showerror("Clipboard Manager", f"Failed to save clipboard history:\n{str(e)}")

    def load_history(self):
        try:
            with open('clipboard_history.pkl', 'rb') as f:
                self.history = pickle.load(f)
        except FileNotFoundError:
            self.history = []
        except Exception as e:
            messagebox.showerror("Clipboard Manager", f"Failed to load clipboard history:\n{str(e)}")

    def open_link(self, url):
        os.system(f"start {url}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    manager = ClipboardManager()
    manager.run()
