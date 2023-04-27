import re
import tkinter as tk 
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from os import remove
import socket
import threading
from tkinter.constants import SE
from typing import ForwardRef

import pyodbc
import requests
import json
import time
from typing import Container

HOST = "127.0.0.1"
PORT = 34567
FORMAT = "utf8"
LOGIN = "login"
SIGNUP = "signup"
LOGOUT = "logout"
DISCONN = "disconnect"
SEARCH = "search"
DEFAULT = "Default"

BRAND = []
TYPE = []
AREA = []
 
Onl_Acc = []                             #list luu tai khoan dang online 
Id = []                               #list luu dia chi - tai khoan dang online        
clients = {}

LARGE_FONT = ("verdana", 14, "bold")
SMALL_FONT = ("verdana", 11, "bold")

dbase = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};\
     SERVER=KHANHDUY\SQLEXPRESS;\
          Database=Socket;\
              UID=khanhduy;PWD=123456')
cursor = dbase.cursor()  

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

#Trang dang nhap
class StartPage(tk.Frame):
    def __init__(self, parent, appController):             #parent: container
        tk.Frame.__init__(self, parent)
        
        self.configure()

        label_title = tk.Label(self, text = "SERVER LOGIN", font = LARGE_FONT, fg = "DodgerBlue4")         
        label_user = tk.Label(self, text = "USERNAME")
        label_pswd = tk.Label(self, text = "PASSWORD")

        self.label_notice = tk.Label(self, text = "")
        self.entry_user = tk.Entry(self, width = 20, bg = "old lace")                                   #Entry: khung de nhap du lieu
        self.entry_pswd = tk.Entry(self, width = 20, bg = "old lace")

         #Nhan LOG IN/SIGN UP thi chuyen qua Homepage
        button_login = tk.Button(self, text = "LOG IN", fg = "white", bg = "DodgerBlue4", command = lambda: appController.logIn(self))
        button_login.configure(width = 10)

        label_title.pack()                                                                                  #pack(): hien ra cua so
        label_user.pack()
        self.entry_user.pack()
        label_pswd.pack()
        self.entry_pswd.pack()
        self.label_notice.pack()
        button_login.pack()

#Trang chu
class HomePage(tk.Frame):
    def __init__(self, parent, appController):   

        tk.Frame.__init__(self, parent)

        self.configure()

        button_logout = tk.Button(self, text = "LOG OUT", bg = "DodgerBlue4", fg = "white", command=lambda: appController.logOut(self))

        #IP server:
        label_IPaddr = tk.Label(self, text = "IP Address", font = SMALL_FONT, fg = "DodgerBlue4").place(x = 50, y = 30)
        text_IP = tk.StringVar()
        entry_IPaddr = tk.Entry(self, width = 20, bg = "old lace", textvariable = text_IP).place(x = 155, y = 30)
        text_IP.set("127.0.0.1")     

        #Port server:
        label_Port = tk.Label(self, text = "Port", font = SMALL_FONT, fg = "DodgerBlue4").place(x = 50, y = 60)
        text_Port = tk.StringVar()
        entry_Port = tk.Entry(self, width = 15, bg = "old lace", textvariable = text_Port).place(x = 155, y = 60)
        text_Port.set("34567")
      
        label_info = tk.Label(self, text = "Client connection", font = SMALL_FONT, fg = "black").place(x = 30, y = 100)
    
        self.frame_connection = tk.Frame(self)
        #Tao thanh cuon:
        scrollbar_y_connection = tk.Scrollbar(self.frame_connection, orient = VERTICAL)     #Thanh cuon doc
        scrollbar_x_connection = tk.Scrollbar(self.frame_connection, orient = HORIZONTAL)   #Thanh cuon ngang
        self.data = tk.Listbox(self.frame_connection, height = 10, 
                  width = 65, 
                  bg = "antique white",
                  activestyle = "none", 
                  font = "Garamond 16",
                  fg = "black",
                  yscrollcommand = scrollbar_y_connection.set,
                  xscrollcommand = scrollbar_x_connection.set)
        scrollbar_y_connection.config(command = self.data.yview)
        scrollbar_y_connection.pack(side = RIGHT, fill = Y)
        scrollbar_x_connection.config(command = self.data.xview)
        scrollbar_x_connection.pack(side = BOTTOM, fill = X)
            
        self.frame_connection.place_configure(x = 25, y = 130)  

        #------------------------------------------------------------------------------------------
        self.data.pack()

        button_logout.configure(width = 10)
        button_logout.place(x = 450, y = 45)

    def refresh(self):                          #xoa ket noi da dang xuat
        
        self.data.delete( first= 0, last= self.data.size())
        for row in Id:
            slash = row.find('/')
            self.data.insert(END,"Address: " + row[: slash] + " has logged in - Username: " + row[slash + 1:])
        self.data.pack()

    
    def printMSG(self, msg, addr):              #hien ket noi len man hinh

        for row in Id:
            slash = row.find('/')
            if row[: slash] == str(addr):
                if msg == LOGIN:
                    self.data.insert(END,"Address: " + row[: slash] + " has logged in - Username: " + row[slash + 1:])
                if msg == SIGNUP:
                    self.data.insert(END,"Address: " + row[: slash] + " has signed up - Username: " + row[slash + 1:])
        self.data.pack()

class MyApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.title("SERVER")                           
        self.geometry("500x220")    
        self.protocol("WM_DELETE_WINDOW", self.on_closing)                         
        self.resizable(width = False, height = False)      #False: khong chinh size cua so

        container = tk.Frame()
                
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}                   #dictionary
        for i in (StartPage, HomePage):
            frame = i(container, self)
            frame.grid(row = 0, column = 0, sticky = "nsew")
            self.frames[i] = frame
        self.frames[StartPage].tkraise()   #tkraise(): Hien StartPage len truoc

    def showPage(self, container):        #Khi nhan login thi chuyen page
        
        frame = self.frames[container]
        if container == HomePage:
            self.geometry("725x425")       
        else:
            self.geometry("500x220")
            frame.entry_user.delete(0,'end')
            frame.entry_pswd.delete(0,'end')
        frame.tkraise()

    def on_closing(self):           #dong ket noi khi an X

        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            for sock in clients:
                sock.close()
            
            clients.clear() 
            self.destroy()
    
    def logIn(self,curFrame):           #server dang nhap

        print("Server login")
        #lay thong tin dang nhap
        user = curFrame.entry_user.get()
        pswd = curFrame.entry_pswd.get()
        
        #kiem tra dang nhap
        if pswd == "":
            curFrame.label_notice["text"] = "Password cannot be empty"
            return 

        if user == "admin" and pswd == "795":

            self.frames[HomePage].refresh()
            self.showPage(HomePage)
            curFrame.label_notice["text"] = ""

        else:
            curFrame.label_notice["text"] = "Invalid username or password"


    def logOut(self, curFrame):             #server dang xuat
        
        #thong bao xac nhan dang xuat
        if messagebox.askokcancel("LOG OUT", "Do you want to log out"):
            self.broadcast(DISCONN)
            for sock in clients:
                sock.close()
            
            clients.clear()
            self.showPage(StartPage)

    def broadcast(self, msg):               #gui broadcast
        for sock in clients:
            sock.sendall(str(msg).encode(FORMAT))

#------------------------------------------------------------------------------------------------
def createOption():             #Tao option de users lua chon de search

    cursor.execute("select company from GiaVang GROUP BY company HAVING COUNT(*) > 1")
    data = cursor.fetchall()
    for row in data:
        BRAND.append(row[0])

    cursor.execute("select type from GiaVang GROUP BY type HAVING COUNT(*) > 1")
    data = cursor.fetchall()
    for row in data:
        TYPE.append(row[0])

    cursor.execute("select brand from GiaVang GROUP BY brand HAVING COUNT(*) > 1")
    data = cursor.fetchall()
    for row in data:
        AREA.append(row[0])
    
