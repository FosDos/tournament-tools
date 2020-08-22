import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
import thread
import time
import tkMessageBox
import tohelper
import threading


class to_buddy(tk.Tk):
  def __init__(self, *args, **kwargs):
    tk.Tk.__init__(self, *args, **kwargs)

    self.driver = tohelper.chal_driver()
    self.eventids = {}
    self.addlist = []
    self.title("TO Buddy (ALPHA)")
    self.geometry("450x450")
    self.pmflag = False
    self.s4flag = False
    self.meleeflag = False
    container = tk.Frame(self)
    container.pack(side="top", fill="both", expand=True)
    container.grid_rowconfigure(0,weight=1)
    container.grid_columnconfigure(0,weight=1)
    self.frames = {}
    for F in (StartPage, HomePage, EventPage, RegistrationPage):
      page_name = F.__name__
      frame = F(parent=container, controller=self)
      self.frames[page_name] = frame
      frame.grid(row=0, column=0, sticky="nsew")

    self.show_frame("StartPage")


  def show_frame(self, page_name):
    frame = self.frames[page_name]
    frame.tkraise()
class StartPage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller
    label = tk.Label(self, text="Welcome to TO Buddy!",font=("Helvetica", 20))
    label.pack(side="top", fill="x", pady=10)

    user_name_label = tk.Label(self, text="Challonge User Name",font=("Helvetica", 15))
    self.user_name_entry = tk.Entry(self)
    api_key_label = tk.Label(self, text="API Key",font=("Helvetica", 15))
    self.api_key_entry = tk.Entry(self)
    start_button = tk.Button(self, text="Start", command=lambda: self.start(), pady=10, bd=2)
    sub_label = tk.Label(self, text="Subdomain (Optional)", font=("Helvetica", 15))
    self.sub_entry = tk.Entry(self)

    spacer_label = tk.Label(self, text= "", pady=50)

    spacer_label.pack()
    user_name_label.pack(pady=1)
    self.user_name_entry.pack(pady=5)
    api_key_label.pack(pady=1)
    self.api_key_entry.pack(pady=5)
    sub_label.pack(pady=1)
    self.sub_entry.pack(pady=5)
    start_button.pack(pady=12)
  def start(self):
    if(self.user_name_entry.get() == ""):
      tkMessageBox.showerror("Error", "Please Enter Your Challonge Username")
      return
    if(self.api_key_entry.get() == ""):
      tkMessageBox.showerror("Error", "Please Enter Your API Key\nMore Info At Challonge.com/api")
      return
    self.controller.driver = tohelper.chal_driver(self.user_name_entry.get(), self.api_key_entry.get(), self.sub_entry.get())

    if(self.controller.driver.authenticate()):
      self.subdomain = self.sub_entry.get()
      self.controller.show_frame("HomePage")
    else:
      tkMessageBox.showerror("Authentication Error", "Invalid Username or API Key")
      return

class HomePage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller
    label = tk.Label(self, text="TO Buddy", font=("Helvetica", 20))
    label.pack()

    self.new_event_button = tk.Button(self, text="New Event", command = lambda: self.new_event(), pady=20, bd = 2, width=40)
    self.settings_button = tk.Button(self, text="Settings", command = lambda: self.settings(), pady=20, bd = 2, width=40, state='disabled')
    self.player_profiles_button = tk.Button(self, text="Player Profiles", command= lambda: self.profiles(), pady=20, bd=2, width=40, state='disabled')
    self.about_button = tk.Button(self, text="About", command = lambda: self.about(), pady=20, bd = 2, width=40, state='disabled')
    self.manage_tournaments_button = tk.Button(self, text="Manage Tournaments", command = lambda: self.manage(), pady=20, bd=2, width=40, state='disabled')

    self.new_event_button.pack(pady=15)
    self.manage_tournaments_button.pack(pady=15)
    self.player_profiles_button.pack(pady=15)
    self.settings_button.pack(pady=15)
    self.about_button.pack(pady=15)


  def new_event(self):
    self.controller.show_frame("EventPage")
  def settings(self):
    pass
  def profiles(self):
    pass
  def about(self):
    pass
  def manage(self):
    pass
