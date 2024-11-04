# Import necessary libraries
import mysql.connector# For database connection
import tkinter as tk# For GUI creation
import tkinter.ttk as ttk# For advanced widgets in tkinter
from PIL import Image, ImageTk# For image handling within tkinter
from collections import deque # For using a queue
from datetime import date# To get the current date
from tkinter import messagebox# For displaying message boxes

# Establish connection to MySQL database
mydb = mysql.connector.connect(
    host ='localhost',
    user ='root',
    password ='********',
    database = 'clinic_management'
    )
my_cursor = mydb.cursor()
# Create consultants table if it doesn't exist
my_cursor.execute("create table if not exists consultants (consultantID int AUTO_INCREMENT, Nom_et_Prenom varchar(255) not null ,CIN varchar(255) not null , Age int not null, Telephone varchar(255) not null, Consultation varchar(255) not null, Adresse varchar(255) not null, Traitement varchar(255) not null, Diagnostic varchar(255) not null, Date_de_Consultation date not null, Tarif int not null, primary key(consultantID))")

#a queue to order the consultants# Initialize queue for consultants waiting for consultation
list_attente = deque()

# Function to add a consultant to the queue
def ajouter_au_list_attente(): 
    date_cunsultation = date.today()  # Capture current date as consultation date
    # Define fields and default texts for user input validationf
    entries = [
        (Nom_et_Prenom,'inserer le Nom et Prenom'),(CIN,'inserer CIN'),
        (age,"inserer l'age"),(telephone_number,'inserer le numbero de telephone'),
        (Consultation,'inserer la consultation'),(address,"inserer l'adresse")
        ] #all entries that include the consultant info
    # Check if any field is empty or contains default text
    if any(item[0].get() == item[1] or item[0].get() == '' for item in entries): #check if any entry include the default text or nothing instead of the consultant info 
        messagebox.showinfo("Attention",f"Les information du consultant que vous souhaitez saisir sont incompletes") #a message that tells to user that  he has provided incomplete info of the cunsultant
        #delete the text on the Nom_et_Prenom entry and insert the default text on it:
        Nom_et_Prenom.delete('0', 'end')
        Nom_et_Prenom.config(fg='gray') #change the color of the default text to gray
        Nom_et_Prenom.insert(0,'inserer le Nom et Prenom')
        Nom_et_Prenom.bind("<FocusIn>", lambda e:on_click('inserer le Nom et Prenom',Nom_et_Prenom)) #if the user click on the entry the default text gonna delete and the colore of text on it will change to black
        #delete the text on the Consultation entry and insert the default text on it:
        Consultation.delete('0', 'end')
        Consultation.config(fg='gray')
        Consultation.insert(0,'inserer la consultation')
        Consultation.bind("<FocusIn>", lambda e:on_click('inserer la consultation',Consultation))
        #delete the text on the telephone_number entry and insert the default text on it:
        telephone_number.delete('0', 'end')
        telephone_number.config(fg='gray')
        telephone_number.insert(0,'inserer le numbero de telephone') 
        telephone_number.bind("<FocusIn>", lambda e:on_click('inserer le numbero de telephone',telephone_number))
        #delete the text on the CIN entry and insert the default text on it:
        CIN.delete('0', 'end')
        CIN.config(fg='gray')
        CIN.insert(0,'inserer CIN') 
        CIN.bind("<FocusIn>", lambda e:on_click('inserer CIN',CIN))
        #delete the text on the address entry and insert the default text on it:
        address.delete('0', 'end')
        address.config(fg='gray')
        address.insert(0,"inserer l'adresse") 
        address.bind("<FocusIn>", lambda e:on_click("inserer l'adresse",address))
        #delete the text on the age entry and insert the default text on it:
        age.delete('0', 'end')
        age.config(fg='gray')
        age.insert(0,"inserer l'age") 
        age.bind("<FocusIn>", lambda e:on_click("inserer l'age",age))
        return
    consultant_info = [
        ('Nom_et_Prenom',Nom_et_Prenom.get()),('CIN',CIN.get()),('Age',age.get()),('telephone_number',telephone_number.get()),
        ('Consultation',Consultation.get()),('Adresse',address.get()),('date_cunsultation',date_cunsultation)
        ] #all entries that include the consultant info
    list_attente.append(consultant_info) #append the consultant info to the queue
    messagebox.showinfo("Ajouter un consultant",f"Le consultant '{consultant_info[0][1]}' a ete ajoute avec succes") # a message that shows that the consultant has been added to the queue
    #delete the text on the Nom_et_Prenom entry and insert the default text on it:
    Nom_et_Prenom.delete('0', 'end')
    Nom_et_Prenom.config(fg='gray')
    Nom_et_Prenom.insert(0,'inserer le Nom et Prenom')
    Nom_et_Prenom.bind("<FocusIn>", lambda e:on_click('inserer le Nom et Prenom',Nom_et_Prenom))
    #delete the text on the Consultation entry and insert the default text on it:
    Consultation.delete('0', 'end')
    Consultation.config(fg='gray')
    Consultation.insert(0,'inserer la consultation')
    Consultation.bind("<FocusIn>", lambda e:on_click('inserer la consultation',Consultation))
    #delete the text on the telephone_number entry and insert the default text on it:
    telephone_number.delete('0', 'end')
    telephone_number.config(fg='gray')
    telephone_number.insert(0,'inserer le numbero de telephone') 
    telephone_number.bind("<FocusIn>", lambda e:on_click('inserer le numbero de telephone',telephone_number))
    #delete the text on the CIN entry and insert the default text on it:
    CIN.delete('0', 'end')
    CIN.config(fg='gray')
    CIN.insert(0,'inserer CIN') 
    CIN.bind("<FocusIn>", lambda e:on_click('inserer CIN',CIN))
    #delete the text on the address entry and insert the default text on it:
    address.delete('0', 'end')
    address.config(fg='gray')
    address.insert(0,"inserer l'adresse") 
    address.bind("<FocusIn>", lambda e:on_click("inserer l'adresse",address))
    #delete the text on the age entry and insert the default text on it:
    age.delete('0', 'end')
    age.config(fg='gray')
    age.insert(0,"inserer l'age") 
    age.bind("<FocusIn>", lambda e:on_click("inserer l'age",age))

