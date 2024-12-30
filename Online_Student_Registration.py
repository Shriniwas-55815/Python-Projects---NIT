import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox


# Function to create a database connection
def my_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root', 
        password='0143',
        database='webgui'
    )

# Function to add student records to the database
def Add_record():
    name = e2.get()
    course = e3.get()
    fee = e4.get()
    
    if not name or not course or not  fee:
        messagebox.showerror("Input Error","All Fields, must be filled")
        return
    try:
        conn = my_db_connection()
        mycursor = conn.cursor()
        
        sql = "insert into registration(name, course, fee) VALUES(%s, %s, %s)"
        values = (name, course, fee)
        
        mycursor.execute(sql, values)
        conn.commit()
        
        messagebox.Message("Student record added successfully!")
        e2.delete(0, tk.END)
        e3.delete(0, tk.END)
        e4.delete(0, tk.END)
        
        load_students()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to insert student: {err}")
        
    finally:
        conn.close()    


# Function to update student record
def update_student():
    selected_item = listBox.selection()
    if not selected_item:
        messagebox.showerror("Selection Error", "Please select a student to update.")
        return

    studentid = e1.get()
    studentname = e2.get()
    coursename = e3.get()
    fee = e4.get()

    if not studentname or not coursename or not fee:
        messagebox.showerror("Input Error", "All fields must be filled.")
        return

    try:
        conn = my_db_connection()
        cursor = conn.cursor()

        sql = "UPDATE registration SET name=%s, course=%s, fee=%s WHERE id=%s"
        values = (studentname, coursename, fee, studentid)
        
        cursor.execute(sql, values)
        conn.commit()
        
        messagebox.showinfo("Success", "Student record updated successfully!")

        e1.delete(0, tk.END)
        e2.delete(0, tk.END)
        e3.delete(0, tk.END)
        e4.delete(0, tk.END)

        load_students()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to update student: {err}")
    finally:
        conn.close()



# Function to delete a student
def  delete_student():
    id= e1.get()
    
    if not id:
        messagebox.showerror("Selection Error", "Please select a student to delete.")
        return
    
    try:
        conn= my_db_connection()
        mycursor= conn.cursor()
        
        sql = "delete from registration where id = %s"
        mycursor.execute(sql, (id,))
        conn.commit()
        
        messagebox.showinfo("Success", "Student record updated successfully!")
        e1.delete(0, tk.END)
        e2.delete(0, tk.END)
        e3.delete(0, tk.END)
        e4.delete(0, tk.END)
        
        load_students()
        
    except mysql.connector.errors as err:
        messagebox.showerror("Database Error", f"Failed to delete student: {err}")
        return
    
    finally:
        conn.close()

    

# Function to Load a student
def load_students():
    for row in listBox.get_children():
        listBox.delete(row)

    try:
        conn = my_db_connection()
        mycursor= conn.cursor()
    
        sql = "select * from registration"
        mycursor.execute(sql)
        rows = mycursor.fetchall()
        
        for row in rows:
            listBox.insert("", "end", values=row)
        
        e1.config(state="disabled")  # Initially disabled, editable when selecting a student
        
    except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to load students: {err}")
            
    finally:
            conn.close()


# Function to populate the entry fields when a row is selected
def on_treeview_select(event):
    selected_item = listBox.selection()
    if selected_item:
        student = listBox.item(selected_item)
        id, name, course, fee = student['values']
        
        # Populate the entry fields with the selected student's data
        e1.config(state="normal")  # Make the ID entry editable to update
        e1.delete(0, tk.END)
        e1.insert(0, id)  # Set the student ID for deletion or update

        e2.delete(0, tk.END)
        e2.insert(0, name)

        e3.delete(0, tk.END)
        e3.insert(0, course)

        e4.delete(0, tk.END)
        e4.insert(0, fee)



# Create the main window
root = tk.Tk()
root.title('Registration Form')
root.geometry('650x600')

# Title Label with Border, aligned to the right
lable = tk.Label(root, text='                  Online Student Registration Process                  ', fg='green', font=("Arial", 16, "bold"), borderwidth=2, relief='groove')
lable.grid(row=0, column=0, columnspan=3, pady=10, padx=10)  # 'sticky' aligns it to the right ('e' stands for east)

# Labels and Entry Fields
tk.Label(root, text='STUDENT ID').grid(row=1, column=0,padx=5, pady=5)
tk.Label(root, text='STUDENT NAME').grid(row=2, column=0,padx=5, pady=5)
tk.Label(root, text="COURSE NAME").grid(row=3,column=0,padx=5, pady=5)
tk.Label(root, text="TOTAL FEES").grid(row=4,column=0,padx=5, pady=5)

# Text Boxes
#id
e1 = tk.Entry(root)
e1.grid(row=1, column=1, padx=5, pady=5)
e1.config(state="disabled")  # Initially disabled, editable when selecting a student
# Name
e2 = tk.Entry(root)
e2.grid(row=2, column=1, padx=5, pady=5)
# course
e3 = tk.Entry(root)
e3.grid(row=3, column=1, padx=5, pady=5)
# fees
e4 = tk.Entry(root)
e4.grid(row=4, column=1, padx=5, pady=5)

# Buttons
tk.Button(root, text='ADD', bg='lightgreen',width=10, height=2, command=Add_record).grid(row=1,column=2,padx=5, pady=5)
tk.Button(root, text="UPDATE", bg='lightblue',width=10, height=2, command=update_student).grid(row=2, column=2, padx=5, pady=5)
tk.Button(root, text='DELETE', bg='red',fg=('white'),width=10, height=2, command=delete_student).grid(row=3, column=2, padx=5, pady=5 )

# Treeview to display students
cols = ("STUDENT ID", "STUDENT NAME", "COURSE SELECTED", "TOTAL FEES")
listBox = ttk.Treeview(root, columns=cols, show="headings")
listBox.grid(row=10,column=0,columnspan=3, padx=10, pady=10)

for col in cols:
    listBox.heading(col, text=col)
    listBox.column(col, width=150)

# Bind the select event to populate entry fields when a row is clicked
listBox.bind("<ButtonRelease-1>", on_treeview_select)

# Load the student records when the application starts
load_students()

# View Windwow
root.mainloop()