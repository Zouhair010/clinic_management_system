import mysql.connector
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from collections import deque
from datetime import date
from tkinter import messagebox

# Connect to the MySQL database
mydb = mysql.connector.connect(
    host ='localhost',
    user ='root',
    password ='*********',
    database = 'clinic_management'
    )
my_cursor = mydb.cursor()
# Create consultants table if it does not exist
my_cursor.execute("create table if not exists consultants (consultantID int AUTO_INCREMENT, Nom_et_Prenom varchar(255) not null ,CIN varchar(255) not null , Age int not null, Telephone varchar(255) not null, Consultation varchar(255) not null, Adresse varchar(255) not null, Traitement varchar(255) not null, Diagnostic varchar(255) not null, Date_de_Consultation date not null, Tarif int not null, primary key(consultantID))")

list_attente = deque()# Create a deque to manage waiting list of consultants

def ajouter_au_list_attente(): 
    date_cunsultation = date.today()# Get today's date
    # Check if any input fields are incomplete
    if Nom_et_Prenom.get()=="inserer le Nom et Prenom" or CIN.get()=="inserer CIN" or age.get()=="inserer l'age" or telephone_number.get()=="inserer le numbero de telephone" or Consultation.get()=="inserer la consultation" or address.get()=="inserer l'adresse":
        messagebox.showinfo("Attention",f"Les information du consultant que vous souhaitez saisir sont incompletes")
    # Gather consultant information into a list
    consultant_info = [
        ('Nom_et_Prenom',Nom_et_Prenom.get()),('CIN',CIN.get()),('Age',age.get()),('telephone_number',telephone_number.get()),
        ('Consultation',Consultation.get()),('Adresse',address.get()),('date_cunsultation',date_cunsultation)
        ]
    list_attente.append(consultant_info)# Add consultant info to the waiting list
    messagebox.showinfo("Ajouter un consultant",f"Le consultant '{consultant_info[0][1]}' a ete ajoute avec succes")

def passe():
    # Check if there are any consultants in the waiting list
    if len(list_attente) == 0:
        messagebox.showinfo("Next consultant",f"Aucun consultant en list d'attente")
        return
    list_attente.popleft()  # Remove the first consultant from the waiting list
    # Notify about the next consultant if any
    if len(list_attente) == 0:
        messagebox.showinfo("Next consultant",f"Aucun consultant en list d'attente")
    else:
        next_consultant = list_attente[0][0][1]# Get the name of the next consultant
        messagebox.showinfo("Next consultant",f"Le next consultant est: '{next_consultant}'")

def enregistrer_info_consultation():
    # Check if there are any consultants in the waiting list
    if len(list_attente) == 0:
        messagebox.showinfo("Next consultant",f"Aucun consultant en list d'attente")
        return
    consultant = list_attente.popleft()# Get the next consultant from the list
    tarif = int(Tarif.get())# Get consultation fee from the input
    Traitment = traitment.get()# Get treatment info from the input
    Diagnostic = diagnostic.get() # Get diagnostic info from the input
    # Unpack consultant information
    nom_et_Prenom,cIN,Age,Telephone_number,consultation,Adresse,Date_cunsultation= consultant
    # SQL query to insert consultant's consultation details into the database
    sql = 'insert into consultants (Nom_et_Prenom, CIN, Age, Telephone, Consultation, Adresse, Traitement, Diagnostic, Date_de_Consultation, Tarif) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    val = (nom_et_Prenom[1],cIN[1],Age[1],Telephone_number[1],consultation[1],Adresse[1],Traitment,Diagnostic,Date_cunsultation[1],tarif)
    my_cursor.execute(sql,val) # Execute the SQL query
    mydb.commit() # Commit the transaction to the database
    # Notify about the next consultant
    if len(list_attente) == 0:
        messagebox.showinfo("Next consultant",f"Aucun consultant en list d'attente")
    else:
        next_consultant = list_attente[0][0][1]
        messagebox.showinfo("Next consultant",f"Le next consultant est: '{next_consultant}'")