def Check_LiveAccount(username):        #kiem tra tai khoan dang online

    for row in Onl_Acc:
        if row == username:
            return False
    return True

def checkAccountLogin(conn, username, password):               #kiem tra tai khoan           

    if username == "admin" and password == "795":                         
        return 1                                                          

    if Check_LiveAccount(username) == False:
        return -1

    cursor.execute("select username from Account ")             #truy xuat vao database
    for row in cursor:
        if row.username == username:
            cursor.execute("select pass from Account where username= ?", username )
            psw_tuple= str(cursor.fetchone())
            psw = psw_tuple[2:-4]
            if password == psw:
                return 1
    return 0

def checkAccountSignUp( username, password):            #kiem tra dang ky

    if username == "admin" and password == "795":
        return 0

    cursor.execute("select username from Account")
    for row in cursor:
        if row.username == username:
            return 0
    return 1

def insertNewAccount(username, password):    #Them tai khoan vao database

    cursor.execute("insert Account values (?,?)", (username, password))
    cursor.commit() 


def clientLogin(conn, addr):                  #Ham Client dang nhap                                     
        
        #nhan thong tin dang nhap tu client
        username =conn.recv(1024).decode(FORMAT)
        conn.sendall(username.encode(FORMAT))
        password = conn.recv(1024).decode(FORMAT)

        check = checkAccountLogin(conn, username, password)     #Kiem tra tai khoan
        
        #gui kiem tra dang nhap
        conn.sendall(str(check).encode(FORMAT))
        #neu dang nhap thanh cong
        if check == 1:
            Onl_Acc.append(username)        #them username vao danh sach account dang online
            new_id = str(addr) + "/" + str(username)       
            Id.append(new_id)                #them dia chi + username vao Id
            return 1        #tra ve thanh cong
        return 0            #tra ve that bai

def clientSignUp(conn, addr):               #Ham client dang ky

        #nhan thong tin dang ky
        username =conn.recv(1024).decode(FORMAT)
        conn.sendall(username.encode(FORMAT))
        password = conn.recv(1024).decode(FORMAT)

        #kiem tra dang ky
        check = checkAccountSignUp(username, password)
        #gui ket qua kiem tra
        conn.sendall(str(check).encode(FORMAT))

        #neu thanh cong
        if check == 1:
            insertNewAccount(username, password)        #them account vao database
            Onl_Acc.append(username)             #them username vao danh sach account dang online
            new_id = str(addr) + "/" + str(username) 
            Id.append(new_id)                       #them dia chi + username vao Id
            return 1
        return 0

def removeOnlineAccount(addr):          #xoa tai khoan dang online

    for row in Id:
        slash = row.find("/")           #tim kiem vi tri cua "/" trong chuoi diachi/username
        check_addr = row[:slash]
        if check_addr == str(addr):     #kiem tra dia chi dang luu co la dia chi cua client khong, neu co thi xoa khoi danh sach
            name = row[slash + 1:]      #lay username 
            Onl_Acc.remove(name)        #xoa username khoi danh sach
            Id.remove(row)

def clientLogOut(conn,addr):            #ham client dang xuat      
    
    removeOnlineAccount(addr)               #goi ham xoa tai khoan khoi danh sach
    conn.sendall("accepted".encode(FORMAT))

def sendOption(conn, option):           #gui cac option cho user tra cuu
        
        for item in option:
            if item == '':
                continue
            conn.sendall(item.encode(FORMAT))
            item = conn.recv(1024).decode(FORMAT)

        conn.sendall("end".encode(FORMAT))
        conn.recv(1024)

