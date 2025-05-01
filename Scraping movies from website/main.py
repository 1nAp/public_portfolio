import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

response = requests.get(URL)
empire_web_page = response.text

#Initializes the BeautifulSoup object so that we can parse our webpage.
soup = BeautifulSoup(empire_web_page, 'html.parser')

#Finds all title tags within the h3 heading.
titles = soup.find_all(name="h3", class_="title")
list_of_titles = []

#Gets the text from each title tag and appends it to a list.
for title_tag in titles:
    text = title_tag.getText()
    list_of_titles.append(text)

#Reverses the list to ensure the order goes from 1 to 100.
list_of_titles.reverse()

#Writes the entirety of the list to a .txt file.
with open("movies.txt", "w", encoding="utf-8") as movie_file:
    for title in list_of_titles:
        movie_file.write(f"{title}\n")