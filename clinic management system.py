import mysql.connector
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from collections import deque
from datetime import date

# Connect to the MySQL database
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='*********',
    database='clinic_management'
)

# Create a cursor for executing SQL commands
my_cursor = mydb.cursor()

# Create table if it doesn't exist
my_cursor.execute("create table if not exists consultants (consultantID int AUTO_INCREMENT, Nom_et_Prenom varchar(255) not null ,CIN varchar(255) not null , Age int not null, Telephone varchar(255) not null, Consultation varchar(255) not null, Adresse varchar(255) not null, Traitement varchar(255) not null, Diagnostic varchar(255) not null, Date_de_Consultation date not null, Tarif int not null, primary key(consultantID))")

# Queue to store consultant information
queue = deque()

# Function to add a new injury record to the queue
def add_injury_info():
    injury_info = full_name.get()
    phone_number = telephone_number.get()
    type_of_injury = injury_type.get()
    date_cunsultation = date.today()
    
    # Append consultant info as a tuple
    consultant_info = [('FullName', injury_info), ('TelephoneNumber', phone_number), 
                       ('InjuryType', type_of_injury), ('ConsultationDate', date_cunsultation)]
    queue.append(consultant_info)

# Function to move to the next injury in the queue
def next():
    absent_injured = queue.popleft()[0][1]  # Remove the first item
    next_injury = 'no one' if len(queue) == 0 else queue[0][0][1]  # Check next injured person

    # Show popup with the next person in the queue
    popup2 = tk.Toplevel(background='#33ff33')
    popup2.geometry('300x100+1000+140')
    popup2.title('Next Injured')
    notification = tk.Label(
        popup2, text=f"'{next_injury}' is next",
        background='#33ff33', font=('Arial', 11, 'bold'), fg='#003300'
    )
    notification.pack()
    popup2.after(5000, popup2.destroy)  # Destroy after 5 seconds

# Function to process payment and save consultant info to the database
def pay_consultation_fee():
    consultant = queue.popleft()  # Remove the next consultant
    consultation_fee = int(consultation_price.get())
    FullName, TelephoneNumber, InjuryType, ConsultationDate = consultant

    # Insert consultant details into the database
    sql = ('INSERT INTO consultants (FullName, TelephoneNumber, InjuryType, '
           'ConsultationDate, ConsultationFee) VALUES (%s, %s, %s, %s, %s)')
    val = (FullName[1], TelephoneNumber[1], InjuryType[1], ConsultationDate[1], consultation_fee)
    my_cursor.execute(sql, val)
    mydb.commit()

    # Update the next injured person display
    next_injury = 'no one' if len(queue) == 0 else queue[0][0][1]
    popup2 = tk.Toplevel(background='#33ff33')
    popup2.geometry('300x100+1000+140')
    popup2.title('Next Injured')
    notification = tk.Label(
        popup2, text=f"'{next_injury}' is next",
        background='#33ff33', font=('Arial', 11, 'bold'), fg='#003300'
    )
    notification.pack()
    popup2.after(5000, popup2.destroy)

# Function to display the total fees collected for today
def sum_of_fee():
    sql = 'SELECT SUM(ConsultationFee) FROM consultants WHERE ConsultationDate = CURRENT_DATE()'
    my_cursor.execute(sql)
    myresult = my_cursor.fetchall()

    # Display the total fee in a popup
    popup2 = tk.Toplevel(background='#33ff33')
    popup2.geometry('300x100+1000+140')
    popup2.title('Total Fee for Today')
    notification = tk.Label(
        popup2, text=f"The total fee of today is: {int(myresult[0][0])}",
        background='#33ff33', font=('Arial', 11, 'bold'), fg='#003300'
    )
    notification.pack()
    popup2.after(5000, popup2.destroy)

# Function to display the list of all injured persons in the table
def show_list_injured():
    sql = 'SELECT FullName, TelephoneNumber, InjuryType, ConsultationDate, ConsultationFee FROM consultants'
    my_cursor.execute(sql)
    myresult = my_cursor.fetchall()

    # Define table structure and styles
    columns = ("#1", "#2", "#3", "#4", "#5")
    tree = ttk.Treeview(list_frame, columns=columns, height=5, show="headings")
    fieldnames = ['Full Name', 'Telephone Number', 'Injury Type', 'Consultation Date', 'Consultation Fee']
    
    for i in range(1, 6):
        tree.heading(f"#{i}", text=f"{fieldnames[i-1]}", anchor='w')
        tree.column(f"#{i}", width=269)

    # Apply styling to the table
    style = ttk.Style()
    style.configure('Treeview', rowheight=29, background='#80bfff', foreground='black', font=('Arial', 10, 'bold'))
    style.map('Treeview', background=[('selected', '#ff33ff')], foreground=[('selected', 'black')])

    # Insert data into the table
    for data in myresult:
        tree.insert("", "end", values=(data[0], data[1], data[2], data[3], data[4]))

    # Add vertical scrollbar
    scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

