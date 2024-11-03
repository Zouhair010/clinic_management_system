import tkinter as tk  # Import the tkinter library for GUI
import tkinter.ttk as ttk  # Import the themed tkinter widgets
from PIL import Image, ImageTk  # Import Pillow for image handling
import os  # Import os for file path operations
import csv  # Import csv for handling CSV files
from collections import deque  # Import deque for efficient queue operations
from datetime import date  # Import date for handling date-related operations

queue = deque()  # Initialize a deque to manage the injured person's queue

def add_injury_info():
    # Function to add injury information to a CSV file and queue
    path = 'C:\\Users\\dell\\Desktop\\management.csv'  # Specify the CSV file path
    injury_info = full_name.get()  # Get the full name from the entry field
    type_of_injury = injury_type.get()  # Get the type of injury from the entry field
    date_cunsultation = date.today()  # Get the current date
    queue.append(injury_info)  # Add the injured person's name to the queue
    if not os.path.exists(path):  # Check if the file does not exist
        headers = ['FullName', 'Injury', 'date', 'ConsultationFee']  # Define headers for the CSV
        with open(path, mode='w', newline='') as csvfile:  # Open the file for writing
            writer = csv.writer(csvfile)  # Create a CSV writer object
            writer.writerow(headers)  # Write the headers to the CSV file
    with open(path, mode='a', newline='') as csvfile:  # Open the file for appending
        writer = csv.writer(csvfile)  # Create a CSV writer object
        writer.writerow([injury_info, type_of_injury, date_cunsultation, ''])  # Write the injury info

def next():
    # Function to handle the next injured person in line
    absent_injured = queue.popleft()  # Remove the first person from the queue
    path = 'C:\\Users\\dell\\Desktop\\management.csv'  # Specify the CSV file path
    rows = []  # Initialize a list to hold the rows of the CSV
    with open(path, mode='r', newline='') as csvfile:  # Open the CSV file for reading
        reader = csv.reader(csvfile)  # Create a CSV reader object
        rows = list(reader)  # Read all rows into a list
    rows.remove(['FullName', 'Injury', 'date', 'ConsultationFee'])  # Remove the header row
    for row in rows:  # Iterate over the rows to find the absent injured
        if absent_injured in row:  # Check if the absent injured's name is in the row
            rows.remove(row)  # Remove the corresponding row
            if len(queue) == 0:  # Check if the queue is empty
                next_injury = 'no one'  # Set next injured to 'no one'
            else:
                next_injury = queue[0]  # Get the next person in the queue
            popup2 = tk.Toplevel(background='#33ff33')  # Create a popup window
            popup2.geometry('300x100+1000+140')  # Set the popup window size and position
            popup2.title('next injured')  # Set the title of the popup
            notification = tk.Label(popup2, text=f"'{next_injury}' is next", background='#33ff33', font=('Arial', 11, 'bold'), fg='#003300')  # Create a label with the notification
            notification.pack()  # Pack the label into the popup
            popup2.after(5000, popup2.destroy)  # Destroy the popup after 5 seconds
    headers = ['FullName', 'Injury', 'date', 'ConsultationFee']  # Define headers for the CSV
    with open(path, mode='w', newline='') as csvfile:  # Open the CSV file for writing
        writer = csv.DictWriter(csvfile, fieldnames=headers)  # Create a CSV DictWriter
        writer.writeheader()  # Write the headers to the CSV file
        for row in rows:  # Write the remaining rows back to the CSV
            writer.writerow({'FullName': row[0], 'Injury': row[1], 'date': row[2], 'ConsultationFee': row[3]})

def pay_consultation_fee():
    # Function to process the payment of consultation fees
    path = 'C:\\Users\\dell\\Desktop\\management.csv'  # Specify the CSV file path
    consultation_fee = consultation_price.get()  # Get the consultation fee from the entry field
    rows = []  # Initialize a list to hold the rows of the CSV
    with open(path, mode='r', newline='') as csvfile:  # Open the CSV file for reading
        reader = csv.reader(csvfile)  # Create a CSV reader object
        rows = list(reader)  # Read all rows into a list
    rows.remove(['FullName', 'Injury', 'date', 'ConsultationFee'])  # Remove the header row
    for row in rows:  # Iterate over the rows to find the empty consultation fee
        if len(row) <= 4 and row[3] == '':  # Check if the consultation fee is empty
            row[3] = consultation_fee  # Assign the consultation fee to the row
            break  # Exit the loop after updating the fee
    headers = ['FullName', 'Injury', 'date', 'ConsultationFee']  # Define headers for the CSV
    with open(path, mode='w', newline='') as csvfile:  # Open the CSV file for writing
        writer = csv.DictWriter(csvfile, fieldnames=headers)  # Create a CSV DictWriter
        writer.writeheader()  # Write the headers to the CSV file
        for row in rows:  # Write the updated rows back to the CSV
            writer.writerow({'FullName': row[0], 'Injury': row[1], 'date': row[2], 'ConsultationFee': row[3]})
    queue.popleft()  # Remove the first person from the queue
    if len(queue) == 0:  # Check if the queue is empty
        next_injury = 'no one'  # Set next injured to 'no one'
    else:
        next_injury = queue[0]  # Get the next person in the queue
    popup1 = tk.Toplevel(background='#33ff33')  # Create a popup window
    popup1.geometry('300x100+1000+140')  # Set the popup window size and position
    popup1.title('next injured')  # Set the title of the popup
    notification = tk.Label(popup1, text=f"'{next_injury}' is next", background='#33ff33', font=('Arial', 11, 'bold'), fg='#003300')  # Create a label with the notification
    notification.pack()  # Pack the label into the popup
    popup1.after(5000, popup1.destroy)  # Destroy the popup after 5 seconds