def recvGoldInfo(conn):         #nhan thong tin tra cuu
    info = []
    print("recv")
    item = conn.recv(1024).decode(FORMAT)

    while (item != "end"):
        info.append(item)
        conn.sendall(item.encode(FORMAT))
        item = conn.recv(1024).decode(FORMAT)

    return info

def sendGoldInfo(conn, infos):          #gui thong tin tra cuu

    for info in infos:
        for data in info:
            if data == '':
                data = data + " "
            conn.sendall(data.encode(FORMAT))
            conn.recv(1024)
        
        conn.sendall("end".encode(FORMAT))
        conn.recv(1024)
    conn.sendall("complete".encode(FORMAT))

def createList(cursor, info):           #tao list thong tin tu cac dong trong csdl
    list = []

    for row in cursor:
        if row[4][0:10] == info[0]:     #kiem tra date tra cuu
            list.append(row)            #neu thong tin co date giong date yeu cau thi them vao danh sach
    return list

def searchALL(conn ,info):          #tra cuu theo loai, cua hang, khu vuc, ngay
    pointer = cursor.execute("select * from GiaVang where company = ? and type = ? and brand = ?", (info[1],info[2],info[3]))        
    return createList(pointer, info)

def searchTypeBrand(conn,info):     #tra cuu theo loai vang, khu vuc
    pointer = cursor.execute("select * from GiaVang where type = ? and brand = ?", (info[2],info[3]))
    return createList(pointer, info)

def searchCompanyBrand(conn,info):      #tra cuu theo cua hang, khu vuc
    pointer = cursor.execute("select * from GiaVang where company= ? and brand = ?", (info[1],info[3]))
    return createList(pointer, info)

def searchCompanyType(conn,info):       #tra cuu theo cua hang, loai vang
    pointer = cursor.execute("select * from GiaVang where company = ? and type =?", (info[1],info[2]))
    return createList(pointer, info)

def searchCompany(conn,info):           #tra cuu theo cua hang
    pointer = cursor.execute("select * from GiaVang where company = ?", info[1])
    return createList(pointer, info)

def searchType(conn,info):          #tra cuu theo loai vang
    pointer = cursor.execute("select * from GiaVang where type = ?", info[2])
    return createList(pointer, info)

def searchBrand(conn,info):         #tra cuu theo khu vuc
    pointer = cursor.execute("select * from GiaVang where brand = ?", info[3])
    return createList(pointer, info)

def searchDate(conn,info):          #tra cuu theo ngay
    pointer = cursor.execute("select * from GiaVang")
    return createList(pointer, info)

def clientSearch(conn):              #ham tra cuu

    info = recvGoldInfo(conn)          #nhan thong tin tra cuu
    print(info)

    if info[1] != DEFAULT and info[2] != DEFAULT and info[3] != DEFAULT:   #phan loai yeu cau
        list = searchALL(conn,info)
    elif  info[2] != DEFAULT and info[3] != DEFAULT:
        list = searchTypeBrand(conn,info)
    elif info[1] != DEFAULT and info[3] != DEFAULT:
        list = searchCompanyBrand(conn,info)
    elif info[1] != DEFAULT and info[2] != DEFAULT:
        list = searchCompanyType(conn,info)
    elif info[1] != DEFAULT:
        list = searchCompany(conn,info)
    elif info[2] != DEFAULT:
        list = searchType(conn,info)
    elif info[3] != DEFAULT:
        list = searchBrand(conn,info)
    elif info[0] != DEFAULT:
        list = searchDate(conn,info)

    if list == []:                      #neu list rong thi thong bao
        print("empty")
        conn.sendall("empty".encode(FORMAT))
    else:
        print("sending")                #gui toan bo danh sach thong tin
        sendGoldInfo(conn,list)

