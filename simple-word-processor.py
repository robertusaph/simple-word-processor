import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import os

class WordProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Word Processor")
        self.root.geometry("800x600")

        self.text_area = ScrolledText(self.root, wrap=tk.WORD, undo=True)
        self.text_area.pack(expand=1, fill=tk.BOTH)

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Print", command=self.print_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_program)

        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.text_area.edit_undo)
        edit_menu.add_command(label="Redo", command=self.text_area.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: self.text_area.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.text_area.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.text_area.event_generate("<<Paste>>"))
        edit_menu.add_command(label="Select All", command=lambda: self.text_area.event_generate("<<SelectAll>>"))

        self.file_name = None

    def new_file(self):
        if self.confirm_discard_changes():
            self.text_area.delete(1.0, tk.END)
            self.file_name = None
            self.root.title("Untitled - Simple Word Processor")

    def open_file(self):
        if self.confirm_discard_changes():
            file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
            if file_path:
                with open(file_path, "r") as file:
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, file.read())
                self.file_name = file_path
                self.root.title(f"{os.path.basename(self.file_name)} - Simple Word Processor")

    def save_file(self):
        if self.file_name:
            self._save_to_file(self.file_name)
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self._save_to_file(file_path)

    def _save_to_file(self, file_path):
        try:
            with open(file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
            self.file_name = file_path
            self.root.title(f"{os.path.basename(self.file_name)} - Simple Word Processor")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save file: {str(e)}")

    def print_file(self):
        try:
            messagebox.showinfo("Print", "This would send the document to the printer.")
        except Exception as e:
            messagebox.showerror("Print Error", f"Failed to print: {str(e)}")

    def exit_program(self):
        if self.confirm_discard_changes():
            self.root.quit()

    def confirm_discard_changes(self):
        if self.text_area.edit_modified():
            response = messagebox.askyesnocancel("Unsaved Changes", "Do you want to save changes before closing?")
            if response:
                self.save_file()
                return True
            elif response is None:
                return False
        return True

if __name__ == "__main__":
    root = tk.Tk()
    app = WordProcessor(root)
    root.mainloop()