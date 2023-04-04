from bs4 import BeautifulSoup
import requests


class JobScraper:
    infostud = "https://poslovi.infostud.com/oglasi-za-posao-python-developer?scope=srpoz&esource=homepage"
    hello_world = "https://www.helloworld.rs/oglasi-za-posao-python-developer"

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
        kls = "relative bg-transparent shadow-none border border-gray-600 dark:bg-gray-800 rounded-lg overflow-hidden"
        jobs_add = soup.find_all("div", class_=kls)
        for job_add in jobs_add:
            description = job_add.find("h3").text.strip()
            link = site + job_add.find("h3").a["href"]
            company = job_add.find("h4").text.strip()
            paragraphs = job_add.find_all("p", class_="text-sm font-semibold")
            date = None
            for paragraph in paragraphs:
                if "." in paragraph.text:
                    date = paragraph.text
            yield company, description, date, link
