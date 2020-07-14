import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import math
import csv

cevaplar= []
tarihler = []

def sayfasayisibulucu(a):
    a = a.replace("Cevap","")
    a = a.replace(".","")
    sayfa_sayisi = math.ceil(float(a)/20) 
    return sayfa_sayisi+1

f = open("linkler.txt", "r", encoding='utf-8-sig')
icerik = list(f)
for ic in icerik:
    try:
        linkler = 'https://forum.donanimhaber.com' + ic.strip()
        URL = linkler
        page = requests.get(URL)
        soup = BeautifulSoup(page.content,features='html.parser')
        tumicerik = soup.find(class_ = 'dhfull')
        cevap_sayisi = soup.find(class_ = 'sayisal-text').text
        sayfa_sayisi = sayfasayisibulucu(cevap_sayisi)
        print(sayfa_sayisi)
        icerikler = tumicerik.find_all('div', class_ ='kl-icerik-satir')
        
        for i in range(1,sayfa_sayisi, 1):
            
            i = str(i)
            print(i + '. sayfadayım')
            URL = linkler + '-'+ i +''
            print(URL)
            page = requests.get(URL)
            soup = BeautifulSoup(page.content,features='html.parser')
            tumicerik = soup.find(class_ = 'dhfull')
            icerikler = tumicerik.find_all('div', class_ ='kl-icerik-satir')
            
            try:
                for icerik in icerikler:
                    mesaj = icerik.find('span', class_ ='msg')
                    m = mesaj.find('td')
                    cevaplar.append(m.text.strip())
                    tarih = icerik.find('span', class_ ='ki-cevaptarihi')
                    t = tarih.find('a')
                    tarihler.append(t.text.strip())
            except:
                print("Sayfada Sorun çıktı!")
                continue
    except:
        print("Komple Başlıkta Sorun Çıktı")
        continue


df = pd.DataFrame({'Cevaplar':cevaplar, 'Tarihler': tarihler})
df.to_csv('corpus.csv', index = False, encoding='utf-8-sig', sep = 'æ')

