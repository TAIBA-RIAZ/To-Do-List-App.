# To-Do List App
import tkinter as tk  # Import tkinter for GUI components
from tkinter import messagebox  # For showing error or info messages
import json  # For saving and loading tasks from a JSON file
import os  # To check if file exists
from datetime import datetime  # For timestamping tasks

# JSON File Setup
TASKS_FILE = "tasks.json" # File where tasks will be stored

# Load tasks from file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            data = json.load(f)

            # Convert old list to new format
            if isinstance(data, list) and all(isinstance(item, str) for item in data):
                return [{"title": item, "done": False, "date": datetime.today().strftime("%Y-%m-%d")} for item in data]

            # Add date if missing
            for task in data:
                if "date" not in task:
                    task["date"] = datetime.today().strftime("%Y-%m-%d")
            return data
    return []

# Save tasks to file
def save_tasks():
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

# Add new task
def add_task():
    title = entry.get().strip()
    if title:
        today = datetime.today().strftime("%Y-%m-%d")
        task = {"title": title, "done": False, "date": today}
        tasks.append(task)
        save_tasks()
        update_tasks_ui()
        entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")

# Toggle task completion
def toggle_task(index): # index is the task's position in the list
    tasks[index]["done"] = not tasks[index]["done"]
    save_tasks()
    update_tasks_ui()

# Delete completed tasks
def delete_completed_tasks():
    global tasks
    tasks = [t for t in tasks if not t["done"]]
    save_tasks()
    update_tasks_ui()

# Display tasks with date
def update_tasks_ui():
    for widget in task_frame.winfo_children():
        widget.destroy()

    for i, task in enumerate(tasks):
        var = tk.BooleanVar(value=task["done"])
        date = task.get("date", "Unknown")
        label_text = f"{task['title']} (Added: {date})"
        cb = tk.Checkbutton(task_frame, text=label_text, variable=var,
                            font=("Arial", 12), anchor="w", width=50,
                            bg="white", justify="left", wraplength=400,
                            command=lambda idx=i: toggle_task(idx))
        cb.pack(anchor="w", padx=10, pady=2)

# Setup GUI
root = tk.Tk()
root.title("📝 To-Do List with Date")
root.geometry("500x500")
root.configure(bg="white")

entry = tk.Entry(root, font=("Arial", 14), width=30)
entry.pack(pady=10)

add_btn = tk.Button(root, text="Add Task", command=add_task,
                    bg="purple", fg="white", width=15, font=("Arial", 12))
add_btn.pack(pady=5)

del_btn = tk.Button(root, text="Delete Completed", command=delete_completed_tasks,
                    bg="purple", fg="white", width=15, font=("Arial", 12))
del_btn.pack(pady=5)

task_frame = tk.Frame(root, bg="white")
task_frame.pack(pady=10)

tasks = load_tasks()
update_tasks_ui()

root.mainloop()
