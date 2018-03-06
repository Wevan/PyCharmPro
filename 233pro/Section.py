import urllib.request
from urllib.parse import urljoin
import time
from bs4 import BeautifulSoup


def saveFile(data, name):
    path = "E:\\sxks\\JavaProblems\\" + name + ".txt"
    print(path)
    data = data.encode('utf-8')
    f = open(path, 'wb+')
    f.write(data)
    f.close()


urllist = []
for i in range(8, 10):
    urlx = "http://www.233.com/ncre2/JAVA/moniti/index0" + str(i) + ".html"
    urllib.parse.quote(urlx)
    urllist.append(urlx)

for url in urllist:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    req = urllib.request.Request(url=url, headers=headers)
    res = urllib.request.urlopen(req)
    res.encoding = 'utf-8'
    data = res.read()
    soup = BeautifulSoup(data, "html.parser")
    lista = []
    lista = soup.select('ul.fl.f14.list-box.best-list.mt10 li a')
    print("result len is", len(lista))
    urls = []
    for li in lista:
        urls.append(li['href'])
    for r in urls:
        req = urllib.request.Request(url=r, headers=headers)
        res = urllib.request.urlopen(req)
        data = res.read()
        soup = BeautifulSoup(data, "html.parser")
        name = soup.select('h2')
        listp = []
        listp = soup.select('.newsArea-2nd-PageWord p')
        if (name[0].text == "网校课程" or len(name) == 0):
            name = soup.select('.news-con-blk h1')
            listp = soup.select('.news-body p')
        sdata = []
        for p in listp:
            sdata.append(p.text)
        s = '\n'.join(sdata)

        saveFile(s, name[0].text)
        print(name[0].text + "保存成功")
        time.sleep(1)
time.sleep(1)
