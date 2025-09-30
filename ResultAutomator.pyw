import customtkinter as ctk
from pathlib import Path

directory_path = Path("Dependencies")

if not(directory_path.is_dir()):
    directory_path.mkdir(parents=True, exist_ok=True)
    for f in ['file.txt','scan.txt','student_names.txt']:
        with open("Dependencies/"+f,'w') as file:
            file.write('')

from Dependencies import app
from Dependencies import constants

import threading

# Set appearance and theme (optional)
ctk.set_appearance_mode("Dark")  # Options: "Dark", "Light", "System"
ctk.set_default_color_theme("dark-blue")  # Options: "blue", "green", "dark-blue"


# Session Class
class Session(ctk.CTk):
    def __init__(self,Range=["abcd","1234"],gng=""):
        super().__init__()

        self.title("RGPV Result Automator")
        self.geometry("750x430")
        self.resizable(False, False)

        #self.logs_text="These are the logs \n"

        ctk.CTkLabel(self, text="Scanning RGPV results",font=("Arial", 24, "bold")).place(x=20, y=20)
        ctk.CTkLabel(self, text="From  : "+Range[0],font=("Consolas", 18)).place(x=20, y=60)
        ctk.CTkLabel(self, text="To    : "+Range[1],font=("Consolas", 18)).place(x=20, y=100)

        if gng=='ng':
            ctk.CTkLabel(self, text="Result system : Non-Grading",font=("Consolas", 18)).place(x=20, y=140)
        else:
            ctk.CTkLabel(self, text="Result system : Grading",font=("Consolas", 18)).place(x=20, y=140)

        self.textbox = ctk.CTkTextbox(self, width=470, height=230,font=("Consolas", 12))
        self.textbox.place(x=20,y=190)

        self.student_textbox = ctk.CTkTextbox(self, width=235, height=400,font=("Arial", 12))
        self.student_textbox.place(x=500,y=20)


        self.update_label()



        # Start Button to Close session
        #self.button = ctk.CTkButton(self, text="Close", width=120, command=self.close_app)
        #self.button.place(x=500, y=350)

    def update_label(self):
        try:

            with open('Dependencies/student_names.txt', 'r') as file:
                content = file.read()
                self.student_textbox.configure(state="normal")
                self.student_textbox.delete(1.0, "end")
                self.student_textbox.insert("end", content)
                self.student_textbox.configure(state="disabled")
                self.student_textbox.see("end")

            with open('Dependencies/file.txt', 'r') as file:
                content = file.read()
                self.textbox.configure(state="normal")
                self.textbox.delete(1.0, "end")
                self.textbox.insert("end", content)
                self.textbox.configure(state="disabled")
                self.textbox.see("end")

        except FileNotFoundError:
            self.textbox.configure(state="normal")
            self.textbox.delete(1.0, "end")
            self.textbox.insert("end", "Logs File Not Found")
            self.textbox.configure(state="disabled")
        
        # Schedule the function to run again in 1000 ms (1 second)
        self.after(1000, self.update_label)


