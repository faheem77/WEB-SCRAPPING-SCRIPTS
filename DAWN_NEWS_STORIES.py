import requests
from bs4 import BeautifulSoup, SoupStrainer
import time
import pandas as pd
from tqdm import tqdm
from multiprocessing import Process, Pool
import json
class scrap:
  def __init__(self):
    self.data()
  def urls(self):
    links=[]
    global session
    session= requests.Session()
    for i in range(1,13):
      global headers
      headers= {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
      url= f'https://www.dawn.com/trends/no-confidence/{i}'
      only_a_tags= SoupStrainer('a')
      r= session.get(url,headers=headers)
      # print(r.status_code)
      soup= BeautifulSoup(r.content,'lxml', parse_only=only_a_tags)
      for x in soup.findAll('a', class_='story__link'):
        links.append(x.get('href'))
    return links
  def data(self):
    title, body, time, link=[],[],[],[]
    for url in self.urls():
      r= session.get(url,headers=headers)
      # print("current process: ", os.getpid())
      print(r.status_code)
      tags= SoupStrainer(['article','div','a','span'])
      soup=BeautifulSoup(r.content,'lxml', parse_only=tags)
      for i in soup.findAll('article', class_=['story','single','bg-white font-georgia']):
        data=i.find('a', class_='story__link').text
        content= i.find('div', class_=['story__content'])
        t = i.find('span', class_='story__time')
        if content !=None:
          title.append(data)
          body.append(content.text)
          time.append(t.text)
          link.append(url)

    final = [{"Title": t, "Time": s, "Body":b, "URL": u} for t, s, b, u in zip(title,time,body,link)]
    with open('data3.json', 'w') as f:
      f.write(json.dumps(final))
    # df=pd.DataFrame({"Title":title, "TIME":time, "Body":body, "URL": link})
    # df.to_csv("DAWN-NEWS-STORIES-on-NO-CONFIDENCE-MOTION.csv", index=True)

if __name__ == '__main__':
  d= scrap()
  p = Process(target=d)
  p.start()
  p.join()


  
