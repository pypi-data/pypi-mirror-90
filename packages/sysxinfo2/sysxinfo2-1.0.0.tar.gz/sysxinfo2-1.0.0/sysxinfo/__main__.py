import platform,socket,re,uuid,psutil,logging
from art import *

def main():
    tprint("sysinfo", font="bulbhead")

    info={}
    info['Platform']=platform.system()
    info['Platform Release']=platform.release()
    info['Platform Version']=platform.version()
    info['Architecture']=platform.machine()
    info['Hostname']=socket.gethostname()
    info['IP Address']=socket.gethostbyname(socket.gethostname())
    info['Processor']=platform.processor()
    info['RAM']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"


    for key, value in info.items():
        print(key + " : " + value)

main()