def show_list_injured():
    # Function to display the list of injured persons in a treeview
    path = 'C:\\Users\\dell\\Desktop\\management.csv'  # Specify the CSV file path
    with open(path, 'r') as csvfile:  # Open the CSV file for reading
        reader = csv.DictReader(csvfile)  # Create a CSV DictReader
        data = list(reader)  # Read all data into a list
    columns = ("#1", "#2", "#3", "#4")  # Define the column numbers for the treeview
    tree = ttk.Treeview(list_frame, columns=columns, show="headings")  # Create a treeview for displaying data
    fieldnames = ['FullName', 'Injury', 'date', 'ConsultationFee']  # Define column names
    for i in range(1, 5):  # Set the column headings and widths
        tree.heading(f"#{i}", text=f"{fieldnames[i-1]}")  # Set the heading for each column
        tree.column(f"#{i}", width=220)  # Set the width for each column

    tree['style'] = 'Treeview'  # Set the style for the treeview
    style = ttk.Style()  # Create a style object for the treeview
    style.configure('Treeview', rowheight=25, background='#80bfff', foreground='black', font=('Arial', 10, 'bold'))  # Configure treeview style
    style.map('Treeview', background=[('selected', '#ff33ff')], foreground=[('selected', 'black')])  # Set selection colors

    for d in data:  # Iterate through the data to insert into the treeview
        tree.insert("", "end", values=(f"{d['FullName']}", f"{d['Injury']}", f"{d['date']}", f"{d['ConsultationFee']}"))  # Insert each row into the treeview

    scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)  # Create a vertical scrollbar for the treeview
    tree.configure(yscroll=scrollbar.set)  # Link the scrollbar to the treeview
    tree.grid(row=0, column=0, sticky="nsew")  # Position the treeview in the grid
    scrollbar.grid(row=0, column=1, sticky="ns")  # Position the scrollbar in the grid

def sum_of_fee():
    # Function to calculate and display the total consultation fee for today
    path = 'C:\\Users\\dell\\Desktop\\management.csv'  # Specify the CSV file path
    consultation_fee = []  # Initialize a list to store consultation fees
    date_cunsultation = date.today()  # Get today's date
    with open(path, mode='r', newline='') as csvfile:  # Open the CSV file for reading
        reader = csv.DictReader(csvfile)  # Create a CSV DictReader
        for row in reader:  # Iterate over the rows to find today's consultation fees
            if row['date'] == str(date_cunsultation):  # Check if the date matches today
                consultation_fee.append(row['ConsultationFee'])  # Add the fee to the list
    consultation_fees = [int(num) for num in consultation_fee if num.isdigit()]  # Convert fees to integers
    popup = tk.Toplevel(background='#33ff33')  # Create a popup window
    popup.geometry('300x100+1000+0')  # Set the popup window size and position
    popup.title('Total consultation fee')  # Set the title of the popup
    notification = tk.Label(popup, text=f'total fee of today is: {sum(consultation_fees)}', background='#33ff33', font=('Arial', 11, 'bold'), fg='#003300')  # Create a label with the total fee
    notification.pack()  # Pack the label into the popup
    popup.after(5000, popup.destroy)  # Destroy the popup after 5 seconds

window = tk.Tk()  # Create the main application window
window.title("Injured Management")  # Set the window title
window.geometry("900x600")  # Set the window size
window.resizable()  # Allow the window to be resizable

# Load and resize the background image
background_image = Image.open("C:\\Users\\dell\\Desktop\\—Pngtree—a doctor in white coat.png")  # Specify the path for the background image
background_image = background_image.resize((900, 600), Image.LANCZOS)  # Resize the image
background_photo = ImageTk.PhotoImage(background_image)  # Convert the image for tkinter usage