# Function to handle a consultant skipping their consultation
def passe(): # if a consultant exit the queue without visiting the doctor
    if len(list_attente) == 0: # if the queue is empty
        messagebox.showinfo("Next consultant",f"Aucun consultant en list d'attente") # message that tells the user there is no cunsultant on the queue
        return
    list_attente.popleft() # the consultant leave the queue without visiting the doctor
    if len(list_attente) == 0:# if the queue is empty
        messagebox.showinfo("Next consultant",f"Aucun consultant en list d'attente")# message that tells the user there is no cunsultant on the queue
    else: # there are cunsultants on the queue
        next_consultant = list_attente[0][0][1] # the name the next consultant 
        messagebox.showinfo("Next consultant",f"Le next consultant est: '{next_consultant}'") # message that tells the user the name of the next cunsultant

# Function to save consultation information to the database
def enregistrer_info_consultation():
    entries = [
        (Tarif,"inserer tarif du consultation"),
        (traitment,"inserer periode du traitment"),
        (diagnostic,"inserer diagnostic")] #the consultant health status info after visiting the doctor
    if any(entry[0].get() == entry[1] or entry[0].get() == '' for entry in entries):#check if any entry include the default text or nothing instead of the consultant health status info 
        messagebox.showinfo("Attention",f"Les information du consultant que vous souhaitez saisir sont incompletes")#a message that tells to the user that he has provided incomplete health status info of the cunsultant
        #delete the text on the Tarif entry and insert the default text on it:
        Tarif.delete('0', 'end')
        Tarif.config(fg='gray')#change the color of the default text to gray
        Tarif.insert(0,'inserer tarif du consultation') 
        Tarif.bind("<FocusIn>", lambda e:on_click('inserer tarif du consultation',Tarif))#if the user click on the entry the default text gonna delete and the colore of text on it will change to black
        #delete the text on the diagnostic entry and insert the default text on it:
        diagnostic.delete('0', 'end')
        diagnostic.config(fg='gray')
        diagnostic.insert(0,'inserer diagnostic')
        diagnostic.bind("<FocusIn>", lambda e:on_click('inserer diagnostic',diagnostic))
        #delete the text on the traitment entry and insert the default text on it:
        traitment.delete('0', 'end')
        traitment.config(fg='gray')
        traitment.insert(0,'inserer periode du traitment') 
        traitment.bind("<FocusIn>", lambda e:on_click('inserer periode du traitment',traitment))
        return
    if len(list_attente) == 0:# if the queue is empty
        messagebox.showinfo("Next consultant",f"Aucun consultant en list d'attente")# message that tells the user there is no cunsultant on the queue
        #delete the text on the Tarif entry and insert the default text on it:
        Tarif.delete('0', 'end')
        Tarif.config(fg='gray')
        Tarif.insert(0,'inserer tarif du consultation') 
        Tarif.bind("<FocusIn>", lambda e:on_click('inserer tarif du consultation',Tarif))
        #delete the text on the diagnostic entry and insert the default text on it:
        diagnostic.delete('0', 'end')
        diagnostic.config(fg='gray')
        diagnostic.insert(0,'inserer diagnostic')
        diagnostic.bind("<FocusIn>", lambda e:on_click('inserer diagnostic',diagnostic))
        #delete the text on the traitment entry and insert the default text on it:
        traitment.delete('0', 'end')
        traitment.config(fg='gray')
        traitment.insert(0,'inserer periode du traitment') 
        traitment.bind("<FocusIn>", lambda e:on_click('inserer periode du traitment',traitment))
        return
    consultant = list_attente.popleft() #the consultant that leave the queue to visit the doctor
    # Prepare data for database insertion
    #get the consultant health status info after leaving the doctor:
    tarif = int(Tarif.get())
    Traitment = traitment.get()
    Diagnostic = diagnostic.get()
    #get the identity info and the postal address of the consultant:
    nom_et_Prenom,cIN,Age,Telephone_number,consultation,Adresse,Date_cunsultation= consultant
    # insert the the identity info and the postal address and the health status info of the consultant in the database
    sql = 'insert into consultants (Nom_et_Prenom, CIN, Age, Telephone, Consultation, Adresse, Traitement, Diagnostic, Date_de_Consultation, Tarif) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    val = (nom_et_Prenom[1],cIN[1],Age[1],Telephone_number[1],consultation[1],Adresse[1],Traitment,Diagnostic,Date_cunsultation[1],tarif)
    my_cursor.execute(sql,val)
    mydb.commit()
    #delete the text on the Tarif entry and insert the default text on it:
    Tarif.delete('0', 'end')
    Tarif.config(fg='gray')
    Tarif.insert(0,'inserer tarif du consultation')     
    Tarif.bind("<FocusIn>", lambda e:on_click('inserer tarif du consultation',Tarif))
    #delete the text on the diagnostic entry and insert the default text on it:
    diagnostic.delete('0', 'end')
    diagnostic.config(fg='gray')
    diagnostic.insert(0,'inserer diagnostic')
    diagnostic.bind("<FocusIn>", lambda e:on_click('inserer diagnostic',diagnostic))
    #delete the text on the traitment entry and insert the default text on it:
    traitment.delete('0', 'end')
    traitment.config(fg='gray')
    traitment.insert(0,'inserer periode du traitment') 
    traitment.bind("<FocusIn>", lambda e:on_click('inserer periode du traitment',traitment))
    if len(list_attente) == 0:# if the queue is empty
        messagebox.showinfo("Next consultant",f"Aucun consultant en list d'attente")# message that tells the user there is no cunsultant on the queue
    else:# there are cunsultants on the queue
        next_consultant = list_attente[0][0][1]# the name the next consultant 
        messagebox.showinfo("Next consultant",f"Le next consultant est: '{next_consultant}'")# message that tells the user the name of the next cunsultant

