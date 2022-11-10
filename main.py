from datetime import datetime
from platform import platform
import AutoSearcherFunction
import time 
import schedule
from datetime import datetime 
import os 
import configparser
import pytz
import sys
from termcolor import colored

#prova 

print('Version 0.2.6')

path = ''
if sys.platform.startswith('linux'):
    #linux
    path = '/home/ubuntu/AutoSearcher'
if sys.platform == 'win32':
    #windows
    path = 'C:\\Users\\loren\\Desktop\\GitHub\\AutoSearcher'

def current_time():
    now = datetime.now(pytz.timezone('Europe/Rome'))
    current_time = now.strftime("%H:%M:%S")
    return current_time

searching_items = []
config = configparser.ConfigParser()
#Tryng the path
try:
    config.read(os.path.join(path,'PhoneLinkConfiguration.ini'))
    ITEMS = {}
    for key in config['ITEMS']:
        value = config.get("ITEMS", key)
        if key[0:3] == 'typ':
            ITEMS[key] = value 
            searching_items.append(value)
        if key[0:3] == 'cur':
            ITEMS[key] = value.replace('%','%%') 
        if key[0:3] == 'sol':
            ITEMS[key] = value.replace('%','%%') 
except: 
    print(colored('Edit the path', 'red'))
    sys.exit()

#Current search
risposta_ricerche = input('Ricerche in corso: (y)').lower()
if risposta_ricerche == 'y':
    for i in searching_items:
        print(i.replace('+',' '))

search_int = input('Vuoi inserire altri oggetti: (y)').lower()
if search_int == 'y':
    print('Procedi con inserire la ricerca che vuoi efettuare')
    i = True 
    while i == True:
        items_name = input("Nome dell'oggetto: ").replace(' ','+')
        #finding if the items already exist 
        items_already_exist = False
        for x in config['ITEMS']:
            if x.lower().find(items_name.lower()) != -1: 
                print(colored('Ricerca già inserita', 'red'))
                items_already_exist = True
                break
        if items_already_exist == False:
            search_remove = input('Parole da rimuovere: ').replace(' ','+')
            size_question = input('Vuoi differenziare la memoria: (y)')
            if size_question == 'y':
                x = 1
                while x <= 5:
                    if x == 1: 
                        size = '32GB'
                    elif x == 2: 
                        size = '64GB'
                    elif x == 3: 
                        size = '128GB'
                    elif x == 4: 
                        size = '256GB'
                    elif x == 5:
                        size = '512GB'
                        
                    #setting up links and name
                    ITEMS['type_'+items_name+'_'+size] = items_name + '+' + size
                    ITEMS['current_link_'+items_name+'_'+size] = AutoSearcherFunction.link_current_items(items_name, search_remove, size).replace('%','%%')
                    ITEMS['solded_link_'+items_name+'_'+size] = AutoSearcherFunction.link_solded_items(items_name, search_remove, size).replace('%','%%')
                    x = x + 1 

            else:
                #setting up links and name 
                ITEMS['type_'+items_name] = items_name
                ITEMS['current_link_'+items_name] = AutoSearcherFunction.link_current_items(items_name, search_remove, size='').replace('%','%%')
                ITEMS['solded_link_'+items_name] = AutoSearcherFunction.link_solded_items(items_name, search_remove, size='').replace('%','%%')

            risposta = ''
            while risposta != 'y' or risposta!= 'n':
                risposta = input('Vuoi inserire un altro oggetto? (y/n): ').lower()
                if risposta == 'n':
                    i = False
                    break
                if risposta == 'y':
                    print('Procedi con inserire i dati richiesti')
                    break
                else:
                    print('Rispondi solamente y o n')
    
    config['ITEMS'] = ITEMS
    #Saving items
    with open(os.path.join(path,'PhoneLinkConfiguration.ini'), 'w') as phone_link:
        config.write(phone_link)
    print(colored('CONFIGURATION DONE','green'))

#Starting the search
risposta_starter = input('Vuoi iniziare la ricerca: (y)')
if risposta_starter == 'y':
    #converting dictionary to array 
    phone_type_array = []
    selling_phone_array = []
    solded_phone_array = [] 
    for x in config['ITEMS']:
        value = config.get("ITEMS", x)
        if x[0:3] == 'typ':
            phone_type_array.append(value)
        if x[0:3] == 'cur':
            selling_phone_array.append(value.replace('%%','%'))
        if x[0:3] == 'sol':
            solded_phone_array.append(value.replace('%%','%'))

    def search_phone(): 
        print('Searching...')   
        for x in phone_type_array:
            item_position = phone_type_array.index(x)
            AutoSearcherFunction.timer_trigger(
                selling_phone_array[item_position],
                solded_phone_array[item_position],
                '2h'
            )
            time.sleep(15)
        AutoSearcherFunction.telegram_message('Ciclo andato a buon fine '+str(current_time()))
        print('Ciclo andato a buon fine '+str(current_time()))

    AutoSearcherFunction.telegram_message('Ricerca iniziata alle: '+str(current_time()))
    print('Searching...')
    schedule.every(1).hours.do(search_phone)
    i = True
    while i:
        try:
            schedule.run_pending()
            time.sleep(1800)
        except Exception as e:
            AutoSearcherFunction.telegram_message('ERROR: '+str(e))
            i = False