def total_tarif():
    # SQL query to calculate the total fee for today's consultations
    sql ='select sum(Tarif) from consultants where Date_de_Consultation = CURRENT_DATE()'
    my_cursor.execute(sql)
    myresult = my_cursor.fetchall()# Fetch the result of the query
    messagebox.showinfo("Total des produits",f"Total des produits pour aujourd'hui: {int(myresult[0][0])} DH")

def list_des_consultants():
    # SQL query to fetch all consultants' information
    sql ='select Nom_et_Prenom,CIN,Age,Telephone,Adresse,Consultation,Date_de_Consultation from consultants'
    my_cursor.execute(sql)
    myresult = my_cursor.fetchall()# Fetch all results from the query
    columns = ("#1", "#2", "#3", "#4", "#5", "#6") #number of columns in the table # Define columns for the Treeview
    tree = ttk.Treeview(list_frame, columns=columns,height=11, show="headings") #treeview that shows a table   # Create a Treeview widget for displaying data
    fieldnames = ['Nom et Prenom' ,'CIN' ,'Age' ,'telephone' ,'Adresse' ,'Consultation' ,'Date de Consultation'] #column names
    for i in range(1, 7): # Loop through the number of columns
        tree.heading(f"#{i}", text=f"{fieldnames[i-1]}",anchor='w')# Set the heading for each column
        tree.column(f"#{i}", width=224) # Set width for each column

    tree['style'] = 'Treeview'  # Set style for Treeview
    style = ttk.Style() #add style(colors ,font ...) to the table
    # Configure Treeview style attributes
    style.configure('Treeview', rowheight=29, background='#80bfff', foreground='black',font=('Arial',10,'bold')) 
    style.map('Treeview', background=[('selected', '#ff33ff')],foreground=[('selected', 'black')])# Map selected row styles
    for data in myresult: #include employees info to the table to shows them # Loop through the results to insert them into the Treeview
        tree.insert("", "end", values=(data[0],data[1],data[2],data[3],data[4],data[5],data[6]))

    scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview) #scrollbar to scroll up or down(vertically) the table that includes info
    tree.configure(yscroll=scrollbar.set) # Configure Treeview to use scrollbar
    tree.grid(row=0, column=0, sticky="nsew") # Position the Treeview in the grid
    scrollbar.grid(row=0, column=1, sticky="ns")# Position the scrollbar in the grid

def chercher_consultant():
    # SQL query to fetch a specific consultant's information based on CIN
    sql = 'select Nom_et_Prenom,Consultation,Date_de_Consultation,Traitement,Diagnostic from consultants where CIN=%s'
    val = (search.get(),) # Get the CIN value from the search entry
    my_cursor.execute(sql,val)# Execute the query
    myresult = my_cursor.fetchall() # Fetch results
    # Check if any result is found
    if myresult == []:
        messagebox.showinfo("Notification",f"Il n'ya aucun consultant dans la base des donnees avec ce CIN: {search.get()}")
        return
    popup2 = tk.Toplevel() # Create a new popup window
    popup2.geometry('605x100+440+300')# Set size and position of the popup window
    popup2.title('')# Title of the popup window
    notification = tk.LabelFrame(popup2 ,text='les information du Consultant',background='#80bfff',fg='#800080',highlightbackground='#800080',border=1,relief="solid",font=('Arial',10,'bold')) # Create a label frame for displaying info
    # Treeview for displaying consultant's information in the popup
    columns = ("#1", "#2", "#3", "#4", "#5") #number of columns in the table
    tree = ttk.Treeview(notification, columns=columns,height=2, show="headings") #treeview that shows a table 
    fieldnames = ['Nom et Prenom' ,'Consultation' ,'Date de Consultation' ,'Traitement' ,'Diagnostic'] #column names
    for i in range(1, 6): #numbers of columns
        tree.heading(f"#{i}", text=f"{fieldnames[i-1]}",anchor='w')# Set heading for each column
        tree.column(f"#{i}", width=120) #width of a column

    tree['style'] = 'Treeview'
    style = ttk.Style() #add style(colors ,font ...) to the table
    style.configure('Treeview', rowheight=29, background='#80bfff', foreground='black',font=('Arial',10,'bold')) 
    style.map('Treeview', background=[('selected', '#ff33ff')],foreground=[('selected', 'black')])
    for data in myresult: #include employees info to the table to shows them
        tree.insert("", "end", values=(data[0],data[1],data[2],data[3],data[4]))

    scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview) #scrollbar to scroll up or down(vertically) the table that includes info
    tree.configure(yscroll=scrollbar.set)
    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")
    notification.pack()
    # popup2.after(5000, popup2.destroy)

