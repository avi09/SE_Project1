from bs4 import BeautifulSoup
import requests


link_file = open("/home/mnagdev/NCSU Courses/SE/Sentiment_Analysis/SE_Project1/sentimental_analysis/movie_review_link.txt", "r")

URL = link_file.readline()
print("Movie Link - ", URL)

if "imdb" in URL[:30]:
  #URL="https://www.imdb.com/title/tt10970552/reviews?ref_=tt_urv"
  r=requests.get(URL)
  soup=BeautifulSoup(r.content)
  result=soup.findAll('div', {'class' : 'text show-more__control'}, limit=None)

else:
  abc=""
  #URL="https://www.rottentomatoes.com/m/on_the_rocks_2020/reviews"
  #r=requests.get(URL)
  for i in range(25):
    tempURL=URL+"?type=&sort=&page="+str(i)
    print(tempURL)
    r=requests.get(tempURL)
    soup=BeautifulSoup(r.content)
    result=soup.findAll('div', {'class' : 'the_review'}, limit=None)
    for item in result:
      abc=abc+(item.text)
  result=abc

text_file = open("/home/mnagdev/NCSU Courses/SE/Sentiment_Analysis/SE_Project1/sentimental_analysis/movie_reviews.txt", "w")
text_file.write(str(result))
text_file.close()