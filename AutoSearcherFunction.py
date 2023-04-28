from operator import sub
import requests
from bs4 import BeautifulSoup
from datetime import datetime 
import pytz

#Parole da rimovere per ogni ricerca
word_remove_list = ['scheda', 'ricambi', 'cover', 'protezione', 'rotto', 'batteria', 'custodia']

def average(list):
    if len(list) == 0:
        avg = 0
    else:
        avg = sum(list)/len(list)
    return avg

def out_average(list):
    outList = []
    averageValue = average(list)
    for x in list: 
        if x > averageValue/2: 
            if x < averageValue*2:
                outList.append(x)
    return outList

def is_float(list):
    floatList = []
    for x in list:
        xIsFloat = False
        try:
            float(x)
            xIsFloat = True
        except ValueError:
            xIsFloat = False

        if xIsFloat == True: 
            floatList.append(float(x))
    return floatList

def page_request_result(site_url, id_string):
    request_result=requests.get(site_url)
    soup = BeautifulSoup(request_result.text, "html.parser")
    page_top=soup.find(id=id_string)
    return page_top

def gen_word_remover(list):
    single_string = ''
    for x in list: 
        if list.index(x) != 0:
            single_string = single_string + '+' + x
        else: 
            single_string = x
    return single_string

def link_current_items(search, search_remove, size, list = word_remove_list):
    if search_remove != '':
        complete_searche_remove = search_remove + '+' + size_differential(size) + '+' + gen_word_remover(list)
    else:
        complete_searche_remove = size_differential(size) + '+' + gen_word_remover(list)
    complete_searche = search + '+' + size
    site_url = f'https://www.ebay.it/sch/i.html?_from=R40&_nkw={complete_searche}&_in_kw=3&_ex_kw={complete_searche_remove}&_sacat=0&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=39100&_sargn=-1%26saslc%3D1&_salic=101&_sop=1&_dmd=1&_ipg=60'
    return site_url

def link_solded_items(search, search_remove, size, list = word_remove_list):
    if search_remove != '':
        complete_searche_remove = search_remove + '+' + size_differential(size) + '+' + gen_word_remover(list)
    else:
        complete_searche_remove = size_differential(size) + '+' + gen_word_remover(list)
    complete_searche = search + '+' + size
    site_url = f'https://www.ebay.it/sch/i.html?_from=R40&_nkw={complete_searche}&_in_kw=3&_ex_kw={complete_searche_remove}&_sacat=0&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=39100&_sargn=-1%26saslc%3D1&_salic=101&_sop=1&_dmd=1&_ipg=60&LH_Sold=1&rt=nc'
    return site_url

def telegram_message(message):
    token = "5222921867:AAFzL-IV4o1CU8C2Ncgea3yQO3VRREtGfwo"
    chat_id = '236543289'
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url).json()

def items_price_average(url):
    page_top = page_request_result(url,"mainContent")
    if page_top is not None:
        #finding the cost
        phone_price = page_top.find_all(class_="s-item__price")
        phone_shipping = page_top.find_all(class_="s-item__shipping s-item__logisticsCost")
    
        prices = []
        shipping = []
        i = 0 
        for info in phone_price:
            if len(phone_shipping) > i:
                if len(phone_price) > i:
                    if phone_shipping[i].getText() != 'Spedizione non specificata':
                        if str(phone_price[i]).find('ITALIC') == -1:
                                prices.append(info.getText().replace('EUR ', '').replace('.','').replace(',','.'))
            i = i + 1 

        i = 0
        for info in phone_shipping:
            if len(phone_shipping) > i:
                if len(phone_price) > i:
                    if phone_shipping[i].getText() != 'Spedizione non specificata':
                        if str(phone_price[i]).find('ITALIC') == -1:
                            shipping.append(info.getText().replace('+EUR ', '').replace(',','.').replace(' di spedizione', '').replace('Spedizione gratis', '0').replace('Spedizione non specificata','0'))
            i = i + 1
        
        average_price = average(out_average(is_float(prices)))
        average_shipping = average(out_average(is_float(shipping)))
        return average_price + average_shipping

    else: 
        #returning fake output
        fake_price = 0.00
        return fake_price