class EventPage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller
    label = tk.Label(self, text="TO Buddy!", font=("Helvetica", 20))
    label.pack(side="top", fill="x", pady=10)

    self.PMCheck = IntVar()
    self.MeleeCheck = IntVar()
    self.S4Check = IntVar()

    self.name_label = tk.Label(self, text="Event Name")
    self.name_entry = tk.Entry(self)
    self.PM_check = tk.Checkbutton(self, text="PM", variable = self.PMCheck, onvalue =1, offvalue = 0, height = 5, width = 20 )
    self.Melee_check = tk.Checkbutton(self, text="Melee", variable = self.MeleeCheck, onvalue =1, offvalue = 0, height = 5, width = 20 )
    self.Smash4_check = tk.Checkbutton(self, text="Smash 4", variable = self.S4Check, onvalue =1, offvalue = 0, height = 5, width = 20 )
    self.create_button = tk.Button(self, text="Create Tournaments", command = lambda: self.create(), width = 15, bd=2)

    self.name_label.pack()
    self.name_entry.pack()
    self.PM_check.pack()
    self.Melee_check.pack()
    self.Smash4_check.pack()
    self.create_button.pack(pady=10)

  def create(self):
    if(self.PMCheck.get()==0 and self.MeleeCheck.get()==0 and self.S4Check.get()==0):
      tkMessageBox.showerror("Error", "At Least One Box Must Be Checked")
      return
    if(self.name_entry.get()==""):
      tkMessageBox.showerror("Error", "Please Enter A Name For The Event")
      return
    if(self.PMCheck.get()!=0):
      try:
        self.controller.eventids['pm'] = self.controller.driver.create_bracket(self.name_entry.get(), "PM")
        self.controller.pmflag = True
      except:
        tkMessageBox.showerror("Error", "Error Creating PM Bracket")
    else:
      self.controller.frames['RegistrationPage'].PM_check['state'] = 'disabled'
    if(self.MeleeCheck.get()!=0):
      try:
        self.controller.eventids['melee'] = self.controller.driver.create_bracket(self.name_entry.get() , "Melee")
        self.controller.meleeflag = True
      except:
        tkMessageBox.showerror("Error", "Error Creating Melee Bracket")
    else:
      self.controller.frames['RegistrationPage'].Melee_check['state'] = 'disabled'
    if(self.S4Check.get()!=0):
      try:
        self.controller.eventids['s4'] = self.controller.driver.create_bracket(self.name_entry.get(), "Smash4")
        self.controller.s4flag = True
      except:
        tkMessageBox.showerror("Error", "Error Creating Smash 4 Bracket")
    else:
      self.controller.frames['RegistrationPage'].Smash4_check['state'] = 'disabled'
    self.controller.show_frame("RegistrationPage")


class RegistrationPage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller
    label = tk.Label(self, text="RegistrationPage", font=("Helvetica", 20))
    label.pack(side="top", fill="x", pady=10)

    self.PMCheck = IntVar()
    self.MeleeCheck = IntVar()
    self.S4Check = IntVar()

    self.name_label = tk.Label(self, text="Player Name")
    self.name_entry = tk.Entry(self)
    self.PM_check = tk.Checkbutton(self, text="PM", variable = self.PMCheck, onvalue =1, offvalue = 0, height = 5, width = 20 )
    self.Melee_check = tk.Checkbutton(self, text="Melee", variable = self.MeleeCheck, onvalue =1, offvalue = 0, height = 5, width = 20 )
    self.Smash4_check = tk.Checkbutton(self, text="Smash 4", variable = self.S4Check, onvalue =1, offvalue = 0, height = 5, width = 20 )
    self.add_button = tk.Button(self, text="Add Player", command = lambda: self.add_player(), width = 15, bd=2)

    self.name_label.pack()
    self.name_entry.pack()
    self.PM_check.pack()
    self.Melee_check.pack()
    self.Smash4_check.pack()
    self.add_button.pack(pady=10)
  def add_player(self):
    if(self.PMCheck.get()==0 and self.MeleeCheck.get()==0 and self.S4Check.get()==0):
      tkMessageBox.showerror("Error", "At Least One Bracket Must Be Selected")
      return
    if(self.name_entry.get()==""):
      tkMessageBox.showerror("Error", "Please Enter A Name")
      return
    if(self.PMCheck.get()!=0):
      thread.start_new_thread(self.controller.driver.add, (self.controller.eventids['pm'], self.name_entry.get()))

      self.PM_check.toggle()
    if(self.MeleeCheck.get()!=0):
      thread.start_new_thread(self.controller.driver.add, (self.controller.eventids['melee'], self.name_entry.get()))

      self.Melee_check.toggle()
    if(self.S4Check.get()!=0):
      thread.start_new_thread(self.controller.driver.add, (self.controller.eventids['s4'], self.name_entry.get()))
      self.Smash4_check.toggle()
    self.name_entry.delete(0, 50)

app = to_buddy()
app.mainloop()
