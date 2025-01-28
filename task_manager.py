import os
import tkinter as tk
from tkinter import ttk, messagebox


# Hard-coded base directory for storing user files
BASE_DIR = ""

# Ensure the base directory exists
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)


# Utility function to get the full path for a user's file
def get_user_file_path(username):
    return os.path.join(BASE_DIR, f"{username}_task.txt")


def main():
    def login():
        username = username_entry.get()
        password = password_entry.get()
        user_file_path = get_user_file_path(username)

        try:
            with open(user_file_path, "r") as file:
                stored_password = file.readline().strip()
                if password == stored_password:
                    show_task_manager(username)
                else:
                    messagebox.showerror("Error", "Incorrect password!")
        except FileNotFoundError:
            messagebox.showerror("Error", "Account not found!")

    def signup():
        username = username_entry.get()
        password = password_entry.get()
        user_file_path = get_user_file_path(username)

        try:
            with open(user_file_path, "x") as file:
                file.write(f"{password}\n")  # Save password on the first line
            messagebox.showinfo("Success", "Account created successfully!")
        except FileExistsError:
            messagebox.showerror("Error", "Account already exists!")

    def show_task_manager(username):
        for widget in root.winfo_children():
            widget.destroy()

        ttk.Label(root, text=f"Welcome, {username}!", style="Header.TLabel").pack(pady=10)

        task_frame = ttk.Frame(root)
        task_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tree = ttk.Treeview(task_frame, columns=("Task", "Deadline"), show="headings", height=10)
        tree.heading("Task", text="Task")
        tree.heading("Deadline", text="Deadline")
        tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(task_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        try:
            user_file_path = get_user_file_path(username)
            with open(user_file_path, "r") as file:
                tasks = file.readlines()[1:]  # Skip the password line
            for idx, task in enumerate(tasks):
                if task.strip():
                    task_data = task.split(",")  # Tasks are stored as "Task: ..., Deadline: ..."
                    task_name = task_data[0].replace("Task: ", "").strip()
                    task_deadline = task_data[1].replace("Deadline: ", "").strip() if len(
                        task_data) > 1 else "No Deadline"
                    tree.insert("", "end", values=(task_name, task_deadline))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tasks: {str(e)}")

        button_frame = ttk.Frame(root)
        button_frame.pack(fill="x", pady=10)

        ttk.Button(button_frame, text="Add Task", command=lambda: add_task(username, tree)).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Edit Task", command=lambda: edit_task(username, tree)).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Sign Out", command=sign_out).pack(side="right", padx=5)

    def add_task(username, tree):
        def save_task():
            task_name = task_entry.get()
            task_deadline = deadline_entry.get()
            if not task_name or not task_deadline:
                messagebox.showerror("Error", "Both fields are required!")
                return
            try:
                user_file_path = get_user_file_path(username)
                with open(user_file_path, "a") as file:
                    file.write(f"Task: {task_name}, Deadline: {task_deadline}\n")
                tree.insert("", "end", values=(task_name, task_deadline))
                messagebox.showinfo("Success", "Task added successfully!")
                add_task_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        add_task_window = tk.Toplevel(root)
        add_task_window.title("Add Task")

        ttk.Label(add_task_window, text="Add a New Task", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(add_task_window, text="Task Name:").grid(row=1, column=0, sticky="w", padx=10)
        task_entry = ttk.Entry(add_task_window, width=30)
        task_entry.grid(row=1, column=1, pady=5)

        ttk.Label(add_task_window, text="Deadline:").grid(row=2, column=0, sticky="w", padx=10)
        deadline_entry = ttk.Entry(add_task_window, width=30)
        deadline_entry.grid(row=2, column=1, pady=5)

        ttk.Button(add_task_window, text="Add Task", command=save_task).grid(row=3, column=0, columnspan=2, pady=10)

    def edit_task(username, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No task selected!")
            return

        task_values = tree.item(selected_item, "values")
        task_name, task_deadline = task_values

        def save_changes():
            new_task_name = task_entry.get()
            new_task_deadline = deadline_entry.get()
            if not new_task_name or not new_task_deadline:
                messagebox.showerror("Error", "Both fields are required!")
                return
            try:
                user_file_path = get_user_file_path(username)
                with open(user_file_path, "r") as file:
                    lines = file.readlines()
                with open(user_file_path, "w") as file:
                    for line in lines:
                        if f"Task: {task_name}, Deadline: {task_deadline}" in line:
                            file.write(f"Task: {new_task_name}, Deadline: {new_task_deadline}\n")
                        else:
                            file.write(line)
                tree.item(selected_item, values=(new_task_name, new_task_deadline))
                messagebox.showinfo("Success", "Task updated successfully!")
                edit_task_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update task: {str(e)}")

        edit_task_window = tk.Toplevel(root)
        edit_task_window.title("Edit Task")

        ttk.Label(edit_task_window, text="Edit Task", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(edit_task_window, text="Task Name:").grid(row=1, column=0, sticky="w", padx=10)
        task_entry = ttk.Entry(edit_task_window, width=30)
        task_entry.insert(0, task_name)
        task_entry.grid(row=1, column=1, pady=5)

        ttk.Label(edit_task_window, text="Deadline:").grid(row=2, column=0, sticky="w", padx=10)
        deadline_entry = ttk.Entry(edit_task_window, width=30)
        deadline_entry.insert(0, task_deadline)
        deadline_entry.grid(row=2, column=1, pady=5)

        ttk.Button(edit_task_window, text="Save Changes", command=save_changes).grid(row=3, column=0, columnspan=2, pady=10)

    def sign_out():
        root.destroy()
        main()

    root = tk.Tk()
    root.title("Task Manager")

    style = ttk.Style()
    style.configure("Header.TLabel", font=("Arial", 16, "bold"))

    ttk.Label(root, text="Task Manager", style="Header.TLabel").pack(pady=10)

    username_label = ttk.Label(root, text="Username:")
    username_label.pack(pady=5)
    username_entry = ttk.Entry(root)
    username_entry.pack(pady=5)

    password_label = ttk.Label(root, text="Password:")
    password_label.pack(pady=5)
    password_entry = ttk.Entry(root, show="*")
    password_entry.pack(pady=5)

    ttk.Button(root, text="Login", command=login).pack(pady=5)
    ttk.Button(root, text="Sign Up", command=signup).pack(pady=5)

    root.mainloop()


main()