def updateGoldInfo():                   #cap nhat csdl

    cursor.execute("delete from GiaVang")       #xoa csdl co san
    res = requests.get('https://tygia.com/json.php')        #truy cap den web server lay data
    decoded_data = res.content.decode('utf-8-sig')          #ma hoa du lieu ve chu tieng viet
    data = json.loads(decoded_data)                         #gan vao data

    print("Updating database...")               #them data vao database 
    for i in range(0, len(data['golds'])):
        for info in data['golds'][i]['value']:
            if info['company'] == 'DOJI' or info['company'] == '3BANKS' or info['company'] == '2GROUP' or info['company'] == '1OTHER':
                cursor.execute('insert into GiaVang (buy,sell,company,brand,updated,brand1,day,id,type,code) values (?,?,?,?,?,?,?,?,?,?)',
                (info['buy'],info['sell'], info['company'],info['brand'],info['updated'],info['brand1'],info['day'],info['id'],info['type'],info['code']))
                cursor.commit()


def handleClients(conn, addr):    

        clients[conn] = addr        #list Clients luu cac ket noi
        start = time.time()         #khoi chay ham thoi gian

        try: 
            while True:
                end = time.time()       #dung thoi gian
                count_time = end - start        #tinh thoi gian

                check_conn = conn.recv(1024).decode(FORMAT)         #kiem tra ket noi
                if check_conn == "reset":                          
                    conn.sendall("reset".encode(FORMAT))
                    continue
                conn.sendall(check_conn.encode(FORMAT))

                msg = conn.recv(1024).decode(FORMAT)            #nhan cac yeu cau tu Client
                print(addr, ": ", msg)
                
                if msg == LOGIN:
                    conn.sendall(msg.encode(FORMAT))
                    clientLogin(conn, addr) 
                    app.frames[HomePage].printMSG(msg, addr)

                elif msg == SIGNUP:
                    conn.sendall(msg.encode(FORMAT))
                    if clientSignUp(conn,addr) == 1:
                        app.frames[HomePage].printMSG(msg, addr)

                elif msg == SEARCH:
                    conn.sendall(msg.encode(FORMAT))
                    clientSearch(conn)

                elif msg == LOGOUT:
                    clientLogOut(conn,addr)
                    app.frames[HomePage].refresh()
                    print(addr, "has quit")  

                if count_time > 1800.0:         #neu thoi gian hon 30p thi cap nhat database
                    updateGoldInfo()
                    start = end                 #gan start = end de cho hieu end - start vao khoang hon 30p
                    
        except ConnectionResetError:
            removeOnlineAccount(addr)
            app.frames[HomePage].refresh()
            print(addr, " has quit")
            conn.close()
            del clients[conn]  

        except ConnectionAbortedError:
            removeOnlineAccount(addr)
            app.frames[HomePage].refresh()
            print(addr, " has quit")
            conn.close()
            del clients[conn]  

        except KeyboardInterrupt:
            print("Error")
            removeOnlineAccount(addr)
            s.close()

def accept_incoming_connections():                      #ham nhan ket noi
        """Sets up handling for incoming clients."""
        try:
            print("Server:", HOST, " port: ", PORT)
            print("Waiting for client...")

            createOption()                          #tạo option: brand, type, area cho client tìm kiếm
            while True:
                
                conn, addr = s.accept()
                print("Connected by", addr)
                
                sendOption(conn,BRAND)                  #gửi các option
                sendOption(conn,TYPE)
                sendOption(conn,AREA)

                conn.sendall("Start".encode(FORMAT))    #bắt đầu

                threading.Thread(target=handleClients, args=(conn,addr)).start()
        except OSError:
            print("Server closed")
        except ConnectionError:
            print("Connnection Error")
        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            conn.close()
            dbase.close()   

if __name__ == "__main__":
    app = MyApp()
    updateGoldInfo()
    accept_thread = threading.Thread(target=accept_incoming_connections)
    accept_thread.start()
    
    app.mainloop()

    dbase.close()        
    s.close()

