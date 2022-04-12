import requests
from bs4 import BeautifulSoup, SoupStrainer
import time
import pandas as pd
from multiprocessing import Process
def urls():
  links=[]
  session= requests.session()
  for i in range(1,13):
    headers= {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
    url= f'https://www.dawn.com/trends/no-confidence/{i}'
    only_a_tags= SoupStrainer('a')
    r= session.get(url,headers=headers)
    soup= BeautifulSoup(r.content,'lxml', parse_only=only_a_tags)
    for x in soup.findAll('a', class_='story__link'):
      links.append(x.get('href'))
    print()
  return links
def scrap():
  title=[]
  body=[]
  time=[]
  link=[]
  session= requests.session()
  for url in urls():
    headers= {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
    r= session.get(url,headers=headers)
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
  df=pd.DataFrame({"Title":title, "TIME":time, "Body":body, "URL": link})
  df.to_csv("DAWN-NEWS-STORIES-on-NO-CONFIDENCE-MOTION.csv", index=True)

if __name__ == '__main__':

  p=Process(target=scrap)
  p2=Process(target=scrap)

  p.start()
  p2.start()
  p.join()
  p2.join()
  
