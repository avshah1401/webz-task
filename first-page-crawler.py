import requests
import re
import json
from datetime import datetime


class FirstPageCrawler:
    url = 'https://www.phpbb.com/community/viewtopic.php?f=46&t=2159437'
    html = None
    data = []

    def crawl(self):
        self.get_html()
        self.get_texts()
        self.get_titles()
        self.get_authors()
        self.get_datetimes()

        json_string = json.dumps(self.data)

        with open("first_page.json", "w") as f:
            f.write(json_string)


    def get_html(self):
        self.html = requests.get(self.url).text
        

    def get_texts(self):
        pattern = r'<div class="content">((?:(?!<div|<\/div>).)*)<\/div>'

        texts = re.findall(pattern, self.html)
        altered_texts = []

        for text in texts:
            altered_text = re.sub('<.*?>', '', text)

            self.data.append(
                {
                'text': altered_text
                }
            )

        return altered_texts

    def get_titles(self):
        pattern = r'class="postbody">\s*.*\s*<h3.*\s*.a href=".*">(.*)<\/a>'

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

    def get_authors(self):
        pattern = r'<span class="r.*class="username">(.*)<\/a>'

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
        pattern = r'<span class="r.*datetime="(.*)"'

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


f = FirstPageCrawler()
f.crawl()