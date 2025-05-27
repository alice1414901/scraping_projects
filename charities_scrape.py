#import dependencies 
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re

#function to find the number of pages
def num_of_pages():
    url = "https://hubcymruafrica.wales/funding/page/3/"
    my_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"}
    r = requests.get(url, headers=my_headers)
    soup = bs(r.content, "html.parser")
    button = soup.find("button", attrs={"data-view": "pages"}).text
    max_page = int(button.split("of")[1].strip())
    return max_page

#function to generate the required URLs 
def root_pages():
    max_page = num_of_pages()
    urls = []
    for page_num in range(1, max_page +1):
        url = f"https://hubcymruafrica.wales/funding/page/{page_num}/"
        urls.append(url)
    return urls

root_pages() #generate urls list

#scraping function
def scrape():
    urls = root_pages()
    big_l = []
    for url in urls:
        r = requests.get(url, headers=my_headers)
        if r.status_code == 200:
            soup = bs(r.content, "html.parser")
            all_pages_posts = soup.select("g-col.posts")
            for page in all_pages_posts:
                post_tiles = page.find_all("post-tile", class_="funding")
                for post in post_tiles:
                    small_l = []
                    themes = post.find("the-themes")
                    themes1 = themes.find_all("theme-item")
                    themes_list = []
                    for theme in themes1:
                        themes_list.append(theme.text)
                    organisation = post.find("h2", attrs = {"class":"h4"}).text
                    details = post.find("dl", attrs={"class": "details"})
                    details1 = details.find_all("dd")

                    length = len(details1)
                    #iterating through list and assigning variables based on length. if not available assigns None
                    location = details1[0].text.strip() if length > 0 else None
                    grant = details1[1].text.strip() if length > 1 else None
                    eligibility = details1[2].text.strip() if length > 2 else None
                    status = details1[3].text.strip() if length > 3 else None
                    deadline = details1[4].text.strip() if length > 4 else None
                    page = post.select_one("a")
                    charity_url= page["href"]

                    small_l.append(organisation)
                    small_l.append(location)
                    small_l.append(grant)
                    small_l.append(eligibility)
                    small_l.append(status)
                    small_l.append(deadline)
                    small_l.append(charity_url)
                    big_l.append(small_l)
    return big_l

#data frame 
data = scrape()
my_columns=["organisation", "location", "grant", "eligibility", "status", "deadline", "url"]
df = pd.DataFrame(data, columns=my_columns)
df.to_csv("funding_data.csv")