# New Session Class
class New_session(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("RGPV Result Automator")
        self.geometry("600x200")
        self.resizable(False, False)

        
        # Labels and Entries
        ctk.CTkLabel(self, text="First Enrolment number").place(x=20, y=20)
        ctk.CTkLabel(self, text="Last Enrolment number").place(x=20, y=60)

        self.e1 = ctk.CTkEntry(self, width=200)
        self.e1.place(x=170, y=20)

        self.e2 = ctk.CTkEntry(self, width=200)
        self.e2.place(x=170, y=60)

        # Semester Dropdown
        days = ["1", "2", "3", "4", "5", "6", "7", "8"]
        self.semester_var = ctk.StringVar(value="<Select>")
        ctk.CTkLabel(self, text="Semester").place(x=20, y=150)
        self.sem_dropdown = ctk.CTkOptionMenu(self, variable=self.semester_var, values=days)
        self.sem_dropdown.place(x=100, y=150)


        self.ctk_radio_var = ctk.StringVar(value="g")

        ctk_radio1 = ctk.CTkRadioButton(self, text="Grading", variable=self.ctk_radio_var, value="g")
        ctk_radio2 = ctk.CTkRadioButton(self, text="Non-Grading", variable=self.ctk_radio_var, value="ng")

        ctk_radio1.place(x=450,y=20)
        ctk_radio2.place(x=450,y=60)

        # Start Button that leads to Session
        self.button = ctk.CTkButton(self, text="Start", width=120, command=self.open_session)
        self.button.place(x=450, y=150)

    def open_session(self):
        a,b=[self.e1.get(),self.e2.get()]
        sem=self.sem_dropdown.get()
        gng=self.ctk_radio_var.get()
        valid=False

        if len(a)==12:
            if len(a)==len(b):
                if sem in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                    valid=True
        if valid:
            with open('Dependencies/file.txt','w') as file:
                file.write('')

            with open('Dependencies/student_names.txt','w') as file:
                file.write('')

            self.destroy()  # Close New Session window
            session_app = Session([a,b],gng)  # Open Session window
            calc_range(a,b,sem,gng)
            
            my_thread = threading.Thread(target=app.scan, args=(a,b,True))
            my_thread.daemon = True
            my_thread.start()
            session_app.mainloop()


# Initial Menu to choose between Session or New Session
def start_app(Range,sem,gng):
    app = ctk.CTk()
    app.geometry("500x200")
    app.resizable(False, False)
    app.title("RGPV Result Automator")

    g_ng='Grading System'
    if gng=='ng':
        g_ng='Non-Grading System'

    # Labels to inform user of options
    ctk.CTkLabel(app, text="Previous Session was Unfinished!", font=("Arial", 24, "bold")).place(x=20, y=10)
    ctk.CTkLabel(app, text="From  : "+Range[0],font=("Consolas", 18)).place(x=20, y=60)
    ctk.CTkLabel(app, text="To    : "+Range[1],font=("Consolas", 18)).place(x=20, y=100)
    ctk.CTkLabel(app, text=g_ng,font=("Consolas", 18)).place(x=20, y=150)

    # Button to continue old session
    button_old_session = ctk.CTkButton(app, text="Continue old Session", width=120, command=lambda: open_session(app,Range,sem,gng))
    button_old_session.configure(fg_color="Green")
    button_old_session.place(x=350, y=150)

    # Button to start a new session
    button_new_session = ctk.CTkButton(app, text="Start new Session", width=120, command=lambda: open_new_session(app))
    button_new_session.configure(fg_color="Red")
    button_new_session.place(x=220, y=150)

    app.mainloop()


# Function to open the Session window
def open_session(parent,Range,sem,gng):
    parent.destroy()
    session_app = Session(Range,gng)
    calc_range(Range[0],Range[1],sem,gng)

    my_thread = threading.Thread(target=app.scan,args=(Range[0],Range[1]))
    my_thread.daemon = True
    my_thread.start()

    session_app.mainloop()


# Function to open the New Session window
def open_new_session(parent):
    parent.destroy()
    new_session_app = New_session()
    new_session_app.mainloop()

def create_new_session():
    new_session_app = New_session()
    new_session_app.mainloop()


def calc_range(First_eno,Last_eno,sem,gng):
    batch=""

    for i in range(len(First_eno)):
      i=len(First_eno)-i
      c=First_eno[i-1]
      if not(c in ["0","1", "2", "3", "4", "5", "6", "7", "8","9"]):
         constants.Range=[ int(First_eno[i:])  , int(Last_eno[i:]) ]
         batch=First_eno[:i]
         break
    else:
      constants.Range=[ int(First_eno),int(Last_eno) ]

    constants.Batch=batch
    constants.Sem=sem
    constants.GNG=gng


start_old=False
First_eno='abcd'
Last_eno='1234'
sem=''
gng=''
with open(constants.ScanLogs,'r') as file:
   data=file.readlines()
   if len(data)==5:
      First_eno=data[0].replace('\n','').replace(' ','')
      Last_eno=data[1].replace('\n','').replace(' ','')
      sem=data[2].replace('\n','').replace(' ','')
      constants.CsvFile=data[3].replace('\n','').replace(' ','')
      gng=data[4].replace('\n','').replace(' ','')
      if len(First_eno)==len(Last_eno) and not(First_eno==Last_eno):
         start_old=True

if start_old:
    start_app([First_eno,Last_eno],sem,gng)
else:
    create_new_session()
