import tkinter as tk
import winsound
import time
import threading
import numpy as np
import random

ikkuna = tk.Tk()

ikkuna.geometry("800x500+200+200")

canvas = tk.Canvas(ikkuna, width=800, height=500, bg='lightblue')
canvas.pack()



canvas.create_rectangle(0, 0, 100, 500, fill="sandybrown")

canvas.create_rectangle(700, 0, 800, 500, fill="green")

saari_label=tk.Label(text="Saari",bg="sandybrown")
saari_label.place(x=10,y=200)

mantere_label=tk.Label(text="Mantere",bg="green")
mantere_label.place(x=710,y=200)

pohteri_label=tk.Label(text="Pohteri",bg="brown")
pohteri_label.place(x=710,y=10)

eteteri_label=tk.Label(text="Eteteri",bg="yellow")
eteteri_label.place(x=710,y=450)

# Globaali "dictionary"
tiedot={}
tiedot['apinamaara']=0
tiedot['apina']={}
hataviesti=["Ernesti", "ja", "Kernesti", 
            "tässä" ,"terve!", "Olemme", 
            "autiolla", "saarella,", "voisiko", 
            "joku", "tulla", "sieltä", 
            "sivistyneestä", "maailmasta", 
            "hakemaan", "meidät", "pois!", "Kiitos!"
            ]*6
ernesti_sanat=[]
kernesti_sanat=[]
tiedot['ernestin_eloonjaaneet']=0
tiedot['kernestin_eloonjaaneet']=0

laiva_lahetetty=False

#Muistetaan mikä sana on menossa
def opeta_sana():
    return random.choice(hataviesti)

def ernesti_apina_ja_uimaan():
    global tiedot
    tiedot['apinamaara']+=1
    apina_id=tiedot['apinamaara']


    #Opetetaan apinalle sana
    monkey_word = opeta_sana()


    print('Apina luotu ja laitettu uimaan')
    #Tätä tiedontallennusmuotoa kannattaa miettiä ja sisäistää...
    tiedot['apina'][apina_id]={
        'nimi': 'Ernestin apina',
        'sana': monkey_word,
        'x':100,'y':70,
        'väri':'ruskea',
        'elossa':1,
        'ID':apina_id}
  
    print("Tällä hetkelllä",tiedot['apinamaara'])
    winsound.Beep(440,500)
    time.sleep(0.5)

    # Havainnollistetaan apina näytölle
    apinakahva=tk.Label(text="".join(['E',str(tiedot['apina'][apina_id]['ID'])]))
    apinakahva.place(x=tiedot['apina'][apina_id]['x'],y=tiedot['apina'][apina_id]['y'])

    tiedot['apina'][apina_id]['kahva']=apinakahva

    #niksi
    

    for i in range(100):
        tiedot['apina'][apina_id]['x']=tiedot['apina'][apina_id]['x']+6
        tiedot['apina'][apina_id]['y']=tiedot['apina'][apina_id]['y']+np.random.randint(-6,6)

        apinakahva.place(x=tiedot['apina'][apina_id]['x'],y=tiedot['apina'][apina_id]['y'])
        winsound.Beep(440+apina_id*10,200)
        time.sleep(0.1)

        if tiedot['apina'][apina_id]['x']>=700:
            winsound.Beep(440,500)
            print(f"Apina {apina_id} selvisi mantereelle ja osasi sanoa: {monkey_word}")
            tiedot['ernestin_eloonjaaneet']+=1
            pohteri_threader()
            break

        if random.random()<0.01:
            tiedot['apina'][apina_id]['elossa']=0
            print(f"Apina {apina_id} syötiin!")
            apinakahva = tk.Label(text="".join(['E',str(tiedot['apina'][apina_id]['ID'])]))
            winsound.Beep(200,300)
            break

        time.sleep(0.1)

def pohteri():
    global tiedot, ernesti_sanat

    #Tarkistetaan kaikki apinoiden tiedot
    for apina_id, apina_info in tiedot['apina'].items():

        #Tarkistetaan mitkä on ernestin apinoita ja selvinneet mantereelle
        if apina_info ["nimi"] == "Ernestin apina" and apina_info ["x"] >= 700:

            #Tarkistetaan onko sana jo listassa ja jos ei niin se lisätään listaan
            if apina_info ["sana"] not in ernesti_sanat:
                ernesti_sanat.append(apina_info ["sana"])

    #Tulostetaan mitä sanoja ernestin apinat osasivat
    print("Ernestin apinat osasivat seuraavat sanat:",ernesti_sanat)
                
    if len(ernesti_sanat) >= 10:
        Laheta_laiva_ernesti()
        print("Ernesti on lähettänyt laivan hakemaan apinoita")
        

