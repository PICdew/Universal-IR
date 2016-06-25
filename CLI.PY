import serial,time
import win32api, win32con
import sys
class IR:
    def __init__(self,com):
        self.ser=serial.Serial(com,57600)
        self.ser.flushInput()
        self.db="Database.bin"
        #commands: Vol_up,Vol_down,Vol_mute,Enter,left,Right,UP,Down,Left_Click,Right_Click,mouse_up,mouse_down,mouse_left,mouse_right
        self.data=[]
        self.commands=['AF','AE','AD','0D','ALTF4','25','27','26','28','MCL','MCR','MU','MD','ML','MR']
        self.commands_labels=['Volume +','Volume -','Volume mute','Enter','ALT+F4','left arrow','Right arrow','UP arrow','Down arrow','Left Click','Right Click','mouse up','mouse down','mouse left','mouse right']
    def press_key(self,key):
        if key[0]=='M':
            self.move_mouse(key)
            return
        if key=='ALTF4':
            self.ALTF4()
            return
        win32api.keybd_event(int(key,16),0,0,0)
        time.sleep(0.05)
        win32api.keybd_event(int(key,16),0,win32con.KEYEVENTF_KEYUP,0)
    def move_mouse(self,dire):
        current_pos=win32api.GetCursorPos()
        if dire=='MU':
            win32api.SetCursorPos((current_pos[0],current_pos[1]-10))
        elif dire=='MD':
            win32api.SetCursorPos((current_pos[0],current_pos[1]+10))
        elif dire=='ML':
            win32api.SetCursorPos((current_pos[0]-10,current_pos[1]))
        elif dire=='MR':
            win32api.SetCursorPos((current_pos[0]+10,current_pos[1]))
        elif dire=='MCL':
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,current_pos[0],current_pos[1],0,0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,current_pos[0],current_pos[1],0,0)
        elif dire=='MCR':
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,current_pos[0],current_pos[1],0,0)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,current_pos[0],current_pos[1],0,0)
    def ALTF4(self):
        win32api.keybd_event(int('12',16),0,0,0)
        win32api.keybd_event(int('73',16),0,0,0)
        time.sleep(0.05)
        win32api.keybd_event(int('12',16),0,win32con.KEYEVENTF_KEYUP,0)
        win32api.keybd_event(int('73',16),0,win32con.KEYEVENTF_KEYUP,0)
    def learn(self):
        print "learning keys..."
        o=open(self.db,'w')
        for i in self.commands_labels:
            print "Press the key you want it to do "+i
            success=0
            while success==0:
                code=self.recv()
                if code<>0:
                    success=1
                    o.write(code+'#\n')
        print 'Done learning...'
        print 'updating Database...'
        time.sleep(1)
        print 'Database updated successfully !! '
        o.close()
    def read_db(self):
        o=open(self.db,'r')
        self.data=o.read().split('#\n')
        o.close()
    def check_valid(self,var):
        if var[200:250]=='00000000000000000000000000000000000000000000000000':
            return 0
        if var.find('N')<>-1:  #if found return index , else return -1
            return 0
        return 1
    def decode(self,data):
        code=''
        decoded=data.replace('1111111111111111111111111111111111111111111111111','s')
        decoded=decoded.replace('1111','s')
        decoded=decoded.replace('111','s')
        try:
            decoded=decoded.replace('1','')
        except:
            pass
        decoded=decoded.split('s')
        #print decoded
        for i in decoded:
            if len(i)>5:
                code+='1'
            else:
                code+='0'
        return code
    def get_value(self):
        value=ord(self.ser.read(1))
        if value==1:
            value='1'
        elif value==0:
            value='0'
        else:
            value='N'
        return value
    def recv(self,check=1):
        value='0'
        if check==0:
            value='1'
        while value=='0':
            value=self.get_value()
        i=0
        data=''
        while i<500:
            value=self.get_value()
            data+=value
            i+=1
        valid=1
        if check==1:
            valid=self.check_valid(data)
        if valid==0:
            return 0
        if check==0:
            return data
        data=self.decode(data)
        return data
    def start(self):
        try:
            self.read_db()
        except:
            self.learn()
            self.read_db()
        while True:
            code=self.recv()
            if code==0:
                continue
            try:
                index=self.data.index(code)
                self.press_key(self.commands[index])
                while self.recv(check=0).count('0')<>500:
                    self.press_key(self.commands[index])
            except:
                pass
IR_Recv=IR(sys.argv[1])
IR_Recv.start()