def total_tarif():
    #total the fee of today
    sql ='select sum(Tarif) from consultants where Date_de_Consultation = CURRENT_DATE()'
    my_cursor.execute(sql)
    myresult = my_cursor.fetchall()
    if myresult[0][0] is None:#if there is no fee today
        messagebox.showinfo("Total des produits",f"Il n'y a aucune produit pour aujourd'hui")# message that tells to user there is no fee today
        return
    messagebox.showinfo("Total des produits",f"Total des produits pour aujourd'hui: {int(myresult[0][0])} DH")# message that tells to user the sum of fees today

def list_des_consultants():#show the consultants and some info of them in a table
    sql ='select Nom_et_Prenom,CIN,Age,Telephone,Adresse,Consultation,Date_de_Consultation from consultants'
    my_cursor.execute(sql)
    myresult = my_cursor.fetchall() #the consultants info from the database
    columns = ("#1", "#2", "#3", "#4", "#5", "#6") #number of columns in the table
    tree = ttk.Treeview(list_frame, columns=columns,height=11, show="headings") #treeview that shows a table 
    fieldnames = ['Nom et Prenom' ,'CIN' ,'Age' ,'telephone' ,'Adresse' ,'Consultation' ,'Date de Consultation'] #column names
    for i in range(1, 7): #numbers of columns
        tree.heading(f"#{i}", text=f"{fieldnames[i-1]}",anchor='w')
        tree.column(f"#{i}", width=224) #width of a column

    tree['style'] = 'Treeview'
    style = ttk.Style() #add style(colors ,font ...) to the table
    style.configure('Treeview', rowheight=29, background='#80bfff', foreground='black',font=('Arial',10,'bold')) 
    style.map('Treeview', background=[('selected', '#ff33ff')],foreground=[('selected', 'black')])
    for data in myresult: #include consultants info to the table to shows them
        tree.insert("", "end", values=(data[0],data[1],data[2],data[3],data[4],data[5],data[6]))

    scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview) #scrollbar to scroll up or down(vertically) the table that includes info
    tree.configure(yscroll=scrollbar.set)
    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

