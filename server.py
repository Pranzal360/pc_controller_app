import socket
import threading
import os
import time
SER = "192.168.1.112"
PORT = 5050
addr = (SER,PORT)
FORMAT = "utf-8"

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

server.bind(addr)

def clientHandler(conn,addr):
    connection = True
    print(f"{addr} has been connected")
    while True:
        msg = conn.recv(2048).decode(FORMAT)
        if msg:
            print(msg)

            if msg == "disc":
                conn.send("disconnecting ".encode(FORMAT))
                break
            elif msg == "shutdown":
                conn.send("Shutting Down".encode(FORMAT))
                os.system("shutdown now")
            
            elif msg == "restart":
                conn.send("Restarting ..".encode(FORMAT))
                os.system("shutdown -r now")
            
            elif msg == "hi" or msg == "hello":
                conn.send(f"hello ! user {addr}".encode(FORMAT))        

            elif msg == "anything else":
                conn.send("nothing ".encode(FORMAT))
                
            elif msg == "sleep":
                conn.send("Sleeping ..".encode(FORMAT))
                thread1 = threading.Thread(target = threadings())
                thread1.start()
            else:
                conn.send("command not found".encode(FORMAT))
    conn.close()
    

def threadings():
    import pyautogui as py
    py.FAILSAFE = True
    os.system("gnome-terminal -e 'bash -c \"sudo su; exec bash\"'")
    time.sleep(1.5)
    pas = "pranzal@#$"

    py.write(pas,interval = 0.23)
    py.press('enter')
    time.sleep(1.5)
    py.write("pm-suspend")
    py.press('enter')
def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = clientHandler,args = (conn,addr))
        thread.start()
        print(f"{addr} has connected ! ")
        print(f"active = {threading.active_count() - 1}")

start()

