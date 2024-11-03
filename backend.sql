import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('students.db')
c = conn.cursor()

# Query to select all students
c.execute("SELECT * FROM students")

# Fetch all results
students = c.fetchall()
    
# Print the results
if students:
    print(f"{'ID':<5} {'Name':<20} {'Age':<5} {'Course':<15}")
    print("-" * 50)  # Separator
    for student in students:
        print(f"{student[0]:<5} {student[1]:<20} {student[2]:<5} {student[3]:<15}")
else:
    print("No students found.")

# Close the database connection
conn.close()