# Helper function to handle entry focus
def on_click(event,tool):#function that take the dafault text(event) and the entry(tool) as arguments:
    text = tool.get() #get the text in the entry 
    if text.startswith(event): #if the entry include the default text delete it and change the frontground color to black
        tool.delete(0, len(event))
        tool.config(fg="black")

def chercher_consultant():
    if search.get()=="enter le CIN du consultant" or search.get()=='':# if the entry include the default text or it's empty
        messagebox.showinfo("Attention",f"Vous devez saisir le CIN du consultant")#message that tells the user that he must enter the correct cin of consultant
        #delete the text on the search entry and 
        search.delete('0','end')
        search.config(fg='gray')
        search.insert(0,'enter le CIN du consultant') #insert the default text on the search entry with gray color
        search.bind("<FocusIn>", lambda e:on_click("enter le CIN du consultant",search))#if the user click on the entry the default text gonna delete and the next text will be in black color
        return
    # select the consultant info with the specific cin(ID) from the database
    sql = 'select Nom_et_Prenom,Consultation,Date_de_Consultation,Traitement,Diagnostic from consultants where CIN=%s'
    val = (search.get(),)
    my_cursor.execute(sql,val)
    myresult = my_cursor.fetchall()
    #delete the text on the search entry and 
    search.delete('0','end')
    search.config(fg='gray')
    search.insert(0,'enter le CIN du consultant') 
    search.bind("<FocusIn>", lambda e:on_click("enter le CIN du consultant",search)) #insert the default text on the search entry with gray color
    if myresult == []: #if there is no consultant with the specific cin(ID) 
        messagebox.showinfo("Notification",f"Il n'ya aucun consultant dans la base des donnees avec ce CIN: {search.get()}") #message that tells the user there is no consultant with this cin
        return
    popup2 = tk.Toplevel() #small subframe 
    popup2.geometry('605x100+440+300')
    popup2.title('')
    notification = tk.LabelFrame(popup2 ,text='les information du Consultant',background='#80bfff',fg='#800080',highlightbackground='#800080',border=1,relief="solid",font=('Arial',10,'bold'))
    columns = ("#1", "#2", "#3", "#4", "#5") #number of columns in the table
    tree = ttk.Treeview(notification, columns=columns,height=2, show="headings") #treeview that shows a table 
    fieldnames = ['Nom et Prenom' ,'Consultation' ,'Date de Consultation' ,'Traitement' ,'Diagnostic'] #column names
    for i in range(1, 6): #numbers of columns
        tree.heading(f"#{i}", text=f"{fieldnames[i-1]}",anchor='w')
        tree.column(f"#{i}", width=120) #width of a column

    tree['style'] = 'Treeview'
    style = ttk.Style() #add style(colors ,font ...) to the table
    style.configure('Treeview', rowheight=29, background='#80bfff', foreground='black',font=('Arial',10,'bold')) 
    style.map('Treeview', background=[('selected', '#ff33ff')],foreground=[('selected', 'black')])
    for data in myresult: #include consultants info to the table to shows them
        tree.insert("", "end", values=(data[0],data[1],data[2],data[3],data[4]))

    scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview) #scrollbar to scroll up or down(vertically) the table that includes info
    tree.configure(yscroll=scrollbar.set)
    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")
    notification.pack()
    # popup2.after(5000, popup2.destroy) #after 5 second the subframe will disappear

