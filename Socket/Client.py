from ctypes import FormatError
from re import search
import tkinter as tk 
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from tkcalendar import DateEntry

import time
import socket
import threading
from typing import Container, ForwardRef, no_type_check

HOST = "127.0.0.1"
PORT = 34567
FORMAT = "utf8"
LOGIN = "login"
SIGNUP = "signup"
LOGOUT = "logout"
DISCONN = "disconnect"
SEARCH = "search"
CHECKCONN = "check_connection"

BRAND = ['Default']
TYPE = ['Default']
AREA = ['Default']


LARGE_FONT = ("verdana", 14, "bold")
SMALL_FONT = ("verdana", 10, "bold")

class ConnectionPage(tk.Frame):             #trang ket noi
    def __init__(self, parent, appController):             
        tk.Frame.__init__(self, parent)
        self.configure()

        label_ipaddr = tk.Label(self, text = "IP Address", font = SMALL_FONT, fg = "DodgerBlue4")
        label_port = tk.Label(self, text = "Port", font = SMALL_FONT, fg = "DodgerBlue4")
        
        self.label_notice_connect = tk.Label(self, text = "")

        text_ipaddr = tk.StringVar()
        self.entry_ipaddr = tk.Entry(self, width = 20, bg = "old lace", textvariable = text_ipaddr)  

        text_port = tk.StringVar()                           
        self.entry_port = tk.Entry(self, width = 15, bg = "old lace", textvariable = text_port)
        #--------------------------------------------------------------------------------------------
        check = tk.IntVar()     
        def isChecked():
            if (check.get() == 1):
                text_ipaddr.set("127.0.0.1")
                text_port.set("34567")
            else:
                text_ipaddr.set("")
                text_port.set("")
        checkbox = tk.Checkbutton(self, text = "Automatic", variable = check, command = isChecked)
                    
        button_connect = tk.Button(self, text = "Connect", fg = "white", bg = "DodgerBlue4", command = lambda: appController.Connect(self))
        button_connect.configure(width = 15)
        button_connect.place(x = 365, y = 35)
        
        label_ipaddr.place(x = 40, y = 20)
        label_port.place(x = 215, y = 20)
        self.label_notice_connect.place(x = 365, y = 65)
        self.entry_ipaddr.place(x = 40, y = 40)   
        self.entry_port.place(x = 215, y = 40) 
        checkbox.place(x = 40, y = 65)

class StartPage(tk.Frame):                  #trang dang nhap
    def __init__(self, parent, appController):              
        tk.Frame.__init__(self, parent)

        self.configure()

        label_title = tk.Label(self, text = "USER LOGIN", font = LARGE_FONT, fg = "DodgerBlue4")         #Lable: muon de chu gi trong cua so thi dung lenh nay
        label_user = tk.Label(self, text = "USERNAME")
        label_pswd = tk.Label(self, text = "PASSWORD")

        self.label_notice = tk.Label(self, text = "")
        self.entry_user = tk.Entry(self, width = 20, bg = "old lace")                                   #Entry: khung de nhap du lieu
        self.entry_pswd = tk.Entry(self, width = 20, bg = "old lace")
        
        button_login = tk.Button(self, text = "LOG IN", fg = "white", bg = "DodgerBlue4", command = lambda: appController.clientLogin(self))
        button_login.configure(width = 10)
        button_signup = tk.Button(self, text = "SIGN UP", fg = "white", bg = "DodgerBlue4", command = lambda: appController.clientSignUp(self))
        button_signup.configure(width = 10)

        label_title.pack()                                                                                  #pack(): hien ra cua so
        label_user.pack()
        self.entry_user.pack()
        label_pswd.pack()
        self.entry_pswd.pack()
        self.label_notice.pack()
        button_login.pack()
        button_signup.pack()

