import requests
import re
from bs4 import BeautifulSoup
import pandas as pd


konular = []
cevaplar = []
okumalar = []
sonmesajlar = []
linkler = []
print("başladı")
for i in range(2,180,3):
    i = str(i)
    print(i +". sayfadayım")
    URL = 'https://forum.donanimhaber.com/forumid_2598/p_'+i+'/tt.htm'
    page = requests.get(URL, timeout = 2)

    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find(id='topic-list-context')
    konuicerikleri = results.find_all('div', class_ ='kl-icerik-satir yenikonu')
    for konuicerik in konuicerikleri:
        #çek
        konu_elemt = konuicerik.find('div', class_='kl-konu')
        konu= konu_elemt.find('h3')
        link = konu_elemt.find('a')['href']
        #yaz
        konular.append(konu.text.strip())
        linkler.append(link)

        #çek
        cevap_elemt = konuicerik.find('div',class_='kl-cevap')
        cevap = cevap_elemt.find('span')
        cevaplar.append(cevap)

        okunma_elemt = konuicerik.find('div',class_='kl-okunma')
        okuma = okunma_elemt.find('span')
        okumalar.append(okuma)

        sonmesaj_elemt = konuicerik.find('div',class_='kl-sonmesaj no-border')
    
        sonmesajlar.append(sonmesaj_elemt.text.strip()[0:25])
print("yazmaya geçti")
df = pd.DataFrame({'Konular': konular, 'Link': linkler, 'Cevaplar':cevaplar, 'Okumalar': okumalar, 'Son Mesaj Tarihi': sonmesajlar})
df.to_csv('veriler.csv', index = False, encoding='utf-8-sig', sep = '@')
print("yazma bitti")