# Set up main window
window = tk.Tk()
window.title("Clinic Management System") # Title for the application
screen_width =window.winfo_screenwidth() # Get screen width
screen_height = window.winfo_screenheight()# Get screen height
window.geometry(f"{screen_width}x{screen_height}")# Set window size to full screen
# window.resizable(False, False) to disable window resizing

# Load and display background image
background_image = Image.open("C:\\Users\\dell\\Desktop\\—Pngtree—a doctor in white coat.png")  #image path
background_image = background_image.resize((screen_width, screen_height), Image.LANCZOS) # size of the image
background_photo = ImageTk.PhotoImage(background_image)# Convert image for Tkinter

# Create canvas to hold background and widgets
canvas = tk.Canvas(window, width=window.winfo_screenwidth(), height=window.winfo_screenheight())
canvas.pack(fill="both", expand=True)# Fill and expand to entire window
canvas.create_image(0, 0, image=background_photo, anchor="nw")# Set background image

# Draw horizontal dividing lines on canvas
line1 = canvas.create_line(0,160,screen_width,160,fill='black',width=2)
line2 = canvas.create_line(0,246,screen_width,246,fill='black',width=2)
line3 = canvas.create_line(0,315,screen_width,315,fill='black',width=2)
canvas.tag_raise(line1)
canvas.tag_raise(line2)
canvas.tag_raise(line3)