def timer_trigger(url, url_solded, trigger_timer):
    page_top = page_request_result(url, "srp-river-results")
    #Making sure that the page is correctly loaded 
    if page_top is not None:
        timer_asta = page_top.find_all(class_='s-item__time-left')
        phone_name = page_top.find_all(class_='s-item__title')
        phone_link = page_top.find_all(class_='s-item__link', href=True)
        phone_price = page_top.find_all(class_='s-item__price')
        phone_shipping = page_top.find_all(class_='s-item__shipping s-item__logisticsCost')
        phone_condition = page_top.find_all(class_='SECONDARY_INFO')
        for info in timer_asta:
            #trigger condition
            if info.getText()[0:2] == trigger_timer:
                if phone_shipping[timer_asta.index(info)].getText().find(' spedizione stimata') == -1:

                    if phone_condition[timer_asta.index(info)].getText() != 'Solo ricambi':

                        if str(phone_price[timer_asta.index(info)]).find('ITALIC') == -1:

                            if phone_price[timer_asta.index(info)].getText()[0:3] == 'EUR':
                                
                                if phone_shipping[timer_asta.index(info)].getText() != 'Spedizione non specificata':
                                    float_phone_price = float(phone_price[timer_asta.index(info)].getText().replace('EUR ', '').replace('.','').replace(',','.'))
                                    float_phone_shipping = float(phone_shipping[timer_asta.index(info)].getText().replace('+EUR ', '').replace('.','').replace(',','.').replace(' di spedizione', '').replace('Spedizione gratis', '0').replace(' spedizione stimata','').replace('Spedizione non specificata','0'))
                                    
                                    if (float_phone_price + float_phone_shipping) <= items_price_average(url_solded):
                                        if (float_phone_price + float_phone_shipping) <= 300.0: 
                                            
                                            #Minimum ROI percentage (20%)
                                            if (items_price_average(url_solded) / (float_phone_price + float_phone_shipping)) >= 1.2:
                                            
                                                if (float_phone_price + float_phone_shipping) >= (items_price_average(url_solded)/4):
                                                    telegram_message(
                                                        phone_name[timer_asta.index(info)].getText() +'\n'+
                                                        '\n'+ 
                                                        info.getText() +'\n'+
                                                        'CONDIZIONE: '+phone_condition[timer_asta.index(info)].getText() +'\n'+
                                                        'PREZZO: '+phone_price[timer_asta.index(info)].getText() +'\n'+
                                                        'SPEDIZIONE: '+phone_shipping[timer_asta.index(info)].getText().replace('di spedizione','').replace(' spedizione stimata','').replace('Spedizione non specificata','0') +'\n'+
                                                        'PREZZO MEDIO: EUR '+str(f'{items_price_average(url_solded):.2f}').replace('.',',') +'\n'+
                                                        phone_link[timer_asta.index(info)]['href'])

#Size differential
def size_differential(size):
    size_removal = ''
    if size == '32GB':
        size_removal = '64GB+128GB+256GB+512GB+1TB'
    elif size == '64GB':
        size_removal = '32GB+128GB+256GB+512GB+1TB'
    elif size == '128GB':
        size_removal = '32GB+64GB+256GB+512GB+1TB'
    elif size == '256GB':
        size_removal = '32GB+64GB+128GB+512GB+1TB'
    elif size == '512GB':
        size_removal = '32GB+64GB+128GB+256GB+1TB'
    return size_removal

#Stop the search during the night and then restart
def night_stopper(list): 
    now = datetime.now(pytz.timezone('Europe/Rome'))
    current_time = now.strftime("%H")
    running = True
    for i in list: 
        if str(current_time) == i: 
            running = False
            print('Search stopped for night')
    return running

#exit handler function 
def exit_handler(text):
    print(text)
    telegram_message(text)

#aggiungere funzione che riconosce che sono spediti dalla germania 
#aggiungere funzione che riconosce quando il face ID non funziona 
#automatizzare la lista di oggetti ricercati 