def Laheta_laiva_ernesti():
    laheta_laiva("ernesti")
           
#Luodaan laiva labelilla
def laheta_laiva(kohde):
    global laiva_lahetetty
    if laiva_lahetetty == True:
        return
    else:
        laiva_lahetetty = True
        laiva_label=tk.Label(text="SHIP",font=("Arial", 24))

        if kohde == "ernesti":
            riemu = "Ernestin apinat sai viestin perille!"
            winsound.Beep(600,700)
            start_x, start_y = 710, 10 #Lähtöpaikka pohterilta
            target_x, target_y = 10, 30 #Kohteena ernesti

        elif kohde == "kernesti":
            riemu = "Kernestin apinat sai viestin perille!"
            winsound.Beep(600,700)
            start_x, start_y = 710, 450 #Lähtöpaikka eteteriltä
            target_x, target_y = 10, 470 #Kohteena kernesti

        #Asetetaan laiva lähtöpaikkaan
        laiva_label.place(x=start_x, y=start_y)

         # voittaja ilmoitetaan ikkunassa
        voittaja = tk.Label(ikkuna, text=riemu, font=("Arial", 12))
        voittaja.place(x=180, y=200)

        #Animoidaan vene liikkuman kohteeseen
        steps = 50
        for i in range(steps):
            x = start_x + (target_x - start_x) * i / steps
            y = start_y + (target_y - start_y) * i / steps
            laiva_label.place(x=x, y=y)
            time.sleep(0.1)

def kernesti_apina_ja_uimaan():
    global tiedot
    tiedot['apinamaara']+=1
    apina_id=tiedot['apinamaara']

    #Opetetaan apinalle sana
    monkey_word = opeta_sana()

    print('Apina luotu ja laitettu uimaan')
    #Tätä tiedontallennusmuotoa kannattaa miettiä ja sisäistää...
    tiedot['apina'][apina_id]={
        'nimi': 'Kernestin apina',
        'sana': monkey_word,
        'x':100,'y':400,
        'väri':'ruskea',
        'elossa':1,
        'ID':apina_id}
    
    print("Tällä hetkelllä yhteensä",tiedot['apinamaara'])
    winsound.Beep(440,500)
    time.sleep(0.5)

    # Havainnollistetaan apina näytölle
    apinakahva=tk.Label(text="".join(['K',str(tiedot['apina'][apina_id]['ID'])]))
    apinakahva.place(x=tiedot['apina'][apina_id]['x'],y=tiedot['apina'][apina_id]['y'])

    tiedot['apina'][apina_id]['kahva']=apinakahva


    for i in range(100):
        tiedot['apina'][apina_id]['x']=tiedot['apina'][apina_id]['x']+6
        tiedot['apina'][apina_id]['y']=tiedot['apina'][apina_id]['y']+np.random.randint(-6,6)

        apinakahva.place(x=tiedot['apina'][apina_id]['x'],y=tiedot['apina'][apina_id]['y'])
        winsound.Beep(440+apina_id*10,200)
        time.sleep(0.1)

        if tiedot['apina'][apina_id]['x']>=700:
            winsound.Beep(440,500)
            print(f"Apina {apina_id} selvisi mantereelle ja osasi sanoa: {monkey_word}")
            tiedot['kernestin_eloonjaaneet']+=1
            eteteri_threader()
            break

        if random.random()<0.01:
            tiedot['apina'][apina_id]['elossa']=0
            print(f"Apina {apina_id} syötiin!")
            apinakahva = tk.Label(text="".join(['K',str(tiedot['apina'][apina_id]['ID'])]))
            winsound.Beep(200,300)
            break

        time.sleep(0.1)