# Create entry fields with placeholder text and focus-in events to clear text
# Name field
Nom_et_Prenom = tk.Entry(canvas, width=30)
Nom_et_Prenom.insert(0, 'inserer le Nom et Prenom')
Nom_et_Prenom.bind("<FocusIn>", lambda e: Nom_et_Prenom.delete('0', 'end'))
Nom_et_Prenom.grid(row=0, column=0, sticky='nsew', padx=(120, 100), pady=(20, 0))
# Consultation field
Consultation = tk.Entry(canvas, width=30)
Consultation.insert(0, 'inserer la consultation')
Consultation.bind("<FocusIn>", lambda e: Consultation.delete('0', 'end'))
Consultation.grid(row=1, column=0, sticky='nsew', padx=(120, 100), pady=20)
# Telephone number field
telephone_number = tk.Entry(canvas, width=30)
telephone_number.insert(0, 'inserer le numbero de telephone')
telephone_number.bind("<FocusIn>", lambda e: telephone_number.delete('0', 'end'))
telephone_number.grid(row=2, column=0, sticky='nsew', padx=(120, 100), pady=(0,20))
# CIN field
CIN = tk.Entry(canvas, width=30)
CIN.insert(0, 'inserer CIN')
CIN.bind("<FocusIn>", lambda e: CIN.delete('0', 'end'))
CIN.grid(row=0, column=1, sticky='nsew', padx=(63, 100), pady=(20, 0))
# Address field
address = tk.Entry(canvas, width=30)
address.insert(0, "inserer l'adresse")
address.bind("<FocusIn>", lambda e: address.delete('0', 'end'))
address.grid(row=1, column=1, sticky='nsew', padx=(63, 100), pady=20)
# Age field
age = tk.Entry(canvas, width=30)
age.insert(0, "inserer l'age")
age.bind("<FocusIn>", lambda e: age.delete('0', 'end'))
age.grid(row=2, column=1, sticky='nsew', padx=(63, 100), pady=(0,20))
# Button to pass on consultation
pass_button = tk.Button(canvas,text='Pass',command=passe,width=15,background='#ff1a1a',font=('Arial',10,'bold'),border=1)
pass_button.grid(row=1,column=3,sticky='nsew', padx=(27,5), pady=(20))
# Button to add patient to waiting list
add_button = tk.Button(canvas, text='Ajouter', command=ajouter_au_list_attente, width=15, background='#3385ff', font=('Arial', 10, 'bold'), border=1)
add_button.grid(row=2, column=3, sticky='nsew', padx=(27,5), pady=(0,20))
# Field for consultation fee
Tarif = tk.Entry(canvas,width=30)
Tarif.insert(0,'inserer tarif du consultation') 
Tarif.bind("<FocusIn>",lambda e:Tarif.delete('0','end'))
Tarif.grid(row=3,column=2,sticky='nsew', padx=(63, 100), pady=(40,0))
# Diagnostic field
diagnostic = tk.Entry(canvas,width=30)
diagnostic.insert(0,'inserer diagnostic')
diagnostic.bind("<FocusIn>",lambda e:diagnostic.delete('0','end'))
diagnostic.grid(row=3,column=0,sticky='nsew', padx=(120, 100), pady=(40,0))
# Treatment duration field
traitment = tk.Entry(canvas,width=30)
traitment.insert(0,'inserer periode du traitment') 
traitment.bind("<FocusIn>",lambda e:traitment.delete('0','end'))
traitment.grid(row=3,column=1,sticky='nsew', padx=(63, 100), pady=(40,0))
# Button to save consultation information
enregistrer_button = tk.Button(canvas,text='Enregistrer',command=enregistrer_info_consultation,width=15,background='#00ff00',font=('Arial',10,'bold'),border=1)
enregistrer_button.grid(row=3,column=3,sticky='nsew', padx=(27,5), pady=(40,0))
# Search field for consultant by CIN
search = tk.Entry(canvas,width=30)
search.insert(0,'enter le CIN du consultant') 
search.bind("<FocusIn>",lambda e:search.delete('0','end'))
search.grid(row=5,column=2,sticky='nsew', padx=(63, 100), pady=(50,0))
# Search button
search_button = tk.Button(canvas,text='Recherche',command=chercher_consultant ,width=15,background='#00ffcc',font=('Arial',10,'bold'),border=1)
search_button.grid(row=5,column=3,sticky='nsew', padx=(27,5), pady=(50,0))
# Button to display total consultation fees
total_fee_button = tk.Button(canvas,text='Total du tarif',command=total_tarif,width=15,background='#66ccff',font=('Arial',10,'bold'),border=1)
total_fee_button.grid(row=6,column=3,sticky='nsew', padx=(27,5), pady=(40,0))
# Button to refresh the list of consultants
actualiser = tk.Button(canvas,text='Actualiser',command=list_des_consultants,width=15,background='#ff33ff',font=('Arial',10,'bold'),border=1)
actualiser.grid(row=7,column=3,sticky='nsew', padx=(27,5), pady=20)
# Create a frame to display list of consultants
list_frame = tk.LabelFrame(window, text='List des consultants',background='#80bfff',fg='#800080',highlightbackground='#800080',border=1,width=900,relief="solid",font=('Arial',11,'bold'))
list_frame.pack(side=('left'))
# Configure row layout
window.rowconfigure(4,weight=1)
# Function call to display the list of consultants
list_des_consultants()
# Run the main event loop
window.mainloop()