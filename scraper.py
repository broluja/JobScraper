from bs4 import BeautifulSoup
import requests
from datetime import datetime

from utils import slugify


class JobScraper:
    """Class for scraping sites."""

    infostud = "https://poslovi.infostud.com/oglasi-za-posao-python-developer?scope=srpoz&esource=homepage"
    hello_world = "https://www.helloworld.rs/oglasi-za-posao-python-developer?sort=p_vreme_postavljanja_sort"
    teamcubate = "https://careers.teamcubate.com"
    jooble = "https://rs.jooble.org/SearchResult?p=3&rgns=Srbija&ukw=python"
    joberty = "https://backend-test.joberty.rs/api/v1/jobs"

    def scrape_joberty(self):
        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'sr-RS,sr;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,hr;q=0.5,it;q=0.4,mk;q=0.3',
            'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI1NTI3NSIsImlhdCI6MTY4MTk5MDA4MCwiZXhwIjoxNjgyODU0MDgwfQ.CdIbh4h0jS1GmLafDUk__dn47FHKi3gmMRYYIYhBOzFqjliXD1Ul8bGq9DZ5Clu-SbdXIQPi6loBOWdqUMx-tA',
            'Connection': 'keep-alive',
            'Origin': 'https://www.joberty.rs',
            'Referer': 'https://www.joberty.rs/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'sec-ch-ua': '^\\^Chromium^\\^;v=^\\^112^\\^, ^\\^Google',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '^\\^Windows^\\^',
        }

        params = (
            ('page', '0'),
            ('pageSize', '10'),
            ('search', 'python'),
            ('sort', 'created'),
        )

        response = requests.get(self.joberty, headers=headers, params=params).json()
        total_page = response["totalPage"]

        for i in range(total_page):
            params = (
                ('page', i),
                ('pageSize', '10'),
                ('search', 'python'),
                ('sort', 'created'),
            )
            response = requests.get('https://backend-test.joberty.rs/api/v1/jobs', headers=headers, params=params)

            items = response.json()["items"]
            for item in items:
                try:
                    company = item["companyName"]
                    expiration_date = item["expirationDate"]
                    expiration_date = datetime.fromtimestamp(expiration_date // 1000).strftime("%A, %B %d, %Y %I:%M:%S")
                    job_title = item["jobTitle"]
                    path = "/".join([slugify(company.lower()), slugify(job_title), str(item["id"])])
                    link = f"https://www.joberty.rs/posao/{path}"
                    yield company, job_title, link, expiration_date
                except AttributeError:
                    continue

    def scrape_jooble(self):
        html_text = requests.get(self.jooble).text
        soup = BeautifulSoup(html_text, "lxml")
        main = soup.find("main", class_="yYtoPY")
        articles = main.find_all("article")
        for article in articles:
            try:
                description = article.header.a.text
                link = article.header.a['href']
                date = article.find("div", class_="caption e0VAhp").text
                company = article.find("div", class_="_1JrOtp _30OfJk").text
                yield company, description, link, date
            except AttributeError:
                continue

    def scrape_teamcubate(self):
        html_text = requests.get(self.teamcubate).text
        soup = BeautifulSoup(html_text, "lxml")
        job_adds = soup.find_all("li", class_="w-full")
        for job_add in job_adds:
            try:
                link = job_add.a.get('href')
                description = job_add.a.span.text
                yield description, link
            except AttributeError:
                continue

    def scrape_infostud(self):
        html_text = requests.get(self.infostud).text
        soup = BeautifulSoup(html_text, "lxml")
        job_titles = soup.find_all(
            "div", class_="job uk-card uk-card-small uk-card-default uk-card-body uk-margin-bottom uk-box-shadow-small"
        )
        for job_title in job_titles:
            title = job_title.h2.text.strip()
            company = job_title.p.text.strip()
            path = job_title.h2.a["href"]
            link = f"https://poslovi.infostud.com/{path}"
            yield title, company, link

    def scrape_hello_world(self):
        html_text = requests.get(self.hello_world).text
        site = "https://www.helloworld.rs/"

        soup = BeautifulSoup(html_text, "lxml")
        ads = soup.find_all("div", class_="flex flex-col gap-4 flex-1 px-4 md:pl-4 mb-4 w-full")
        for ad in ads:
            description = ad.h3.text.strip()
            company = ad.h4.text.strip()
            link = site + ad.h3.a["href"]
            paragraphs = ad.find_all("p", class_="text-sm font-semibold")
            date = None
            for paragraph in paragraphs:
                if "." in paragraph.text:
                    date = paragraph.text
            yield company, description, date, link