def eteteri():
    global tiedot, kernesti_sanat

    #Tarkistetaan kaikki apinoiden tiedot
    for apina_id, apina_info in tiedot['apina'].items():

        #Tarkistetaan mitkä on kernestin apinoita ja selvinneet mantereelle
        if apina_info ["nimi"] == "Kernestin apina" and apina_info ["x"] >= 700:

            #Tarkistetaan onko sana jo listassa ja jos ei niin se lisätään listaan
            if apina_info ["sana"] not in kernesti_sanat:
                kernesti_sanat.append(apina_info ["sana"])

    #Tulostetaan mitä sanoja kernestin apinat osasivat
    print("Kernestin apinat osasivat seuraavat sanat:",kernesti_sanat)
                
    if len(kernesti_sanat) >= 10:
        Laheta_laiva_kernesti()
        print("Kernesti on lähettänyt laivan hakemaan apinoita")
        

def Laheta_laiva_kernesti():
    laheta_laiva("kernesti")


def laske_ruuan_maarat():
    ernestin_ruoka = tiedot['ernestin_eloonjaaneet'] * 4 
    kernestin_ruoka = tiedot['kernestin_eloonjaaneet'] * 4  
    
    yhteensa_ruoka = ernestin_ruoka + kernestin_ruoka
    
    yhteensa_pippuri = (yhteensa_ruoka / 4) * 2
    
    ruoka_ikkuna = tk.Toplevel(ikkuna)
    ruoka_ikkuna.title("Ruokamäärät")
    
    ruoka_teksti = tk.Text(ruoka_ikkuna, width=50, height=10)
    ruoka_teksti.pack()
    
    ruoka_teksti.insert(tk.END, f"Ernestin ruoan määrä: {ernestin_ruoka} henkilöä\n")
    ruoka_teksti.insert(tk.END, f"Kernestin ruoan määrä: {kernestin_ruoka} henkilöä\n")
    ruoka_teksti.insert(tk.END, f"Yhteensä ruokaa: {yhteensa_ruoka} henkilöä\n")
    ruoka_teksti.insert(tk.END, f"Yhteensä pippuria: {yhteensa_pippuri} tl\n")


def ernesti_apina_ja_uimaan_saikeistin():
    kahva=threading.Thread(target=ernesti_apina_ja_uimaan)
    kahva.start()

def ernesti_lahettaa_10_apinaa():
    for i in range(10):
       kahva=threading.Thread(target=ernesti_apina_ja_uimaan) 
       kahva.start()

def pohteri_threader():
    kahva=threading.Thread(target=pohteri)
    kahva.start()



def kernesti_apina_ja_uimaan_saikeistin():
    kahva=threading.Thread(target=kernesti_apina_ja_uimaan)
    kahva.start()

def kernesti_lahettaa_10_apinaa():
    for i in range(10):
        kahva=threading.Thread(target=kernesti_apina_ja_uimaan)
        kahva.start()

def eteteri_threader():
    kahva=threading.Thread(target=eteteri)
    kahva.start()

def tarkkailija():
    global tiedot
    for i in range(tiedot['apinamaara']):
        print("Apinamaara juuri nyt on:",tiedot['apinamaara'])
        print("Ernestin apinoita on selvinnyt mantereelle:",tiedot['ernestin_eloonjaaneet'])
        print("Kernestin apinoita on selvinnyt mantereelle:",tiedot['kernestin_eloonjaaneet'])
        time.sleep(1)
        break


def tarkkaile_saikeistin():
    kahva=threading.Thread(target=tarkkailija)
    kahva.start()

ernersti_lahettaa=tk.Button(text='Ernesti lähettää', command=ernesti_apina_ja_uimaan_saikeistin)
ernersti_lahettaa.place(x=5, y=40)

ernersti_lahettaa_10=tk.Button(text='Ernesti lähettää 10', command=ernesti_lahettaa_10_apinaa)
ernersti_lahettaa_10.place(x=5, y=65)

tarkkailija_painike=tk.Button(text='Tarkkailija',command=tarkkaile_saikeistin)
tarkkailija_painike.place(x=345,y=450)

kernersti_lahettaa=tk.Button(text='Kernesti lähettää', command=kernesti_apina_ja_uimaan_saikeistin)
kernersti_lahettaa.place(x=5, y=440)

kernersti_lahettaa_10=tk.Button(text='Kernesti lähettää 10', command=kernesti_lahettaa_10_apinaa)
kernersti_lahettaa_10.place(x=5, y=465)

laske_ruoka_maarat=tk.Button(text='Laske ruokamäärät',command=laske_ruuan_maarat)
laske_ruoka_maarat.place(x=345,y=475)



ikkuna.mainloop()