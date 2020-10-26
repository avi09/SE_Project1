from bs4 import BeautifulSoup
import requests

variable=input("Which website? IMDB?(1) Rotten tomatoes?(2)")
print(variable)
if int(variable)==1:
  URL="https://www.imdb.com/title/tt10970552/reviews?ref_=tt_urv"
  r=requests.get(URL)
  soup=BeautifulSoup(r.content)
  gg=soup.findAll('div', {'class' : 'text show-more__control'}, limit=None)
  print(gg)
if int(variable)==2:
  abc=""
  URL="https://www.rottentomatoes.com/m/on_the_rocks_2020/reviews"
  r=requests.get(URL)
  soup=BeautifulSoup(r.content)
  gg=soup.findAll('div', {'class' : 'the_review'}, limit=None)
  for item in gg:
    abc=abc+(item.text)
  print(abc)