# Initialize the main application window using tkinter
window = tk.Tk()
window.title("Clinic Management System")
screen_width =window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(f"{screen_width}x{screen_height}")

# Change the default icon of the application window
window.iconbitmap("C:\\Users\\dell\\Desktop\\medical-15_icon-icons.com_73938.ico") #to change the default icon
# window.resizable(False, False)

# Get the screen dimensions for full-screen display
background_image = Image.open("C:\\Users\\dell\\Desktop\\—Pngtree—a doctor in white coat_156802721.png") 
background_image = background_image.resize((screen_width, screen_height), Image.LANCZOS)   # Resize to fit screen
background_photo = ImageTk.PhotoImage(background_image) # Create a PhotoImage object for tkinter

# Create a canvas to hold the background image and widgets
canvas = tk.Canvas(window, width=window.winfo_screenwidth(), height=window.winfo_screenheight())
canvas.pack(fill="both", expand=True) # Expand the canvas to fill the window
canvas.create_image(0, 0, image=background_photo, anchor="nw")# Place the background image on the canvas

# Draw horizontal lines on the canvas for layout separation
line1 = canvas.create_line(0,160,screen_width,160,fill='black',width=2)# Line for visual separation
line2 = canvas.create_line(0,246,screen_width,246,fill='black',width=2)# Another separation line
line3 = canvas.create_line(0,315,screen_width,315,fill='black',width=2)# Third separation line

# Bring the lines to the front of the canvas
canvas.tag_raise(line1)
canvas.tag_raise(line2)
canvas.tag_raise(line3)

