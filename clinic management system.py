import os  # For checking if a file exists and handling file paths
import csv  # For reading and writing CSV files
import tkinter as tk  # For creating GUI elements
from collections import deque  # For using a queue data structure
import tkinter.ttk as ttk  # For adding more complex widgets like Treeview
from datetime import date  # For handling dates
from PIL import ImageTk, Image  # For handling images in Tkinter

# Initialize a queue to keep track of injured individuals
queue = deque()

# Function to add injury information to CSV file and queue
def add_injury_info():
    path = 'C:\\Users\\dell\\Desktop\\management.csv'  # Path to CSV file
    injury_info = full_name.get()  # Get the name from entry field
    type_of_injury = injury_type.get()  # Get the injury type from entry field
    date_cunsultation = date.today()  # Get today's date for the injury entry
    queue.append(injury_info)  # Add injured person's name to the queue
    
    # Check if the CSV file exists, if not, create it with headers
    if not os.path.exists(path):
        headers = ['FullName', 'Injury', 'date', 'ConsultationFee']  # Define headers for CSV file
        with open(path, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
    
    # Append new injury information to the CSV file
    with open(path, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([injury_info, type_of_injury, date_cunsultation, ''])

# Function to handle moving to the next injured person in queue
def next():
    absent_injured = queue.popleft()  # Remove the first person from the queue
    path = 'C:\\Users\\dell\\Desktop\\management.csv'  # Path to CSV file
    rows = []
    
    # Read all rows from CSV file and store in list
    with open(path, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
    
    rows.remove(['FullName', 'Injury', 'date', 'ConsultationFee'])  # Remove header row
    
    # Find the row with the absent injured person and remove it
    for row in rows:
        if absent_injured in row:
            rows.remove(row)
            next_injury = 'no one' if len(queue) == 0 else queue[0]  # Set the next injured person if available

            # Create a popup window showing the next injured person
            popup2 = tk.Toplevel(background='#33ff33')
            popup2.geometry('300x150+500+300')
            popup2.title('next injured')
            notification = tk.Label(popup2, text=f"'{next_injury}' is next", background='#33ff33', 
                                    font=('Arial', 11, 'bold'), fg='#003300')
            notification.pack()
            popup2.after(5000, popup2.destroy)
    
    # Write updated list back to CSV, including header
    headers = ['FullName', 'Injury', 'date', 'ConsultationFee']
    with open(path, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow({'FullName': row[0], 'Injury': row[1], 'date': row[2], 'ConsultationFee': row[3]})

# Function to handle payment of consultation fee
def pay_consultation_fee():
    path = 'C:\\Users\\dell\\Desktop\\management.csv'  # Path to CSV file
    consultation_fee = consultation_price.get()  # Get consultation fee from input
    rows = []
    
    # Read all rows from CSV file and store in list
    with open(path, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
    
    rows.remove(['FullName', 'Injury', 'date', 'ConsultationFee'])  # Remove header row
    
    # Find first unpaid consultation entry and add the fee
    for row in rows:
        if len(row) <= 4 and row[3] == '':
            row[3] = consultation_fee  # Add fee to consultation column
            break
    
    # Write updated list back to CSV, including header
    headers = ['FullName', 'Injury', 'date', 'ConsultationFee']
    with open(path, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow({'FullName': row[0], 'Injury': row[1], 'date': row[2], 'ConsultationFee': row[3]})
    
    queue.popleft()  # Remove first person from queue
    next_injury = 'no one' if len(queue) == 0 else queue[0]  # Determine next injured person
    
    # Display a popup with the next injured person's name
    popup1 = tk.Toplevel(background='#33ff33')
    popup1.geometry('300x150+500+300')
    popup1.title('next injured')
    notification = tk.Label(popup1, text=f"'{next_injury}' is next", background='#33ff33', 
                            font=('Arial', 11, 'bold'), fg='#003300')
    notification.pack()
    popup1.after(5000, popup1.destroy)

# Function to display the list of injured people in a table
def show_list_injured():
    path = 'C:\\Users\\dell\\Desktop\\management.csv'  # Path to CSV file
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)  # Store all data from CSV
    
    columns = ("#1", "#2", "#3", "#4")  # Define table columns
    tree = ttk.Treeview(list_frame, columns=columns, show="headings")  # Treeview for table display
    fieldnames = ['FullName', 'Injury', 'date', 'ConsultationFee']  # Column headers
    
    # Configure columns and headers in Treeview
    for i in range(1, 5):
        tree.heading(f"#{i}", text=f"{fieldnames[i - 1]}")
        tree.column(f"#{i}", width=220)
    
    # Set up Treeview style
    tree['style'] = 'Treeview'
    style = ttk.Style()
    style.configure('Treeview', rowheight=25, background='#ceffa4', foreground='black', font=('Arial', 10, 'bold'))
    style.map('Treeview', background=[('selected', '#1af125')], foreground=[('selected', 'black')])

    # Insert each row of data into the Treeview
    for d in data:
        tree.insert("", "end", values=(f"{d['FullName']}", f"{d['Injury']}", f"{d['date']}", f"{d['ConsultationFee']}"))

    # Add vertical scrollbar to Treeview
    scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

# Function to calculate total consultation fees for today's date
def sum_of_fee():
    path = 'C:\\Users\\dell\\Desktop\\management.csv'  # Path to CSV file
    consultation_fee = []
    date_cunsultation = date.today()  # Get today's date
    
    # Read consultation fees for today's date from CSV
    with open(path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['date'] == str(date_cunsultation):
                consultation_fee.append(row['ConsultationFee'])
    
    # Convert fees to integers, calculate total
    consultation_fees = [int(num) for num in consultation_fee if num.isdigit()]
    
    # Show popup displaying the total consultation fees for today
    popup = tk.Toplevel(background='#33ff33')
    popup.geometry('300x150+1000+0')
    popup.title('Total consultation fee')
    notification = tk.Label(popup, text=f'total fee of today is: {sum(consultation_fees)}', background='#33ff33', 
                            font=('Arial', 11, 'bold'), fg='#003300')
    notification.pack()
    popup.after(5000, popup.destroy)

# Initialize main Tkinter window
window = tk.Tk()
window.title("Injured Management")

# Main frame with green background for layout of other frames and widgets
frame = tk.Frame(window, background='#4dffa6')
frame.grid(row=0, column=0, sticky='nsew')

# Frame for adding injury information
frame0 = tk.Frame(frame, background='#4dffa6', border=1, relief='solid', highlightbackground='#4dffa6', pady=27, padx=160)
frame0.grid(row=0, column=0, sticky='nsew')
full_name_label = tk.Label(frame0, text='Full Name', background='#4dffa6', font=('Arial', 10, 'bold'), fg='#1a1a00')
full_name_label.grid(row=0, column=0, sticky='nsew', padx=(0, 27), pady=(20, 0))
full_name = tk.Entry(frame0, width=30, background='#eeffcc')
full_name.insert(0, ' insert the full name')
full_name.bind("<FocusIn>", lambda e: full_name.delete('0', 'end'))
full_name.grid(row=0, column=1, sticky='nsew', padx=(63, 100), pady=(20, 0))

injury_type_label = tk.Label(frame0, text='Injury type', background='#4dffa6', font=('Arial', 10, 'bold'), fg='#1a1a00')
injury_type_label.grid(row=1, column=0, sticky='nsew', padx=(0, 27), pady=20)
injury_type = tk.Entry(frame0, width=30, background='#eeffcc')
injury_type.insert(0, ' insert the injury type')
injury_type.bind("<FocusIn>", lambda e: injury_type.delete('0', 'end'))
injury_type.grid(row=1, column=1, sticky='nsew', padx=(63, 100), pady=20)

add_button = tk.Button(frame0, text='add', command=add_injury_info, width=15, background='#39ac39', font=('Arial', 9, 'bold'), border=1)
add_button.grid(row=1, column=2, sticky='nsew', padx=(0, 27), pady=20)

# Frame for entering consultation fee
frame1 = tk.Frame(frame, background='#4dffa6', border=1, relief='solid', highlightbackground='#4dffa6', pady=27, padx=160)
frame1.grid(row=1, column=0, sticky='nsew')
consultation_label = tk.Label(frame1, text='Consultation Fee', background='#4dffa6', font=('Arial', 10, 'bold'), fg='#1a1a00')
consultation_label.grid(row=0, column=0, sticky='nsew', padx=(0, 27))
consultation_price = tk.Entry(frame1, width=30, background='#eeffcc')
consultation_price.insert(0, ' insert the consultation fee')
consultation_price.bind("<FocusIn>", lambda e: consultation_price.delete('0', 'end'))
consultation_price.grid(row=0, column=1, sticky='nsew', padx=(27, 100))

pay_button = tk.Button(frame1, text='payed', command=pay_consultation_fee, width=15, background='#39ac39', font=('Arial', 9, 'bold'), border=1)
pay_button.grid(row=0, column=2, sticky='nsew')

# Frame for pass, total fee, and show data buttons
frame2 = tk.Frame(frame, background='#4dffa6', border=1, relief='solid', highlightbackground='#4dffa6', pady=27)
frame2.grid(row=2, column=0, sticky='nsew')

pass_button = tk.Button(frame2, text='pass', command=next, width=15, background='#39ac39', font=('Arial', 9, 'bold'), border=1)
pass_button.grid(row=0, column=2, sticky='nsew', padx=(140, 0))

total_fee_button = tk.Button(frame2, text='total fee', command=sum_of_fee, width=15, background='#39ac39', font=('Arial', 9, 'bold'), border=1)
total_fee_button.grid(row=0, column=3, sticky='nsew', padx=130)

show_button = tk.Button(frame2, text='show data', command=show_list_injured, width=15, background='#39ac39', font=('Arial', 9, 'bold'), border=1)
show_button.grid(row=0, column=4, sticky='nsew', padx=(0, 140))

# Frame for displaying list of injured persons
list_frame = tk.LabelFrame(frame, text='The injured list', background='#ceffa4', fg='#2c530c', width=300, height=330, border=1, relief="solid", font=('Arial', 12, 'bold'))
list_frame.grid(row=3, column=0, sticky='nsew')

window.mainloop()  # Run the main event loop for the GUI
