from bs4 import BeautifulSoup
from requests import get

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'
}

def fun(word):
    word_eng = word.select_one('td span a:nth-of-type(2)')
    word_pl = word.select_one('td:nth-of-type(2)')
    if word_pl != None: 
        if word_eng != None:
            yeet = word_pl.get_text() + ' - ' + word_eng.get_text()+'\n'
            translations.append(yeet)
global url 
url = 'https://angielskie-slowka.pl'
links = []
headers = []
req = get(url+'/slowka-angielskie', headers)
global soup 
soup = BeautifulSoup(req.content, 'html.parser')
word_containers = soup.find_all('div', class_ = 'col-xs-6 col-md-4 col-lg-3 col-category')
for word_container in word_containers:
    link = word_container.find('a', class_ = 'category')
    links.append(link['href'])
for link in links:
    req = get(url+link, headers)
    soup = BeautifulSoup(req.content, 'html.parser') 
    words = soup.find('table', class_ = 'standard').find_all('tr')
    paginator = soup.find('ul', class_='pagination')
    header = soup.find('h1', class_='with-breadcrumbs').text
    words_eng = []
    words_pl = []
    translations = []
    links2 = []
    if paginator:
        paginator_lis = paginator.find_all('li')
        for li in paginator_lis:
            link = li.find('a', href=True)
            if link != None:
                links2.append(link['href'])
    if header == 'Najważniejsze słówka angielskie (poziom rozszerzony)':
        for x in range(70):
            req = get(url+'/poziom-rozszerzony,16,kategoria,' + str(x+1), headers)
            soup = BeautifulSoup(req.content, 'html.parser')              
            words = soup.find('table', class_ = 'standard').find_all('tr')
            for word in words:
                fun(word)
    elif header == 'Najważniejsze słówka angielskie (poziom podstawowy)':
        for x in range(21):
            req = get(url+'/poziom-podstawowy,15,kategoria,' + str(x+1), headers)
            soup = BeautifulSoup(req.content, 'html.parser')              
            words = soup.find('table', class_ = 'standard').find_all('tr')
            for word in words:
                fun(word)
    elif len(links2) > 0:
        for link in links2:
            req = get(url+link, headers)
            soup = BeautifulSoup(req.content, 'html.parser')              
            words = soup.find('table', class_ = 'standard').find_all('tr')
            for word in words:
                fun(word)
    else:
        for word in words:
            fun(word)
    for i in range(0, len(translations), 100):
        file = open('./words/'+header+str(i)+'.txt', 'w', encoding="utf-8")
        file.writelines(translations[i:i + 100])