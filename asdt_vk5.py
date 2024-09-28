import tkinter as tk
import winsound
import time
import threading
import numpy as np

ikkuna = tk.Tk()

ikkuna.geometry("800x500+200+200")

# Globaali "dictionary"
tiedot={}
tiedot['apinamaara']=0
tiedot['apina']={}


def luo_apina_ja_laita_uimaan():
    global tiedot
    tiedot['apinamaara']+=1
    apina_id=tiedot['apinamaara']

    print('Apina luotu ja laitettu uimaan')
    #Tätä tiedontallennusmuotoa kannattaa miettiä ja sisäistää...
    tiedot['apina'][apina_id]={'nimi': 'Ernestin apinoitahan tässä...','x':10,'y':200,'väri':'ruskea','elossa':1,'ID':apina_id}
    print("Tällä hetkelllä yhteensä",tiedot['apinamaara'])
    winsound.Beep(440,500)
    time.sleep(0.5)

    # Havainnollistetaan apina näytölle
    apinakahva=tk.Label(text="".join(['E',str(tiedot['apina'][apina_id]['ID'])]))
    apinakahva.place(x=tiedot['apina'][apina_id]['x'],y=tiedot['apina'][apina_id]['y'])

    tiedot['apina'][apina_id]['kahva']=apinakahva

    #niksi
    

    for i in range(10):
        tiedot['apina'][apina_id]['x']=tiedot['apina'][apina_id]['x']+10
        tiedot['apina'][apina_id]['y']=tiedot['apina'][apina_id]['y']+np.random.randint(-10,10)

        apinakahva.place(x=tiedot['apina'][apina_id]['x'],y=tiedot['apina'][apina_id]['y'])
        winsound.Beep(440+apina_id*10,200)
        time.sleep(0.5)


def luo_apina_ja_laita_uimaan_saikeistin():
    kahva=threading.Thread(target=luo_apina_ja_laita_uimaan)
    kahva.start()

def tarkkailija():
    global tiedot
    for i in range(tiedot['apinamaara']):
        print("Apinamaara juuri nyt on:",tiedot['apinamaara'])
        time.sleep(1)

def tarkkaile_saikeistin():
    kahva=threading.Thread(target=tarkkailija)
    kahva.start()

ernersti_lahettaa=tk.Button(text='Ernesti lähettää', command=luo_apina_ja_laita_uimaan_saikeistin)
ernersti_lahettaa.place(x=50, y=400)

tarkkailija_painike=tk.Button(text='Tarkkailija',command=tarkkaile_saikeistin)
tarkkailija_painike.place(x=200,y=400)

#kernersti_lahettaa=tk.Button(text='Kernesti lähettää')
#kernersti_lahettaa.place(x=50, y=350)


#niksi
#ikkuna.after(5000, ikkuna.destroy)

ikkuna.mainloop()