class HomePage(tk.Frame):                       #trang chu
    def __init__(self, parent, appController):             
        tk.Frame.__init__(self, parent)
        self.configure()       

        label_title = tk.Label(self, text = "GOLD PRICES", font=LARGE_FONT, fg = "DodgerBlue4")
        label_title.pack()
         
        label_date = tk.Label(self, text = "Date", font = SMALL_FONT, fg = "DodgerBlue4").place(x = 100, y = 30)
        label_brand = tk.Label(self, text = "Brand", font = SMALL_FONT, fg = "DodgerBlue4").place(x = 275, y = 30)
        label_type = tk.Label(self, text = "Type", font = SMALL_FONT, fg = "DodgerBlue4").place(x = 475, y = 30)
        label_area = tk.Label(self, text = "Area", font = SMALL_FONT, fg = "DodgerBlue4").place(x = 675, y = 30)
        #--------------------------------------------
        self.setCalendar()                              #tao calendar
        #--------------------------------------------
        self.combo_brand = Combobox(self)
        self.combo_brand['values']= BRAND
        self.combo_brand.current(0) #set the selected item 
        self.combo_brand.place(x = 275, y = 50)
        #--------------------------------------------
        self.combo_type = Combobox(self)
        self.combo_type['values']= TYPE
        self.combo_type.current(0) #set the selected item 
        self.combo_type.place(x = 475, y = 50)
        #--------------------------------------------
        self.combo_area = Combobox(self)
        self.combo_area['values']= AREA
        self.combo_area.current(0) #set the selected item 
        self.combo_area.place(x = 675, y = 50)

        #-----------------------------------------------
        button_search = tk.Button(self, text = "SEARCH", fg = "white", bg = "DodgerBlue4", command = lambda: self.clientSearch())
        button_reset = tk.Button(self, text = "RESET", fg = "white", bg = "DodgerBlue4", command = lambda: self.reset())
        button_search.place(x = 100, y = 80)
        button_reset.place(x = 175, y = 80)

        #------------------------------------------------
        self.tree = ttk.Treeview(self, height = 50)         
       
        scrollbar = ttk.Scrollbar(self, orient = VERTICAL, command = self.tree.yview)   #tao thanh cuon
        scrollbar.place(x = 988, y = 120, height = 420)
        self.tree.configure(yscrollcommand = scrollbar.set)

        self.tree["column"] = ("Type", "Brand", "Area", "Buy", "Sell", "Date")
        
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Type", anchor='c', width=130)
        self.tree.column("Brand", anchor='c', width=130)
        self.tree.column("Area", anchor='c', width=180)
        self.tree.column("Buy", anchor='c', width=170)
        self.tree.column("Sell", anchor='c', width=170)
        self.tree.column("Date", anchor='c', width=170)


        self.tree.heading("0", text="", anchor='c')
        self.tree.heading("Type", text="Type", anchor='c')
        self.tree.heading("Brand", text="Brand", anchor='c')
        self.tree.heading("Area", text="Area", anchor='c')
        self.tree.heading("Buy", text="Buy", anchor='c')
        self.tree.heading("Sell", text="Sell", anchor='c')
        self.tree.heading("Date", text="Date", anchor='c')
    
        self.tree.pack(pady = 100)  

        button_logout = tk.Button(self, text = "LOG OUT", fg = "white", bg = "DodgerBlue4", command = lambda: appController.clientLogOut(self, conn)).place(x = 875, y = 45)  
    
    def setCalendar(self):          #tao calendar
        date = time.localtime()  
        self.cal = DateEntry(self, width=12, year=date.tm_year, month= date.tm_mon, day=date.tm_mday, 
                background='white', foreground='white', borderwidth=2)
        self.cal.place(x = 100, y = 50)

    def reset(self):            #ham tro ve khung du lieu ban dau

        #kiem tra ket noi
        try:
            conn.sendall("reset".encode(FORMAT))
            conn.recv(1024)

            # reset ve default    
            self.combo_brand.current(0) 
            self.combo_type.current(0)
            self.combo_area.current(0) 
            #reset calendar
            self.setCalendar()
            #tra cuu theo mac dinh
            self.clientSearch()

        except ConnectionAbortedError:
            if messagebox.askokcancel("SERVER","Server closed."):
                    conn.close()
                    # self.destroy()
                    app.showPage(StartPage)
        except ConnectionResetError:
             if messagebox.askokcancel("SERVER","Server closed."):
                    conn.close()
                    # self.destroy()
                    app.showPage(StartPage)

    def sendGoldInfo(self, info):           #gui yeu cau tra cuu
        print("Sending...")
        for item in info:
            conn.sendall(item.encode(FORMAT))
            item = conn.recv(1024).decode(FORMAT)

        conn.sendall("end".encode(FORMAT))
    
    def recvGoldInfo(self):                 #nhan danh sach gia vang
        infos = []
        print("Receiving...")

        item = conn.recv(1024).decode(FORMAT)   
        if item == "empty":                 #neu nhan thong bao rong thi tra ve danh sach rong
            return infos

        while item != "complete":           #Khi chua hoan tat nhan danh sach thi tiep tuc 
            info = []
            while item != "end":             #   
                info.append(item)
                conn.sendall(item.encode(FORMAT))
                item = conn.recv(1024).decode(FORMAT)
            
            infos.append(info)
            conn.sendall("next".encode(FORMAT))
            item = conn.recv(1024).decode(FORMAT)

        print("Complete")
        return infos
    
    def clientSearch(self):                     #ham tra cuu gia vang
        try:
            #kiem tra ket noi
            conn.sendall(CHECKCONN.encode(FORMAT))
            conn.recv(1024)

            #thu thap yeu cau tra cuu
            date = self.cal.get_date().strftime("%Y-%m-%d")         
            brand = self.combo_brand.get()
            type = self.combo_type.get()
            area = self.combo_area.get()    

            info = [date,brand,type,area]     

            #gui thong bao SEARCH
            print(SEARCH)
            conn.sendall(SEARCH.encode(FORMAT))
            conn.recv(1024)

            #gui yeu cau tra cuu
            self.sendGoldInfo(info)
            #nhan danh sach tra cuu
            info_recv = self.recvGoldInfo()

            #xoa tat ca du lieu dang hien tren giao dien
            oldItem = self.tree.get_children()
            for item in oldItem:
                self.tree.delete(item)

            #neu danh sach rong thi thong bao No information
            if info_recv == []:
                print("No Information")
                self.tree.insert(parent = "", index = 0, iid = 0, text = "", values = "No Information")
                self.tree.pack()

            else:   #nguoc lai thi in ra giao dien
                for i in range(0, len(info_recv)): 
                    self.tree.insert(parent = "", index = i + 1, iid = i + 1, text = "",
                        values= (info_recv[i][8],info_recv[i][2],info_recv[i][3], info_recv[i][0],info_recv[i][1],info_recv[i][4]))                 
                self.tree.pack()

        except ConnectionAbortedError:
            if messagebox.askokcancel("SERVER","Server closed."):
                    conn.close()
                    #self.destroy()
                    app.showPage(StartPage)
                    
        except ConnectionResetError:
             if messagebox.askokcancel("SERVER","Server closed."):
                    conn.close()
                    #self.destroy()
                    app.showPage(StartPage)
            
class MyApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.title("ACCOUNT")                           
        self.geometry("550x150")  
        self.protocol("WM_DELETE_WINDOW", self.on_closing)                        
        self.resizable(width = False, height = False)

        self.container = tk.Frame()
        # self.container.configure(bg = "red") 
        
        self.container.pack(side = "top", fill = "both", expand = True)
        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)

        self.frames = {}         #dictionary
        for i in (ConnectionPage, StartPage):
            frame = i(self.container, self)
            frame.grid(row = 0, column = 0, sticky = "nsew")
            self.frames[i] = frame
        self.frames[ConnectionPage].tkraise()     

    def showPage(self, container):         #Khi nhan login thi chuyen page
        frame = self.frames[container]
        if container == ConnectionPage:
            self.geometry("550x150")
        elif container == HomePage:
            self.geometry("1024x630")
        else:
            self.geometry("500x220")
            frame.entry_user.delete(0,'end')         #thiet lap khung username, password rong                    
            frame.entry_pswd.delete(0,'end')
            
        frame.tkraise()

    def clientLogin(self, curFrame):                #dang nhap
        try: 
    
            #kiem tra ket noi
            conn.sendall(CHECKCONN.encode(FORMAT))
            conn.recv(1024)

            #nhan thong tin dang nhap
            user = curFrame.entry_user.get()
            pwd = curFrame.entry_pswd.get()

            #kiem tra thong tin rong
            if user == "":
                curFrame.label_notice["text"] = "Username cannot be empty"
                conn.sendall("cancel_login".encode(FORMAT))
                return            
            if pwd == "":
                curFrame.label_notice["text"] = "Password cannot be empty"
                conn.sendall("cancel_login".encode(FORMAT))
                return            

            #gui thong bao dang nhap
            conn.sendall(LOGIN.encode(FORMAT))
            conn.recv(1024)
            #gui thong tin dang nhap
            conn.sendall(user.encode(FORMAT))
            conn.recv(1024)
            conn.sendall(pwd.encode(FORMAT))
            
            #kiem tra dang nhap 
            validCheck = conn.recv(1024).decode(FORMAT)
            print("Server: ", validCheck)
        
            if (validCheck == "1"):
                #goi ham tra cuu theo mac dinh
                print("Login successfully.")
                self.frames[HomePage].clientSearch()
                curFrame.label_notice["text"] = ""
                self.showPage(HomePage)

            elif (validCheck == "0"): 
                print("Invalid login or password. Please try again.")
                curFrame.label_notice["text"] = "Invalid login or password. Please try again."
                
            elif (validCheck == "-1"):
                curFrame.label_notice["text"] = "Username has logged in."
                
        except:
            print("Error: Server is not responding")
            curFrame.label_notice["text"] = "Error: Server is not responding"
            if messagebox.askokcancel("ERROR","Server is not responding. Click OK to quit!"):
                self.destroy()
    
    def clientSignUp(self, curFrame):               #dang ky
        try: 
            #kiem tra ket noi
            conn.sendall(CHECKCONN.encode(FORMAT))
            conn.recv(1024)
            
            #lay thong tin dang ky
            user = curFrame.entry_user.get()
            pwd = curFrame.entry_pswd.get()

            if user == "":
                curFrame.label_notice["text"] = "Username cannot be empty"
                conn.sendall("cancel_signup".encode(FORMAT))
                return            
            if pwd == "":
                curFrame.label_notice["text"] = "Password cannot be empty"
                conn.sendall("cancel_signup".encode(FORMAT))
                return            

            #check username and password validation
            conn.sendall(SIGNUP.encode(FORMAT))
            conn.recv(1024)

            #send account to server
            conn.sendall(user.encode(FORMAT))
            conn.recv(1024)
            conn.sendall(pwd.encode(FORMAT))
            
            #receive message from server
            validCheck = conn.recv(1024).decode(FORMAT)
            print("Server: ", validCheck)
           
            if (validCheck == "1"):

                self.frames[HomePage].clientSearch()
                print("Sign up successfully.")
                curFrame.label_notice["text"] = ""
                self.showPage(HomePage)

            elif (validCheck == "0"): 
                print("Username has exist. Please try again.")
                curFrame.label_notice["text"] = "Username has exist. Please use another username."

        except:
            print("Error: Server is not responding")
            curFrame.label_notice["text"] = "Error: Server is not responding"
            if messagebox.askokcancel("ERROR","Server is not responding. Click OK to quit!"):
                self.destroy()

        
    def clientLogOut(self,curFrame, conn):          #dang xuat
        try:
            #kiem tra ket noi
            conn.sendall(CHECKCONN.encode(FORMAT))
            conn.recv(1024)

            #thong bao xac nhan dang xuat
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                try:
                    conn.sendall(LOGOUT.encode(FORMAT))
                    accepted = conn.recv(1024).decode(FORMAT)
                    
                    #neu dong y dang xuat thi thuc hien  
                    if accepted == "accepted":
                        print("Log out successfully")
                        curFrame.reset()
                        self.showPage(StartPage)
                except:
                    curFrame.label_notice["text"] = "Error: Server is not responding"
            else:
                #gui goi tin bat ki cho server de khong bi treo
                #gui thong bao huy dang xuat cho server
                conn.sendall("logout_cancel".encode(FORMAT))

        except ConnectionAbortedError:
            if messagebox.askokcancel("SERVER","Server closed."):
                    conn.close()
                    self.destroy()
        except ConnectionResetError:
            if messagebox.askokcancel("SERVER","Server closed."):
                    conn.close()
                    self.destroy()  
        except:
            pass

    def on_closing(self):                        #dong ket noi khi an X       
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            try:
                conn.sendall(LOGOUT.encode(FORMAT))
            except:
                pass

    def Connect(self, curFrame):                #ham thiet lap ket noi     
        Ip = curFrame.entry_ipaddr.get()
        Port = curFrame.entry_port.get()
        if Ip == "127.0.0.1" and Port == "34567":

            conn.connect((HOST,PORT))

            #nhan cac option co trong database
            recvOption(conn, BRAND)
            recvOption(conn, TYPE)
            recvOption(conn, AREA)
            conn.recv(1024)
        
            #khoi tao Homepage
            frame = HomePage(self.container, self)
            frame.grid(row = 0, column = 0, sticky = "nsew")
            self.frames[HomePage] = frame

            self.showPage(StartPage)
            curFrame.label_notice_connect["text"] = ""
        else:
            curFrame.label_notice_connect["text"] = "invalid IP Address or Port"

def recvOption(conn, option):               #nhan cac option cho viec tra cuu
    item = conn.recv(1024).decode(FORMAT)

    while (item != "end"):
        option.append(item)
        conn.sendall(item.encode(FORMAT))
        item = conn.recv(1024).decode(FORMAT)
    conn.sendall(item.encode(FORMAT))
    
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bat dau chay giao dien
app = MyApp()
try:
    app.mainloop()
except:
    print("Server closed")
conn.close()