# Create a canvas to hold the background image
canvas = tk.Canvas(window, width=window.winfo_screenwidth(), height=window.winfo_screenheight())
canvas.pack(fill="both", expand=True)  # Fill the window with the canvas
canvas.create_image(0, 0, image=background_photo, anchor="nw")  # Place the background image

# Create lines on the canvas for visual separation
line1 = canvas.create_line(0, 120, 900, 120, fill='black', width=1)
line2 = canvas.create_line(0, 200, 900, 200, fill='black', width=1)
canvas.tag_raise(line1)  # Raise the first line above the image
canvas.tag_raise(line2)  # Raise the second line above the image

# Create labels and entry fields for user input
full_name_label = tk.Label(canvas, text='Full Name            ', font=('Arial', 10, 'bold'), fg='#800080')  # Label for full name
full_name_label.grid(row=0, column=0, sticky='nsew', padx=(130, 27), pady=(20, 0))  # Position the label
full_name = tk.Entry(canvas, width=30, background='#eeffcc')  # Entry field for full name
full_name.insert(0, ' insert the full name')  # Placeholder text
full_name.bind("<FocusIn>", lambda e: full_name.delete('0', 'end'))  # Clear placeholder on focus
full_name.grid(row=0, column=1, sticky='nsew', padx=(63, 100), pady=(20, 0))  # Position the entry

injury_type_label = tk.Label(canvas, text='Injury type           ', font=('Arial', 10, 'bold'), fg='#800080')  # Label for injury type
injury_type_label.grid(row=1, column=0, sticky='nsew', padx=(130, 27), pady=20)  # Position the label
injury_type = tk.Entry(canvas, width=30, background='#eeffcc')  # Entry field for injury type
injury_type.insert(0, ' insert the injury type')  # Placeholder text
injury_type.bind("<FocusIn>", lambda e: injury_type.delete('0', 'end'))  # Clear placeholder on focus
injury_type.grid(row=1, column=1, sticky='nsew', padx=(63, 100), pady=20)  # Position the entry

# Create buttons for actions
add_button = tk.Button(canvas, text='add', command=add_injury_info, width=15, background='#3385ff', font=('Arial', 10, 'bold'), border=1)  # Button to add injury info
add_button.grid(row=1, column=2, sticky='nsew', padx=(27, 5), pady=20)  # Position the button

consultation_label = tk.Label(canvas, text='Consultation Fee', font=('Arial', 10, 'bold'), fg='#800080')  # Label for consultation fee
consultation_label.grid(row=2, column=0, sticky='nsew', padx=(130, 27), pady=40)  # Position the label
consultation_price = tk.Entry(canvas, width=30, background='#eeffcc')  # Entry field for consultation fee
consultation_price.insert(0, ' insert the consultation fee')  # Placeholder text
consultation_price.bind("<FocusIn>", lambda e: consultation_price.delete('0', 'end'))  # Clear placeholder on focus
consultation_price.grid(row=2, column=1, sticky='nsew', padx=(63, 100), pady=40)  # Position the entry

pay_button = tk.Button(canvas, text='payed', command=pay_consultation_fee, width=15, background='#00ff00', font=('Arial', 10, 'bold'), border=1)  # Button to pay consultation fee
pay_button.grid(row=2, column=2, sticky='nsew', padx=(27, 5), pady=40)  # Position the button

pass_button = tk.Button(canvas, text='pass', command=next, width=15, background='#00ffcc', font=('Arial', 10, 'bold'), border=1)  # Button to skip to the next injured person
pass_button.grid(row=3, column=2, sticky='nsew', padx=(27, 5), pady=10)  # Position the button

total_fee_button = tk.Button(canvas, text='total fee', command=sum_of_fee, width=15, background='#66ccff', font=('Arial', 10, 'bold'), border=1)  # Button to calculate total fees
total_fee_button.grid(row=4, column=2, sticky='nsew', padx=(27, 5))  # Position the button

show_button = tk.Button(canvas, text='show data', command=show_list_injured, width=15, background='#ff33ff', font=('Arial', 10, 'bold'), border=1)  # Button to show the list of injured persons
show_button.grid(row=5, column=2, sticky='nsew', padx=(27, 5), pady=10)  # Position the button

# Create a frame to display the list of injured persons
list_frame = tk.LabelFrame(window, text='The injured list', background='#80bfff', fg='#800080', highlightbackground='#800080', border=1, width=900, height=300, relief="solid", font=('Arial', 11, 'bold'))
list_frame.pack(side=('left'))  # Pack the frame to the left side of the window

window.rowconfigure(4, weight=1)  # Configure the grid weight for proper resizing

window.mainloop()  # Start the main event loop
