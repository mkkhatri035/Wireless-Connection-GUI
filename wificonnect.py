import pywifi
import time
import subprocess
from pywifi import const
import json
import PySimpleGUI as sg
'''
By: Manish
A module used to connect to WIFI using python uses pywifi module as base

Method:-
curconnection() :- returns the name of currently connected wireless network as string
ncondirect(wifiname,password) :- takes 2 positional arguments as wifiname:string and password:string
returns a message as string does not checks that wifi in range or not
nconnect(wifiname,password) :- takes 2 positional arguments as wifiname:string and password:string
returns a message as string
connect(wifiname) :-takes 1 positional arguments as wifiname:string
returns a message as string
showallsavednames() :- returns list of names of all wifi connections stored on device 
delallsavednames() :- return a message string
delwifi(wifiname) :- takes 1 positional arguments as wifiname:string
returns a message string
searchnearby() :- returns a list of available wifi network nearby
shownearbywifi() :- return json object of available wifi network nearby
guitake() :- shows all the integration of the function as GUI
'''

def curconnection():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    if iface.status()== const.IFACE_CONNECTED:
        return iface.network_profiles()[0].ssid
    else:
        return "Not connected"

def ncondirect(wifiname,password):
    try:
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]
        profile = pywifi.Profile()
        profile.ssid = wifiname
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password
        tmp_profile = iface.add_network_profile(profile)
        iface.connect(tmp_profile)
        time.sleep(6)
        if iface.status()==const.IFACE_CONNECTED:
            return "Successfully Connected Wireless Network"
        else:
            iface.disconnect()
            delwifi(wifiname)
            return "try again later"
    except Exception as e:
        return "error" + str(e)

def nconnect(wifiname,password):
    
    if wifiname in searchnearby():
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]
        if iface.status() in (const.IFACE_CONNECTED,const.IFACE_CONNECTING):
            iface.disconnect()
            time.sleep(1)

        profile = pywifi.Profile()
        profile.ssid = wifiname
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password
        tmp_profile = iface.add_network_profile(profile)
        iface.connect(tmp_profile)
        time.sleep(4)
        if iface.status()==const.IFACE_CONNECTED:
            return "Successfully Connected Wireless Network"
        else:
            iface.disconnect()
            delwifi(wifiname)
            return "error connecting network try again"
    else:
        return "Network not available in range"


def showallsavednames():
    wifi = pywifi.PyWiFi() 
    iface = wifi.interfaces()[0]
    ls=[]
    for i in iface.network_profiles():
        ls.append(i.ssid)
    return ls

def delallsavednames():
    wifi = pywifi.PyWiFi() 
    iface = wifi.interfaces()[0]
    if iface.status() in (const.IFACE_CONNECTED,const.IFACE_CONNECTING):
        iface.disconnect()
        time.sleep(1)
    iface.remove_all_network_profiles()
    return "Deleted all saved Wireless connections Successfully"
    

def connect(wifiname):
    if wifiname in searchnearby():
        wifi = pywifi.PyWiFi()

        iface = wifi.interfaces()[0]
        if iface.status() in (const.IFACE_CONNECTED,const.IFACE_CONNECTING):
            iface.disconnect()
            time.sleep(1)
        profile=pywifi.Profile()
        profile.ssid=wifiname
        iface.connect(profile)
        time.sleep(3)
        if iface.status()==const.IFACE_CONNECTED:
            return "Successfully Connected Wireless Network"
        else:
            return "error connecting network try again"
    else:
        return "Network not available in range"

def delwifi(wifiname):
    if wifiname in showallsavednames():
        wifi=pywifi.PyWiFi()
        iface=wifi.interfaces()[0]
        if iface.status() in (const.IFACE_CONNECTED,const.IFACE_CONNECTING):
            iface.disconnect()
            time.sleep(1)
        profile = pywifi.Profile()
        profile.ssid = wifiname
        iface.remove_network_profile(profile)
        return 'Deleted Successfully'
    else:
        return 'Wireless SSID does not exists in the system'

def searchnearby():
    wifi=pywifi.PyWiFi()
    iface=wifi.interfaces()[0]
    time.sleep(1)
    ls=[]
    for i in iface.scan_results():
        ls.append(i.ssid)
    return ls


def shownearbywifi():
    wifi=pywifi.PyWiFi()
    iface=wifi.interfaces()[0]
    iface.scan()
    time.sleep(1)
    j=0
    wifis=dict()
    for i in iface.scan_results():
        w=dict()
        w["name"]=i.ssid
        w["BSSID"]= i.bssid
        w['sec']=i.akm[0]
        if i.akm[0]==0:
            w["security"]="None"
        elif i.akm[0]==1:
            w["security"]="WPA"
        elif i.akm[0]==2:
            w["security"]="WPAPSK"
        elif i.akm[0]==3:
            w["security"]="WPA2"
        elif i.akm[0]==4:
            w["security"]="WPA2PSK"
        elif i.akm[0]==5:
            w["security"]="Unknown"
        w['auth']=i.auth[0]
        if i.auth[0]==0:
            w["Authorisation"]="Open"
        elif i.auth[0]==1:
            w["Authorisation"]="Shared"
        w['ciph']=i.cipher
        if i.cipher==0:
            w["Cipher"]="None"
        elif i.cipher==1:
            w["Cipher"]="WEP"
        elif i.cipher==2:
            w["Cipher"]="TKIP"
        elif i.cipher==3:
            w["Cipher"]="CCMP"
        elif i.cipher==4:
            w["Cipher"]="Unknown"
        w["Signal"]=i.signal
        w["Frequency"]=i.freq
        wifis[j]=w
        j+=1
        
    return json.loads(json.dumps(wifis))


