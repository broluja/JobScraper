from bs4 import BeautifulSoup
import requests


class JobScraper:
    """Class for scraping sites."""

    infostud = "https://poslovi.infostud.com/oglasi-za-posao-python-developer?scope=srpoz&esource=homepage"
    hello_world = "https://www.helloworld.rs/oglasi-za-posao-python-developer"
    linked_in = """https://www.linkedin.com/jobs/search/?currentJobId=3557468116&f_TPR=r604800&geoId=101855366&
    keywords=python%20developer&location=Serbia&refresh=true"""
    teamcubate = "https://careers.teamcubate.com"
    jooble = "https://rs.jooble.org/SearchResult?p=3&rgns=Srbija&ukw=python"

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

    def scrape_linkedin(self):
        html_text = requests.get(self.linked_in).text
        soup = BeautifulSoup(html_text, "lxml")
        kls = "base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card "
        kls += "base-search-card--link job-search-card"
        main = soup.find("main")
        unordered_list = main.find("ul")
        companies = unordered_list.find_all("a", class_="hidden-nested-link")
        divs = unordered_list.find_all("div", class_=kls)

        for div, company in zip(divs, companies):
            company_name = company.text.strip()
            job_description = div.a.span.text.strip()
            link = div.a['href']
            yield company_name, job_description, link

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


if __name__ == "__main__":
    JobScraper().scrape_jooble()
