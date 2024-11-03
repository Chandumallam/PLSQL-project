import customtkinter as ctk
from tkinter import messagebox, StringVar
import sqlite3

# Set the theme and appearance
ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('students.db')
c = conn.cursor()

# Create a students table if it doesn't exist
c.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    course TEXT
)
''')
conn.commit()

# Initialize Tkinter window
root = ctk.CTk()
root.title("Student Database Management System")
root.geometry("400x720")

# Create StringVar for courses
course_var_add = StringVar(value="Select Course")
course_var_update = StringVar(value="Select Course")

# Sample courses
courses = ["Mathematics", "Science", "English", "History"]

# Function to add a student
def add_student():
    name = entry_name.get()
    age = entry_age.get()
    course = course_var_add.get()

    if name and age.isdigit() and course in courses:
        c.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)"
                  , (name, int(age), course))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully!")
        clear_entries()
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields with valid data.")

# Function to clear input fields after operations
def clear_entries():
    entry_name.delete(0, ctk.END)
    entry_age.delete(0, ctk.END)
    course_var_add.set("Select Course")

# Function to update a student
def update_student():
    name = entry_update_name.get()
    age = entry_update_age.get()
    course = course_var_update.get()

    if name and age.isdigit() and course in courses:
        c.execute("UPDATE students SET age=?, course=? WHERE name=?", (int(age), course, name))
        conn.commit()
        
        if c.rowcount > 0:
            messagebox.showinfo("Success", "Student updated successfully!")
        else:
            messagebox.showwarning("Not Found", "Student not found. Cannot update.")
        
        clear_update_entries()
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields with valid data.")

# Function to clear update input fields
def clear_update_entries():
    entry_update_name.delete(0, ctk.END)
    entry_update_age.delete(0, ctk.END)
    course_var_update.set("Select Course")

# Function to delete a student
def delete_student():
    name = entry_delete_name.get()

    if name:
        c.execute("DELETE FROM students WHERE name=?", (name,))
        conn.commit()
        
        if c.rowcount > 0:
            messagebox.showinfo("Success", "Student deleted successfully!")
        else:
            messagebox.showwarning("Not Found", "Student not found. Cannot delete.")
        
        clear_delete_entries()
    else:
        messagebox.showwarning("Input Error", "Please enter a name.")

# Function to clear delete input fields
def clear_delete_entries():
    entry_delete_name.delete(0, ctk.END)

# Function to search for a student
def search_student():
    name = entry_search_name.get()

    if name:
        c.execute("SELECT * FROM students WHERE name=?", (name,))
        students = c.fetchall()  # Fetch all records with the matching name
        
        if students:
            student_info = "\n".join([f"Name: {student[1]}, Age: {student[2]}, Course: 
                                      {student[3]}" for student in students])
            messagebox.showinfo("Students Found", student_info)
        else:
            messagebox.showwarning("Not Found", "No students found with this name.")
        
        clear_search_entries()
    else:
        messagebox.showwarning("Input Error", "Please enter a name.")

# Function to clear search input fields
def clear_search_entries():
    entry_search_name.delete(0, ctk.END)

# Layout for adding a student
frame = ctk.CTkFrame(root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

ctk.CTkLabel(frame, text="Add Student", font=('Arial', 14)).grid(row=0, columnspan=2, pady=10)

ctk.CTkLabel(frame, text="Name:").grid(row=1, column=0, padx=10, pady=5)
entry_name = ctk.CTkEntry(frame)
entry_name.grid(row=1, column=1, padx=10, pady=5)

ctk.CTkLabel(frame, text="Age:").grid(row=2, column=0, padx=10, pady=5)
entry_age = ctk.CTkEntry(frame)
entry_age.grid(row=2, column=1, padx=10, pady=5)

ctk.CTkLabel(frame, text="Select Course:").grid(row=3, column=0, padx=10, pady=5)
course_menu_add = ctk.CTkOptionMenu(frame, variable=course_var_add, values=courses)
course_menu_add.grid(row=3, column=1, padx=10, pady=5)

ctk.CTkButton(frame, text="Add Student", command=add_student).grid(row=4, columnspan=2, pady=10)

# Layout for updating a student
ctk.CTkLabel(frame, text="Update Student", font=('Arial', 14)).grid(row=5, columnspan=2, pady=10)

ctk.CTkLabel(frame, text="Name:").grid(row=6, column=0, padx=10, pady=5)
entry_update_name = ctk.CTkEntry(frame)
entry_update_name.grid(row=6, column=1, padx=10, pady=5)

ctk.CTkLabel(frame, text="New Age:").grid(row=7, column=0, padx=10, pady=5)
entry_update_age = ctk.CTkEntry(frame)
entry_update_age.grid(row=7, column=1, padx=10, pady=5)

ctk.CTkLabel(frame, text="Select Course:").grid(row=8, column=0, padx=10, pady=5)
course_menu_update = ctk.CTkOptionMenu(frame, variable=course_var_update, values=courses)
course_menu_update.grid(row=8, column=1, padx=10, pady=5)

ctk.CTkButton(frame, text="Update Student", command=update_student).grid(row=9, columnspan=2, pady=10)

# Layout for deleting a student
ctk.CTkLabel(frame, text="Delete Student", font=('Arial', 14)).grid(row=10, columnspan=2, pady=10)

ctk.CTkLabel(frame, text="Name:").grid(row=11, column=0, padx=10, pady=5)
entry_delete_name = ctk.CTkEntry(frame)
entry_delete_name.grid(row=11, column=1, padx=10, pady=5)

ctk.CTkButton(frame, text="Delete Student", command=delete_student).grid(row=12, columnspan=2, pady=10)

# Layout for searching a student
ctk.CTkLabel(frame, text="Search Student", font=('Arial', 14)).grid(row=13, columnspan=2, pady=10)

ctk.CTkLabel(frame, text="Name:").grid(row=14, column=0, padx=10, pady=5)
entry_search_name = ctk.CTkEntry(frame)
entry_search_name.grid(row=14, column=1, padx=10, pady=5)

ctk.CTkButton(frame, text="Search Student", command=search_student).grid(row=15, columnspan=2, pady=10)

# Start the Tkinter main loop
root.mainloop()

# Close the database connection
conn.close()