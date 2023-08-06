import os,sys
from win32com.client import Dispatch
bol=Dispatch("Sapi.Spvoice")
chk=(os.path.isfile("file.txt"))
if __name__ == "__main__" or  __name__ == "__main__":
    
    if (chk==True):
        m=open("file.txt",'r')
        for x in m.readlines():
            bol.speak(x)
            print(x)
else:
    bol.speak("i dont want to wish you")