# Initialize the main window
window = tk.Tk()
window.title("Injured Management")
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(f"{screen_width}x{screen_height}")

# Load and set the background image
background_image = Image.open("C:\\Users\\dell\\Desktop\\—Pngtree—a doctor in white coat.png")
background_image = background_image.resize((screen_width, screen_height), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

# Create canvas and display the background
canvas = tk.Canvas(window, width=screen_width, height=screen_height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_photo, anchor="nw")

# Draw lines on the canvas
line1 = canvas.create_line(0, 180, screen_width, 180, fill='black', width=1)
line2 = canvas.create_line(0, 270, screen_width, 270, fill='black', width=1)
canvas.tag_raise(line1)
canvas.tag_raise(line2)

# Set up input fields and buttons
full_name_label = tk.Label(canvas, text='Full Name            ', font=('Arial', 10, 'bold'), fg='#800080')
full_name_label.grid(row=0, column=0, sticky='nsew', padx=(130, 27), pady=(20, 0))
full_name = tk.Entry(canvas, width=30, background='#eeffcc')
full_name.insert(0, ' insert the full name')
full_name.bind("<FocusIn>", lambda e: full_name.delete('0', 'end'))
full_name.grid(row=0, column=1, sticky='nsew', padx=(63, 100), pady=(20, 0))

injury_type_label = tk.Label(canvas, text='Injury type           ', font=('Arial', 10, 'bold'), fg='#800080')
injury_type_label.grid(row=1, column=0, sticky='nsew', padx=(130, 27), pady=20)
injury_type = tk.Entry(canvas, width=30, background='#eeffcc')
injury_type.insert(0, ' insert the injury type')
injury_type.bind("<FocusIn>", lambda e: injury_type.delete('0', 'end'))
injury_type.grid(row=1, column=1, sticky='nsew', padx=(63, 100), pady=20)

telephone_number_label = tk.Label(canvas, text='Telephone Number', font=('Arial', 10, 'bold'), fg='#800080')
telephone_number_label.grid(row=2, column=0, sticky='nsew', padx=(130, 27), pady=20)
telephone_number = tk.Entry(canvas, width=30, background='#eeffcc')
telephone_number.insert(0, ' insert the telephone number')
telephone_number.bind("<FocusIn>", lambda e: telephone_number.delete('0', 'end'))
telephone_number.grid(row=2, column=1, sticky='nsew', padx=(63, 100), pady=20)

# Add buttons for different actions
add_button = tk.Button(canvas, text='Add', command=add_injury_info, width=15, background='#3385ff', font=('Arial', 10, 'bold'), border=1)
add_button.grid(row=2, column=2, sticky='nsew', padx=(27, 5), pady=20)

consultation_label = tk.Label(canvas, text='Consultation Fee', font=('Arial', 10, 'bold'), fg='#800080')
consultation_label.grid(row=3, column=0, sticky='nsew', padx=(130, 27), pady=40)
consultation_price = tk.Entry(canvas, width=30, background='#eeffcc')
consultation_price.insert(0, ' insert the consultation fee')
consultation_price.bind("<FocusIn>", lambda e: consultation_price.delete('0', 'end'))
consultation_price.grid(row=3, column=1, sticky='nsew', padx=(63, 100), pady=40)

pay_button = tk.Button(canvas, text='Paid', command=pay_consultation_fee, width=15, background='#00ff00', font=('Arial', 10, 'bold'), border=1)
pay_button.grid(row=3, column=2, sticky='nsew', padx=(27, 5), pady=40)

pass_button = tk.Button(canvas, text='Pass', command=next, width=15, background='#00ffcc', font=('Arial', 10, 'bold'), border=1)
pass_button.grid(row=4, column=2, sticky='nsew', padx=(27, 5), pady=10)

total_fee_button = tk.Button(canvas, text='Total Fee', command=sum_of_fee, width=15, background='#66ccff', font=('Arial', 10, 'bold'), border=1)
total_fee_button.grid(row=5, column=2, sticky='nsew', padx=(27, 5))

show_button = tk.Button(canvas, text='Show Data', command=show_list_injured, width=15, background='#ff33ff', font=('Arial', 10, 'bold'), border=1)
show_button.grid(row=6, column=2, sticky='nsew', padx=(27, 5), pady=10)

# Frame to display the list of injured persons
list_frame = tk.LabelFrame(window, text='The Injured List', background='#80bfff', fg='#800080', highlightbackground='#800080', border=1, width=900, relief="solid", font=('Arial', 11, 'bold'))
list_frame.pack(side='left')

# Set row configuration for the main window
window.rowconfigure(4, weight=1)

# Display the list of injured persons on launch
show_list_injured()

# Start the main application loop
window.mainloop()
