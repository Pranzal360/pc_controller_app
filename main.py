
from kivymd.app import MDApp
from kivy.lang.builder import Builder
import socket
from kivymd.uix.relativelayout import RelativeLayout
from kivymd.uix.tab import MDTabsBase
from plyer import notification
from kivymd.uix.label import MDLabel
import threading
from kivy.clock import Clock
from functools import partial



kv = """
#:import ScrollEffect  kivy.effects.scroll.ScrollEffect
Screen:
    id:scrn
    
    MDTabs:
        id:tab
        tab_padding : [0,10,80,0]
        
        Tab:
            title:'Controller'
            MDLabel:
                text : "Welcome to Pc Controller "
                halign:'center'
                pos_hint:{'center_x':.5,'center_y':.8}
                font_size : '20sp'
            
            MDRaisedButton:
                id:connect_btn 
                text: "Connect To Server "
                size_hint:.3,None
                pos_hint:{'center_x':.5,'center_y':.64}
                on_press:
                    app.connect()

            MDTextField:
                id:command
                hint_text:'command'
                size_hint:.4,.1
                pos_hint:{'center_x':1.1,'center_y':1.1}
            
            MDRaisedButton:
                id:sendbtn
                text : "Send"
                size_hint:.3,None
                pos_hint:{'center_x':1.1,'center_y':1.1}

                on_press:
                    app.send(command.text)
        Tab:
            title:"Logs"
            id:los
            
            ScrollView:
                size_hint:1,1
                do_scroll_x: False
                do_scroll_y: True
                GridLayout:
                    size_hint_y : None
                    height: self.minimum_height
                    # height:self.height
                    width : self.minimum_width
                    cols : 1
                    id:label
                    
                
"""
# default values set for the server, these are constants but you can chnage server address
PORT = 5050
SERVER = "192.168.1.112"
FORMAT = 'utf-8'
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'

# class used for the tab , without this we can't create tabs
class Tab(RelativeLayout, MDTabsBase):
    '''Class implementing content for a tab.'''
    ""

class shutDown(MDApp):
    # for theme
    def build(self):
        self.theme_cls.theme_style=  "Dark"
        return Builder.load_string(kv)

    def connect(self):
          # trying to connect to the server  
        try:
            # defining the client here so that we won't get problem during reconnection !
            self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.client.connect(ADDR) 
            self.status = True
            # adding the widgets its a function
            self.addWidgets()
            # adding to logs
            self.root.ids.label.add_widget(MDLabel(text="[ CONNECTED TO THE SERVER ]",size_hint_y = None,halign = "center"))
            # removing the connect button after connection !
            self.root.ids.connect_btn.pos_hint ={'center_x':1.5,'center_y':1.5}

        
        except Exception as e:
            print(e)
            # getting what is the error and adding to logs
            self.root.ids.label.add_widget(MDLabel(text="Server not found make sure its running :)  !",size_hint_y= None))
            # sending notification to the user that it's been disconected !
            notification.notify(title = "error",message= "Error Connecting Try again ",timeout=2,toast = True)
            

    def addWidgets(self):
        # once connected adding all these widgets in the main tab
        self.root.ids.sendbtn.pos_hint = {'center_x':.5,'center_y':.4}
        self.root.ids.command.pos_hint = {'center_x':.5,'center_y':.5}
    

    def send(self,msg):
        # messages are always sent in byte format 
        print(msg)

        # we are sending the message in byte format
        try : 
            self.client.send(bytes(msg.encode(FORMAT)))
            
            # after sending .. we are adding the message to the log tab in gridlayout of scroll view
            s = MDLabel(text=f"{msg}        :[CLIENT]     ",size_hint_y= .1,halign= "right")

            self.root.ids.label.add_widget(s)
            
            # getting the message that server is going to send ! 
            serverSays = self.client.recv(2048).decode(FORMAT)
            
            # adding the message to the log tab !
            self.root.ids.label.add_widget(MDLabel(text=f"[SERVER]: {serverSays}",size_hint_y= .1))

            # check if the message == disc -> for disconnection
            if msg.lower() == "disc":
                " try to make reconnection !"
                print("disconnected !")
                
                # adding all those widgets we can remove the widgets but this seems working
                self.root.ids.sendbtn.pos_hint ={'center_x':1.5,'center_y':1.5}
                self.root.ids.command.pos_hint = {'center_x':1.5,'center_y':1.5}
                self.root.ids.connect_btn.pos_hint ={'center_x':.5,'center_y':.5}
                
                # adding the msg in logs tab
                self.root.ids.label.add_widget(MDLabel(text=f"[CLIENT]: Disconnecting",size_hint_y= .1,halign= "right"))
        except Exception :
            self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.client.connect(ADDR) 
    def on_stop(self):
        msg = "disc"
        self.send(msg)

        
shutDown().run()