def guitake():
    lay=[[sg.Text('Currently Connected to'),sg.Text(curconnection(),key='current',enable_events=True)],
         [sg.Button('Get Saved wifi list',key='btngetsaved',size=(20,2))],
         [sg.Button('Delete Saved wifi',key='btndelsaved',size=(20,2))],
         [sg.Button('Clear saved wifi',key='btnclearsaved',size=(20,2))],
         [sg.Button('Connect to new wifi',key='btnnewcon',size=(20,2))],
         [sg.Button('Connect to saved wifi',key='btnconsaved',size=(20,2))],
         [sg.Button('Show Nearby Wifi',key='btnshownear',size=(20,2))],
         [sg.Button('Exit',size=(20,2))]
         ]
    
    window=sg.Window('WIFI Option',layout=lay)
    l=[]
    while True:
        event,value=window.read()
        window['current'].update(curconnection())
        if event in ('Close',sg.WIN_CLOSED):
            break
        
        if event=='btngetsaved':
            l=[[sg.Text('WIFI list:-',size=(20,1))]]
            for i in showallsavednames():
                l.append([sg.Text('WiFi SSID:',size=(10,1)),sg.Text(i)])
            l.append([sg.Button('Back',size=(10,2))])
            wind=sg.Window(window[event].get_text(),layout=l)
            window.disappear()
            e,v=wind.read()
            if e in ('Close',sg.WIN_CLOSED,'Back'):
                l=[]
                wind.close()
                window.reappear()
                          
            
        if event=='btndelsaved':
            l=[[sg.Text('Saved WIFI list:-',size=(20,1))]]
            n=0
            keyss=[]
            for i in showallsavednames():
                keyss.append(str(n)+i)
                l.append([sg.Text('WiFi SSID:',size=(10,1)),sg.Text(i,key=str(n)+i,enable_events=True)])
                n+=1
            l.append([sg.Button('Back',size=(10,2))])
            wind=sg.Window(window[event].get_text(),layout=l)
            window.disappear()
            while True:
                e,v=wind.read()
                if e in ('Close',sg.WIN_CLOSED,'Back'):
                    l=[]
                    wind.close()
                    window.reappear()
                    break
                if e in keyss:
                    sg.Popup(delwifi(wind[e].get()))
                if e==sg.PopupOK:
                    break
                wind.close()
                window['btndelsaved'].click()
                    
                
        if event=='btnclearsaved':
            sg.Popup(delallsavednames())         

        if event=='btnnewcon':
            l=[[sg.Text('WIFI list:-',size=(20,1))]]
            n=0
            keyss=[]
            for i in searchnearby():
                keyss.append(str(n)+i)
                l.append([sg.Text('WiFi SSID:',size=(10,1)),sg.Text(i,key=str(n)+i,enable_events=True)])
                n+=1

            l.extend([[sg.Text('Enter wifi name:',size=(15,1)),sg.Input(key='conn')],
               [sg.Text('Enter wifi passkey:',size=(15,1)),sg.Input(key='passs')],
               [sg.Button('Connect',size=(10,2))],
               [sg.Button('Back',size=(10,2))]])
            
            wind=sg.Window(window[event].get_text(),layout=l)
            window.disappear()
            while True:
                e,v=wind.read()
                if e in ('Close',sg.WIN_CLOSED,'Back'):
                    l=[]
                    wind.close()
                    window.reappear()
                    break
                if e=='Connect':
                    sg.Popup(nconnect(wind['conn'].get(),wind['passs'].get()))
            
        if event=='btnconsaved':
            l=[[sg.Text('Saved WIFI list:-',size=(20,1))]]
            n=0
            keyss=[]
            for i in showallsavednames():
                keyss.append(str(n)+i)
                l.append([sg.Text('WiFi SSID:',size=(10,1)),sg.Text(i,key=str(n)+i,enable_events=True)])
                n+=1
            l.append([sg.Button('Back',size=(10,2))])
            wind=sg.Window(window[event].get_text(),layout=l)
            window.disappear()
            while True:
                e,v=wind.read()
                if e in ('Close',sg.WIN_CLOSED,'Back'):
                    l=[]
                    wind.close()
                    window.reappear()
                    break
                if e in keyss:
                    sg.Popup(connect(wind[e].get()))
                if e==sg.PopupOK:
                    break
                wind.close()
                window['btnconsaved'].click()
                
        if event == 'btnshownear':
            l=[[sg.Text('WIFI list:-',size=(10,1))],[sg.Text('Wifi SSid'),sg.Text('Security'),sg.Text('Signal Strength'),sg.Text('Cipher')],[]]
            nearby=shownearbywifi()
            for i in nearby:
                l.append([sg.Text(nearby[i]['name']),sg.Text(nearby[i]['security']),sg.Text(nearby[i]['Signal']),sg.Text(nearby[i]['Cipher'])])
            l.append([sg.Button('Back',size=(10,2))])
            wind=sg.Window(window[event].get_text(),layout=l)
            window.disappear()
            e,v=wind.read()
            if e in ('Close',sg.WIN_CLOSED,'Back'):
                l=[]
                wind.close()
                window.reappear()
                
        if event=='Exit':
            break
    window.close()



if __name__=='__main__':
    guitake()
