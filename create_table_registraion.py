import mysql.connector

conn = mysql.connector.connect(host='localhost', user='root', password='0143', database='webgui')
mycursor = conn.cursor()

# Create the table
mycursor.execute('''
    CREATE TABLE registration(
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(30),
        course VARCHAR(30),
        fee VARCHAR(30)
    )
''')

# Commit the changes and close the connection
conn.commit()

print("Table Created!!")  # Print confirmation

conn.close()
