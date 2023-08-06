import os,sys
from win32com.client import Dispatch
bol=Dispatch("Sapi.Spvoice")
chk=(os.path.isfile("file.txt"))

if (chk==True):
    m=open("file.txt",'r')
    for x in m.readlines():
        bol.speak(x)
        print(x)