# Create entry field for the consultant's name and surname
Nom_et_Prenom = tk.Entry(canvas, width=30,fg='gray')# Entry for name
Nom_et_Prenom.insert(0,'inserer le Nom et Prenom')# Placeholder text
Nom_et_Prenom.bind("<FocusIn>", lambda e:on_click('inserer le Nom et Prenom',Nom_et_Prenom)) # Clear placeholder on focus
Nom_et_Prenom.grid(row=0, column=0, sticky='nsew', padx=(120, 100), pady=(20, 0)) # Position in grid
# Create entry field for consultation type
Consultation = tk.Entry(canvas, width=30,fg='gray')
Consultation.insert(0,'inserer la consultation')
Consultation.bind("<FocusIn>", lambda e:on_click('inserer la consultation',Consultation)) # Clear placeholder on focus
Consultation.grid(row=1, column=0, sticky='nsew', padx=(120, 100), pady=20)
# Create entry field for telephone number
telephone_number = tk.Entry(canvas, width=30,fg='gray')
telephone_number.insert(0,'inserer le numbero de telephone') 
telephone_number.bind("<FocusIn>", lambda e:on_click('inserer le numbero de telephone',telephone_number)) # Clear placeholder on focus
telephone_number.grid(row=2, column=0, sticky='nsew', padx=(120, 100), pady=(0,20))
# Create entry field for CIN (National ID number)
CIN = tk.Entry(canvas, width=30,fg='gray')
CIN.insert(0,'inserer CIN') 
CIN.bind("<FocusIn>", lambda e:on_click('inserer CIN',CIN)) # Clear placeholder on focus
CIN.grid(row=0, column=1, sticky='nsew', padx=(63, 100), pady=(20, 0))
# Create entry field for address
address = tk.Entry(canvas, width=30,fg='gray')
address.insert(0,"inserer l'adresse") 
address.bind("<FocusIn>", lambda e:on_click("inserer l'adresse",address)) # Clear placeholder on focus
address.grid(row=1, column=1, sticky='nsew', padx=(63, 100), pady=20)
# Create entry field for age
age = tk.Entry(canvas, width=30,fg='gray')
age.insert(0,"inserer l'age") 
age.bind("<FocusIn>", lambda e:on_click("inserer l'age",age)) # Clear placeholder on focus
age.grid(row=2, column=1, sticky='nsew', padx=(63, 100), pady=(0,20))
# Create button to pass the current consultant in the queue
pass_button = tk.Button(canvas,text='Pass',command=passe,width=15,background='#ff1a1a',font=('Arial',10,'bold'),border=1)
pass_button.grid(row=1,column=3,sticky='nsew', padx=(27,5), pady=(20))
# Create button to add the consultant to the waiting list
add_button = tk.Button(canvas, text='Ajouter', command=ajouter_au_list_attente, width=15, background='#3385ff', font=('Arial', 10, 'bold'), border=1)
add_button.grid(row=2, column=3, sticky='nsew', padx=(27,5), pady=(0,20))
# Create entry field for consultation fee
Tarif = tk.Entry(canvas,width=30,fg='gray')
Tarif.insert(0,'inserer tarif du consultation') 
Tarif.bind("<FocusIn>", lambda e:on_click('inserer tarif du consultation',Tarif)) # Clear placeholder on focus
Tarif.grid(row=3,column=2,sticky='nsew', padx=(63, 100), pady=(40,0))
# Create entry field for diagnostic information
diagnostic = tk.Entry(canvas,width=30,fg='gray')
diagnostic.insert(0,'inserer diagnostic') 
diagnostic.bind("<FocusIn>", lambda e:on_click('inserer diagnostic',diagnostic)) # Clear placeholder on focus
diagnostic.grid(row=3,column=0,sticky='nsew', padx=(120, 100), pady=(40,0))
# Create entry field for treatment duration
traitment = tk.Entry(canvas,width=30,fg='gray')
traitment.insert(0,'inserer periode du traitment') 
traitment.bind("<FocusIn>", lambda e:on_click('inserer periode du traitment',traitment)) # Clear placeholder on focus
traitment.grid(row=3,column=1,sticky='nsew', padx=(63, 100), pady=(40,0))
# Create button to save consultation information to the database
enregistrer_button = tk.Button(canvas,text='Enregistrer',command=enregistrer_info_consultation,width=15,background='#00ff00',font=('Arial',10,'bold'),border=1)
enregistrer_button.grid(row=3,column=3,sticky='nsew', padx=(27,5), pady=(40,0))
# Create entry field for searching consultants by CIN
search = tk.Entry(canvas,width=30,fg='gray')
search.insert(0,'enter le CIN du consultant') 
search.bind("<FocusIn>", lambda e:on_click("enter le CIN du consultant",search)) # Clear placeholder on focus
search.grid(row=5,column=2,sticky='nsew', padx=(63, 100), pady=(50,0))
# Create button to search for a consultant in the database
search_button = tk.Button(canvas,text='Recherche',command=chercher_consultant ,width=15,background='#00ffcc',font=('Arial',10,'bold'),border=1)
search_button.grid(row=5,column=3,sticky='nsew', padx=(27,5), pady=(50,0))
# Create button to calculate and display total fees
total_fee_button = tk.Button(canvas,text='Total du tarif',command=total_tarif,width=15,background='#66ccff',font=('Arial',10,'bold'),border=1)
total_fee_button.grid(row=6,column=3,sticky='nsew', padx=(27,5), pady=(40,0))
# Create button to refresh the list of consultants
actualiser = tk.Button(canvas,text='Actualiser',command=list_des_consultants,width=15,background='#ff33ff',font=('Arial',10,'bold'),border=1)
actualiser.grid(row=7,column=3,sticky='nsew', padx=(27,5), pady=20)
# Create a labeled frame to display the list of consultants
list_frame = tk.LabelFrame(window, text='List des consultants',background='#80bfff',fg='#800080',highlightbackground='#800080',border=1,width=900,relief="solid",font=('Arial',11,'bold'))
list_frame.pack(side=('left'))

window.rowconfigure(4,weight=1)# Configure row weight for resizing

# Call function to list consultants on startup
list_des_consultants()
# Start the tkinter main event loop
window.mainloop()