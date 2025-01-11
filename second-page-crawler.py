import requests
import re
import json
from datetime import datetime

class SecondPageCrawler:
    url = 'https://forum.vbulletin.com/forum/vbulletin-3-8/vbulletin-3-8-questions-problems-and-troubleshooting/414325-www-vs-non-www-url-causing-site-not-to-login'
    html = None
    data = []

    def crawl(self):
        self.get_html()
        self.get_texts()
        self.get_titles()
        self.get_authors()
        self.get_datetimes()

        json_string = json.dumps(self.data)

        with open("second_page.json", "w") as f:
            f.write(json_string)

    def get_html(self):
        self.html = requests.get(self.url).text

    def get_titles(self):
        pattern = r'post-title.*\s+(.*)'

        titles = re.findall(pattern, self.html)

        for i, title in enumerate(titles):

            if i < len(self.data):
                self.data[i]['title'] = title

            else:
                self.data.append(
                    {
                        'title': title
                    }
                )

        return titles
    
    def get_texts(self):
        pattern = r'content-text.*\s+([A-Za-z ,.]*)'

        texts = re.findall(pattern, self.html)

        for text in texts:

            self.data.append(
                {
                'text': text
                }
            )

        return texts
    
    def get_authors(self):
        pattern = r'itemprop="author".*\s+.*\s+.*\s+.*\s+.*name">([A-Za-z.]*)'

        authors = re.findall(pattern, self.html)

        for i, author in enumerate(authors):
            if i < len(self.data):
                self.data[i]['author'] = author

            else:
                self.data.append(
                    {
                        'author': author
                    }
                )

        return authors
    
    def get_datetimes(self):
        pattern = r"b-post__timestamp.*datetime='([0-9\-:T]*)"

        datetimes = re.findall(pattern, self.html)

        for i, datetime_string in enumerate(datetimes):
            formated_datetime = datetime.fromisoformat(datetime_string)
            formated_datetime = formated_datetime.strftime("%Y/%m/%d %H:%M")

            if i < len(self.data):
                self.data[i]['datetime'] = formated_datetime

            else:
                self.data.append(
                    {
                        'datetime': formated_datetime
                    }
                )

        return datetimes
    
s = SecondPageCrawler()
s.crawl()