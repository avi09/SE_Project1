from bs4 import BeautifulSoup
import requests

variable=input("Which website? IMDB?(1) Rotten tomatoes?(2)")
print(variable)
if int(variable)==1:
  URL="https://www.imdb.com/title/tt10970552/reviews?ref_=tt_urv"
  r=requests.get(URL)
  soup=BeautifulSoup(r.content)
  result=soup.findAll('div', {'class' : 'text show-more__control'}, limit=None)
 
if int(variable)==2:
  abc=""
  URL="https://www.rottentomatoes.com/m/on_the_rocks_2020/reviews"
  
  for i in range(25):
    tempURL=URL+"?type=&sort=&page="+str(i)
    print(tempURL)
    r=requests.get(tempURL)
    soup=BeautifulSoup(r.content)
    result=soup.findAll('div', {'class' : 'the_review'}, limit=None)
    for item in result:
      abc=abc+(item.text)
  result=abc
return result
