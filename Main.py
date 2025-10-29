import tkinter as tk
from tkinter import messagebox, ttk
import json

#classes and init
class Student:
    def __init__(self, roll, name, marks):
        self.name = name
        self.roll = roll
        self.marks = marks


class StudentManager:
    def __init__(self, filepath="students.json"):
        self.students = []
        self.filepath = filepath
        self.load_from_json()

    def load_from_json(self):
        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)
                for d in data:
                    self.students.append(Student(d["roll"], d["name"], d["marks"]))
        except FileNotFoundError:
            self.students = []

    def save_to_json(self):
        data = [{"roll": s.roll, "name": s.name, "marks": s.marks} for s in self.students]
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=4)

    def add_student(self, roll, name, marks):
        for s in self.students:
            if s.roll == roll:
                return False
        new_student = Student(roll, name, marks)
        self.students.append(new_student)
        self.save_to_json()
        return True

    def search_student(self, roll):
        for s in self.students:
            if s.roll == roll:
                return s
        return None


#TkinTer
manager = StudentManager()
window = tk.Tk()
window.geometry("650x550")
window.title("🎓 Student Management System")
window.configure(bg="#f4f6f9")

title_label = tk.Label(
    window,
    text="Student Management System",
    font=("Segoe UI", 18, "bold"),
    fg="#2c3e50",
    bg="#f4f6f9"
)
title_label.pack(pady=15)

#fRames
form_frame = tk.LabelFrame(window, text="➕ Add Student", font=("Segoe UI", 12, "bold"), bg="#ecf0f1", padx=15, pady=15)
form_frame.pack(padx=10, pady=10, fill="x")

tk.Label(form_frame, text="Roll Number:", font=("Segoe UI", 10, "bold"), bg="#ecf0f1").grid(row=0, column=0, padx=10, pady=8, sticky="e")
roll_entry = tk.Entry(form_frame, width=30)
roll_entry.grid(row=0, column=1, padx=10, pady=8)

tk.Label(form_frame, text="Name:", font=("Segoe UI", 10, "bold"), bg="#ecf0f1").grid(row=1, column=0, padx=10, pady=8, sticky="e")
name_entry = tk.Entry(form_frame, width=30)
name_entry.grid(row=1, column=1, padx=10, pady=8)

tk.Label(form_frame, text="Marks:", font=("Segoe UI", 10, "bold"), bg="#ecf0f1").grid(row=2, column=0, padx=10, pady=8, sticky="e")
marks_entry = tk.Entry(form_frame, width=30)
marks_entry.grid(row=2, column=1, padx=10, pady=8)

add_btn = tk.Button(form_frame, text="Add Student", bg="#27ae60", fg="white", font=("Segoe UI", 10, "bold"), command=lambda: add_student())
add_btn.grid(row=3, column=0, columnspan=2, pady=10)


#SEARCH FRAME
search_frame = tk.LabelFrame(window, text="🔍 Search Student", font=("Segoe UI", 12, "bold"), bg="#ecf0f1", padx=15, pady=15)
search_frame.pack(padx=10, pady=10, fill="x")

tk.Label(search_frame, text="Enter Roll Number:", font=("Segoe UI", 10, "bold"), bg="#ecf0f1").grid(row=0, column=0, padx=10, pady=5)
search_entry = tk.Entry(search_frame, width=30)
search_entry.grid(row=0, column=1, padx=10, pady=5)
search_btn = tk.Button(search_frame, text="Search", bg="#2980b9", fg="white", font=("Segoe UI", 10, "bold"), command=lambda: search_student())
search_btn.grid(row=0, column=2, padx=10, pady=5)


#STUDENT LIST
list_frame = tk.LabelFrame(window, text="📋 All Students", font=("Segoe UI", 12, "bold"), bg="#ecf0f1", padx=10, pady=10)
list_frame.pack(padx=10, pady=10, fill="both", expand=True)

listbox = tk.Listbox(list_frame, width=60, height=10, font=("Consolas", 10))
listbox.pack(padx=10, pady=5)


#EXIT BUTTON
exit_btn = tk.Button(window, text="Exit", bg="#c0392b", fg="white", font=("Segoe UI", 11, "bold"), width=12, command=lambda: exit_app())
exit_btn.pack(pady=15)


#FUNCTIONS
def add_student():
    roll = roll_entry.get().strip()
    name = name_entry.get().strip()
    marks = marks_entry.get().strip()

    if not roll or not name or not marks:
        messagebox.showwarning("Warning", "All fields are required!")
        return

    if manager.add_student(roll, name, marks):
        messagebox.showinfo("Success", f"Student '{name}' added successfully!")
        roll_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        marks_entry.delete(0, tk.END)
        refresh_list()
    else:
        messagebox.showerror("Error", "Roll number already exists!")


def search_student():
    roll = search_entry.get().strip()
    s = manager.search_student(roll)
    if s:
        messagebox.showinfo("Student Found", f"Name: {s.name}\nRoll: {s.roll}\nMarks: {s.marks}")
    else:
        messagebox.showerror("Not Found", f"No student found with roll {roll}")


def refresh_list():
    listbox.delete(0, tk.END)
    for s in manager.students:
        listbox.insert(tk.END, f"{s.roll:<10} | {s.name:<20} | Marks: {s.marks}")


def exit_app():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        window.destroy()


refresh_list()
window.mainloop()
